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
}  PyBoard;

static int PyBoard_init()

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

/*
def check_done(board: np.ndarray, row: int, column: int, color: int) -> int:
    # check vertically
    in_a_row = 1
    for r in range(row + 1, row_count):
        if board[r][column] == color:
            in_a_row += 1
        else:
            break
    if in_a_row >= 4:
        return 10*color

    # check horizontally
    in_a_row = 1
    for c in range(column + 1, column_count):
        if board[row][c] == color:
            in_a_row += 1
        else:
            break
    for c in range(column - 1, -1, -1):
        if board[row][c] == color:
            in_a_row += 1
        else:
            break
    if in_a_row >= 4:
        return 10*color

    # check diagonally right
    in_a_row = 1
    r = row - 1
    c = column + 1
    while r >= 0 and c < column_count:
        if board[r][c] == color:
            in_a_row += 1
        else:
            break
        r -= 1
        c += 1
    r = row + 1
    c = column - 1
    while r < row_count and c >= 0:
        if board[r][c] == color:
            in_a_row += 1
        else:
            break
        r += 1
        c -= 1
    if in_a_row >= 4:
        return 10*color

    # check diagonally left
    in_a_row = 1
    r = row - 1
    c = column - 1
    while r >= 0 and c >= 0:
        if board[r][c] == color:
            in_a_row += 1
        else:
            break
        r -= 1
        c -= 1
    r = row + 1
    c = column + 1
    while r < row_count and c < column_count:
        if board[r][c] == color:
            in_a_row += 1
        else:
            break
        r += 1
        c += 1
    if in_a_row >= 4:
        return 10*color

    return 0
*/

static PyObject* method_check_done(PyObject* self, PyObject* args) {
    // Parse args.
    PyObject* py_board;
    int row, column, color;
    if (!PyArg_ParseTuple(args, "Oiii", &py_board, &row, &column, &color)) {
        return NULL;
    }

    // Fill in the board.
    Color board[kRows][kColumns];

    // Board is a list of lists with kRows and kColumns.
    if (!PyList_Check(py_board) || PyList_Size(py_board) != kRows) {
        return NULL;
    }
    for (int i = 0; i < kRows; i++) {
        PyObject* py_row = PyList_GetItem(py_board, i);
        if (!PyList_Check(py_row) || PyList_Size(py_row) != kColumns) {
            return NULL;
        }
        for (int j = 0; j < kColumns; j++) {
            PyObject* py_entry = PyList_GetItem(py_row, j);
            if (!PyLong_Check(py_entry)) {
                return NULL;
            }
            board[i][j] = (Color)PyLong_AsLong(py_entry);
        }
    }

    return PyLong_FromLong(check_done(board, row, column, color));
}

static PyObject* method_test(PyObject* self, PyObject* args) {
    return PyLong_FromLong(42);
}

static PyMethodDef methods[] = {
    {"test", method_test, METH_VARARGS, "Python interface for awesome connect four"},
    {"check_done", method_check_done, METH_VARARGS, "Checks if connect four is won by anybody"},
    {NULL, NULL, 0, NULL},
};

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
