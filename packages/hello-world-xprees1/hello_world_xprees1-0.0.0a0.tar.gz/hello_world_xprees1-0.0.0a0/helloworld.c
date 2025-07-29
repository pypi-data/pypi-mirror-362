#include <Python.h>

static PyObject* hello(PyObject* self, PyObject* args) {
    PySys_WriteStdout("Hello World!\n");  
    return Py_BuildValue("");  
}

static PyMethodDef HelloWorldMethods[] = {
    {"hello", hello, METH_NOARGS, "Print hello world"},
    {NULL, NULL, 0, NULL}  
};

static struct PyModuleDef helloworldmodule = {
    PyModuleDef_HEAD_INIT,
    "helloworld", 
    NULL, 
    -1,
    HelloWorldMethods
};

PyMODINIT_FUNC PyInit_helloworld(void) {
    return PyModule_Create(&helloworldmodule);
}