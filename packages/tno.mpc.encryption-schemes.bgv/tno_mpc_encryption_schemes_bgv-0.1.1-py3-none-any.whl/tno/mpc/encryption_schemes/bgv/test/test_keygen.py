"""
This module tests the key generation of BGV.
"""

import pytest

from tno.mpc.encryption_schemes.bgv.bgv import BGV, BGVPublicKey, BGVSecretKey
from tno.mpc.encryption_schemes.bgv.test.const import key_pairs


@pytest.mark.parametrize("public_key, secret_key", key_pairs)
def test_encryption_creation(
    public_key: BGVPublicKey, secret_key: BGVSecretKey
) -> None:
    """
    Test whether the creation of BGV schemes work with the keys.

    :param public_key: BGVPublicKey for BGV scheme.
    :param secret_key: BGVSecretKey for BGV scheme.
    """
    BGV(public_key, secret_key)
    BGV(public_key, None)

    # Check for no exceptions
    assert 1


@pytest.mark.parametrize("public_key, secret_key", key_pairs)
def test_key_value_equality(public_key: BGVPublicKey, secret_key: BGVSecretKey) -> None:
    r"""
    Test whether the polynomials $a,b$ and $s$ in an BGV keypair are defined over the same $R_q$.

    :param public_key: Public key for BGV scheme.
    :param secret_key: Secret key for BGV scheme.
    """
    assert public_key.a.q == public_key.b.q
    assert public_key.a.q == secret_key.s.q
    assert public_key.a.n == public_key.b.n
    assert public_key.a.n == secret_key.s.n


@pytest.mark.parametrize("q", [0, -1, 1])
def test_key_value_q(q: int) -> None:
    r"""
    Test whether trying to generate keys with $q < 2$ raises an error.

    :param q: Integer modulus of the coefficients smaller than 2.
    """
    with pytest.raises(ValueError) as error:
        BGV.generate_key_material(
            q=q,
            n=8,
            t=4,
            secret_distribution=2.0,
            error_distribution=2.0,
        )
    assert (
        str(error.value)
        == f"For generating keys we need a positive integer modulus q larger than 1, {q} is no"
        f" such integer."
    )


@pytest.mark.parametrize("t", [0, -1, 1, 5, 8])
def test_key_value_t(t: int) -> None:
    r"""
    Test whether trying to generate keys with $t < 2$ raises an error.

    :param t: Integer modulus of the coefficients of the message space smaller than 2.
    """
    with pytest.raises(ValueError) as error:
        BGV.generate_key_material(
            q=5,
            n=8,
            t=t,
            secret_distribution=2.0,
            error_distribution=2.0,
        )
    assert (
        str(error.value)
        == f"For generating keys we need t to be in the range [2, 5), {t} is no such "
        f"integer."
    )


@pytest.mark.parametrize("n", [0, 6, -8])
def test_key_value_n(n: int) -> None:
    """
    Test whether keys trying to generate keys with n not a power of 2 raises an error.

    :param n: Not a power of 2.
    """
    with pytest.raises(ValueError) as error:
        BGV.generate_key_material(
            q=5,
            n=n,
            t=4,
            secret_distribution=2.0,
            error_distribution=2.0,
        )
    assert (
        str(error.value)
        == f"The degree of the ideal of the quotient ring should be a power of 2, {n} is not."
    )


@pytest.mark.parametrize("q,t", [(25, 5), (14, 7)])
def test_key_value_qt(q: int, t: int) -> None:
    r"""
    Test whether keys trying to generate keys with $q$ and $t$ not coprime raises an error.

    :param q: Integer modulus of the coefficients not coprime to t.
    :param t: Integer modulus of the coefficients of the message space not coprime to q.
    """
    with pytest.raises(ValueError) as error:
        BGV.generate_key_material(
            q=q,
            n=4,
            t=t,
            secret_distribution=2.0,
            error_distribution=2.0,
        )
    assert (
        str(error.value)
        == f"The coefficient modulus q of the ciphertext space and the coefficient modulus t"
        f" of the message space should be coprime, {q} and {t} are not."
    )
