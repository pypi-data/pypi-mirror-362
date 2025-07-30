from .utils import identity


det_cache: dict = {}


class Matrix:
    def __init__(
            self, matrix: list[list[int | float | complex]]) -> None:
        l: int = len(matrix[0])
        for row in matrix:
            if len(row) != l:
                raise ValueError("matrix must be rectangular.")
        self.matrix: list[list[int | float | complex]] = matrix
        self.nrows: int = len(matrix)
        self.ncols: int = len(matrix[0])
        self.size = (self.nrows, self.ncols)

    def __str__(self) -> str:
        output: str = ""
        for row in self.matrix:
            output += str(row) + "\n"
        return output

    def __repr__(self) -> str:
        return str(self)

    def __add__(self, matrix1: "Matrix") -> "Matrix":
        if self.size != matrix1.size:
            raise ValueError("matrices must be of the same size.")
        output: list[list[int | float | complex]] = []
        for i in range(self.nrows):
            row: list[int | float | complex] = []
            for j in range(self.ncols):
                row.append(self.matrix[i][j] + matrix1.matrix[i][j])
            output.append(row)
        return Matrix(output)

    def __sub__(self, matrix1: "Matrix") -> "Matrix":
        return self + (-1) * matrix1

    def transpose(self,) -> "Matrix":
        output: list[list[int | float | complex]] = []
        for j in range(self.ncols):
            row: list[int | float | complex] = []
            for i in range(self.nrows):
                row.append(self.matrix[i][j])
            output.append(row)
        return Matrix(output)

    def __mul__(self, other) -> "Matrix":
        if isinstance(other, Matrix):
            if self.ncols != other.nrows:
                raise ValueError("matrix sizes are incompatible.")
            output = []
            for i in range(self.nrows):
                row = []
                for k in range(other.ncols):
                    total = sum(
                        self.matrix[i][j] * other.matrix[j][k] for j in range(self.ncols)
                    )
                    row.append(total)
                output.append(row)
            return Matrix(output)

        elif isinstance(other, (int, float, complex)):
            output = [
                [elem * other for elem in row]
                for row in self.matrix
            ]
            return Matrix(output)

        else:
            raise TypeError(f"Unsupported operand type(s) for *: 'Matrix' and '{type(other).__name__}'")

    def __rmul__(self, other) -> "Matrix":
        return self * other

    def __pow__(self, n) -> "Matrix":
        if n < 0:
            return self.inverse() ** (-n)
        output = 1
        for i in range(n):
            output *= self
        return output

    def __neg__(self):
        return -1 * self

    def __pos__(self):
        return self

    def concat(self, matrix1: "Matrix") -> "Matrix":
        if self.nrows != matrix1.nrows:
            raise ValueError("matrix sizes are incompatible.")
        output: list[list[int | float | complex]] = []
        for i in range(self.nrows):
            output.append(self.matrix[i] + matrix1.matrix[i])
        return Matrix(output)

    def __eq__(self, matrix1: "Matrix") -> bool:
        return self.matrix == matrix1.matrix

    def __ne__(self, matrix1: "Matrix") -> bool:
        return not (self == matrix1)

    def __hash__(self) -> int:
        output: int = 0
        for i in range(self.nrows):
            for x in self.matrix[i]:
                output += i * x
        return output

    def is_symmetric(self) -> bool:
        return self.matrix == self.transpose().matrix

    def is_skew_symmetric(self) -> bool:
        return (
                self.matrix
                == (self.transpose() * -1).matrix
        )

    def is_square(self) -> bool:
        return self.nrows == self.ncols

    def is_zeros(self) -> bool:
        for row in self.matrix:
            for element in row:
                if element != 0:
                    return False
        return True

    def is_ones(self) -> bool:
        for row in self.matrix:
            for element in row:
                if element != 1:
                    return False
        return True

    def row_add(
            self, index1: int, index2: int, scalar_multiple: int | float | complex
    ) -> None:
        result: list[int | float | complex] = []
        for i in range(self.ncols):
            result.append(
                self.matrix[index1][i] + scalar_multiple * self.matrix[index2][i]
            )
        self.matrix[index1] = result

    def row_multiply(self, index: int, scalar_multiple: int | float | complex) -> None:
        result: list[int | float | complex] = []
        for i in range(self.ncols):
            result.append(self.matrix[index][i] * scalar_multiple)
        self.matrix[index] = result

    def row_swap(self, index1: int, index2: int) -> None:
        self.matrix[index1], self.matrix[index2] = (
            self.matrix[index2],
            self.matrix[index1],
        )

    def num_elements(self) -> int:
        return self.nrows * self.ncols

    def det(self) -> int | float | complex:
        if not self.is_square():
            raise ValueError("matrix is not square.")
        key = tuple(tuple(row) for row in self.matrix)
        if key in det_cache:
            return det_cache[key]
        if self.num_elements() == 1:
            return self.matrix[0][0]
        result: int | float | complex = 0
        for i in range(self.ncols):
            new_matrix = []
            for x in range(1, self.nrows):
                row = []
                for y in range(self.ncols):
                    if y != i:
                        row.append(self.matrix[x][y])
                new_matrix.append(row)
            result += (
                    (-1) ** i
                    * self.matrix[0][i]
                    * Matrix(new_matrix).det()
            )
        det_cache[key] = result
        return result

    def is_singular(self) -> bool:
        return self.det() == 0

    def is_invertible(self) -> bool:
        return not self.is_singular()

    def is_orthogonally_diagonalisable(self) -> bool:
        return self.is_symmetric()

    def in_ref(self) -> bool:
        lead_col = -1
        zero_row_found = False
        for row in self.matrix:
            if all(elem == 0 for elem in row):
                zero_row_found = True
                continue
            if zero_row_found:
                return False
            for j, elem in enumerate(row):
                if elem != 0:
                    if j <= lead_col:
                        return False
                    lead_col = j
                    break
        return True

    def in_rref(self) -> bool:
        if not self.in_ref():
            return False
        for row in self.matrix:
            for j, elem in enumerate(row):
                if elem != 0:
                    if elem != 1:
                        return False
                    for i in range(self.nrows):
                        if i != self.matrix.index(row) and self.matrix[i][j] != 0:
                            return False
                    break
        return True

    def rref(self, tol: float = 1e-10) -> "Matrix":
        mat = [row[:] for row in self.matrix]
        nrows, ncols = self.nrows, self.ncols
        lead = 0
        for r in range(nrows):
            if lead >= ncols:
                break
            i = r
            while i < nrows and abs(mat[i][lead]) < tol:
                i += 1
            if i == nrows:
                lead += 1
                if lead == ncols:
                    break
                r -= 1
                continue
            mat[r], mat[i] = mat[i], mat[r]
            lv = mat[r][lead]
            if abs(lv) > tol:
                mat[r] = [mrx / lv for mrx in mat[r]]
            for i in range(nrows):
                if i != r:
                    lv = mat[i][lead]
                    mat[i] = [iv - lv * rv for rv, iv in zip(mat[r], mat[i])]
            lead += 1
        for i in range(nrows):
            for j in range(ncols):
                if abs(mat[i][j]) < tol:
                    mat[i][j] = 0
        return Matrix(mat)

    def inverse(self) -> "Matrix":
        if not self.is_invertible():
            raise ValueError("matrix is not invertible.")
        aug_matrix = self.concat(
            identity(self.nrows, as_matrix=True),
        )
        reduced = aug_matrix.rref()
        inv = [row[self.nrows :] for row in reduced.matrix]
        return Matrix(inv)