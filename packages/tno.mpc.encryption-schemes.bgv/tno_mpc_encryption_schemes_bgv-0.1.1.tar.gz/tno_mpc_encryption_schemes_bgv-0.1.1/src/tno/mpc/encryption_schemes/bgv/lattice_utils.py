"""
Useful functions for polynomials, e.g. for creating lattice based encryption schemes.
"""

from __future__ import annotations

from math import ceil, exp, floor, pi, sqrt
from random import SystemRandom
from typing import Any

from tno.mpc.encryption_schemes.templates.exceptions import SerializationError

# Check to see if the communication module is available
try:
    from tno.mpc.communication import RepetitionError, Serialization

    COMMUNICATION_INSTALLED = True
except ModuleNotFoundError:
    COMMUNICATION_INSTALLED = False

_sysrand = SystemRandom()


class Polynomial:
    r"""
    Represents polynomial $c_0 + c_1 x + c_2 x^2 + ... + c_d x^d$ in a ring
    $R_q = \mathbb{Z}_q[x]/(x^n + 1)$, where $q$ is a positive integer and $n$ is a power of 2.
    """

    def __init__(self, coefficients: list[int], q: int, n: int) -> None:
        r"""
        Construct a new Polynomial $c_0 + c_1 x + c_2 x^2 + ... + c_d x^d$, an element of the a ring
        $R_q = \mathbb{Z}_q[x]/(x^n + 1)$. Coefficients are represented in the range
        $\[-\lfloor(q-1)/2\rfloor, \lceil(q-1)/2\rceil\]$.

        :param coefficients: Coefficients of the polynomial in order of increasing degree.
        :param q: Positive integer modulus of the coefficients.
        :param n: Power of 2, degree of ideal for quotient ring of which the polynomial is an
            element.
        :raise ValueError: When list of coefficients is empty, q is smaller than 1 or given n is not
            a power of 2.
        """

        if len(coefficients) < 1:
            raise ValueError(
                "List of coefficients is empty, expected at least one coefficient."
            )

        if q <= 0:
            raise ValueError("Value of q should be larger than 0.")

        if not n or (n & (n - 1)):
            raise ValueError("Value of n is not a power of 2.")

        self.q = q
        self.n = n
        self.coefficients = coefficients

        # reduce polynomial modulo (x^n + 1, q)
        while len(self.coefficients) > self.n:
            self.coefficients[-(self.n + 1)] -= self.coefficients[-1]
            self.coefficients.pop()
        self.coefficients = [coefficient % self.q for coefficient in self.coefficients]

        # remove zero coefficients of terms higher than the degree of the polynomial
        index = len(self.coefficients) - 1
        while self.coefficients[index] == 0 and index > 0:
            self.coefficients.pop(index)
            index -= 1

        # make sure coefficients are in the range [-floor((q-1)/2), ceil((q-1)/2)]
        self.coefficients = list(
            map(
                lambda coefficient: (
                    coefficient - self.q
                    if (self.q % 2 == 1 and coefficient > (self.q // 2))
                    or coefficient > ((self.q + 1) // 2)
                    else coefficient
                ),
                self.coefficients,
            )
        )

    def __eq__(self, other: object) -> bool:
        """
        Compare this Polynomial with another object to determine (in)equality.

        :param other: Object to compare this Polynomial with.
        :raise TypeError: If other object is not of the same type as this Polynomial.
        :return: Boolean representation of (in)equality of both objects.
        """
        if not isinstance(other, type(self)):
            raise TypeError(
                f"Expected comparison with another {type(self)}, got {type(other)} instead."
            )
        return (
            self.coefficients == other.coefficients
            and self.q == other.q
            and self.n == other.n
        )

    def __neg__(self) -> Polynomial:
        """
        Negate Polynomial by negating its coefficients.

        :return: Polynomial object with negated coefficients.
        """
        coefficients = [-coefficient for coefficient in self.coefficients]
        return Polynomial(coefficients, self.q, self.n)

    def __add__(self, other: Polynomial | int) -> Polynomial:
        """
        Add a Polynomial or integer scalar to this Polynomial.

        :raise ValueError: When adding Polynomials that are defined over different rings.
        :return: Polynomial object that results from adding the inputs.
        """
        if isinstance(other, int):
            coefficients = self.coefficients[:]
            coefficients[0] += other
        else:
            if self.q != other.q or self.n != other.n:
                raise ValueError(
                    f"Adding a polynomial over Z_{self.q}[x]/(x^{self.n} + 1)"
                    f"to a polynomial over Z_{other.q}[x]/(x^{other.n} + 1) is not possible."
                )

            coefficients = [
                (s + o) % self.q for s, o in zip(self.coefficients, other.coefficients)
            ]
            coefficients += self.coefficients[len(other.coefficients) :]
            coefficients += other.coefficients[len(self.coefficients) :]

        return Polynomial(coefficients, self.q, self.n)

    def __sub__(self, other: Polynomial | int) -> Polynomial:
        """
        Subtract another Polynomial or integer scalar from this Polynomial.

        :raise ValueError: When subtracting Polynomials that are defined over different rings.
        :return: Polynomial object that results from subtracting the inputs.
        """
        return self + -other

    def __radd__(self, other: Polynomial | int) -> Polynomial:
        """
        Right add this Polynomial with another Polynomial or integer. Because this
        operation is commutative, we can just left add.

        :return: Polynomial object that results from adding the inputs.
        """
        return self + other

    def __rsub__(self, other: Polynomial | int) -> Polynomial:
        """
        Subtract this Polynomial from another Polynomial or integer.

        :return: Polynomial object that results from subtracting the inputs.
        """
        return other + -self

    def __mul__(self, other: Polynomial | int) -> Polynomial:
        """
        Multiply this Polynomial with another Polynomial or integer scalar.

        :raise ValueError: When multiplying Polynomials that are defined over different rings.
        :return: Polynomial object that results from multiplying the inputs.
        """
        if isinstance(other, int):
            coefficients = [coefficient * other for coefficient in self.coefficients]
        else:
            if self.q != other.q or self.n != other.n:
                raise ValueError(
                    f"Multiplying a polynomial over Z_{self.q}[x]/(x^{self.n} + 1)"
                    f"with a polynomial over Z_{other.q}[x]/(x^{other.n} + 1) is not possible."
                )

            coefficients = [0] * (len(self.coefficients) + len(other.coefficients) - 1)
            for i, coefficient_self in enumerate(self.coefficients):
                for j, coefficient_other in enumerate(other.coefficients):
                    coefficients[i + j] += coefficient_self * coefficient_other

        return Polynomial(coefficients, self.q, self.n)

    def __rmul__(self, other: Polynomial | int) -> Polynomial:
        """
        Right multiply this Polynomial with another Polynomial or integer scalar. Because this
        operation is commutative, we can just left multiply.

        :return: Polynomial object that results from multiplying the inputs.
        """
        return self * other

    def __hash__(self) -> int:
        """
        Compute a hash from this Polynomial instance.

        :return: Hash value.
        """
        return hash((tuple(self.coefficients), self.q, self.n))

    def __str__(self) -> str:
        """
        String representaton of Polynomial.

        :return: String representation of Polynomial and its ring.
        """
        polynomial_string = str(self.coefficients[0])
        for i in range(1, len(self.coefficients)):
            polynomial_string += " + " + str(self.coefficients[i]) + "x^" + str(i)
        polynomial_string += " in Z_" + str(self.q) + "[x]/(x^" + str(self.n) + " + 1)"

        return polynomial_string

    def deg(self) -> int:
        """
        Returns degree of the Polynomial.

        :return: Integer degree of Polynomial
        """
        if self.coefficients == [0]:
            return -1
        return len(self.coefficients) - 1

    # region Serialization logic

    def serialize(self, **_kwargs: Any) -> dict[str, Any]:
        r"""
        Serialization function for Polynomial, which will be passed to the communication module.

        :param \**_kwargs: optional extra keyword arguments
        :raise SerializationError: When communication library is not installed.
        :return: serialized version of this Polynomial.
        """
        if not COMMUNICATION_INSTALLED:
            raise SerializationError()
        return {
            "coefficients": self.coefficients,
            "q": self.q,
            "n": self.n,
        }

    @staticmethod
    def deserialize(obj: dict[str, Any], **_kwargs: Any) -> Polynomial:
        r"""
        Deserialization function for Polynomial, which will be passed to the communication module.

        :param obj: serialized version of a Polynomial.
        :param \**_kwargs: Optional extra keyword arguments.
        :raise SerializationError: When communication library is not installed.
        :return: Deserialized Polynomial from the given dict.
        """
        if not COMMUNICATION_INSTALLED:
            raise SerializationError()
        return Polynomial(coefficients=obj["coefficients"], q=obj["q"], n=obj["n"])

    # endregion


def unif_rand_polynomial(q: int, n: int) -> Polynomial:
    r"""
    Returns uniformly random polynomial over $R_q = \mathbb{Z}_q[x]/(x^n + 1)$ by sampling
    coefficients uniformly randomly from $\mathbb{Z}_q$.

    :param q: Modulus of the coefficients.
    :param n: Degree of ideal for quotient ring of which the polynomial is an element.
    :return: Polynomial object.
    """
    coefficients = []
    for _ in range(n):
        coefficients.append(_sysrand.randrange(q))
    return Polynomial(coefficients, q, n)


def ternary_rand_polynomial(q: int, n: int) -> Polynomial:
    r"""
    Returns uniformly random polynomial over $R_q = \mathbb{Z}_q[x]/(x^n + 1)$ by sampling
    coefficients from the set ${-1,0,1}$.

    :param q: Modulus of the coefficients.
    :param n: Degree of ideal for quotient ring of which the polynomial is an element.
    :return: Polynomial object.
    """
    coefficients = []
    for _ in range(n):
        coefficients.append(_sysrand.randrange(3) - 1)
    return Polynomial(coefficients, q, n)


def gauss_rand_polynomial(
    q: int,
    n: int,
    standard_deviation: float,
    center: float = 0,
) -> Polynomial:
    r"""
    Returns random polynomial over $R_q = \mathbb{Z}_q[x]/(x^n + 1)$ by sampling
    coefficients from a discrete Gaussian distribution over $\mathbb{Z}_q$ with the given center
    and standard deviation.

    :param q: Modulus of the coefficients.
    :param n: Degree of ideal for quotient ring of which the polynomial is an element.
    :param standard_deviation: Standard deviation of the distribution.
    :param center: Center of distribution, default is 0.
    :return: Polynomial object.
    """
    coefficients = []
    for _ in range(n):
        coefficients.append(gauss_rand_int_rejection_karnay(standard_deviation, center))
    return Polynomial(coefficients, q, n)


def gauss_rand_int_rejection_karnay(
    standard_deviation: float, center: float = 0
) -> int:
    r"""
    Generate a random integer from a discrete Gaussian distribution centered at $c \in \mathbb{R}$
    with the given standard deviation $\sigma \in \mathbb{R}_+}$ by rejection sampling.
    The default center is at 0.

    Following Algorithm D in Karnay, J., GAUSSIAN SAMPLING IN LATTICE BASED CRYPTOGRAPHY
    https://www.sav.sk/journals/uploads/0212094402follat.pdf
    This algorithm was recommended in the Homomorphic Encryption Standard (2018) by Albrecht et al.
    https://homomorphicencryption.org/standard/

    :param standard_deviation: Standard deviation of the distribution.
    :param center: Center of distribution, default is 0.
    :raise ValueError: When given standard deviation is nonpositive.
    :return: Random integer from a discrete Gaussian distribution.
    """
    if standard_deviation <= 0:
        raise ValueError(
            f"Standard deviation should be positive, now it is {standard_deviation}."
        )

    while True:
        while True:
            # D1
            k = 0
            while True:
                if half_exponential_bernouilli_deviate():
                    break
                k += 1
            # D2
            r = _sysrand.random()
            p = exp(-0.5 * k * (k - 1))
            if r < p:
                break
        # D3
        s = _sysrand.choice([1, -1])
        # D4
        j = _sysrand.randint(0, floor(standard_deviation))
        i_zero = ceil(standard_deviation * k + s * center)
        x_zero = (i_zero - (standard_deviation * k + s * center)) / standard_deviation
        x = x_zero + j / standard_deviation
        # D5 - D7
        r = _sysrand.random()
        p = exp(-0.5 * x * (2 * k + x))
        if x < 1 and not (k == 0 and x == 0 and s < 0) and r < p:
            break
    # D8 - D9
    return s * (i_zero + j)


def half_exponential_bernouilli_deviate() -> int:
    r"""
    Generates a Bernouilli random value $H$ which is true with probability $1/\sqrt{e}$.

    Following Algorithm H in Karnay, J., GAUSSIAN SAMPLING IN LATTICE BASED CRYPTOGRAPHY
    https://www.sav.sk/journals/uploads/0212094402follat.pdf

    :return: Bernouilli random value $H$ which is true with probability $1/\sqrt{e}$.
    """
    # H1
    n = 0
    number = 0.5
    while True:
        next_number = uniform_deviate()
        if number <= next_number:
            # H2
            return n % 2 == 0
        n += 1
        number = next_number


def uniform_deviate() -> float:
    r"""
    Generates a uniform random value $U$ from the open interval (0,1).

    Following Karnay, J., GAUSSIAN SAMPLING IN LATTICE BASED CRYPTOGRAPHY
    https://www.sav.sk/journals/uploads/0212094402follat.pdf

    :return: Uniform random value $U$ from the open interval (0,1).
    """
    value = 0.0
    while value == 0.0:
        value = _sysrand.random()
    return value


# The following are alternative functions for sampling a discrete Gaussian distribution.
# These are described in literature, but not necessarily recommended for BGV.


def gauss_rand_int_rejection_follath(
    standard_deviation: float, tailcut: float, center: float = 0
) -> int:
    r"""
    Generate a random integer from a discrete Gaussian distribution centered at $c \in \mathbb{R}$
    with the given standard deviation $\sigma \in \mathbb{R}_+}$ by rejection sampling.
    Note that standard deviation = $s / \sqrt{2 \pi}$, where $s$ is the Gaussian parameter of the
    distribution.
    The default center is at 0.
    Instead of sampling over $\mathbb{Z}$, we sample over the range
    $[c - tailcut * s \rceil, \lfloor c + tailcut * s] \cap \mathbb{Z}$.

    Following Algorithm 1 in Follath, J., GAUSSIAN SAMPLING IN LATTICE BASED CRYPTOGRAPHY
    https://www.sav.sk/journals/uploads/0212094402follat.pdf

    :param standard_deviation: Standard deviation of the distribution.
    :param tailcut: Tailcut of distribution.
    :param center: Center of distribution, default is 0.
    :raise ValueError: When given standard deviation or tailcut is nonpositive.
    :return: Random integer from a discrete Gaussian distribution.
    """
    if standard_deviation <= 0:
        raise ValueError(
            f"Standard deviation should be positive, now it is {standard_deviation}."
        )
    if tailcut <= 0:
        raise ValueError(f"Tailcut t should be positive, now it is {tailcut}.")

    # In real-world crypto float is not precise enough for cryptographic operations, use other,
    # more precise floating point numbers. This also holds for exp function.
    s = sqrt(2 * pi) * standard_deviation
    h = -pi / s**2
    lower_bound = ceil(center - tailcut * s)
    upper_bound = floor(center + tailcut * s)
    while True:
        x = _sysrand.randrange(upper_bound - lower_bound + 1) + lower_bound
        r = _sysrand.random()
        p = exp(h * (x - center) ** 2)
        if r < p:
            return x


def gauss_rand_int_round(standard_deviation: float, center: float = 0) -> int:
    r"""
    Generate a random integer from a discrete Gaussian distribution centered at $c \in \mathbb{R}$
    with the given standard deviation $\sigma \in \mathbb{R}_+}$ by rounding a sample from a
    continuous Gaussian distribution with the same paramaters.
    The default center is at 0.

    Following the sampling steps in section 1.3 in Brakerski, Z. and Vaikuntanathan, V.,
    Fully Homomorphic Encryption from Ring-LWE and Security for Key Dependent Messages
    https://www.wisdom.weizmann.ac.il/~zvikab/localpapers/IdealHom.pdf

    :param standard_deviation: Standard deviation of the distribution.
    :param center: Center of distribution, default is 0.
    :return: Random integer from a discrete Gaussian distribution.
    """
    sample = _sysrand.normalvariate(center, standard_deviation)
    return int(round(sample))


if COMMUNICATION_INSTALLED:
    try:
        Serialization.register_class(Polynomial)
    except RepetitionError:
        pass
