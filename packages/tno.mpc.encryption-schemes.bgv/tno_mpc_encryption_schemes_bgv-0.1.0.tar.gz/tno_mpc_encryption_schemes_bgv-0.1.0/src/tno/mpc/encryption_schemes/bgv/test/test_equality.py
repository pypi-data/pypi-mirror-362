"""
This module tests the equality functions of BGV.
"""

from tno.mpc.encryption_schemes.bgv.bgv import BGV

key_pairs = [
    BGV.generate_key_material(
        q=5,
        n=8,
        t=4,
        secret_distribution=2.0,
        error_distribution=2.0,
    ),
    # Different key pair with the same parameters (key material contains randomness)
    BGV.generate_key_material(
        q=5,
        n=8,
        t=4,
        secret_distribution=2.0,
        error_distribution=2.0,
    ),
]

same_schemes = [BGV(*key_pairs[0]), BGV(*key_pairs[0])]

diff_scheme = BGV(*key_pairs[1])


def test_keys_equality() -> None:
    """
    Test whether comparing the same keys used in different BGV schemes works.
    """
    assert same_schemes[0].public_key == same_schemes[1].public_key
    assert same_schemes[0].secret_key == same_schemes[1].secret_key


def test_keys_inequality() -> None:
    """
    Test whether inequality of keys holds.
    """
    assert same_schemes[0].public_key != diff_scheme.public_key
    assert same_schemes[0].secret_key != diff_scheme.secret_key


def test_cipher_equality() -> None:
    """
    Test whether equality of two BGVCiphertexts was implemented properly.
    """
    ciphertext = diff_scheme.encrypt(5)
    ciphertext_copy = type(ciphertext)(
        raw_value=ciphertext.peek_value(), scheme=diff_scheme
    )
    assert ciphertext == ciphertext_copy


def test_cipher_inequality() -> None:
    """
    Test whether inequality of the same ciphertext encrypted with different keys holds.
    """
    ciphertext0 = same_schemes[0].encrypt(5)
    ciphertext1 = diff_scheme.encrypt(5)
    assert ciphertext0 != ciphertext1


def test_scheme_equality() -> None:
    """
    Test whether equality of BGV schemes was implemented properly.
    """
    assert same_schemes[0] == same_schemes[1]


def test_scheme_inequality() -> None:
    """
    Test whether inequality of schemes with different keys holds.
    """
    assert same_schemes[0] != diff_scheme
