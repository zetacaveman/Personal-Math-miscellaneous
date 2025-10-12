class Dual:
# We use dual number to realize forward pass of automatic differentiation. 
# The calculus is easy, dual number is a number \e (actually it should be understood in terms of abstract algebra not real number)
# \e^2 = 0. So f(x + a * \e) = f(x) + a * f'(x) e. This gives easy way to calculate the first derivative. 
    def __init__(self, value, derivative=0.0):
        self.value = float(value)
        self.derivative = float(derivative)  # acts like ẋ

    # --- helpers ---
    @staticmethod
    def _coerce(other):
        return other if isinstance(other, Dual) else Dual(other, 0.0)

    # --- addition / subtraction ---
    def __add__(self, other):
        other = Dual._coerce(other)
        return Dual(self.value + other.value, self.derivative + other.derivative)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        other = Dual._coerce(other)
        return Dual(self.value - other.value, self.derivative - other.derivative)

    def __rsub__(self, other):
        other = Dual._coerce(other)
        return Dual(other.value - self.value, other.derivative - self.derivative)

    # --- multiplication / division ---
    def __mul__(self, other):
        other = Dual._coerce(other)
        return Dual(self.value * other.value,
                    self.value * other.derivative + self.derivative * other.value)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        other = Dual._coerce(other)
        v = self.value / other.value
        d = (self.derivative * other.value - self.value * other.derivative) / (other.value ** 2)
        return Dual(v, d)

    def __rtruediv__(self, other):
        other = Dual._coerce(other)
        return other.__truediv__(self)

    # --- power (n is a real scalar) ---
    def __pow__(self, n):
        # f = x^n => f' = n*x^(n-1) * x'
        return Dual(self.value ** n, n * (self.value ** (n - 1)) * self.derivative)

    # --- unary ---
    def __neg__(self):
        return Dual(-self.value, -self.derivative)

    def __repr__(self):
        return f"Dual(value={self.value}, derivative={self.derivative})"
