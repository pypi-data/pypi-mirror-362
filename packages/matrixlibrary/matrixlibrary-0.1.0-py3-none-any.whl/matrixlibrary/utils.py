from .matrix import Matrix


def zeros(r: int, c: int, as_matrix: bool = True) -> Matrix | list[list[int]]:
    output: list[list[int]] = []
    for i in range(r):
        row: list[int] = []
        for j in range(c):
            row.append(0)
        output.append(row)
    return Matrix(output) if as_matrix else output


def ones(r: int, c: int, as_matrix: bool = True) -> Matrix | list[list[int]]:
    output: list[list[int]] = []
    for i in range(r):
        row: list[int] = []
        for j in range(c):
            row.append(1)
        output.append(row)
    return Matrix(output) if as_matrix else output


def diag(
        seq: list[int | float | complex] | tuple[int | float | complex],
        as_matrix: bool = True,
) -> Matrix | list[list[int | float | complex]]:
    n: int = len(seq)
    output: list[list[int]] = zeros(n, n, as_matrix=False)
    for i in range(n):
        output[i][i] = seq[i]
    return Matrix(output) if as_matrix else output


def identity(
        n: int, as_matrix: bool = True
) -> Matrix | list[list[int | float | complex]]:
    return diag([1] * n, as_matrix=as_matrix)


def display(matrix: list[list[int | float | complex]]) -> None:
    for row in matrix:
        print(row)
