from typing import List
import numpy as np


class Matrix:
    def __init__(self, values):
        # if not (isinstance(values, list)):
        #     raise ValueError('Expected LIST of values as argument')
        if len(values) == 0:
            self.n = 0
            self.m = 0
            pass
        self.n = len(values)
        self.m = len(values[0])
        self.values = values
        # if not all(list(map(lambda x: isinstance(x, list), values))):
        #     raise ValueError('Every element of values expected to be a list')
        if not all(list(map(lambda x: x == self.m, [len(elem) for elem in values]))):
            raise ValueError(f'Every row is expected to have the same length equal to {self.m}')

    def __compare_dimensions__(self, other):
        if self.n != other.n or self.m != other.m:
            raise ValueError(
                f'Matrix dimensions missmatch: {self.n}x{self.m} vs {other.n}x{other.m}'
            )

    def __add__(self, other):
        self.__compare_dimensions__(other)
        result = [
            [self.values[i][j] + other.values[i][j] for j in range(self.m)]
            for i in range(self.n)
        ]
        return Matrix(result)

    def __mul__(self, other):
        self.__compare_dimensions__(other)
        result = [
            [self.values[i][j] * other.values[i][j] for j in range(self.m)]
            for i in range(self.n)
        ]
        return Matrix(result)

    def __matmul__(self, other):
        if self.m != other.m:
            raise RuntimeError(
                f'Matrix dimension mismatch: {self.n}x{self.m} and {other.m}x{other.n}')
        result = [[0 for _ in range(self.m)]for _ in range(self.m)]
        for i in range(self.n):
            for j in range(self.m):
                for k in range(self.m):
                    result[i][j] += self.values[i][k] * other.values[k][j]
        return Matrix(result)

    def __str__(self):
        return np.array(self.values).__str__()


class StrMixIn:
    def __str__(self):
        return self.value.__str__()


class GetterMixIn:
    def get(self, i, j):
        return self.value[i][j]


class SetterMixIn:
    def set(self, i, j, value):
        self.value[i][j] = value


class WriteToFileMixIn:
    def write_to_file(self, filepath):
        with open(filepath, 'w') as f:
            f.write(self.__str__())


class ArrayLike(np.lib.mixins.NDArrayOperatorsMixin,
                StrMixIn, WriteToFileMixIn,
                GetterMixIn, SetterMixIn):
    def __init__(self, value):
        self.value = np.asarray(value)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        out = kwargs.get('out', ())
        for x in inputs + out:
            # Only support operations with instances of _HANDLED_TYPES.
            # Use ArrayLike instead of type(self) for isinstance to
            # allow subclasses that don't override __array_ufunc__ to
            # handle ArrayLike objects.
            if not isinstance(x, (np.ndarray, ArrayLike)):
                return NotImplemented

        # Defer to the implementation of the ufunc on unwrapped values.
        inputs = tuple(x.value if isinstance(x, ArrayLike) else x
                       for x in inputs)
        if out:
            kwargs['out'] = tuple(
                x.value if isinstance(x, ArrayLike) else x
                for x in out)
        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple:
            # multiple return values
            return tuple(type(self)(x) for x in result)
        elif method == 'at':
            # no return value
            return None
        else:
            # one return value
            return type(self)(result)


if __name__ == '__main__':
    np.random.seed(0)
    # Easy
    a = Matrix(np.random.randint(0, 10, (10, 10)))
    b = Matrix(np.random.randint(0, 10, (10, 10)))
    with open('artifacts/easy/matrix+.txt', 'w') as f:
        f.write((a + b).__str__())
    with open('artifacts/easy/matrix_dot.txt', 'w') as f:
        f.write((a * b).__str__())
    with open('artifacts/easy/matrix@.txt', 'w') as f:
        f.write((a @ b).__str__())
    # Medium
    a = ArrayLike(np.random.randint(0, 10, (10, 10)))
    b = ArrayLike(np.random.randint(0, 10, (10, 10)))
    (a + b).write_to_file('artifacts/medium/matrix+.txt')
    (a * b).write_to_file('artifacts/medium/matrix_dot.txt')
    (a @ b).write_to_file('artifacts/medium/matrix@.txt')
