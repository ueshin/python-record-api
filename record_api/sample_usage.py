import numpy as np


def fn():
    x = np.arange(10)
    # unary method
    +x
    -x
    ~x

    # bool or length
    try:
        not x
    except ValueError:
        pass
    # iter
    for _ in x:
        pass

    # binary methods
    x[0]
    y = 2

    x ** y
    y ** x
    x * y
    y * x
    x @ x
    x // y
    y // x
    x % y
    y % x
    x + y
    y + x
    x - y
    y - x
    x << y
    y << x
    x >> y
    y >> x
    x & y
    y & x
    x | y
    y | x

    y = 2
    x **= y
    y = 2
    y **= x
    y = 2
    x *= y
    y = 2
    y *= x
    y = 2
    x //= y
    x %= y
    x += y
    x -= y
    x <<= y
    x >>= y
    x &= y
    x |= y
    x[0] = y

    # unpack
    _, *_s = x

    # create arrays

    np.arange(10)
    np.array([1, 2, 3])
    np.zeros((4, 5))
    np.ones((5, 4))
    np.linspace(0, 2, 100)
    np.eye(10)

    # attribtues
    x = np.arange(10)
    x.shape
    x.ndim
    x.dtype
    x.size

    # math

    x + x
    np.add(x, x)
    np.exp(x)
    np.log(x)

    # comparison
    x == x
    x < 2

    # sorting
    x.sort()
    x.sort(axis=0)

    # slicing
    x[x > 10]
    x[0]
    x[1:2]
    np.arange(10).reshape(5, 2)[((1, 2, 3), (0, 1, 1))]

    # manipulation
    x.T
    x.reshape((5, 2))
    np.column_stack([x, x])
    np.concatenate((x, x), axis=0)


fn()
