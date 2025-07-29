# TNO PET Lab - Secure Multi-Party Computation (MPC) - Encryption Schemes - BGV

Implementation of the additive part of the BGV homomorphic encryption scheme.

Note that the BGV scheme is a fully homomorphic scheme, but homomorphic multiplication is not implemented here. Only scalar multiplication is supported.

Supports:

- Positive and negative numbers.
- Homomorphic addition of ciphertexts, negation of ciphertexts, multiplication of ciphertext with integral scalars.

### PET Lab

The TNO PET Lab consists of generic software components, procedures, and functionalities developed and maintained on a regular basis to facilitate and aid in the development of PET solutions. The lab is a cross-project initiative allowing us to integrate and reuse previously developed PET functionalities to boost the development of new protocols and solutions.

The package `tno.mpc.encryption_schemes.bgv` is part of the [TNO Python Toolbox](https://github.com/TNO-PET).

_Limitations in (end-)use: the content of this software package may solely be used for applications that comply with international export control laws._
_This implementation of cryptographic software has not been audited. Use at your own risk._

## Documentation

Documentation of the `tno.mpc.encryption_schemes.bgv` package can be found
[here](https://docs.pet.tno.nl/mpc/encryption_schemes/bgv/0.1.1).

## Install

Easily install the `tno.mpc.encryption_schemes.bgv` package using `pip`:

```console
$ python -m pip install tno.mpc.encryption_schemes.bgv
```

_Note:_ If you are cloning the repository and wish to edit the source code, be
sure to install the package in editable mode:

```console
$ python -m pip install -e 'tno.mpc.encryption_schemes.bgv'
```

If you wish to run the tests you can use:

```console
$ python -m pip install 'tno.mpc.encryption_schemes.bgv[tests]'
```

_Note:_ A significant performance improvement can be achieved by installing the GMPY2 library.

```console
$ python -m pip install 'tno.mpc.encryption_schemes.bgv[gmpy]'
```

## Usage

Basic usage is as follows:

```python
from tno.mpc.encryption_schemes.bgv.bgv import BGV

if __name__ == "__main__":
    # initialize BGV with given parameters q, n, t, error_distribution and secret_distribution
    bgv_scheme = BGV.from_security_parameter(
        q=262139,
        n=16,
        t=32,
        error_distribution=3.19,
        secret_distribution=0.0,
    )
    # encrypt the number 8
    ciphertext1 = bgv_scheme.encrypt(8)
    # add 5 to the original plaintext
    ciphertext1 += 5
    # multiply the original plaintext by 10
    ciphertext1 *= 10
    # encrypt the number 10
    ciphertext2 = bgv_scheme.encrypt(10)
    # add both encrypted numbers together
    encrypted_sum = ciphertext1 + ciphertext2
    # ...communication...
    # decrypt the encrypted sum to 140
    decrypted_sum = bgv_scheme.decrypt(encrypted_sum)
    assert decrypted_sum == 140
```

Note that the choice of parameters is described in literature, see also the [background section](https://raw.githubusercontent.com/TNO-MPC/encryption_schemes.bgv/main/#background-of-the-bgv-scheme).

Running this example will show several warnings. The remainder of this documentation explains why the warnings are issued and how to get rid of them depending on the users' preferences.

## Fresh and unfresh ciphertexts

An encrypted message is called a ciphertext. A ciphertext in the current package has a property `is_fresh` that indicates whether this ciphertext has fresh randomness, in which case it can be communicated to another player securely. More specifically, a ciphertext `c` is fresh if another user, knowledgeable of all prior communication and all current ciphertexts marked as fresh, cannot deduce any more private information from learning `c`.

The package understands that the freshness of the result of a homomorphic operation depends on the freshness of the inputs, and that the homomorphic operation renders the inputs unfresh. For example, if `c1` and `c2` are fresh ciphertexts, then `c12 = c1 + c2` is marked as a fresh encryption (no rerandomization needed) of the sum of the two underlying plaintexts. After the operation, ciphertexts `c1` and `c2` are no longer fresh.

The fact that `c1` and `c2` were both fresh implies that, at some point, we randomized them. After the operation `c12 = c1 + c2`, only `c12` is fresh. This implies that one randomization was lost in the process. In particular, we wasted resources. An alternative approach was to have unfresh `c1` and `c2` then compute the unfresh result `c12` and only randomize that ciphertext. This time, no resources were wasted. The package issues a warning to inform the user this and similar efficiency opportunities.

The package integrates naturally with `tno.mpc.communication` and if that is used for communication, its serialization logic will ensure that all sent ciphertexts are fresh. A warning is issued if a ciphertext was randomized in the proces. A ciphertext is always marked as unfresh after it is serialized. Similarly, all received ciphertexts are considered unfresh.

## Tailor behavior to your needs

The crypto-neutral developer is facilitated by the package as follows: the package takes care of all bookkeeping, and the serialization used by `tno.mpc.communication` takes care of all randomization. The warnings can be [disabled](https://raw.githubusercontent.com/TNO-MPC/encryption_schemes.bgv/main/#warnings) for a smoother experience.

The eager crypto-youngster can improve their understanding and hone their skills by learning from the warnings that the package provides in a safe environment. The package is safe to use when combined with `tno.mpc.communication`. It remains to be safe while you transform your code from 'randomize-early' (fresh encryptions) to 'randomize-late' (unfresh encryptions, randomize before exposure). At that point you have optimized the efficiency of the library while ensuring that all exposed ciphertexts are fresh before they are serialized. In particular, you no longer rely on our serialization for (re)randomizing your ciphertexts.

Finally, the experienced cryptographer can turn off warnings / turn them into exceptions, or benefit from the `is_fresh` flag for own purposes (e.g. different serializer or communication).

### Warnings

By default, the `warnings` package prints only the first occurence of a warning for each location (module + line number) where the warning is issued. The user may easily [change this behaviour](https://docs.python.org/3/library/warnings.html#the-warnings-filter) to never see warnings:

```py
from tno.mpc.encryption_schemes.bgv import EncryptionSchemeWarning

warnings.simplefilter("ignore", EncryptionSchemeWarning)
```

Alternatively, the user may pass `"once"`, `"always"` or even `"error"`.

Finally, note that some operations issue two warnings, e.g. `c1-c2` issues a warning for computing `-c2` and a warning for computing `c1 + (-c2)`.

## Background of the BGV scheme

There are many (fully) homomorphic encryption schemes based on the Ring Learning with Errors problem, in this module one can find an implementation by BGV. Although that scheme is fully/somewhat homomorphic, only the additive component was implemented at this point.

The BGV scheme was first presented by [Brakerski, Gentry and Vaikuntanathan](https://dl.acm.org/doi/10.1145/2090236.2090262), but more configurations are described in the [Homomorphic Encryption Security Standard](https://homomorphicencryption.org/standard/) and the more recent [Security Guidelines for Implementing Homomorphic Encryption](https://eprint.iacr.org/2024/463.pdf). Following the practices described in these documents, the chosen ring to work in is $R=Z\left[x\right]/\left(x^n+1\right)$, where $n$ is a power of $2$. The plaintext ring is then $R/tR=Z_t\left[x\right]/\left(x^n+1\right)$ and the ciphertext ring $R/qR=Z_q\left[x\right]/\left(x^n+1\right)$ , where $t<q$ and $t$ and $q$ are coprime.

For this scheme, the parameters include a secret distribution and an error distribution for sampling polynomials. Note that the secret distribution is for sampling secrets, and need not be kept secret. For better performance, small secrets and errors are desired. Therefore, the implementation supports sampling secrets from ternary distribution (default) or a discrete Gaussian distribution. As a ternary distribution gives smaller coefficients, it gives significant better performance than using a discrete Gaussian distribution. For the ternary distribution, coefficients of the polynomial are chosen uniformly from $\{-1,0,1\}$. For the error distribution, a normal Gaussian distribution is used. The implemented discrete Gaussian sampling algorithm is described by [Karnay](https://dl.acm.org/doi/abs/10.1145/2710016).

### Choosing Parameters

Choosing parameters for BGV remains a challenge in the field. Here we highlight some documents that cover example parameter sets. For the Gaussian distributions, a standard deviation $\sigma$ can be specified. In practice, $\sigma$ is often chosen as $8/\sqrt{2\pi}\approx3.19$ in order to get small values. In Tables 1 and 2 of [Homomorphic Encryption Security Standard](https://homomorphicencryption.org/standard/), and, more recently, in Tables 5.2, 5.3 and 5.5 of [Security Guidelines for Implementing Homomorphic Encryption](https://eprint.iacr.org/2024/463.pdf) corresponding values for $\sigma$, $n$ and $q$ are given for different security levels and secret distributions. For example, when $\sigma = 3.19$ and $n=2048$ are chosen, a security level of 128 bits is desired and one uses a ternary distribution to sample the secret, in a setting with only classical attackers, the Homomorphic Encryption Standard recommends $q$ to have a maximum bitsize of $56$ while the more recent Security Guidelines for Implementing Homomorphic Encryption recommend a maximum bitsize of $53$. Note that a larger value for $q$ allows for more operations to be applied to a ciphertext, but it's size is a trade-off for security. Therefore, these maxima is given.

### Encoding Scheme

Lastly, we discuss the encoding of the scheme in this implementation. Elements of $R/qR$ are stored as polynomials modulo $q$ and $({x}^n+1)$, with coefficients in $[-\left\lfloor\frac{\left(q-1\right)}{2}\right\rfloor,\left\lceil\frac{\left(q-1\right)}{2}\right\rceil]$. In order for the decryption to work correctly, it is important that coefficients do not wrap around $q$, as described by [Brakerski, Gentry and Vaikuntanathan](https://dl.acm.org/doi/10.1145/2090236.2090262). To avoid this, $t$ should be sufficiently smaller than $q$, and sampling from the secret and error distributions should result in polynomials with small coefficients.

Further, to encode a cleartext message (integer value) in the plaintext space a binary encoding scheme for integers is used. Here, a cleartext value is taken in binary representation and we encode it in the plaintext space by using the bits as coefficients of a polynomial. Here, it also holds that coefficients should not wrap around $t$ in order for the algorithm to work correctly, see also [this website](https://www.inferati.com/blog/fhe-schemes-bfv). Note that instead of binary encoding, other k-ary encodings can also be used as long as the previous statement is satisfied, but this is currently not implemented.

## Advanced usage

The [basic usage](https://raw.githubusercontent.com/TNO-MPC/encryption_schemes.bgv/main/#usage) can be improved upon by explicitly randomizing at late as possible.

```python
from tno.mpc.encryption_schemes.bgv.bgv import BGV

if __name__ == "__main__":
    bgv_scheme = BGV.from_security_parameter(
        q=262139,
        n=16,
        t=32,
        error_distribution=3.19,
        secret_distribution=0.0,
    )
    # unsafe_encrypt does NOT randomize the generated ciphertext; it is deterministic still
    ciphertext1 = bgv_scheme.unsafe_encrypt(8)
    ciphertext1 += 5
    ciphertext1 *= 2
    ciphertext2 = bgv_scheme.unsafe_encrypt(10)
    # no randomness can be wasted by multiplying the two unfresh encryptions
    encrypted_multiplication = ciphertext1 * ciphertext2
    # randomize the result, which is now fresh
    encrypted_multiplication.randomize()
    # ...communication...
    decrypted_multiplication = bgv_scheme.decrypt(encrypted_multiplication)
    assert decrypted_multiplication == 140
```

As explained [above](https://raw.githubusercontent.com/TNO-MPC/encryption_schemes.bgv/main/#fresh-and-unfresh-ciphertexts), this implementation avoids wasted randomization for `encrypted_sum` and therefore is more efficient.

## Speed-up encrypting and randomizing

Encrypting messages and randomizing ciphertexts is an involved operation that requires randomly generating large values and processing them in some way. This process can be sped up which will boost the performance of your script or package. The base package `tno.mpc.encryption_schemes.templates` provides several ways to more quickly generate randomness and we will show two of them below.

### Generate randomness with multiple processes on the background

The simplest improvement gain is to generate the required amount of randomness as soon as the scheme is initialized (so prior to any call to `randomize` or `encrypt`):

```py
from tno.mpc.encryption_schemes.bgv.bgv import BGV

if __name__ == "__main__":
    bgv_scheme = BGV.from_security_parameter(
        q=262139,
        n=16,
        t=32,
        error_distribution=3.19,
        secret_distribution=0.0,
    )
    bgv_scheme.boot_randomness_generation(amount=5)
    # Possibly do some stuff here
    for msg in range(5):
        # The required randomness for encryption is already prepared, so this operation is faster.
        bgv_scheme.encrypt(msg)
    bgv_scheme.shut_down()
```

Calling `BGV.boot_randomness_generation` will generate a number of processes that is each tasked with generating some of the requested randomness. By default, the number of processes equals the number of CPUs on your device.

### Share BGV scheme and generate randomness a priori

A more advanced approach is to generate the randomness a priori and store it. Then, if you run your main protocol, all randomness is readily available. This looks as follows. First, the key-generating party generates a public-private keypair and shares the public key with the other participants. Now, every player pregenerates the amount of randomness needed for her part of the protocol and stores it in a file. For example, this can be done overnight or during the weekend. When the main protocol is executed, every player uses the same scheme (public key) as communicated before, configures the scheme to use the pregenerated randomness from file, and runs the main protocol without the need to generate randomness for encryption at that time. A minimal example is provided below.

```py
import base64
from pathlib import Path
from typing import Any, List

from tno.mpc.communication import Serialization
from tno.mpc.encryption_schemes.templates.random_sources import FileSource

from tno.mpc.encryption_schemes.bgv.bgv import BGV, BGVCiphertext


def deserializer(serialized_data) -> Any:
    """Deserialize bytes back to the original randomness."""
    serialized_data = serialized_data.encode("ascii")
    serialized_data = base64.b64decode(serialized_data)
    _, randomness = Serialization.unpack(serialized_data, use_pickle=False)
    return randomness


def initialize_and_store_scheme() -> None:
    # Generate scheme
    scheme = BGV.from_security_parameter(
        q=262139,
        n=16,
        t=32,
        error_distribution=3.19,
        secret_distribution=0.0,
    )

    # Store without secret key for others
    with open(Path("scheme_without_secret_key"), "wb") as file:
        file.write(Serialization.pack(scheme, msg_id="", use_pickle=False))

    # Store with secret key for own use
    scheme.share_secret_key = True
    with open(Path("scheme_with_secret_key"), "wb") as file:
        file.write(Serialization.pack(scheme, msg_id="", use_pickle=False))

    # Tidy up to simulate real environment (program terminates)
    scheme.clear_instances()


def load_scheme(path: Path) -> BGV:
    # Load scheme from disk
    with open(path, "rb") as file:
        scheme_raw = file.read()
    return Serialization.unpack(scheme_raw)[1]


def pregenerate_randomness_in_weekend(scheme: BGV, amount: int, path: Path) -> None:
    # Generate randomness
    scheme.boot_randomness_generation(amount)
    # Save randomness to comma-separated csv
    with open(path, "w") as file:
        for _ in range(amount):
            randomness = scheme.get_randomness()
            serialized_randomness = Serialization.pack(
                randomness, msg_id="<unused>", use_pickle=False
            )
            encoded_randomness = base64.b64encode(serialized_randomness).decode("ascii")
            file.write(f"{encoded_randomness};")
    # Shut down processes gracefully
    scheme.shut_down()


def show_pregenerated_randomness(scheme: BGV, amount: int, path: Path) -> None:
    # Configure file as randomness source
    scheme.register_randomness_source(
        FileSource(path, delimiter=";", deserializer=deserializer)
    )
    # Consume randomness from file
    for i in range(amount):
        print(f"Random element {i}: {scheme.get_randomness()}")


def use_pregenerated_randomness_in_encryption(
    scheme: BGV, amount: int, path: Path
) -> List[BGVCiphertext]:
    # Configure file as randomness source
    scheme.register_randomness_source(
        FileSource(path, delimiter=";", deserializer=deserializer)
    )
    # Consume randomness from file
    ciphertexts = [scheme.encrypt(_) for _ in range(amount)]
    return ciphertexts


def decrypt_result(scheme: BGV, ciphertexts: List[BGVCiphertext]) -> None:
    # Show result
    for i, ciphertext in enumerate(ciphertexts):
        print(f"Decryption of ciphertext {i}: {scheme.decrypt(ciphertext)}")


if __name__ == "__main__":
    AMOUNT = 5
    RANDOMNESS_PATH = Path("randomness.csv")

    # Alice initializes, stores and distributes the BGV scheme
    initialize_and_store_scheme()

    # Tidy up to simulate real environment (second party doesn't yet have the BGV instance)
    BGV.clear_instances()

    # Bob loads the BGV scheme, pregenerates randomness and encrypts the values 0,...,AMOUNT-1
    scheme_without_secret_key = load_scheme("scheme_without_secret_key")
    assert (
        scheme_without_secret_key.secret_key is None
    ), "Loaded BGV scheme contains secret key! This is not supposed to happen."
    pregenerate_randomness_in_weekend(
        scheme_without_secret_key, AMOUNT, RANDOMNESS_PATH
    )
    show_pregenerated_randomness(scheme_without_secret_key, AMOUNT, RANDOMNESS_PATH)
    # Prints the following to screen (numbers will be different):
    # Random element 0: 663667452419034735381232312860937013...
    # Random element 1: ...
    # ...
    ciphertexts = use_pregenerated_randomness_in_encryption(
        scheme_without_secret_key, AMOUNT, RANDOMNESS_PATH
    )

    # Tidy up to simulate real environment (first party should use own BGV instance)
    BGV.clear_instances()

    # Alice receives the ciphertexts from Bob and decrypts them
    scheme_with_secret_key = load_scheme("scheme_with_secret_key")
    decrypt_result(scheme_with_secret_key, ciphertexts)
    # Prints the following to screen:
    # Decryption of ciphertext 0: 0.000
    # Decryption of ciphertext 1: 1.000
    # ...
```
