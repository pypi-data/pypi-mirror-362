#ifndef CCEBINDING
#define CCEBINDING
#include "ccebinding.hpp"

static void
PyCCED_dealloc(PyCCEDObject *self)
{
    delete self->cpp_obj;

    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject *
PyCCED_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    PyCCEDObject *self = (PyCCEDObject*)type->tp_alloc(type, 0);
    if (self) {
        self->cpp_obj = nullptr;
    }
    return (PyObject*)self;
}

static int
PyCCED_init(PyCCEDObject *self, PyObject *args, PyObject *kwds)
{
    try {
        self->cpp_obj = new CCED();
    } catch (const std::exception &e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return -1;
    }
    return 0;
}

static PyObject * 
PyCCED_forward(PyCCEDObject *self, PyObject *args, PyObject *kwds){
    PyArrayD2Object *output_obj = NULL;  
    PyArrayI2Object *actual_obj = NULL;  

    static char *kwlist[] = { "output", "actual", NULL };

    if (!PyArg_ParseTupleAndKeywords(
            args, kwds,
            "O!O!",                   /* two objects, both must be ArrayD2 */
            kwlist,
            &PyArrayD2Type, &output_obj,
            &PyArrayI2Type, &actual_obj))
    {
        /* PyArg_ParseTupleAndKeywords has already set an exception */
        return NULL;
    }

    double loss;
    try {
        loss = self->cpp_obj->forwardClass(*output_obj->cpp_obj, 8, 8, *actual_obj->cpp_obj);
    } catch (const std::exception &e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return NULL;
    }

    return PyFloat_FromDouble(loss);

}

static PyObject * 
PyCCED_backward(PyCCEDObject *self, PyObject *args, PyObject *kwds){
    PyArrayD2Object *output_obj = NULL;  
    PyArrayI2Object *actual_obj = NULL;  

    static char *kwlist[] = { "output", "actual", NULL };

    if (!PyArg_ParseTupleAndKeywords(
            args, kwds,
            "O!O!",                   /* two objects, both must be ArrayD2 */
            kwlist,
            &PyArrayD2Type, &output_obj,
            &PyArrayI2Type, &actual_obj))
    {
        /* PyArg_ParseTupleAndKeywords has already set an exception */
        return NULL;
    }

    PyObject *out_py = PyArrayD2Type.tp_new(&PyArrayD2Type, NULL, NULL);
    try {
        ArrayD2 grad_cpp = self->cpp_obj->backwardClass(*actual_obj->cpp_obj, *output_obj->cpp_obj);
        ((PyArrayD2Object *)out_py)->cpp_obj = new ArrayD2(std::move(grad_cpp));
    } catch (const std::exception &e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return NULL;
    }

    return out_py;

}


PyMethodDef PyCCED_methods[] = {
    {"forward", (PyCFunction)PyCCED_forward, METH_VARARGS | METH_KEYWORDS, "forward(output, actual)->loss"},
    {"backward", (PyCFunction)PyCCED_backward, METH_VARARGS | METH_KEYWORDS, "backward(output, actual)->dvals"},
    {NULL, NULL, 0, NULL}
};

PyGetSetDef PyCCED_getset[] = {
    {NULL, NULL, NULL, NULL, NULL}
};

PyTypeObject PyCCEDType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name      = "pypearl.CCED",
    .tp_basicsize = sizeof(PyCCEDObject),
    .tp_dealloc   = (destructor)PyCCED_dealloc,
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_doc       = "Neural Network CCED",
    .tp_methods   = PyCCED_methods,
    .tp_getset    = PyCCED_getset,
    .tp_new       = PyCCED_new,
    .tp_init      = (initproc)PyCCED_init,
};

#endif