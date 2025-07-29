#pragma once

#include <pybind11/functional.h>
#include <pybind11/pybind11.h>
#include <pybind11/typing.h>

#include <memory>

#include <amulet/pybind11_extensions/nogil_holder.hpp>
#include <amulet/pybind11_extensions/pybind11.hpp>

#include <amulet/utils/python.hpp>

#include "signal.hpp"

namespace py = pybind11;
namespace pyext = Amulet::pybind11_extensions;

namespace Amulet {

template <typename... Args>
class PySignal : public py::object {
    PYBIND11_OBJECT_DEFAULT(PySignal, object, PyObject_Type)
    using object::object;
};

template <typename... Args>
class PySignalToken : public py::object {
    PYBIND11_OBJECT_DEFAULT(PySignalToken, object, PyObject_Type)
    using object::object;
};

// Create a python binding for the signal class.
template <typename signalT>
void create_signal_binding()
{
    if (!pyext::is_class_bound<signalT>()) {
        pybind11::class_<typename signalT::tokenT>(pybind11::handle(), "SignalToken", pybind11::module_local());

        pybind11::class_<signalT, pyext::nogil_shared_ptr<signalT>>(pybind11::handle(), "Signal", pybind11::module_local())
            .def(
                "connect",
                [](signalT& self, typename signalT::callbackT callback, ConnectionMode mode) {
                    // Bad things happen if this is called after python shuts down.
                    // Add a wrapper to make sure python is still running.
                    auto py_valid = get_py_valid();
                    auto callback_wrapper = [callback, py_valid](auto... args) {
                        if (*py_valid) {
                            callback(args...);
                        } else {
                            throw std::runtime_error(
                                "Cannot execute Python function connected to signal because the Python interpreter has been shut down. "
                                "Python callbacks must be disconnected before the interpreter shuts down.");
                        }
                    };
                    py::gil_scoped_release nogil;
                    return self.connect(callback_wrapper, mode);
                },
                py::arg("callback"),
                py::arg("mode") = Amulet::ConnectionMode::Direct)
            .def("disconnect", &signalT::disconnect, py::call_guard<py::gil_scoped_release>())
            .def("emit", &signalT::emit, py::call_guard<py::gil_scoped_release>());
    }
}

// Define a signal getter on a class.
// This automatically creates the binding class.
template <typename PyCls, typename CppCls, typename... Args, typename... Extra>
void def_signal(PyCls& cls, const char* name, const Signal<Args...> CppCls::*attr, const Extra&... extra)
{
    create_signal_binding<Signal<Args...>>();
    cls.def_property_readonly(
        name,
        py::cpp_function(
            [attr](const typename PyCls::type& self) -> PySignal<Args...> {
                return pybind11::cast(self.*attr, py::return_value_policy::reference);
            },
            py::keep_alive<0, 1>()),
        extra...);
}

};

namespace pybind11 {
namespace detail {
    namespace {

        template <typename T, typename... Ts>
        constexpr auto get_args_str()
        {
            if constexpr ((sizeof...(Ts)) == 0) {
                return make_caster<T>::name;
            } else {
                return make_caster<T>::name + ((const_name(", ") + make_caster<Ts>::name) + ...);
            }
        }

    }

    template <>
    struct handle_type_name<Amulet::PySignal<>> {
        static constexpr auto name = const_name("amulet.utils.signal.Signal[()]");
    };

    template <typename T, typename... Ts>
    struct handle_type_name<Amulet::PySignal<T, Ts...>> {
        static constexpr auto name = const_name("amulet.utils.signal.Signal[") + get_args_str<T, Ts...>() + const_name("]");
    };

    template <>
    struct handle_type_name<Amulet::PySignalToken<>> {
        static constexpr auto name = const_name("amulet.utils.signal.SignalToken[()]");
    };

    template <typename T, typename... Ts>
    struct handle_type_name<Amulet::PySignalToken<T, Ts...>> {
        static constexpr auto name = const_name("amulet.utils.signal.SignalToken[") + get_args_str<T, Ts...>() + const_name("]");
    };
}
}
