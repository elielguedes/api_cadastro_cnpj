import re


def normalize_cnpj(value: str) -> str:
    """Remove qualquer caractere não numérico do CNPJ e retorne apenas dígitos.

    Ex: '00.000.000/0001-00' -> '00000000000100'
    """
    if value is None:
        return ''
    return re.sub(r"\D+", "", str(value))
