#define PY_SSIZE_T_CLEAN
#include <Python.h>

typedef enum {
    EMPTY = 0,
    YELLOW = -1,
    RED = 1,
} Color;

static const int kRows = 6;
static const int kColumns = 7;

typedef struct {
    PyObject_HEAD
    Color board[kRows][kColumns];
} PyBoard;

static int PyBoard_init(PyBoard* self, PyObject* args, PyObject* kwds) {
    return 0;
}

static void PyBoard_dealloc(PyBoard* self) {
    Py_TYPE(self)->tp_free(self);
}

// Return an integer: 0 for not done, 10*color for the color that wins.
static int check_done(const Color board[kRows][kColumns], int row, int column, Color color) {
    // Check vertically.
    int in_a_row = 1;
    for (int r = row + 1; r < kRows; r++) {
        if (board[r][column] == color) {
            in_a_row++;
        } else {
            break;
        }
    }
    if (in_a_row >= 4) {
        return 10 * color;
    }

    // Check horizontally.
    in_a_row = 1;
    for (int c = column + 1; c < kColumns; c++) {
        if (board[row][c] == color) {
            in_a_row ++;
        }
        else {
            break;
        }
    }

    for (int c = column - 1; c >= 0; c--) {
        if (board[row][c] == color) {
            in_a_row++;
        }
        else {
            break;
        }
    }

    if (in_a_row >= 4) {
        return 10 * color;
    }


    // check diagonally right
    in_a_row = 1;
    for (int r = row + 1, c = column - 1; r < kRows && c >= 0; r++, c--) {
        if (board[r][c] == color) {
            in_a_row ++;
        }
        else {
            break;
        }
    }
    
    for (int r = row - 1, c = column + 1; r >= 0 && c < kColumns; r--, c++) {
        if (board[r][c] == color) {
            in_a_row++;
        }
        else {
            break;
        }
    }

    if (in_a_row >= 4) {
        return 10 * color;
    }
    // check diagonally left

    in_a_row = 1;
    for (int r = row + 1, c = column + 1; r < kRows && c < kColumns; c++, r++) {
        if (board[r][c] == color) {
            in_a_row++;
        }
        else {
            break;
        }
    }

    for (int r = row - 1, c = column - 1; r >= 0 && c >= 0; r--, c--)  {
        if (board[r][c] == color) {
            in_a_row++;
        }
        else {
            break;
        }
    }

    if (in_a_row >= 4) {
        return 10 * color;
    }
    return 0;

}

static PyObject* PyBoard_check_done(PyBoard* self, PyObject* args) {
    // Parse args.
    PyObject* py_board;
    int row, column, color;
    if (!PyArg_ParseTuple(args, "iii", &row, &column, &color)) {
        return NULL;
    }

    return PyLong_FromLong(check_done(self->board, row, column, color));
}

static PyObject* PyBoard_test(PyBoard* self, PyObject* args) {
    return PyLong_FromLong(42);
}

static PyMethodDef PyVoice_methods[] = {
    {"test", (PyCFunction)PyBoard_test, METH_VARARGS, "Python interface for awesome connect four"},
    {"check_done", (PyCFunction)PyBoard_check_done, METH_VARARGS, "Checks if connect four is won by anybody"},
    {NULL, NULL, 0, NULL},
};

static PyTypeObject PyBoardType - { PyVarObject_HEAD_INIT(NULL, 0)

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "cConnectFour",
    "Python interface module for connect four",
    -1,
    methods,
};

PyMODINIT_FUNC PyInit_cConnectFour() {
    return PyModule_Create(&module);
}
