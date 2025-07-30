from .matrix import Matrix


class Vector(Matrix):
    def __init__(
            self,
            lst: list[int | float | complex],
            axis: int = 0
    ) -> None:
        for x in lst:
            if not isinstance(x, (int, float, complex)):
                raise ValueError("vector elements must be numbers.")
        self.elems: list = lst
        if axis == 0:
            self.vector: list[list[int | float | complex]] = [[x] for x in lst]
        elif axis == 1:
            self.vector: list[list[int | float | complex]] = [lst]
        else:
            raise ValueError("axis must be 0 (column vector) or 1 (row vector).")
        self.num_elems: int = len(lst)
        super().__init__(self.vector)

    def norm(self) -> float:
        return sum(abs(x) ** 2 for x in self.elems) ** 0.5

    def dot(self, vector1: "Vector") -> int | float | complex:
        if self.num_elems != vector1.num_elems:
            raise ValueError("vectors must be of the same size.")
        result: int | float | complex = 0
        for i in range(self.num_elems):
            result += self.elems[i] * vector1.elems[i]
        return result

    def cross(
            self, vector1: "Vector", axis: int = 0) -> "Vector":
        if not (self.num_elems == 3 == vector1.num_elems):
            raise ValueError("both vectors must have 3 elements each.")
        return Vector(
            [
                self.elems[1] * vector1.elems[2] - self.elems[2] * vector1.elems[1],
                self.elems[2] * vector1.elems[0] - self.elems[0] * vector1.elems[2],
                self.elems[0] * vector1.elems[1] - self.elems[1] * vector1.elems[0],
                ],
            axis=axis,
        )