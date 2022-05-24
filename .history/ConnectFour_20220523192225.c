#define PY_SSIZE_T_CLEAN
#include <Python.h>

typedef enum
{
    EMPTY = 0,
    YELLOW = -1,
    RED = 1,
} Color;

#define kRows 6
#define kColumns 7

typedef struct
{
    PyObject_HEAD;
    Color board[kRows][kColumns];
} PyBoard;

static int place_piece(Color board[kRows][kColumns], int column, Color color)
{
    for (int i = kRows - 1; i >= 0; i--)
    {
        if (board[i][column] == EMPTY)
        {
            board[i][column] = color;
            return i;
        }
    }
    return -1;
}

// Return an integer: 0 for not done, 10*color for the color that wins.
static int check_done(const Color board[kRows][kColumns], int row, int column, Color color)
{
    // Check vertically.
    int in_a_row = 1;
    for (int r = row + 1; r < kRows; r++)
    {
        if (board[r][column] == color)
        {
            in_a_row++;
        }
        else
        {
            break;
        }
    }
    if (in_a_row >= 4)
    {
        return 10 * color;
    }

    // Check horizontally.
    in_a_row = 1;
    for (int c = column + 1; c < kColumns; c++)
    {
        if (board[row][c] == color)
        {
            in_a_row++;
        }
        else
        {
            break;
        }
    }

    for (int c = column - 1; c >= 0; c--)
    {
        if (board[row][c] == color)
        {
            in_a_row++;
        }
        else
        {
            break;
        }
    }

    if (in_a_row >= 4)
    {
        return 10 * color;
    }

    // check diagonally right
    in_a_row = 1;
    for (int r = row + 1, c = column - 1; r < kRows && c >= 0; r++, c--)
    {
        if (board[r][c] == color)
        {
            in_a_row++;
        }
        else
        {
            break;
        }
    }

    for (int r = row - 1, c = column + 1; r >= 0 && c < kColumns; r--, c++)
    {
        if (board[r][c] == color)
        {
            in_a_row++;
        }
        else
        {
            break;
        }
    }

    if (in_a_row >= 4)
    {
        return 10 * color;
    }
    // check diagonally left

    in_a_row = 1;
    for (int r = row + 1, c = column + 1; r < kRows && c < kColumns; c++, r++)
    {
        if (board[r][c] == color)
        {
            in_a_row++;
        }
        else
        {
            break;
        }
    }

    for (int r = row - 1, c = column - 1; r >= 0 && c >= 0; r--, c--)
    {
        if (board[r][c] == color)
        {
            in_a_row++;
        }
        else
        {
            break;
        }
    }

    if (in_a_row >= 4)
    {
        return 10 * color;
    }
    return 0;
}

static PyObject *PyBoard_get_color(PyBoard *self, PyObject *args)
{
    int row, col;
    if (!PyArg_ParseTuple(args, "ii", &row, &col))
    {
        return NULL;
    }
    return PyLong_FromLong(self->board[row][col]);
}

static PyObject *PyBoard_place_piece(PyBoard *self, PyObject *args)
{
    // Parse args.
    int column, color;
    if (!PyArg_ParseTuple(args, "ii", &column, &color))
    {
        return NULL;
    }
    int result = place_piece(self->board, column, color);
    if (result == -1)
    {
        return Py_None;
    }
    else
    {
        return PyLong_FromLong(result);
    }
}

static PyObject *PyBoard_check_done(PyBoard *self, PyObject *args)
{
    // Parse args.
    int row, column, color;
    if (!PyArg_ParseTuple(args, "iii", &row, &column, &color))
    {
        return NULL;
    }

    return PyLong_FromLong(check_done(self->board, row, column, color));
}

static PyObject *PyBoard_test(PyBoard *self, PyObject *args)
{
    return PyLong_FromLong(42);
}

static int PyBoard_init(PyBoard *self, PyObject *args, PyObject *kwds)
{
    memset(self->board, EMPTY, sizeof(self->board));
    return 0;
}

static void PyBoard_dealloc(PyBoard *self)
{
    if (Py_TYPE(self) == Py_None)
    {
        return NULL;
    }
    Py_TYPE(self)->tp_free((PyObject *)self);
}

static PyMethodDef PyBoard_methods[] = {
    {"test", (PyCFunction)PyBoard_test, METH_VARARGS, "Python interface for awesome connect four"},
    {"place_piece", (PyCFunction)PyBoard_place_piece, METH_VARARGS, "Places a piece at col with color"},
    {"check_done", (PyCFunction)PyBoard_check_done, METH_VARARGS, "Checks if connect four is won by anybody"},
    {"get_color", (PyCFunction)PyBoard_get_color, METH_VARARGS, "Returns the piece that is at that place"},
    {NULL, NULL, 0, NULL},
};

static PyTypeObject PyBoardType = {PyVarObject_HEAD_INIT(NULL, 0) "cConnectFour.Board"};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "cConnectFour",
    "Python interface module for connect four",
    -1,
};

PyMODINIT_FUNC PyInit_cConnectFour()
{
    PyObject *m;

    PyBoardType.tp_new = PyType_GenericNew;
    PyBoardType.tp_basicsize = sizeof(PyBoard);
    PyBoardType.tp_dealloc = (destructor)PyBoard_dealloc;
    PyBoardType.tp_flags = Py_TPFLAGS_DEFAULT;
    PyBoardType.tp_doc = "Board type";
    PyBoardType.tp_methods = PyBoard_methods;
    PyBoardType.tp_init = (initproc)PyBoard_init;

    if (PyType_Ready(&PyBoardType) < 0)
        return NULL;

    m = PyModule_Create(&module);
    if (m == NULL)
        return NULL;

    Py_INCREF(&PyBoardType);
    PyModule_AddObject(m, "Board", (PyObject *)&PyBoardType);

    return m;
}
