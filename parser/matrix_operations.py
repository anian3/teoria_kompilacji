def matrix_addition(A, B):
    if isinstance(A, list) and isinstance(B, list):
        if len(A) != len(B) or len(A[0]) != len(B[0]):
            raise ValueError("Dodawanie element po elemencie na różnych rozmiarach macierzy.")
        return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
    else:
        raise ValueError("Dodawanie macierzowe wykonywane nie na macierzach.")


def matrix_substraction(A, B):
    if isinstance(A, list) and isinstance(B, list):
        if len(A) != len(B) or len(A[0]) != len(B[0]):
            raise ValueError("Odejmowanie element po elemencie na różnych rozmiarach macierzy.")
        return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
    else:
        raise ValueError("Odejmowanie macierzowe wykonywane nie na macierzach.")


def matrix_multiplication(A, B):
    if isinstance(A, list) and isinstance(B, list):
        if len(A) != len(B) or len(A[0]) != len(B[0]):
            raise ValueError("Mnożenie element po elemencie na różnych rozmiarach macierzy.")
        return [[A[i][j] * B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
    else:
        raise ValueError("Mnożenie macierzowe wykonywane nie na macierzach.")


def matrix_division(A, B):
    if isinstance(A, list) and isinstance(B, list):
        if len(A) != len(B) or len(A[0]) != len(B[0]):
            raise ValueError("Dzielenie element po elemencie na różnych rozmiarach macierzy.")
        for i in range(len(B)):
            for j in range(len(B[0])):
                if B[i][j] == 0:
                    raise ValueError("Dzielenie przez zero.")
        return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
    else:
        raise ValueError("Odejmowanie macierzowe wykonywane nie na macierzach.")


def matrix_transpose(A):
    if isinstance(A, list):
        return [[row[i] for row in A] for i in range(len(A[0]))]
    else:
        raise ValueError("Transpozycja wykonywana nie dla macierzy.")
