"""
This module tests the encryption an decryption functionalities of BGV.
"""

import itertools
from math import ceil, floor

import pytest

from tno.mpc.encryption_schemes.bgv.bgv import (
    BGV,
    WARN_INEFFICIENT_HOM_OPERATION,
    BGVCiphertext,
    BGVPublicKey,
    BGVSecretKey,
    Plaintext,
)
from tno.mpc.encryption_schemes.bgv.test import conditional_pywarn
from tno.mpc.encryption_schemes.bgv.test.const import key_pairs

public_key, secret_key = BGV.generate_key_material(
    q=262139,
    n=16,
    t=32,
    error_distribution=3.19,
    secret_distribution=0.0,
)

PLAINTEXT_INPUTS = list(range(4)) + [12, 123, 1234, 12345, 123456]
PLAINTEXT_INPUTS = PLAINTEXT_INPUTS + [-x for x in PLAINTEXT_INPUTS]
SCALAR_INPUTS = list(range(4))
SCALAR_INPUTS = SCALAR_INPUTS + [-x for x in SCALAR_INPUTS]


def limit_to_message_space(value: int, scheme: BGV) -> int:
    """
    Limit a value in such a way that it fits in the message space.

    :param value: Value to be limited.
    :param scheme: BGV encryption scheme with which the value should be encrypted.
    :return: Limited value
    """
    if value < scheme.min_value or value > scheme.max_value:
        value = (value - scheme.min_value) % (
            scheme.max_value - scheme.min_value + 1
        ) + scheme.min_value
    return value


def encrypt_with_freshness(value: Plaintext, scheme: BGV, safe: bool) -> BGVCiphertext:
    """
    Encrypt a plaintext in safe or unsafe mode.

    Safe mode will yield a fresh ciphertext, unsafe mode will yield a non-fresh ciphertext.

    :param value: Plaintext message to be encrypted.
    :param scheme: Scheme to encrypt the message with.
    :param safe: Perform safe encrypt if true, unsafe encrypt otherwise.
    :return: BGVCiphertext object with requested freshness.
    """
    if safe:
        return scheme.encrypt(value)
    return scheme.unsafe_encrypt(value)


@pytest.fixture(name="encryption_scheme")
def fixture_scheme() -> BGV:
    """
    Get BGV encryption scheme.

    :return: Initialized BGV scheme.
    """
    return BGV(public_key, secret_key)


@pytest.fixture(name="public_encryption_scheme")
def fixture_public_scheme() -> BGV:
    """
    Get BGV encryption scheme without secret key.

    :return: Initialized BGV scheme without secret key.
    """
    return BGV(public_key, None)


@pytest.mark.parametrize("plaintext", PLAINTEXT_INPUTS)
@pytest.mark.parametrize("keypair", key_pairs)
def test_coding(plaintext: int, keypair: tuple[BGVPublicKey, BGVSecretKey]) -> None:
    """
    Test the encoding and decoding functionality of an BGV scheme.

    :param plaintext: Value to be encoded.
    :param keypair: Keypair for BGV scheme.
    """
    encryption_scheme = BGV(keypair[0], keypair[1])
    plaintext = limit_to_message_space(plaintext, encryption_scheme)
    encoding = encryption_scheme.encode(plaintext)
    decoding = encryption_scheme.decode(encoding)
    assert plaintext == decoding


@pytest.mark.parametrize("plaintext", PLAINTEXT_INPUTS)
def test_encryption(encryption_scheme: BGV, plaintext: int) -> None:
    """
    Test the encryption functionality of an BGV scheme.

    :param encryption_scheme: BGV encryption scheme.
    :param plaintext: Value to be encrypted.
    """
    plaintext = limit_to_message_space(plaintext, encryption_scheme)
    ciphertext = encryption_scheme.encrypt(plaintext)
    decrypted_ciphertext = encryption_scheme.decrypt(ciphertext)
    assert ciphertext.fresh
    assert plaintext == decrypted_ciphertext


@pytest.mark.parametrize("plaintext", PLAINTEXT_INPUTS)
def test_public_encryption(
    encryption_scheme: BGV, public_encryption_scheme: BGV, plaintext: int
) -> None:
    """
    Test the encryption functionality of a public BGV scheme.

    :param encryption_scheme: BGV encryption scheme.
    :param public_encryption_scheme: BGV encryption scheme with same public key and no secret
      key.
    :param plaintext: Value to be encrypted.
    """
    plaintext = limit_to_message_space(plaintext, public_encryption_scheme)
    ciphertext = public_encryption_scheme.encrypt(plaintext)
    decrypted_ciphertext = encryption_scheme.decrypt(ciphertext)

    assert ciphertext.fresh
    assert plaintext == decrypted_ciphertext


@pytest.mark.parametrize("plaintext", PLAINTEXT_INPUTS)
def test_ciphertext_randomization(encryption_scheme: BGV, plaintext: int) -> None:
    """
    Test the rerandomization functionality of BGV.

    :param encryption_scheme: BGV encryption scheme used for encrypting and generating
        randomness.
    :param plaintext: Value to be encrypted.
    """
    plaintext = limit_to_message_space(plaintext, encryption_scheme)
    ciphertext = encryption_scheme.encrypt(plaintext)
    raw_value = ciphertext.get_value()  # sets ciphertext.fresh to False
    ciphertext.randomize()
    randomized_raw_value = ciphertext.peek_value()  # does not alter freshness
    decrypted_value = encryption_scheme.decrypt(ciphertext)

    assert ciphertext.fresh
    assert randomized_raw_value != raw_value
    assert decrypted_value == plaintext


@pytest.mark.parametrize("plaintext", PLAINTEXT_INPUTS)
def test_unsafe_encryption(encryption_scheme: BGV, plaintext: int) -> None:
    """
    Test the unsafe encryption functionality of an BGV scheme with a secret key.

    :param encryption_scheme: BGV encryption scheme with secret key.
    :param plaintext: Value to be encrypted.
    """
    plaintext = limit_to_message_space(plaintext, encryption_scheme)
    ciphertext = encryption_scheme.unsafe_encrypt(plaintext)
    decrypted_ciphertext = encryption_scheme.decrypt(ciphertext)

    assert not ciphertext.fresh
    assert plaintext == decrypted_ciphertext


@pytest.mark.parametrize("plaintext", PLAINTEXT_INPUTS)
def test_encryption_with_randomization(encryption_scheme: BGV, plaintext: int) -> None:
    """
    Test the encryption functionality of an BGV scheme with a secret key while using
    rerandomization.

    :param encryption_scheme: BGV encryption scheme with secret key.
    :param plaintext: Value to be encrypted.
    """
    plaintext = limit_to_message_space(plaintext, encryption_scheme)
    ciphertext1 = encryption_scheme.unsafe_encrypt(plaintext)
    ciphertext2 = encryption_scheme.unsafe_encrypt(plaintext)

    assert not ciphertext1.fresh

    ciphertext1.randomize()

    assert ciphertext1.fresh
    assert ciphertext1 != ciphertext2

    decrypted_ciphertext = encryption_scheme.decrypt(ciphertext1)

    assert plaintext == decrypted_ciphertext


def test_bgv_encoding_exception(encryption_scheme: BGV) -> None:
    """
    Test whether trying to encrypt a message out of the message range of a BGV scheme
    raises an exception.

    :param encryption_scheme: BGV encryption scheme.
    """
    plaintext = encryption_scheme.max_value + 1
    with pytest.raises(ValueError) as error:
        encryption_scheme.encode(plaintext)
    assert (
        str(error.value)
        == f"This encoding scheme only supports values in the range [{encryption_scheme.min_value};"
        f"{encryption_scheme.max_value}], {plaintext} is outside that range."
    )


@pytest.mark.parametrize("is_fresh", (True, False))
@pytest.mark.parametrize("value", PLAINTEXT_INPUTS)
def test_bgv_neg(encryption_scheme: BGV, value: int, is_fresh: bool) -> None:
    """
    Test whether an encrypted nonzero plaintext can successfully be negated.

    :param encryption_scheme: BGV scheme with secret key.
    :param value: Plaintext to be encrypted and then negated.
    :param is_fresh: Freshness of ciphertext.
    """
    value = limit_to_message_space(value, encryption_scheme)

    encrypted_value = encrypt_with_freshness(value, encryption_scheme, is_fresh)

    with conditional_pywarn(is_fresh, WARN_INEFFICIENT_HOM_OPERATION):
        encrypted_neg = encryption_scheme.neg(encrypted_value)

    assert not encrypted_value.fresh
    assert encrypted_neg.fresh == is_fresh
    assert encryption_scheme.decrypt(encrypted_neg) == -value


@pytest.mark.parametrize("is_fresh", (True, False))
@pytest.mark.parametrize("value", PLAINTEXT_INPUTS)
@pytest.mark.parametrize("scalar", SCALAR_INPUTS)
def test_bgv_mul(
    encryption_scheme: BGV, value: int, scalar: int, is_fresh: bool
) -> None:
    """
    Test whether a ciphertext can be multiplied with a scalar.

    :param encryption_scheme: BGV scheme with secret key.
    :param value: Plaintext to be encrypted and then multiplied with the scalar.
    :param scalar: Scalar to multiply with the encrypted plaintext.
    :param is_fresh: Freshness of ciphertext.
    """
    value = limit_to_message_space(value, encryption_scheme)
    scalar = limit_to_message_space(scalar, encryption_scheme)
    scalar = int(round(scalar))

    # make sure outcome of multiplication fits in message space
    if value * scalar > encryption_scheme.max_value:
        limit_factor = ceil(value * scalar / encryption_scheme.max_value)
        value = floor(value / limit_factor)
    elif value * scalar < encryption_scheme.min_value:
        limit_factor = ceil(value * scalar / encryption_scheme.min_value)
        value = ceil(value / limit_factor)
    value = int(value)

    multiplication = value * scalar

    encrypted_value = encrypt_with_freshness(value, encryption_scheme, is_fresh)

    encryption_scheme.decrypt(encrypted_value)

    with conditional_pywarn(is_fresh, WARN_INEFFICIENT_HOM_OPERATION):
        encrypted_multiplication = encrypted_value * scalar

    assert not encrypted_value.fresh
    assert encrypted_multiplication.fresh == is_fresh

    assert encryption_scheme.decrypt(encrypted_multiplication) == multiplication


@pytest.mark.parametrize(
    "is_fresh, is_fresh_2",
    itertools.product((True, False), (True, False)),
)
@pytest.mark.parametrize("value", PLAINTEXT_INPUTS)
@pytest.mark.parametrize("value_2", PLAINTEXT_INPUTS)
def test_add(
    encryption_scheme: BGV,
    value: int,
    value_2: int,
    is_fresh: bool,
    is_fresh_2: bool,
) -> None:
    """
    Test whether two ciphertexts can be added (i.e. their underlying plaintexts are added.)

    :param encryption_scheme: BGV scheme with secret key.
    :param value: First plaintext message to be encrypted.
    :param value_2: Second plaintext message to be encrypted and added to the first.
    :param is_fresh: Freshness of first ciphertext.
    :param is_fresh_2: Freshness of second ciphertext.
    """
    value = limit_to_message_space(value, encryption_scheme)
    value_2 = limit_to_message_space(value_2, encryption_scheme)

    if value + value_2 >= encryption_scheme.max_value:
        value_2 = encryption_scheme.max_value - value
    elif value + value_2 <= encryption_scheme.min_value:
        value_2 = encryption_scheme.min_value - value
    sum_ = value + value_2

    encrypted_value = encrypt_with_freshness(value, encryption_scheme, is_fresh)
    encrypted_value_2 = encrypt_with_freshness(value_2, encryption_scheme, is_fresh_2)

    with conditional_pywarn(is_fresh or is_fresh_2, WARN_INEFFICIENT_HOM_OPERATION):
        encrypted_sum = encrypted_value + encrypted_value_2

    assert not encrypted_value.fresh
    assert not encrypted_value_2.fresh
    assert encrypted_sum.fresh == (is_fresh or is_fresh_2)

    assert encryption_scheme.decrypt(encrypted_sum) == sum_

    encrypted_value = encrypt_with_freshness(value, encryption_scheme, is_fresh)

    with conditional_pywarn(is_fresh, WARN_INEFFICIENT_HOM_OPERATION):
        encrypted_sum = encrypted_value + value_2

    assert not encrypted_value.fresh
    assert encrypted_sum.fresh == is_fresh
    assert encryption_scheme.decrypt(encrypted_sum) == sum_


@pytest.mark.parametrize(
    "is_fresh, is_fresh_2",
    itertools.product((True, False), (True, False)),
)
@pytest.mark.parametrize("value", PLAINTEXT_INPUTS)
@pytest.mark.parametrize("value_2", PLAINTEXT_INPUTS)
def test_sub(
    encryption_scheme: BGV,
    value: int,
    value_2: int,
    is_fresh: bool,
    is_fresh_2: bool,
) -> None:
    """
    Test whether two ciphertexts can be subtracted (i.e. their underlying plaintexts are
    subtracted.)

    :param encryption_scheme: BGV scheme with secret key.
    :param value: First plaintext message to be encrypted.
    :param value_2: Second plaintext message to be encrypted and subtracted from the first.
    :param is_fresh: Freshness of first ciphertext.
    :param is_fresh_2: Freshness of second ciphertext.
    """
    value = limit_to_message_space(value, encryption_scheme)
    value_2 = limit_to_message_space(value_2, encryption_scheme)

    if value - value_2 >= encryption_scheme.max_value:
        value = encryption_scheme.max_value + value_2
    elif value - value_2 <= encryption_scheme.min_value:
        value = encryption_scheme.min_value + value_2

    subtraction = value - value_2

    encrypted_value = encrypt_with_freshness(value, encryption_scheme, is_fresh)
    encrypted_value_2 = encrypt_with_freshness(value_2, encryption_scheme, is_fresh_2)

    with conditional_pywarn(is_fresh or is_fresh_2, WARN_INEFFICIENT_HOM_OPERATION):
        encrypted_subtraction = encrypted_value - encrypted_value_2

    assert not encrypted_value.fresh
    assert not encrypted_value_2.fresh
    assert encrypted_subtraction.fresh == (is_fresh or is_fresh_2)

    assert encryption_scheme.decrypt(encrypted_subtraction) == subtraction

    encrypted_value = encrypt_with_freshness(value, encryption_scheme, is_fresh)

    with conditional_pywarn(is_fresh, WARN_INEFFICIENT_HOM_OPERATION):
        encrypted_subtraction = encrypted_value - value_2

    assert not encrypted_value.fresh
    assert encrypted_subtraction.fresh == is_fresh
    assert encryption_scheme.decrypt(encrypted_subtraction) == subtraction
