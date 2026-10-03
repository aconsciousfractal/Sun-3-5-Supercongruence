"""Deterministic evidence I/O and strict semantic replay comparison."""
import json
from pathlib import Path
from .arithmetic import require

CORE_FILES = ('eta_certificates.json', 'prime_regression.json',
              'invariant_certificates.json', 'modular_polynomials.json',
              'verification_summary.json')
SYMBOLIC_FILE = 'symbolic_identities.json'


def reject_duplicates(pairs):
    result = {}
    for key,value in pairs:
        if key in result:
            raise ValueError(f'duplicate JSON key: {key}')
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError(f'nonfinite JSON constant: {value}')


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'),
                      object_pairs_hook=reject_duplicates, parse_constant=reject_constant)


def write_json(path,data):
    with Path(path).open('w',encoding='utf-8',newline='\n') as stream:
        stream.write(json.dumps(data,sort_keys=True,indent=2,allow_nan=False)+'\n')


def compare_expected(actual_directory,expected_directory,symbolic=False):
    """Compare independently computed results with the fixed named inventory.

    Expected data never feed a scientific calculation. An empty directory,
    duplicate keys, missing/extra files or changed content fail the replay.
    """
    actual_directory,expected_directory = Path(actual_directory),Path(expected_directory)
    require(actual_directory.resolve() != expected_directory.resolve(),
            'generated and expected evidence directories must be distinct')
    require(expected_directory.is_dir(), 'expected evidence directory is missing')
    names = set(CORE_FILES) | ({SYMBOLIC_FILE} if symbolic else set())
    actual_names = {p.name for p in actual_directory.iterdir()}
    expected_names = {p.name for p in expected_directory.iterdir()}
    require(actual_names == names, 'generated evidence inventory differs from fixed schema')
    require(expected_names == names, 'expected evidence inventory differs from fixed schema')
    for name in sorted(names):
        actual = read_json(actual_directory/name)
        expected = read_json(expected_directory/name)
        require(type(actual) is dict and type(expected) is dict and
                actual.get('status') == expected.get('status') == 'PASS' and
                actual.get('schema_version') == expected.get('schema_version') == 1,
                f'invalid evidence root: {name}')
        # Serialized canonical JSON also distinguishes bool, int and float.
        require(json.dumps(actual,sort_keys=True,allow_nan=False) ==
                json.dumps(expected,sort_keys=True,allow_nan=False),
                f'evidence mismatch: {name}')
