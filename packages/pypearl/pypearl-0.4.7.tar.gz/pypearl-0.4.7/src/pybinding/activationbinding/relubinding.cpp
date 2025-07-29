#ifndef RELUBINDING
#define RELUBINDING
#include "relubinding.hpp"

static void
PyReLUD_dealloc(PyReLUDObject *self)
{
    delete self->cpp_obj;

    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject *
PyReLUD_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    PyReLUDObject *self = (PyReLUDObject*)type->tp_alloc(type, 0);
    if (self) {
        self->cpp_obj = nullptr;
    }
    return (PyObject*)self;
}

static int
PyReLUD_init(PyReLUDObject *self, PyObject *args, PyObject *kwds)
{
    Py_ssize_t prev, cur;
    try {
        // allocate your C++ object
        self->cpp_obj = new ReLUD();
    } catch (const std::exception &e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return -1;
    }
    return 0;
}

static PyObject * 
PyReLUD_forward(PyReLUDObject *self, PyObject *arg){
    PyReLUDObject *relu_obj = (PyReLUDObject*) self;

    static char *kwlist[] = { (char*)"x", NULL };
    if (!PyObject_TypeCheck(arg, &PyArrayD2Type)) {
        PyErr_SetString(PyExc_TypeError, "forward() expects an ArrayD2");
        return NULL;
    }
    PyArrayD2Object *input_obj = (PyArrayD2Object*)arg;

    ArrayD2 out_cpp;
    try {
        out_cpp = relu_obj->cpp_obj->forward(*input_obj->cpp_obj, 8, 8);
    } catch (const std::exception &e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return NULL;
    }

    // Allocate a new Python ArrayD2 object
    PyObject *out_py = PyArrayD2Type.tp_new(&PyArrayD2Type, NULL, NULL);
    if (!out_py) return NULL;

    // Steal the C++ result into its cpp_obj
    ((PyArrayD2Object*)out_py)->cpp_obj = new ArrayD2(std::move(out_cpp));

    return out_py;
}

static PyObject * 
PyReLUD_backward(PyReLUDObject *self, PyObject *arg){
    PyReLUDObject *relu_obj = (PyReLUDObject*) self;

    if (!PyObject_TypeCheck(arg, &PyArrayD2Type)) {
        PyErr_SetString(PyExc_TypeError, "forward() expects an ArrayD2");
        return NULL;
    }
    PyArrayD2Object *input_obj = (PyArrayD2Object*)arg;

    ArrayD2 out_cpp;
    try {
        out_cpp = relu_obj->cpp_obj->backward(*input_obj->cpp_obj);
    } catch (const std::exception &e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return NULL;
    }

    // Allocate a new Python ArrayD2 object
    PyObject *out_py = PyArrayD2Type.tp_new(&PyArrayD2Type, NULL, NULL);
    if (!out_py) return NULL;

    // Steal the C++ result into its cpp_obj
    ((PyArrayD2Object*)out_py)->cpp_obj = new ArrayD2(std::move(out_cpp));

    return out_py;
}

PyMethodDef PyReLUD_methods[] = {
    {"forward", (PyCFunction)PyReLUD_forward, METH_O, "forward(x)->y"},
    {"backward", (PyCFunction)PyReLUD_backward, METH_O, "backward(x)->y"},
    {NULL, NULL, 0, NULL}
};

PyGetSetDef PyReLUD_getset[] = {
    {NULL, NULL, NULL, NULL, NULL}
};

PyTypeObject PyReLUDType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name      = "pypearl.ReLU",
    .tp_basicsize = sizeof(PyReLUDObject),
    .tp_dealloc   = (destructor)PyReLUD_dealloc,
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_doc       = "Neural Network Layer",
    .tp_methods   = PyReLUD_methods,
    .tp_getset    = PyReLUD_getset,
    .tp_new       = PyReLUD_new,
    .tp_init      = (initproc)PyReLUD_init,
};



#endif