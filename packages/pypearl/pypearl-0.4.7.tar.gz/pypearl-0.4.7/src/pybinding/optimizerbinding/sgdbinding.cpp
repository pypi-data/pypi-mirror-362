#ifndef SGDBINDING
#define SGDBINDING
#include "sgdbinding.hpp"

static void
PySGDD_dealloc(PySGDDObject *self)
{
    delete self->cpp_obj;

    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject *
PySGDD_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    PySGDDObject *self = (PySGDDObject*)type->tp_alloc(type, 0);
    if (self) {
        self->cpp_obj = nullptr;
    }
    return (PyObject*)self;
}

static int
PySGDD_init(PySGDDObject *self, PyObject *args, PyObject *kwds)
{
    Py_ssize_t prev, cur;
    try {
        // allocate your C++ object
        self->cpp_obj = new SGDD(0.001);
    } catch (const std::exception &e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return -1;
    }
    return 0;
}

static PyObject*
PySGDD_optimize(PySGDDObject *self, PyObject *arg){

    if (!PyObject_TypeCheck(arg, &PyLayerDType)) {
        PyErr_SetString(PyExc_TypeError, "forward() expects an ArrayD2");
        return NULL;
    }
    PyLayerDObject *input_obj = (PyLayerDObject*)arg;

    try {
        self->cpp_obj->optimize_layer(*input_obj->cpp_obj);
    } catch (const std::exception &e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return NULL;
    }


    Py_RETURN_NONE;
}


PyMethodDef PySGDD_methods[] = {
    {"optimize", (PyCFunction)PySGDD_optimize, METH_O, "layer->optimized layer"},
    {NULL, NULL, 0, NULL}
};

PyGetSetDef PySGDD_getset[] = {
    {NULL, NULL, NULL, NULL, NULL}
};

PyTypeObject PySGDDType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name      = "pypearl.SGD",
    .tp_basicsize = sizeof(PySGDDObject),
    .tp_dealloc   = (destructor)PySGDD_dealloc,
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_doc       = "Neural Network SGD",
    .tp_methods   = PySGDD_methods,
    .tp_getset    = PySGDD_getset,
    .tp_new       = PySGDD_new,
    .tp_init      = (initproc)PySGDD_init,
};



#endif