#include <Python.h>

static PyObject* hello(PyObject* self, PyObject* args) {
    printf("Hello, World!");
    Py_RETURN_NONE;
}

static PyObject* hello_with(PyObject* self, PyObject* args) {
    const char* name;
    if (!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }
    printf("Hello %s!\n", name);
    Py_RETURN_NONE;
}

static PyObject* about_info(PyObject* self, PyObject* args) {
    printf(
        "Author: xprees1"
        "Version: 0.0.0hotfix3"
        "Other Info: This version is just a development joke!"
    );
    Py_RETURN_NONE;
}

static PyObject* about_history(PyObject* self, PyObject* args) {
    printf(
        "This is a joke of xprees1! Don't take it seriously! "
        "It's just because xprees1 is really not good at programming python, "
        "so he tried to use his C++ to program Python-C Extension."
    );
    Py_RETURN_NONE;
}

static PyObject* whatsnew(PyObject* self, PyObject* args) {
    printf(
        "Version 0.0.0b0:\n"
        "1. Fixed the version bug while building of 0.0.0a0\n"
        "2. Add \"Hello World with sb\" & \"About\"\n"
        "3. Add \"What's New\" Part\n\n"
        "Version 0.0.0rc0:\n"
        "1.Fixed the bug of return instead of print.\n\n"
        "Version 0.0.0hotfix0~2:\n"
        "NOT REAL VERSION BECAUSE IT DON'T RELEASE\n\n"
        "Version 0.0.0hotfix3(0.0.0rc1-dev):\n"
        "1.Fixed the bug of 0.0.0rc0: Have no return value.\n"
        "2.Fixed the README.md: Don't Update the Version."
    );
    Py_RETURN_NONE;
}

static PyMethodDef methods[] = {
    {"hello", hello, METH_NOARGS, "Print hello world"},
    {"hello_with", hello_with, METH_VARARGS, "Print hello with name"},
    {"whatsnew", whatsnew, METH_NOARGS, "Show update history"},
    {NULL, NULL, 0, NULL}
};

static PyMethodDef about_methods[] = {
    {"info", about_info, METH_NOARGS, "Get module info"},
    {"history", about_history, METH_NOARGS, "Get module history"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "helloworld",
    NULL,
    -1,
    methods
};

static struct PyModuleDef about_module = {
    PyModuleDef_HEAD_INIT,
    "about",
    NULL,
    -1,
    about_methods
};

PyMODINIT_FUNC PyInit_helloworld(void) {
    PyObject* m = PyModule_Create(&module);
    
    PyObject* about = PyModule_Create(&about_module);
    PyModule_AddObject(m, "about", about);
    
    return m;
}