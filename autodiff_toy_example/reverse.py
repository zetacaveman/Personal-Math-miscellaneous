#For the reverse mode, we need to use the computational graph structure
#explicitly, unlike the forward mode. We need to differentiate each node 
#with respect to its parents and store the derivative information.
#So it uses both graph traversing (DFS) and dynamic programing.

class Node:
    def __init__(self, value, _prev=()):
        self.value = float(value)
        self.grad = 0.0
        self._backward = lambda: None
        self._prev = _prev  # parents (tuple)

    # ---- helpers ----
    @staticmethod
    def _coerce(x):
        return x if isinstance(x, Node) else Node(x)

    # ---- addition / subtraction ----
    def __add__(self, other):
        other = Node._coerce(other)
        out = Node(self.value + other.value, (self, other))

        def _backward():
            self.grad += 1.0 * out.grad
            other.grad += 1.0 * out.grad
        out._backward = _backward
        return out

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        other = Node._coerce(other)
        out = Node(self.value - other.value, (self, other))

        def _backward():
            self.grad += 1.0 * out.grad
            other.grad += -1.0 * out.grad
        out._backward = _backward
        return out

    def __rsub__(self, other):
        other = Node._coerce(other)
        return other.__sub__(self)

    # ---- multiplication / division ----
    def __mul__(self, other):
        other = Node._coerce(other)
        out = Node(self.value * other.value, (self, other))

        def _backward():
            self.grad += other.value * out.grad
            other.grad += self.value * out.grad
        out._backward = _backward
        return out

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        other = Node._coerce(other)
        out = Node(self.value / other.value, (self, other))

        def _backward():
            self.grad += (1.0 / other.value) * out.grad
            other.grad += (-self.value / (other.value**2)) * out.grad
        out._backward = _backward
        return out

    def __rtruediv__(self, other):
        other = Node._coerce(other)
        return other.__truediv__(self)

    # ---- power (scalar exponent) ----
    def __pow__(self, n):
        # n is a Python number
        out = Node(self.value ** n, (self,))

        def _backward():
            self.grad += (n * (self.value ** (n - 1))) * out.grad
        out._backward = _backward
        return out

    # ---- unary ----
    def __neg__(self):
        out = Node(-self.value, (self,))
        def _backward():
            self.grad += -1.0 * out.grad
        out._backward = _backward
        return out

    def __repr__(self):
        return f"Node(value={self.value}, grad={self.grad})"


def backward(node: Node):
    # build topological order
    topo = []
    visited = set()
    def build(v):
        if v not in visited:
            visited.add(v)
            for p in v._prev:
                build(p)
            topo.append(v)
    build(node)

    node.grad = 1.0
    for v in reversed(topo):
        v._backward()


# ---- Example ----
x = Node(2.0)
y = (x**4) + 3*(x**2) + 2*x

backward(y)
print(f"f(2) = {y.value}, f'(2) = {x.grad}")
# Expected: f(2) = 32.0, f'(2) = 46.0