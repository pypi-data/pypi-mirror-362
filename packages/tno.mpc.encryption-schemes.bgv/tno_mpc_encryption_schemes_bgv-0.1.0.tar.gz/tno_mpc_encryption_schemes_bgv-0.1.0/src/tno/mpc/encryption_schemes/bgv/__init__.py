"""
Implementation of the BGV cryptosystem based on ring learning with errors (RLWE).
"""

#  pylint: disable=useless-import-alias

# Explicit re-export of all functionalities, such that they can be imported properly. Following
# https://www.python.org/dev/peps/pep-0484/#stub-files and
# https://mypy.readthedocs.io/en/stable/command_line.html#cmdoption-mypy-no-implicit-reexport

from tno.mpc.encryption_schemes.bgv.bgv import BGV as BGV
from tno.mpc.encryption_schemes.bgv.bgv import BGVCiphertext as BGVCiphertext
from tno.mpc.encryption_schemes.bgv.bgv import BGVPublicKey as BGVPublicKey
from tno.mpc.encryption_schemes.bgv.bgv import BGVSecretKey as BGVSecretKey
from tno.mpc.encryption_schemes.bgv.lattice_utils import Polynomial as Polynomial
from tno.mpc.encryption_schemes.bgv.lattice_utils import (
    gauss_rand_polynomial as gauss_rand_polynomial,
)
from tno.mpc.encryption_schemes.bgv.lattice_utils import (
    unif_rand_polynomial as unif_rand_polynomial,
)

__version__ = "0.1.0"
