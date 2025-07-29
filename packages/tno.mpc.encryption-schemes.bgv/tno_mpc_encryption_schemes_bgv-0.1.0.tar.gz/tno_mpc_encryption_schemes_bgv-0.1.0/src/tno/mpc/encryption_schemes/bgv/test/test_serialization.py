"""
This module tests the serialization of BGV instances.
"""

from __future__ import annotations

import asyncio
import warnings
from typing import Any, cast

import pytest

from tno.mpc.communication import Pool
from tno.mpc.encryption_schemes.templates import EncryptionSchemeWarning

from tno.mpc.encryption_schemes.bgv.bgv import (
    BGV,
    WARN_UNFRESH_SERIALIZATION,
    BGVCiphertext,
    BGVPublicKey,
    BGVSecretKey,
)
from tno.mpc.encryption_schemes.bgv.test.test_bgv import (
    PLAINTEXT_INPUTS,
    limit_to_message_space,
)

public_key, secret_key = BGV.generate_key_material(
    q=262139,
    n=16,
    t=32,
    error_distribution=3.19,
    secret_distribution=0.0,
)


@pytest.fixture(name="encryption_scheme")
def fixture_scheme() -> BGV:
    """
    Get BGV encryption scheme.

    :return: Initialized BGV scheme.
    """
    return BGV(public_key, secret_key)


def bgv_scheme() -> BGV:
    """
    Constructs an BGV scheme.

    :return: Initialized BGV scheme.
    """
    return BGV.from_security_parameter(
        q=262139,
        n=16,
        t=32,
        error_distribution=3.19,
        secret_distribution=0.0,
        debug=False,
    )


def test_serialization_public_key(encryption_scheme: BGV) -> None:
    """
    Test to determine whether the public key serialization works properly for BGV scheme.

    :param encryption_scheme: BGV scheme under test.
    """
    serialized_pk = encryption_scheme.public_key.serialize()
    assert encryption_scheme.public_key == BGVPublicKey.deserialize(serialized_pk)


def test_serialization_secret_key(encryption_scheme: BGV) -> None:
    """
    Test to determine whether the secret key serialization works properly for BGV scheme.

    :param encryption_scheme: BGV subscheme under test.
    """
    if encryption_scheme.secret_key is not None:
        serialized_sk = encryption_scheme.secret_key.serialize()
        assert encryption_scheme.secret_key == BGVSecretKey.deserialize(serialized_sk)


@pytest.mark.parametrize("value", PLAINTEXT_INPUTS)
@pytest.mark.parametrize("fresh", (True, False))
def test_serialization_cipher(encryption_scheme: BGV, value: int, fresh: bool) -> None:
    """
    Test to determine whether serialization works properly for the BGVCiphertext.

    :param encryption_scheme: BGV scheme under test.
    :param value: Value to serialize
    :param fresh: Freshness of ciphertext
    """
    value = limit_to_message_space(value, encryption_scheme)
    if fresh:
        cipher = encryption_scheme.encrypt(value)
    else:
        cipher = encryption_scheme.unsafe_encrypt(value)
    with warnings.catch_warnings():
        # The unfresh serialization warning is not in scope of this test.
        warnings.filterwarnings("ignore", WARN_UNFRESH_SERIALIZATION, UserWarning)
        deserialized = BGVCiphertext.deserialize(cipher.serialize())
    assert isinstance(deserialized, BGVCiphertext)
    assert cipher == deserialized


def test_serialization_no_share(encryption_scheme: BGV) -> None:
    """
    Test to determine whether the BGV scheme serialization works properly for schemes
    when the secret key SHOULD NOT be serialized.

    :param encryption_scheme: BGV scheme under test.
    """
    scheme = encryption_scheme
    # by default the secret key is not serialized, but equality should then still hold
    serialized_scheme = scheme.serialize()
    assert "seckey" not in serialized_scheme
    scheme_prime = scheme.deserialize(serialized_scheme)
    scheme.shut_down()
    scheme_prime.shut_down()
    # secret key is still shared due to local instance sharing
    assert scheme.secret_key is scheme_prime.secret_key
    assert scheme == scheme_prime

    # this time empty the list of global instances after serialization
    scheme_serialized = scheme.serialize()
    scheme.clear_instances()
    scheme_prime2 = scheme.deserialize(scheme_serialized)
    scheme.shut_down()
    scheme_prime2.shut_down()
    assert scheme_prime2.secret_key is None
    assert scheme == scheme_prime2


def test_serialization_share(encryption_scheme: BGV) -> None:
    """
    Test to determine whether the BGV scheme serialization works properly for schemes
    when the secret key SHOULD be serialized.

    :param encryption_scheme: BGV scheme under test.
    """
    scheme = encryption_scheme
    scheme.share_secret_key = True
    # We indicated that the secret key should be serialized, so this should be equal
    serialized_scheme = scheme.serialize()
    assert "seckey" in serialized_scheme
    scheme_prime = scheme.deserialize(serialized_scheme)
    scheme_prime.shut_down()
    scheme.shut_down()
    assert scheme == scheme_prime


@pytest.mark.parametrize("value", PLAINTEXT_INPUTS)
def test_serialization_randomization_unfresh(
    encryption_scheme: BGV, value: int
) -> None:
    """
    Test to determine whether the BGV ciphertext serialization correctly randomizes non-fresh
    ciphertexts.

    :param encryption_scheme: BGV subscheme under test.
    :param value: value to serialize
    """
    scheme = encryption_scheme
    value = limit_to_message_space(value, scheme)
    ciphertext = scheme.unsafe_encrypt(value)
    val_pre_serialize = ciphertext.peek_value()
    with pytest.warns(EncryptionSchemeWarning, match=WARN_UNFRESH_SERIALIZATION):
        ciphertext.serialize()
    val_post_serialize = ciphertext.peek_value()
    scheme.shut_down()
    assert val_pre_serialize != val_post_serialize
    assert ciphertext.fresh is False


@pytest.mark.parametrize("value", PLAINTEXT_INPUTS)
def test_serialization_randomization_fresh(encryption_scheme: BGV, value: int) -> None:
    """
    Test to determine whether the BGV ciphertext serialization works properly for fresh
    ciphertexts.

    :param encryption_scheme: BGV scheme under test.
    :param value: Value to serialize
    """
    scheme = encryption_scheme
    value = limit_to_message_space(value, scheme)

    ciphertext = scheme.encrypt(value)

    assert ciphertext.fresh

    ciphertext_prime = BGVCiphertext.deserialize(ciphertext.serialize())

    assert not ciphertext.fresh
    assert not ciphertext_prime.fresh

    scheme.shut_down()
    assert ciphertext == ciphertext_prime


def test_unrelated_instances() -> None:
    """
    Test whether the from_id_arguments and id_from_arguments methods works as intended.
    The share_secret_key variable should not influence the identifier.
    """
    scheme = bgv_scheme()
    pk = scheme.public_key
    sk = scheme.secret_key

    scheme.clear_instances()

    bgv_1 = BGV(public_key=pk, secret_key=None, share_secret_key=False)
    bgv_1_prime = BGV(public_key=pk, secret_key=sk, share_secret_key=True)
    assert bgv_1.identifier == bgv_1_prime.identifier
    bgv_2 = BGV.from_id_arguments(public_key=pk)

    bgv_1.shut_down()
    bgv_1_prime.shut_down()
    bgv_2.shut_down()
    scheme.shut_down()

    assert bgv_1 is bgv_2
    assert bgv_1 == bgv_2


def test_related_serialization(encryption_scheme: BGV) -> None:
    """
    Test whether deserialization of BGV ciphertexts results in correctly deserialized schemes.
    Because ciphertexts are connected to schemes, you want ciphertexts coming from the same scheme
    to still have the same scheme when they are deserialized.

    :param encryption_scheme: BGV scheme under test.
    """
    scheme = encryption_scheme
    ciphertext_1 = scheme.encrypt(1)
    ciphertext_2 = scheme.encrypt(2)
    ser_1 = ciphertext_1.serialize()
    ser_2 = ciphertext_2.serialize()
    new_ciphertext_1 = ciphertext_1.deserialize(ser_1)
    new_ciphertext_2 = ciphertext_1.deserialize(ser_2)

    new_ciphertext_1.scheme.shut_down()
    scheme.shut_down()

    assert (
        new_ciphertext_1.scheme
        is new_ciphertext_2.scheme
        is ciphertext_1.scheme
        is ciphertext_2.scheme
    )


def test_instances_from_security_param_bgv(
    encryption_scheme: BGV,
) -> None:
    """
    Test whether the get_instance_from_sec_param method works as intended. If an BGV scheme
    with the given parameters has already been created before, then that exact same scheme should be
    returned. Otherwise, a new scheme should be generated with those parameters.

    :param encryption_scheme: BGV scheme under test.
    """
    scheme_type = type(encryption_scheme)

    new_bgv_1 = scheme_type.from_security_parameter(
        q=262139,
        n=16,
        t=32,
        error_distribution=3.19,
        secret_distribution=0.0,
        debug=False,
    )
    new_bgv_1.save_globally()
    new_bgv_2 = scheme_type.from_id(new_bgv_1.identifier)
    new_bgv_3 = scheme_type.from_security_parameter(
        q=262139,
        n=16,
        t=32,
        error_distribution=3.19,
        secret_distribution=0.0,
        debug=False,
    )

    new_bgv_1.shut_down()
    new_bgv_2.shut_down()
    new_bgv_3.shut_down()

    assert new_bgv_1 is new_bgv_2
    assert new_bgv_1 is not new_bgv_3
    assert new_bgv_2 is not new_bgv_3
    assert new_bgv_1 != new_bgv_3
    assert new_bgv_2 != new_bgv_3


async def send_and_receive(pools: tuple[Pool, Pool], obj: Any) -> Any:
    """
    Method that sends objects from one party to another.

    :param pools: collection of communication pools
    :param obj: object to be sent
    :return: the received object
    """
    # send from host 1 to host 2
    await pools[0].send("local1", obj)
    item = await pools[1].recv("local0")
    return item


@pytest.mark.asyncio
async def test_sending_and_receiving(
    encryption_scheme: BGV, http_pool_duo: tuple[Pool, Pool]
) -> None:
    """
    This test ensures that serialisation logic is correctly loading into the
    communication module.

    :param encryption_scheme: BGV scheme under test.
    :param http_pool_duo: Collection of two communication pools.
    """
    bgv_prime = await send_and_receive(http_pool_duo, encryption_scheme)
    assert (
        type(encryption_scheme).from_id(encryption_scheme.identifier)
        is encryption_scheme
    )
    assert bgv_prime is encryption_scheme
    # the scheme has been sent once, so the httpclients should be in the scheme's client
    # history.
    assert len(encryption_scheme.client_history) == 2
    assert (
        encryption_scheme.client_history[0] == http_pool_duo[0].pool_handlers["local1"]
    )
    assert (
        encryption_scheme.client_history[1] == http_pool_duo[1].pool_handlers["local0"]
    )

    encryption = encryption_scheme.encrypt(plaintext=4)
    encryption_prime: BGVCiphertext = await send_and_receive(http_pool_duo, encryption)
    encryption_prime.scheme.shut_down()
    assert encryption == encryption_prime

    public_key_prime = await send_and_receive(
        http_pool_duo, encryption_scheme.public_key
    )
    assert encryption_scheme.public_key == public_key_prime

    secret_key_prime = await send_and_receive(
        http_pool_duo, encryption_scheme.secret_key
    )
    assert encryption_scheme.secret_key == secret_key_prime


@pytest.mark.asyncio
async def test_broadcasting(
    encryption_scheme: BGV, http_pool_trio: tuple[Pool, Pool, Pool]
) -> None:
    """
    This test ensures that broadcasting BGV ciphertexts works as expected.

    :param encryption_scheme: BGV scheme under test.
    :param http_pool_trio: Collection of three communication pools.
    """
    await asyncio.gather(
        *(
            http_pool_trio[0].send("local1", encryption_scheme),
            http_pool_trio[0].send("local2", encryption_scheme),
        )
    )
    scheme_prime_1, scheme_prime_2 = await asyncio.gather(
        *(http_pool_trio[1].recv("local0"), http_pool_trio[2].recv("local0"))
    )
    assert (
        type(encryption_scheme).from_id(encryption_scheme.identifier)
        is encryption_scheme
    )
    assert scheme_prime_1 is encryption_scheme
    assert scheme_prime_2 is encryption_scheme
    # the scheme has been sent once to each party, so the httpclients should be in the scheme's
    # client history.
    assert len(encryption_scheme.client_history) == 3
    assert http_pool_trio[0].pool_handlers["local1"] in encryption_scheme.client_history
    assert http_pool_trio[0].pool_handlers["local2"] in encryption_scheme.client_history
    assert http_pool_trio[1].pool_handlers["local0"] in encryption_scheme.client_history
    assert http_pool_trio[2].pool_handlers["local0"] in encryption_scheme.client_history

    encryption = encryption_scheme.encrypt(plaintext=42)
    await http_pool_trio[0].broadcast(encryption, "msg_id")
    encryption_prime_1, encryption_prime_2 = cast(
        tuple[BGVCiphertext, BGVCiphertext],
        await asyncio.gather(
            *(
                http_pool_trio[1].recv("local0", "msg_id"),
                http_pool_trio[2].recv("local0", "msg_id"),
            )
        ),
    )

    encryption_prime_1.scheme.shut_down()
    encryption_prime_2.scheme.shut_down()
    assert encryption == encryption_prime_1
    assert encryption == encryption_prime_2
