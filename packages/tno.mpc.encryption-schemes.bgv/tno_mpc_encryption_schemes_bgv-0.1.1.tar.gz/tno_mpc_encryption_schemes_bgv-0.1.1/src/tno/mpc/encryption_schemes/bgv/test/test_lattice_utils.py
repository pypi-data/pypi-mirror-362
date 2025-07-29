"""
This file contains tests that determine whether the code for lattice utility functions works as
expected.
"""

import pytest

from tno.mpc.encryption_schemes.bgv.lattice_utils import (
    Polynomial,
    gauss_rand_int_rejection_follath,
    gauss_rand_int_rejection_karnay,
    gauss_rand_int_round,
    gauss_rand_polynomial,
    ternary_rand_polynomial,
    unif_rand_polynomial,
)

test_coefficients = [
    [0],
    [0, 0],
    [1, 1, 1],
    [0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1],
    [0, 0, 0, 0, 1],
]

reduced_test_coefficients = [[0], [0], [1, 1, 1], [0], [0, 1, 1, 1], [-1]]

added_test_coefficients = [[1, 1], [1, 1], [-1, -1, 1], [1, 1], [1, -1, 1, 1], [0, 1]]

doubled_test_coefficients = [[0], [0], [-1, -1, -1], [0], [0, -1, -1, -1], [1]]

multiplied_test_coefficients = [[0], [0], [0, -1, 0, -1], [0], [0, 1, 0, -1], [1]]

multiplied_test_coefficients_len = [
    [0],
    [0],
    [1, -1, -1, 1],
    [0],
    [-1, 1, -1, -1],
    [-1, -1],
]

test_degrees = [-1, -1, 2, -1, 3, 0]


def test_poly_init_empty() -> None:
    """
    Test whether trying to create a Polynomial with an empty set of coefficients leads to an
    error.
    """
    with pytest.raises(ValueError) as error:
        Polynomial([], 3, 4)
    assert (
        str(error.value)
        == "List of coefficients is empty, expected at least one coefficient."
    )


@pytest.mark.parametrize("q", [0, -3])
def test_poly_init_small_q(q: int) -> None:
    """
    Test whether trying to create a Polynomial where q is smaller than 1 raises an error.

    :param q: Nonpositive integer modulus of the coefficients.
    """
    with pytest.raises(ValueError) as error:
        Polynomial([0, 1, 2], q, 4)
    assert str(error.value) == "Value of q should be larger than 0."


@pytest.mark.parametrize("n", [0, 3, 6])
def test_poly_init_no_power(n: int) -> None:
    """
    Test whether trying to create a Polynomial where n is not a power of 2 raises an error.

    :param n: Not a power of 2.
    """
    with pytest.raises(ValueError) as error:
        Polynomial([0, 1, 2], 3, n)
    assert str(error.value) == "Value of n is not a power of 2."


@pytest.mark.parametrize(
    "coefficients, reduced_coefficients",
    zip(test_coefficients, reduced_test_coefficients),
)
def test_poly_init(coefficients: list[int], reduced_coefficients: list[int]) -> None:
    """
    Test whether initializing a Polynomial leads to the expected values.

    :param coefficients: Coefficients of the polynomial in order of increasing degree.
    :param reduced_coefficients: Corresponding reduced coefficients of the polynomial.
    """
    polynomial = Polynomial(coefficients, 3, 4)
    assert polynomial.coefficients == reduced_coefficients


def test_poly_eq() -> None:
    """
    Test whether determining equality of two equal polynomials was implemented correctly.
    """
    polynomial1 = Polynomial([1, 1, 1], 5, 4)
    polynomial2 = Polynomial([1, 1, 1], 5, 4)
    assert polynomial1 == polynomial2


@pytest.mark.parametrize("coefficients", test_coefficients)
@pytest.mark.parametrize("q", [3, 5, 6])
@pytest.mark.parametrize("n", [4, 8])
def test_poly_neq(coefficients: list[int], q: int, n: int) -> None:
    """
    Test whether determining inequality of two inequal polynomials was implemented correctly.

    :param coefficients: Coefficients of the polynomial in order of increasing degree.
    :param q: Positive integer modulus of the coefficients.
    :param n: Power of 2, degree of ideal for quotient ring of which the polynomial is an
        element.
    """
    polynomial1 = Polynomial(coefficients, q, n)
    polynomial2 = Polynomial([1], q, n)
    assert polynomial1 != polynomial2


@pytest.mark.parametrize("coefficients", test_coefficients)
@pytest.mark.parametrize("q", [3, 5, 6])
@pytest.mark.parametrize("n", [4, 8])
def test_poly_neg(coefficients: list[int], q: int, n: int) -> None:
    """
    Test whether negation of polynomials was implemented correctly.

    :param coefficients: Coefficients of the polynomial in order of increasing degree.
    :param q: Odd prime modulus of the coefficients.
    :param n: Power of 2, degree of ideal for quotient ring of which the polynomial is an
        element.
    """
    polynomial1 = Polynomial(coefficients, q, n)
    polynomial2 = -polynomial1
    for i, polynomial1coefficient in enumerate(polynomial1.coefficients):
        assert (polynomial1coefficient + polynomial2.coefficients[i]) % q == 0
    assert polynomial1.q == polynomial2.q
    assert polynomial1.n == polynomial2.n


@pytest.mark.parametrize("coefficients", test_coefficients)
@pytest.mark.parametrize(
    "q1,n1,q2,n2", [(3, 4, 3, 8), (3, 4, 5, 4), (3, 4, 5, 8), (6, 4, 5, 4)]
)
def test_poly_add_exception(
    coefficients: list[int], q1: int, n1: int, q2: int, n2: int
) -> None:
    """
    Test whether addition of Polynomials raises an exception when trying to add Polynomials that are
    defined over different rings.

    :param coefficients: Coefficients of the polynomial in order of increasing degree.
    :param q1: Odd prime modulus of the coefficients for first polynomial in addition.
    :param n1: Power of 2, degree of ideal for quotient ring of which the polynomial is an
        element for first polynomial in addition.
    :param q2: Odd prime modulus of the coefficients for second polynomial in addition.
    :param n2: Power of 2, degree of ideal for quotient ring of which the polynomial is an
        element for second polynomial in addition.
    """
    polynomial1 = Polynomial(coefficients, q1, n1)
    polynomial2 = Polynomial(coefficients, q2, n2)
    with pytest.raises(ValueError) as error:
        resulting_polynomial = polynomial1 + polynomial2
        resulting_polynomial += polynomial1
    assert (
        str(error.value) == f"Adding a polynomial over Z_{q1}[x]/(x^{n1} + 1)"
        f"to a polynomial over Z_{q2}[x]/(x^{n2} + 1) is not possible."
    )


@pytest.mark.parametrize(
    "coefficients, doubled_coefficients",
    zip(test_coefficients, doubled_test_coefficients),
)
def test_poly_add(coefficients: list[int], doubled_coefficients: list[int]) -> None:
    """
    Test whether addition of two Polynomials works correctly.

    :param coefficients: Coefficients of the polynomial in order of increasing degree.
    :param doubled_coefficients: Corresponding doubled coefficients.
    """
    polynomial1 = Polynomial(coefficients, 3, 4)
    polynomial2 = Polynomial(coefficients, 3, 4)
    polynomialadd = polynomial1 + polynomial2
    assert polynomialadd.coefficients == doubled_coefficients


@pytest.mark.parametrize(
    "coefficients, added_coefficients",
    zip(test_coefficients, added_test_coefficients),
)
def test_poly_add_len(coefficients: list[int], added_coefficients: list[int]) -> None:
    """
    Test whether addition of two Polynomials with different lengths works correctly.

    :param coefficients: Coefficients of the polynomial in order of increasing degree.
    :param added_coefficients: Corresponding coefficients with [1,1] added.
    """
    polynomial1 = Polynomial(coefficients, 3, 4)
    polynomial2 = Polynomial([1, 1], 3, 4)
    polynomialadd = polynomial1 + polynomial2
    assert polynomialadd.coefficients == added_coefficients


@pytest.mark.parametrize(
    "coefficients, added_coefficients",
    zip(test_coefficients, added_test_coefficients),
)
def test_poly_add_int(coefficients: list[int], added_coefficients: list[int]) -> None:
    """
    Test whether left adding polynomial and integer works correctly.

    :param coefficients: Coefficients of the polynomial in order of increasing degree.
    :param added_coefficients: Corresponding coefficients with [1,1] added.
    """
    polynomial = Polynomial(coefficients, 3, 4)
    polynomialadd = polynomial + 1
    assert polynomialadd.coefficients[0] == added_coefficients[0]
    assert polynomialadd.coefficients[1:] == polynomial.coefficients[1:]


@pytest.mark.parametrize(
    "coefficients, added_coefficients",
    zip(test_coefficients, added_test_coefficients),
)
def test_poly_add_int_right(
    coefficients: list[int], added_coefficients: list[int]
) -> None:
    """
    Test whether right adding polynomial and integer works correctly.

    :param coefficients: Coefficients of the polynomial in order of increasing degree.
    :param coefficients: Corresponding coefficients with [1,1] added.
    """
    polynomial = Polynomial(coefficients, 3, 4)
    polynomialadd = 1 + polynomial
    assert polynomialadd.coefficients[0] == added_coefficients[0]
    assert polynomialadd.coefficients[1:] == polynomial.coefficients[1:]


@pytest.mark.parametrize("coefficients", test_coefficients)
@pytest.mark.parametrize(
    "q1,n1,q2,n2", [(3, 4, 3, 8), (3, 4, 5, 4), (3, 4, 5, 8), (6, 4, 5, 4)]
)
def test_poly_mul_exception(
    coefficients: list[int], q1: int, n1: int, q2: int, n2: int
) -> None:
    """
    Test whether multiplication of Polynomials raises an exception when trying to add Polynomials
    that are defined over different rings.

    :param coefficients: Coefficients of the polynomial in order of increasing degree.
    :param q1: Odd prime modulus of the coefficients for first polynomial in multiplication.
    :param n1: Power of 2, degree of ideal for quotient ring of which the polynomial is an
        element for first polynomial in multiplication.
    :param q2: Odd prime modulus of the coefficients for second polynomial in multiplication.
    :param n2: Power of 2, degree of ideal for quotient ring of which the polynomial is an
        element for second polynomial in multiplication.
    """
    polynomial1 = Polynomial(coefficients, q1, n1)
    polynomial2 = Polynomial(coefficients, q2, n2)
    with pytest.raises(ValueError) as error:
        resulting_polynomial = polynomial1 * polynomial2
        resulting_polynomial *= polynomial1
    assert (
        str(error.value) == f"Multiplying a polynomial over Z_{q1}[x]/(x^{n1} + 1)"
        f"with a polynomial over Z_{q2}[x]/(x^{n2} + 1) is not possible."
    )


@pytest.mark.parametrize(
    "coefficients, multiplied_coefficients",
    zip(test_coefficients, multiplied_test_coefficients),
)
def test_poly_mul(coefficients: list[int], multiplied_coefficients: list[int]) -> None:
    """
    Test whether multiplication of two Polynomials works correctly.

    :param coefficients: Coefficients of the polynomial in order of increasing degree.
    :param multiplied_coefficients: Corresponding coefficients of multiplication of the polynomial
        by itself.
    """
    polynomial1 = Polynomial(coefficients, 3, 4)
    polynomial2 = Polynomial(coefficients, 3, 4)
    polynomialmul = polynomial1 * polynomial2
    assert polynomialmul.coefficients == multiplied_coefficients


@pytest.mark.parametrize(
    "coefficients, multiplied_coefficients",
    zip(test_coefficients, multiplied_test_coefficients_len),
)
def test_poly_mul_len(
    coefficients: list[int], multiplied_coefficients: list[int]
) -> None:
    """
    Test whether addition of two Polynomials with different lengths works correctly.

    :param coefficients: Coefficients of the polynomial in order of increasing degree.
    :param multiplied_coefficients: Corresponding coefficients of multiplication of the polynomial
        by the polynomial with coefficients [1, 1].
    """
    polynomial1 = Polynomial(coefficients, 3, 4)
    polynomial2 = Polynomial([1, 1], 3, 4)
    polynomialmul = polynomial1 * polynomial2
    assert polynomialmul.coefficients == multiplied_coefficients


@pytest.mark.parametrize(
    "coefficients, doubled_coefficients",
    zip(test_coefficients, doubled_test_coefficients),
)
def test_poly_mul_int(coefficients: list[int], doubled_coefficients: list[int]) -> None:
    """
    Test whether left multiplication of a Polynomial and integer works correctly.

    :param coefficients: Coefficients of the polynomial in order of increasing degree.
    :param doubled_coefficients: Corresponding doubled coefficients.
    """
    polynomial = Polynomial(coefficients, 3, 4)
    polynomialmul = polynomial * 2
    assert polynomialmul.coefficients == doubled_coefficients


@pytest.mark.parametrize(
    "coefficients, doubled_coefficients",
    zip(test_coefficients, doubled_test_coefficients),
)
def test_poly_mul_int_right(
    coefficients: list[int], doubled_coefficients: list[int]
) -> None:
    """
    Test whether right multiplication of a Polynomial and integer works correctly.

    :param coefficients: Coefficients of the polynomial in order of increasing degree.
    :param doubled_coefficients: Corresponding doubled coefficients.
    """
    polynomial = Polynomial(coefficients, 3, 4)
    polynomialmul = 2 * polynomial
    assert polynomialmul.coefficients == doubled_coefficients


@pytest.mark.parametrize(
    "coefficients, degree",
    zip(test_coefficients, test_degrees),
)
def test_poly_deg(coefficients: list[int], degree: int) -> None:
    """
    Test whether the degree of a Polynomial is returned correctly.

    :param coefficients: Coefficients of the polynomial in order of increasing degree.
    :param degree: Corresponding degree of the polynomial.
    """
    polynomial = Polynomial(coefficients, 3, 4)
    assert polynomial.deg() == degree


@pytest.mark.parametrize("q", [3, 5, 6])
@pytest.mark.parametrize("n", [4, 8])
def test_unif_rand_polynomial(q: int, n: int) -> None:
    r"""
    Test whether unif_rand_polynomial(q,n) generates a polynomial within
    $R_q = \mathbb{Z}_q[x]/(x^n + 1)$

    :param q: Odd prime modulus of the coefficients.
    :param n: Degree of ideal for quotient ring of which the polynomial is an element.
    """
    polynomial = unif_rand_polynomial(q, n)
    assert polynomial.deg() < n
    for coefficient in polynomial.coefficients:
        if coefficient < 0:
            coefficient += q
        assert 0 <= coefficient < q


@pytest.mark.parametrize("q", [3, 5, 6])
@pytest.mark.parametrize("n", [4, 8])
def test_ternary_rand_polynomial(q: int, n: int) -> None:
    r"""
    Test whether ternary_rand_polynomial(q,n) generates a polynomial with coefficients in
    $\{-1, 0 , 1\}$.

    :param q: Odd prime modulus of the coefficients.
    :param n: Degree of ideal for quotient ring of which the polynomial is an element.
    """
    polynomial = ternary_rand_polynomial(q, n)
    assert polynomial.deg() < n
    for coefficient in polynomial.coefficients:
        assert coefficient in (-1, 0, 1)


@pytest.mark.parametrize("standard_deviation", [-5, 5, 10])
@pytest.mark.parametrize("center", [-5, 0, 5])
def test_gauss_rand_int_rejection_karnay(
    standard_deviation: float, center: float
) -> None:
    r"""
    Test whether gauss_rand_int_rejection raises exceptions when required.

    :param standard_deviation: Standard deviation of the distribution that is sampled.
    :param center: Center of distribution.
    """
    if standard_deviation <= 0:
        with pytest.raises(ValueError) as error:
            gauss_rand_int_rejection_karnay(standard_deviation, center)
            assert (
                str(error.value)
                == f"Standard deviation should be positive, now it is {standard_deviation}."
            )
    else:
        gauss_rand_int_rejection_karnay(standard_deviation, center)
        assert 1


@pytest.mark.parametrize("standard_deviation", [-5, 5, 10])
@pytest.mark.parametrize("tailcut", [-5, 5, 10])
@pytest.mark.parametrize("center", [-5, 0, 5])
def test_gauss_rand_int_rejection_follath(
    standard_deviation: float, tailcut: float, center: float
) -> None:
    r"""
    Test whether gauss_rand_int_rejection raises exceptions when required.

    :param standard_deviation: Standard deviation of the distribution that is sampled.
    :param tailcut: Tailcut of distribution.
    :param center: Center of distribution.
    """
    if standard_deviation <= 0:
        with pytest.raises(ValueError) as error:
            gauss_rand_int_rejection_follath(standard_deviation, tailcut, center)
            assert (
                str(error.value)
                == f"Standard deviation should be positive, now it is {standard_deviation}."
            )
    elif tailcut <= 0:
        with pytest.raises(ValueError) as error:
            gauss_rand_int_rejection_follath(standard_deviation, tailcut, center)
            assert (
                str(error.value)
                == f"Tailcut t should be positive, now it is {tailcut}."
            )
    else:
        gauss_rand_int_rejection_follath(standard_deviation, tailcut, center)
        assert 1


@pytest.mark.parametrize("standard_deviation", [-5, 5, 10])
@pytest.mark.parametrize("center", [-5, 0, 5])
def test_gauss_rand_int_round(standard_deviation: float, center: float) -> None:
    r"""
    Test whether gauss_rand_int_round does not raise exceptions.

    :param standard_deviation: Standard deviation of the distribution that is sampled.
    :param center: Center of distribution.
    """
    gauss_rand_int_round(standard_deviation, center)

    assert 1


@pytest.mark.parametrize("q", [3, 5, 6])
@pytest.mark.parametrize("n", [4, 8])
@pytest.mark.parametrize("standard_deviation", [3.19, 5, 10])
@pytest.mark.parametrize("center", [0, 5])
def test_gauss_rand_polynomial(
    q: int, n: int, standard_deviation: float, center: float
) -> None:
    r"""
    Test whether unif_gauss_rand_polynomial generates a polynomial within
    $R_q = \mathbb{Z}_q[x]/(x^n + 1)$

    :param q: Odd prime modulus of the coefficients.
    :param n: Degree of ideal for quotient ring of which the polynomial is an element.
    :param standard_deviation: Standard deviation of the distribution that is sampled.
    :param center: Center of distribution.
    """
    polynomial = gauss_rand_polynomial(q, n, standard_deviation, center)
    assert polynomial.deg() < n
    for coefficient in polynomial.coefficients:
        if coefficient < 0:
            coefficient += q
        assert 0 <= coefficient < q
