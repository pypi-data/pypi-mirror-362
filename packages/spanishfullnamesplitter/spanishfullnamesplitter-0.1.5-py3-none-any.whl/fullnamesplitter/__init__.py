import sqlite3
from pathlib import Path

from unidecode import unidecode

NAME_DB = Path(__file__).parent / "names.db"

NAME_REPLACERS = ['DE', 'DEL', 'EL', 'LA', 'LAS']


class InconsistentNameException(Exception):
    pass


def select_surname(conn, name: str):
    sql = """SELECT apellido
             from apellidos
             WHERE apellido = ?"""
    cur = conn.cursor()
    res = cur.execute(sql, [unidecode(name).upper()])
    return res.fetchone() is not None


def select_name(conn, name: str):
    processed_name = unidecode(name).upper()
    sql = """SELECT nombre
             from nombres
             WHERE nombre = ?"""
    cur = conn.cursor()
    res = cur.execute(sql, [processed_name])
    return res.fetchone() is not None


def _search(conn, block, selector):
    fullchain = ''
    last_index = 0
    for i in range(len(block)):
        custom_chunk = ' '.join(block[:i + 1])
        if selector(conn, custom_chunk):
            fullchain = custom_chunk
            last_index = i + 1
    return (fullchain, last_index) if last_index else None


def _detect_surname_name_format(conn, name_str):
    """Detect if the format is "surname1 surname2, name" """
    if ',' in name_str:
        parts = name_str.split(',')
        if len(parts) == 2:
            surnames_part = parts[0].strip()
            name_part = parts[1].strip()
            return f"{name_part} {surnames_part}"
        else:
            name_str = name_str.replace(',', '')
    return name_str


def _split_name(conn, name_str, raise_exception=False):
    name_l = name_str.split(' ')
    name, surname1, surname2 = None, None, None
    first_element = 0

    # Name calculation
    name_result = _search(conn, name_l[first_element:], select_name)
    if name_result:
        name, last_index = name_result
        first_element += last_index

    # Surname calculation
    surname_result = _search(conn, name_l[first_element:], select_surname)
    if surname_result:
        surname1, last_index = surname_result
        first_element += last_index

    # The rest is considered the second surname
    surname2 = ' '.join(name_l[first_element:])

    # Move to surname1 if surname1 is not populated
    if not surname1:
        surname1 = surname2
        surname2 = None

    # For surnames that can be confused as compound names, if we haven't got
    # the second surname but we have a compound name, check it.
    if not surname2 and name and len(name.split(' ')) > 1:
        last_name = name.split(' ')[-1]
        if select_surname(conn, last_name):
            name = ' '.join(name.split(' ')[:-1])
            surname2 = surname1
            surname1 = last_name

    # Last check
    if raise_exception:
        if surname1 and not surname2 and not _search(conn, [surname1], select_surname):
            raise InconsistentNameException('Inconsistent surnames')
        elif surname2 and not _search(conn, [surname2], select_surname):
            raise InconsistentNameException('Inconsistent surnames')

    conn.close()
    return [name or None, surname1 or None, surname2 or None]


def swap_name(conn, name_str):
    # Manejar formato sin coma: "Apellido1 Apellido2 Nombre"
    tokens = name_str.split()
    if len(tokens) >= 3:
        # Probar diferentes combinaciones para detectar el patrón
        last_name_index = None
        for i in reversed(range(1, len(tokens))):
            potential_name = tokens[i:]
            # Verificar si el último elemento puede ser un nombre
            current_name_match = select_name(conn, ' '.join(potential_name))

            if not current_name_match and last_name_index:
                tocheck = f"{' '.join(tokens[last_name_index:])} {' '.join(tokens[:last_name_index])}"
                return tocheck
            if current_name_match:
                last_name_index = i


def split_name(name_str):
    conn = sqlite3.connect(NAME_DB)
    # Detectar y reorganizar si es necesario
    # reorganized_name = _detect_surname_name_format(conn, name_str.upper())
    try:
        name, surname, surname2 = _split_name(conn, name_str, raise_exception=True)
    except InconsistentNameException:
        name, surname, surname2 = _split_name(conn, swap_name(conn, name_str.upper()))
    return name, surname, surname2


if __name__ == '__main__':
    import sys

    name = ' '.join(sys.argv[1:])
    print(split_name(name))
