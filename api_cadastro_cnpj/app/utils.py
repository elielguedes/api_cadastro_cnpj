import re
from typing import List


def normalize_cnpj(value: str) -> str:
    """Remove qualquer caractere não numérico do CNPJ e retorne apenas dígitos.

    Ex: '00.000.000/0001-00' -> '00000000000100'
    """
    if value is None:
        return ''
    return re.sub(r"\D+", "", str(value))

def validate_cnpj(cnpj: str) -> bool:
    """Validate Brazilian CNPJ using digit verifiers.

    Returns True if valid, False otherwise.
    """
    if not cnpj:
        return False
    c = normalize_cnpj(cnpj)
    if len(c) != 14 or len(set(c)) == 1:
        return False

    def _calc_digit(digs: str, multipliers: List[int]) -> int:
        s = sum(int(d) * m for d, m in zip(digs, multipliers))
        r = s % 11
        return 0 if r < 2 else 11 - r

    # first verifier
    first = _calc_digit(c[:12], [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
    # second verifier
    second = _calc_digit(c[:12] + str(first), [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])

    return c.endswith(f"{first}{second}")
