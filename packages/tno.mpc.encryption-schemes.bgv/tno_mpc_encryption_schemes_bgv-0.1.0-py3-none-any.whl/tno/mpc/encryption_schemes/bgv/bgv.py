"""
Implementation of an asymmetric encryption scheme based on ring learning with errors (RLWE).
This scheme is partially homomorphic, by implementing part of a fully homomorphic scheme.
Following the scheme as presented by Brakerski, Gentry and Vaikuntanathan, also known as BGV.
This scheme has been described in (Leveled) Fully Homomorphic Encryption without Bootstrapping,
as published in ACM Transactions on Computation Theory (TOCT), Volume 6, Issue 3, pages 1-36,
https://doi.org/10.1145/2090236.2090262.
"""

from __future__ import annotations

import warnings
from dataclasses import asdict, dataclass
from functools import partial
from typing import Any, TypedDict

from tno.mpc.encryption_schemes.templates.asymmetric_encryption_scheme import (
    AsymmetricEncryptionScheme,
    PublicKey,
    SecretKey,
)
from tno.mpc.encryption_schemes.templates.encryption_scheme import (
    EncodedPlaintext,
    EncryptionSchemeWarning,
)
from tno.mpc.encryption_schemes.templates.exceptions import SerializationError
from tno.mpc.encryption_schemes.templates.randomized_encryption_scheme import (
    RandomizableCiphertext,
    RandomizedEncryptionScheme,
)
from tno.mpc.encryption_schemes.utils.utils import extended_euclidean

from tno.mpc.encryption_schemes.bgv.lattice_utils import (
    Polynomial,
    gauss_rand_polynomial,
    ternary_rand_polynomial,
    unif_rand_polynomial,
)

# Check to see if the communication module is available
try:
    from tno.mpc.communication import RepetitionError, Serialization
    from tno.mpc.communication.httphandlers import HTTPClient

    COMMUNICATION_INSTALLED = True
except ModuleNotFoundError:
    COMMUNICATION_INSTALLED = False

WARN_INEFFICIENT_HOM_OPERATION = (
    "Identified a fresh ciphertext as input to a homomorphic operation, which is no longer fresh "
    "after the operation. This indicates a potential inefficiency if the non-fresh input may also "
    "be used in other operations (unused randomness). Solution: randomize ciphertexts as late as "
    "possible, e.g. by encrypting them with scheme.unsafe_encrypt and randomizing them just "
    "before sending. Note that the serializer randomizes non-fresh ciphertexts by default."
)

WARN_UNFRESH_SERIALIZATION = (
    "Serializer identified and rerandomized a non-fresh ciphertext."
)


@dataclass(frozen=True)
class BGVPublicKey(PublicKey):
    r"""
    Public key $(a,b)$ for the BGV encryption scheme, which is a polynomial
    $a \in R_q = \mathbb{Z}_q[x]/(x^n + 1)$ along with polynomial
    $b \in R_q = \mathbb{Z}_q[x]/(x^n + 1)$ for which
    it holds that $b = as + te$, where $s$ is the secret key, $t \in \mathbb{Z}_q^*$ larger than 2
    and coprime with $q$, $e$ a noise polynomial from a Gaussian distribution with a given standard
    deviation, $q$ a positive integer and $n$ a power of 2.

    :param a: Polynomial in $R_q = \mathbb{Z}_q[x]/(x^n + 1)$.
    :param b: Polynomial in $R_q = \mathbb{Z}_q[x]/(x^n + 1)$ such that $b = as + te$.
    :param t: Value in $\mathbb{Z}_q^*$ larger than 2 such that the message space is
        $R_t = \mathbb{Z}_t[x]/(x^n + 1)$.
    :param error_distribution: Standard deviation used for Gaussian sampling in rerandomization.
    :param secret_distribution: 0.0 for ternary distribution, otherwise standard deviation of the
        used Gaussian distribution, default is 0.0.
    """

    a: Polynomial
    b: Polynomial
    t: int
    error_distibution: float
    secret_distribution: float = 0.0

    def __str__(self) -> str:
        """
        Give string representation of this BGVPublicKey.

        :return: String representation of public key prepended by $(a, b = as + te) = $.
        """
        return f"(a, b = as + te) = ({self.a}, {self.b})"

    # region Serialization logic

    def serialize(self, **_kwargs: Any) -> dict[str, Any]:
        r"""
        Serialization function for public keys, which will be passed to the communication module.

        :param \**_kwargs: Optional extra keyword arguments.
        :raise SerializationError: When communication library is not installed.
        :return: Serialized version of this BGVPublicKey.
        """
        if not COMMUNICATION_INSTALLED:
            raise SerializationError()
        return asdict(self)

    @staticmethod
    def deserialize(obj: dict[str, Any], **_kwargs: Any) -> BGVPublicKey:
        r"""
        Deserialization function for public keys, which will be passed to the communication module

        :param obj: serialized version of a BGVPublicKey.
        :param \**_kwargs: Optional extra keyword arguments.
        :raise SerializationError: When communication library is not installed.
        :return: Deserialized BGVPublicKey from the given dict.
        """
        if not COMMUNICATION_INSTALLED:
            raise SerializationError()
        return BGVPublicKey(**obj)

    # endregion


@dataclass(frozen=True)
class BGVSecretKey(SecretKey):
    r"""
    Secret key $s$ for the BGV encryption scheme, which is a polynomial in
    $R_q = \mathbb{Z}_q[x]/(x^n + 1)$, where $q$ is a positive integer and $n$ a power of 2.
    """

    s: Polynomial

    def __str__(self) -> str:
        """
        Give string representation of this BGVSecretKey.

        :return: String representation of secret key prepended by $s = $.
        """
        return f"s = {self.s}"

    # region Serialization logic

    def serialize(self, **_kwargs: Any) -> dict[str, Any]:
        r"""
        Serialization function for secret keys, which will be passed to the communication module.

        :param \**_kwargs: Optional extra keyword arguments.
        :raise SerializationError: When communication library is not installed.
        :return: Serialized version of this BGVSecretKey.
        """
        if not COMMUNICATION_INSTALLED:
            raise SerializationError()
        return asdict(self)

    @staticmethod
    def deserialize(obj: dict[str, Any], **_kwargs: Any) -> BGVSecretKey:
        r"""
        Deserialization function for secret keys, which will be passed to the communication module.

        :param obj: Serialized version of a BGVSecretKey.
        :param \**_kwargs: Optional extra keyword arguments.
        :raise SerializationError: When communication library is not installed.
        :return: Deserialized BGVSecretKey from the given dict.
        """
        if not COMMUNICATION_INSTALLED:
            raise SerializationError()
        return BGVSecretKey(**obj)

    # endregion


KeyMaterial = tuple[BGVPublicKey, BGVSecretKey]
Plaintext = int
RawPlaintext = Polynomial
RawCiphertext = tuple[Polynomial, Polynomial]
RawRandomness = tuple[Polynomial, Polynomial, Polynomial]


class BGVCiphertext(
    RandomizableCiphertext[
        KeyMaterial, Plaintext, RawPlaintext, RawCiphertext, RawRandomness
    ]
):
    """
    Ciphertext for the BGV encryption scheme. This ciphertext is rerandomizable and supports
    additive homomorphic operations.
    """

    scheme: BGV

    def __init__(
        self, raw_value: RawCiphertext, scheme: BGV, *, fresh: bool = False
    ) -> None:
        r"""
        Construct a BGVCiphertext.

        :param raw_value: Ciphertext pair $(c_0, c_1) \in R_q^2$.
        :param scheme: BGV scheme that is used to encrypt this ciphertext.
        :param fresh: Indicate whether fresh randomness is already applied to the raw_value.
        :raise TypeError: When the given scheme is not a BGV scheme.
        """
        if not isinstance(scheme, BGV):
            raise TypeError(f"Expected scheme of type BGV, got {type(scheme)} instead.")
        super().__init__(raw_value, scheme, fresh=fresh)

    def apply_randomness(
        self, randomization_value: tuple[Polynomial, Polynomial, Polynomial]
    ) -> None:
        r"""
        Rerandomize this ciphertext $(c_0, c_1) \in R_q^2$ using the given random value
        triple $(v, e', e'') \in R_q^3$
        by taking $(c_0 + bv + te', c_1 - av + te'').

        :param randomization_value: Random value used for rerandomization.
        """
        # Note that t should be significantly smaller than q in order to not have overflows with
        # the operation below
        self._raw_value = (
            self._raw_value[0]
            + self.scheme.public_key.b * randomization_value[0]
            + self.scheme.public_key.t * randomization_value[1],
            self._raw_value[1]
            - self.scheme.public_key.a * randomization_value[0]
            + self.scheme.public_key.t * randomization_value[2],
        )

    def __eq__(self, other: object) -> bool:
        """
        Compare this BGVCiphertext with another to determine (in)equality.

        :param other: Object to compare this BGVCiphertext with.
        :raise TypeError: When other object is not an BGVCiphertext.
        :return: Boolean value representing (in)equality of both objects.
        """
        if not isinstance(other, BGVCiphertext):
            raise TypeError(
                f"Expected comparison with another BGVCiphertext, got {type(other)} instead."
            )
        return self._raw_value == other._raw_value and self.scheme == other.scheme

    def __str__(self) -> str:
        """
        Give string representation of this BGVCiphertext.

        :return: String representation of ciphertext prepended by (c0, c1) =
        """
        return f"(c0, c1) = ({self._raw_value[0]}, {self._raw_value[1]})"

    # region Serialization logic

    class SerializedBGVCiphertext(TypedDict):
        """Serialized BGV Ciphertext."""

        value: tuple[Polynomial, Polynomial]
        scheme: BGV

    def serialize(self, **_kwargs: Any) -> BGVCiphertext.SerializedBGVCiphertext:
        r"""
        Serialization function for BGV ciphertexts, which will be passed to the communication
        module.

        If the ciphertext is not fresh, it is randomized before serialization. After serialization,
        it is always marked as not fresh for security reasons.

        :param \**_kwargs: optional extra keyword arguments
        :raise SerializationError: When communication library is not installed.
        :return: serialized version of this BGVCiphertext.
        """
        if not COMMUNICATION_INSTALLED:
            raise SerializationError()
        if not self.fresh:
            warnings.warn(
                WARN_UNFRESH_SERIALIZATION, EncryptionSchemeWarning, stacklevel=2
            )
            self.randomize()
        self._fresh = False
        return {
            "value": self._raw_value,
            "scheme": self.scheme,
        }

    @staticmethod
    def deserialize(
        obj: BGVCiphertext.SerializedBGVCiphertext, **_kwargs: Any
    ) -> BGVCiphertext:
        r"""
        Deserialization function for BGV ciphertexts, which will be passed to the
        communication module.

        :param obj: serialized version of a BGVCiphertext.
        :param \**_kwargs: optional extra keyword arguments
        :raise SerializationError: When communication library is not installed.
        :return: Deserialized BGVCiphertext from the given dict.
        """
        if not COMMUNICATION_INSTALLED:
            raise SerializationError()
        return BGVCiphertext(
            raw_value=obj["value"],
            scheme=obj["scheme"],
        )

    # endregion


class BGV(
    AsymmetricEncryptionScheme[
        KeyMaterial,
        Plaintext,
        RawPlaintext,
        RawCiphertext,
        BGVCiphertext,
        BGVPublicKey,
        BGVSecretKey,
    ],
    RandomizedEncryptionScheme[
        KeyMaterial,
        Plaintext,
        RawPlaintext,
        RawCiphertext,
        BGVCiphertext,
        RawRandomness,
    ],
):
    """
    BGV encryption scheme. This is an AsymmetricEncryptionScheme, with a public and secret key.
    This is also a RandomizedEncryptionScheme, thus having internal randomness generation and
    allowing for the use of precomputed randomness. This scheme can be used for the additively
    homomorphic encryption of integers.
    """

    def __init__(
        self,
        public_key: BGVPublicKey,
        secret_key: BGVSecretKey | None,
        share_secret_key: bool = False,
        debug: bool = False,
    ) -> None:
        """
        Construct a new BGV encryption scheme.

        :param public_key: Public key for this BGV Scheme.
        :param secret_key: Optional Secret Key for this BGV Scheme (None when unknown).
        :param share_secret_key: Boolean value stating whether or not the secret key should be
            included in serialization. This should only be set to True if one is really sure of it.
        :param debug: flag to determine whether debug information should be displayed.
        """
        self._generate_randomness = partial(  # type: ignore[method-assign]
            self._generate_randomness_from_args,
            public_a=public_key.a,
            public_error_distribution=public_key.error_distibution,
            public_secret_distribution=public_key.secret_distribution,
        )
        AsymmetricEncryptionScheme.__init__(
            self, public_key=public_key, secret_key=secret_key
        )
        RandomizedEncryptionScheme.__init__(self, debug=debug)

        # Range of message values that can be encrypted with this BGV scheme
        # Note that it is possible to increase this by using base k instead of 2 for the number of
        # values, but that means the encoding needs to be updated accordingly.
        number_of_values = pow(2, public_key.a.n)
        self.max_value = (number_of_values - 1) // 2
        self.min_value = -((number_of_values - 1) // 2)
        if number_of_values % 2 == 0:
            self.max_value += 1

        # Variable that determines whether a secret key is sent when the scheme is sent
        # over a communication channel
        self.share_secret_key = share_secret_key

        self.client_history: list[HTTPClient] = []

        if self.identifier not in self._instances:
            self.save_globally()

    @staticmethod
    def generate_key_material(
        q: int,
        n: int,
        t: int,
        error_distribution: float,
        secret_distribution: float = 0.0,
    ) -> KeyMaterial:  # pylint: disable=arguments-differ
        r"""
        Method to generate key material (BGVSecretKey and BGVPublicKey), consisting of a
        polynomial $s \in R_q = \mathbb{Z}_q[x]/(x^n + 1)$ and a tuple $(a, b = as + te)$, where
        $a, e \in R_q$.

        The coefficients of $s$ are sampled from a ternary (-1, 0, 1) or discrete Gaussian
        distribution depending on the given value (0.0 for ternary, a positive standard deviation
        for the Gaussian distribution) and $e$ is sampled from a discrete Gaussian distribution with
        the given standard deviation.
        The coefficients of $a$ are sampled from a discrete uniform distribution over
        $\mathbb{Z}_q$.

        The values $n$ and $q$ should be chosen according to a chosen security level. In the README
        more information can be found on documentation that can help with this choice.

        The value $t$ should be relatively small to $q$ in order to have ciphertext operations like
        addition or integer multiplication not result the coefficients of the ciphertext wrapping
        around $q$, otherwise it will result in incorrect decryption.

        :param q: Positive integer modulus of the coefficients.
        :param n: Power of 2, degree of ideal for quotient ring of which the polynomial is an
            element.
        :param t: Value in $\mathbb{Z}_q^*$ such that the message space is
            $R_t = \mathbb{Z}_t[x]/(x^n + 1)$.
        :param error_distribution: Standard deviation used for Gaussian sampling in
            rerandomization.
        :param secret_distribution: 0.0 for ternary distribution, otherwise standard deviation of
            the used Gaussian distribution, default is 0.0.
        :raise ValueError: When $q$ or $t$ is smaller than 2, when $n$ is not a power of 2 or when
            $q$ and $t$ are not coprime.
        :return: Tuple with first the public key and then the secret key.
        """
        if q < 2:
            raise ValueError(
                f"For generating keys we need a positive integer modulus q larger than 1, {q} is no"
                f" such integer."
            )

        if t < 2 or t >= q:
            raise ValueError(
                f"For generating keys we need t to be in the range [2, {q}), {t} is no such "
                f"integer."
            )

        if not n or (n & (n - 1)):
            raise ValueError(
                f"The degree of the ideal of the quotient ring should be a power of 2, {n} is not."
            )

        if extended_euclidean(q, t)[0] != 1:
            raise ValueError(
                f"The coefficient modulus q of the ciphertext space and the coefficient modulus t"
                f" of the message space should be coprime, {q} and {t} are not."
            )

        if secret_distribution == 0.0:
            s = ternary_rand_polynomial(q, n)
        else:
            s = gauss_rand_polynomial(q, n, secret_distribution)
        a = unif_rand_polynomial(q, n)
        e = gauss_rand_polynomial(q, n, error_distribution)
        b = a * s + t * e
        return BGVPublicKey(
            a, b, t, error_distribution, secret_distribution
        ), BGVSecretKey(s)

    def encode(self, plaintext: Plaintext) -> EncodedPlaintext[RawPlaintext]:
        """
        Encode integers by converting to base t and using the bits as coefficients in a polynomial
        over $R_t$.

        :param plaintext: Plaintext to be encoded.
        :raise ValueError: If the plaintext is outside the supported range of this BGV scheme.
        :return: EncodedPlaintext object containing the encoded value.
        """
        if not self.min_value <= plaintext <= self.max_value:
            raise ValueError(
                f"This encoding scheme only supports values in the range [{self.min_value};"
                f"{self.max_value}], {plaintext} is outside that range."
            )
        negative = False
        if plaintext < 0:
            plaintext *= -1
            negative = True
        if plaintext == 0:
            return EncodedPlaintext(
                Polynomial([0], self.public_key.t, self.public_key.a.n),
                self,
            )
        coefficients = []
        while plaintext != 0:
            coefficients.append(plaintext % 2)
            if len(coefficients) > self.public_key.a.n:
                raise ValueError(
                    f"This encoding scheme only supports values in the range [{self.min_value};"
                    f"{self.max_value}], {plaintext} is outside that range."
                )
            plaintext = (plaintext - coefficients[-1]) // 2
        if negative:
            coefficients = [-1 * coefficient for coefficient in coefficients]
        return EncodedPlaintext(
            Polynomial(coefficients, self.public_key.t, self.public_key.a.n),
            self,
        )

    def decode(self, encoded_plaintext: EncodedPlaintext[RawPlaintext]) -> Plaintext:
        """
        Decode an encoded plaintext.

        :param encoded_plaintext: Encoded plaintext to be decoded.
        :return: Decoded plaintext value.
        """
        plaintext = 0
        base_power = 1
        for coefficient in encoded_plaintext.value.coefficients:
            plaintext += coefficient * base_power
            base_power *= 2
        return plaintext

    def _unsafe_encrypt_raw(
        self, plaintext: EncodedPlaintext[RawPlaintext]
    ) -> BGVCiphertext:
        r"""
        Encrypts an encoded (raw) plaintext value, but does not apply randomization. Given a raw
        plaintext message $m \in R_t = \mathbb{Z}_t[x]/(x^n + 1)$, convert it to $R_q$ and
        compute the ciphertext value as $(c_0, c_1) = (m, 0)$.

        :param plaintext: EncodedPlaintext object containing the raw value to be encrypted.
        :return: Non-randomized BGVCiphertext object containing the encrypted plaintext.
        """
        plaintext_mod_q = Polynomial(
            plaintext.value.coefficients, self.public_key.a.q, self.public_key.a.n
        )

        return BGVCiphertext(
            (
                plaintext_mod_q,
                Polynomial([0], self.public_key.a.q, self.public_key.a.n),
            ),
            self,
        )

    def _decrypt_raw(self, ciphertext: BGVCiphertext) -> EncodedPlaintext[RawPlaintext]:
        """
        Decrypts a BGVCiphertext to its encoded plaintext value.

        :param ciphertext: BGVCiphertext object containing the ciphertext to be decrypted.
        :raise ValueError: When the scheme has no secret key.
        :return: EncodedPlaintext object containing the encoded decryption of the ciphertext.
        """
        ciphertext_value = ciphertext.peek_value()
        if self.secret_key is None:
            raise ValueError(
                "This scheme only has a public key. Hence it cannot decrypt."
            )

        polynomial = ciphertext_value[0] + ciphertext_value[1] * self.secret_key.s

        return EncodedPlaintext(
            Polynomial(polynomial.coefficients, self.public_key.t, polynomial.n), self
        )

    @staticmethod
    def _generate_randomness_from_args(
        public_a: Polynomial,
        public_error_distribution: float,
        public_secret_distribution: float,
    ) -> tuple[Polynomial, Polynomial, Polynomial]:
        r"""
        Method to generate randomness value triple $(v, e', e'') \in R_q^3$ for BGV.

        :param public_a: Polynomial in $R_q = \mathbb{Z}_q[x]/(x^n + 1)$.
        :param public_error_distribution: Standard deviation used for Gaussian sampling in
            rerandomization.
        :param public_secret_distribution: 0.0 for ternary distribution, otherwise standard
            deviation of the used Gaussian distribution, default is 0.0.
        :return: The triple $v, e', e''$.
        """
        if public_secret_distribution == 0.0:
            v = ternary_rand_polynomial(public_a.q, public_a.n)
        else:
            v = gauss_rand_polynomial(
                public_a.q,
                public_a.n,
                public_secret_distribution,
            )
        e_prime = gauss_rand_polynomial(
            public_a.q,
            public_a.n,
            public_error_distribution,
        )
        e_double_prime = gauss_rand_polynomial(
            public_a.q,
            public_a.n,
            public_error_distribution,
        )
        return v, e_prime, e_double_prime

    def __eq__(self, other: object) -> bool:
        """
        Compare this BGV scheme with another object to determine (in)equality.

        :param other: Object to compare this BGV scheme with.
        :return: Boolean representation of (in)equality of both objects.
        """
        return isinstance(other, type(self)) and self.public_key == other.public_key

    @classmethod
    def id_from_arguments(cls, public_key: BGVPublicKey) -> int:
        """
        Method that turns the arguments for the constructor into an identifier. This identifier is
        used to find constructor calls that would result in identical schemes.

        :param public_key: BGVPublicKey of the BGV instance.
        :return: Identifier of the BGV instance.
        """
        return hash(public_key)

    def neg(self, ciphertext: BGVCiphertext) -> BGVCiphertext:
        """
        Negate the underlying plaintext of this ciphertext.

        The resulting ciphertext is fresh only if the original ciphertext was fresh. The original
        ciphertext is marked as non-fresh after the operation.

        :param ciphertext: BGVCiphertext of which the underlying plaintext should be negated
        :return: BGVCiphertext object corresponding to the negated plaintext.
        """
        if new_ciphertext_fresh := ciphertext.fresh:
            warnings.warn(WARN_INEFFICIENT_HOM_OPERATION, EncryptionSchemeWarning)

        # ciphertext.get_value() automatically marks ciphertext as not fresh
        old_ciphertext = ciphertext.get_value()
        return BGVCiphertext(
            (-1 * old_ciphertext[0], -1 * old_ciphertext[1]),
            self,
            fresh=new_ciphertext_fresh,
        )

    def add(
        self, ciphertext_1: BGVCiphertext, ciphertext_2: BGVCiphertext | Plaintext
    ) -> BGVCiphertext:
        """
        Secure addition.

        If ciphertext_2 is another BGVCiphertext, add the underlying plaintext value of
        ciphertext_1 to the underlying plaintext value of ciphertext_2. If it is a Plaintext,
        add the plaintext value to the underlying value of ciphertext_1.

        The resulting ciphertext is fresh only if at least one of the inputs was fresh. Both inputs
        are marked as non-fresh after the operation.

        :param ciphertext_1: First BGVCiphertext object of which the underlying plaintext is added.
        :param ciphertext_2: Either an BGVCiphertext of which the underlying plaintext is used for
            addition or a Plaintext that is used for addition.
        :raise AttributeError: When ciphertext_2 does not have the same public key as ciphertext_1.
        :return: An BGVCiphertext containing the encryption of the addition.
        """
        if isinstance(ciphertext_2, Plaintext):
            ciphertext_2 = self.unsafe_encrypt(ciphertext_2)
        elif ciphertext_1.scheme != ciphertext_2.scheme:
            raise AttributeError(
                "The public key of your first ciphertext is not equal to the "
                "public key of your second ciphertext."
            )

        if new_ciphertext_fresh := ciphertext_1.fresh or ciphertext_2.fresh:
            warnings.warn(WARN_INEFFICIENT_HOM_OPERATION, EncryptionSchemeWarning)

        # ciphertext.get_value() automatically marks ciphertext as not fresh
        old_ciphertext_1 = ciphertext_1.get_value()
        old_ciphertext_2 = ciphertext_2.get_value()
        return BGVCiphertext(
            (
                old_ciphertext_1[0] + old_ciphertext_2[0],
                old_ciphertext_1[1] + old_ciphertext_2[1],
            ),
            self,
            fresh=new_ciphertext_fresh,
        )

    def mul(  # type: ignore  # pylint: disable=arguments-renamed
        self, ciphertext: BGVCiphertext, scalar: int
    ) -> BGVCiphertext:
        """
        Multiply the underlying plaintext of this ciphertext with a scalar.

        The resulting ciphertext is marked fresh only if the original ciphertext was fresh. The
        original ciphertext is marked as non-fresh after the operation.

        :param ciphertext: BGVCiphertext of which the underlying plaintext is multiplied.
        :param scalar: A scalar with which the plaintext underlying the ciphertext is multiplied.
        :return: BGVCiphertext containing the encryption of the product.
        """
        if new_ciphertext_fresh := ciphertext.fresh:
            warnings.warn(WARN_INEFFICIENT_HOM_OPERATION, EncryptionSchemeWarning)

        # ciphertext.get_value() automatically marks ciphertext as not fresh
        old_ciphertext = ciphertext.get_value()
        return BGVCiphertext(
            (scalar * old_ciphertext[0], scalar * old_ciphertext[1]),
            self,
            fresh=new_ciphertext_fresh,
        )

    # region Serialization logic

    class SerializedBGV(TypedDict, total=False):
        scheme_id: int
        pubkey: BGVPublicKey
        seckey: BGVSecretKey | None

    def serialize(
        self,
        *,
        destination: HTTPClient | list[HTTPClient] | None = None,
        **_kwargs: Any,
    ) -> BGV.SerializedBGV:
        r"""
        Serialization function for BGV schemes, which will be passed to the communication
        module. The sharing of the secret key depends on the attribute share_secret_key.

        :param destination: HTTPClient representing where the message will go if applicable, can
            also be a list of clients in case of a broadcast message.
        :param \**_kwargs: optional extra keyword arguments
        :raise SerializationError: When communication library is not installed.
        :return: serialized version of this BGV scheme.
        """
        if isinstance(destination, HTTPClient):
            destination = [destination]
        if not COMMUNICATION_INSTALLED:
            raise SerializationError()
        if destination is not None and all(
            d in self.client_history for d in destination
        ):
            return {
                "scheme_id": self.identifier,
            }
        if destination is not None:
            for dest in destination:
                if dest not in self.client_history:
                    self.client_history.append(dest)
        if self.share_secret_key:
            return self.serialize_with_secret_key()
        return self.serialize_without_secret_key()

    def serialize_with_secret_key(
        self,
    ) -> BGV.SerializedBGV:
        """
        Serialization function for BGV schemes, that does include the secret key.

        :raise SerializationError: When communication library is not installed.
        :return: Serialized version of this BGV scheme.
        """
        if not COMMUNICATION_INSTALLED:
            raise SerializationError()
        return {
            "pubkey": self.public_key,
            "seckey": self.secret_key,
        }

    def serialize_without_secret_key(self) -> BGV.SerializedBGV:
        """
        Serialization function for BGV schemes, that does not include the secret key.

        :raise SerializationError: When communication library is not installed.
        :return: Serialized version of this BGV scheme (without the secret key).
        """
        if not COMMUNICATION_INSTALLED:
            raise SerializationError()
        return {
            "pubkey": self.public_key,
        }

    @staticmethod
    def deserialize(
        obj: BGV.SerializedBGV,
        *,
        origin: HTTPClient | None = None,
        **_kwargs: Any,
    ) -> BGV:
        r"""
        Deserialization function for BGV schemes, which will be passed to
        the communication module.

        :param obj: Serialized version of a BGV scheme.
        :param origin: HTTPClient representing where the message came from if applicable
        :param \**_kwargs: optional extra keyword arguments
        :raise SerializationError: When communication library is not installed.
        :raise ValueError: When a scheme is sent through ID without any prior communication of the
            scheme
        :return: Deserialized BGV scheme from the given dict. Might not have a secret
            key when that was not included in the received serialization.
        """
        if not COMMUNICATION_INSTALLED:
            raise SerializationError()
        if "scheme_id" in obj:
            bgv: BGV = BGV.from_id(obj["scheme_id"])
            if origin is None:
                raise ValueError(
                    f"The scheme was sent through an ID, but the origin is {origin}"
                )
            if origin not in bgv.client_history:
                raise ValueError(
                    f"The scheme was sent through an ID by {origin.addr}:{origin.port}, "
                    f"but this scheme was never"
                    "communicated with this party"
                )
        else:
            pubkey = obj["pubkey"]
            # This piece of code is specifically used for the case where sending and receiving
            # happens between hosts running the same python instance (local network).
            # In this case, the BGV scheme that was sent is already available before it
            # arrives and does not need to be created anymore.
            identifier = BGV.id_from_arguments(public_key=pubkey)
            if identifier in BGV._instances:
                bgv = BGV.from_id(identifier)
            else:
                bgv = BGV(
                    public_key=pubkey,
                    secret_key=obj["seckey"] if "seckey" in obj else None,
                )
        if origin is not None and origin not in bgv.client_history:
            bgv.client_history.append(origin)
        return bgv

    # endregion


if COMMUNICATION_INSTALLED:
    try:
        Serialization.register_class(BGV)
        Serialization.register_class(BGVCiphertext)
        Serialization.register_class(BGVPublicKey)
        Serialization.register_class(BGVSecretKey)
    except RepetitionError:
        pass
