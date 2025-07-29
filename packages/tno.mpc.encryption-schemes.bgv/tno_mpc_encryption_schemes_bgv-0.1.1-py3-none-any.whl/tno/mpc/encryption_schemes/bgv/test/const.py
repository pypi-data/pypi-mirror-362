"""
This module contains values that are used in multiple test modules.
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
    BGV.generate_key_material(
        q=5,
        n=8,
        t=4,
        secret_distribution=0.0,
        error_distribution=2.0,
    ),
    BGV.generate_key_material(
        q=7,
        n=16,
        t=3,
        secret_distribution=3.0,
        error_distribution=3.0,
    ),
    BGV.generate_key_material(
        q=7,
        n=16,
        t=3,
        secret_distribution=0.0,
        error_distribution=3.0,
    ),
]
