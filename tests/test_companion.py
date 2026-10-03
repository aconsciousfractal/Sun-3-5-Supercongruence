"""Adverse tests of scientific validators and the frozen evidence comparison."""
import copy
from fractions import Fraction
import json
from math import comb
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from companion.arithmetic import eta_quot, seq, weighted_mod
from companion.eta import certificates, validate_period, validate_geometry, add
from companion.primes import cm_matrix, regression
from companion.invariant import validate_invariant, invariant
from companion.modular_polynomial import modular_poly
from companion.modpoly import validate_modular_polynomial
from companion.evidence import CORE_FILES, compare_expected, write_json


class ScientificCorruptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.eta = certificates()
        cls.polys,_,_ = modular_poly(7,9,'raw')

    def test_period_parameters_and_coefficients_are_not_interchangeable(self):
        arrays = self.eta['eta_coefficients']
        Y = add(arrays['A'],arrays['B'])
        J,ell = arrays['J'],self.eta['logarithmic_J']
        validate_period(Y,J,ell,(10,3,9))
        for bad in ((11,3,9),(10,4,9),(10,3,10),(7,2,-8)):
            with self.subTest(parameters=bad),self.assertRaises(ArithmeticError):
                validate_period(Y,J,ell,bad)
        for index in (1,8):
            mutated = Y[:]
            mutated[index] += 1
            with self.subTest(index=index),self.assertRaises(ArithmeticError):
                validate_period(mutated,J,ell,(10,3,9))
        with self.assertRaises(ArithmeticError):
            validate_period(Y[:8],J[:8],ell[:8],(10,3,9))
        with self.assertRaises(ArithmeticError):
            validate_period([],[],[],(10,3,9))
        with self.assertRaises(ArithmeticError):
            validate_period([float(x) for x in Y],J,ell,(10,3,9))

    def test_independent_eta_engines_and_invalid_orders(self):
        for exponents in ({1:-5,2:7,3:7,6:-5},{1:7,2:-5,3:-5,6:7}):
            self.assertEqual(eta_quot(exponents,25),eta_quot(exponents,25,'logarithmic_derivative'))
        for exponents in ({1:1},{1:-24},{0:24},{1:1.0},{}):
            with self.subTest(exponents=exponents),self.assertRaises(ArithmeticError):
                eta_quot(exponents,10)
        with self.assertRaises(ValueError):
            eta_quot({1:24},0,'unknown')

    def test_geometry_certificate_rejects_coefficient_changes_and_short_window(self):
        arrays = self.eta['eta_coefficients']
        arguments = [arrays[name][:] for name in ('h','h3','Rh')]
        validate_geometry(*arguments)
        for index in range(3):
            changed = copy.deepcopy(arguments)
            changed[index][8] += 1
            with self.subTest(series=index),self.assertRaises(ArithmeticError):
                validate_geometry(*changed)
        with self.assertRaises(ArithmeticError):
            validate_geometry(*(a[:10] for a in arguments))

    def test_CM_sign_and_determinant_in_both_classes(self):
        for p,x,y in ((7,2,1),(13,1,2)):
            valid = cm_matrix(p,x,y)
            self.assertEqual(valid['norm'],p*p)
            matrix = valid['matrix'][:]
            matrix[0] += 1
            with self.subTest(p=p),self.assertRaises(ArithmeticError):
                cm_matrix(p,x,y,matrix=matrix)
            with self.subTest(p=p,field='character'),self.assertRaises(ArithmeticError):
                cm_matrix(p,x,y,character=-1)
            with self.subTest(p=p,field='determinant'),self.assertRaises(ArithmeticError):
                cm_matrix(p,x,y,determinant_scale=Fraction(valid['e'],9))
        with self.assertRaises(ArithmeticError):
            cm_matrix(7,1,1)
        with self.assertRaises(ValueError):
            cm_matrix(25,1,2)

    def test_modular_polynomial_corruption_is_semantically_rejected(self):
        validate_modular_polynomial(self.polys,7,'raw')
        mutations = []
        bad = copy.deepcopy(self.polys)
        bad[0][0] += 1
        mutations.append(bad)
        bad = copy.deepcopy(self.polys)
        bad[7][0] += 49  # invisible modulo p^2; exact CM factor must still fail
        mutations.append(bad)
        bad = copy.deepcopy(self.polys)
        bad[-1][0] += 1
        mutations.append(bad)
        bad = copy.deepcopy(self.polys)
        bad[2].extend([0,1])
        mutations.append(bad)
        for i,bad in enumerate(mutations):
            with self.subTest(mutation=i),self.assertRaises(ArithmeticError):
                validate_modular_polynomial(bad,7,'raw')
        with self.assertRaises(ArithmeticError):
            validate_modular_polynomial([],7,'raw')
        with self.assertRaises(ValueError):
            modular_poly(9,10)
        with self.assertRaises(ValueError):
            modular_poly(7,3)

    def test_invariant_resonance_and_singular_control(self):
        p = 11
        u = seq(p,7,2,-8)
        g = [comb(2*n,n)*value for n,value in enumerate(u)]
        valid = validate_invariant(g,p,(7,2,-8))
        self.assertTrue(all(value % (p*p) == 0 for value in valid))
        bad = g[:]
        bad[p] += 1
        with self.assertRaises(ArithmeticError):
            validate_invariant(bad,p,(7,2,-8))
        bad = g[:]
        bad[2] += 1
        with self.assertRaises(ArithmeticError):
            validate_invariant(bad,p,(7,2,-8))
        with self.assertRaises(ArithmeticError):
            validate_invariant(g,p,(7,3,-8))
        with self.assertRaises(ArithmeticError):
            invariant([],7,2,-8)

    def test_domain_rejection_and_nonempty_short_window(self):
        for bound in (0,5,6,-1,7.0,True):
            with self.subTest(bound=bound),self.assertRaises(ValueError):
                regression(bound)
        result = regression(7)
        self.assertEqual(result['prime_count'],2)
        self.assertEqual({c['e'] for c in result['both_CM_class_controls']},{1,3})
        for p,denom,length in ((9,54,9),(5,50,5),(7,54,6)):
            with self.subTest(p=p,denom=denom),self.assertRaises((ValueError,ArithmeticError)):
                weighted_mod([1]*length,denom,p)


class FrozenEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix='sun35-test-')
        base = Path(self.scratch.name)
        self.actual,self.expected = base/'actual',base/'expected'
        self.actual.mkdir()
        self.expected.mkdir()
        self.data = certificates()
        for name in CORE_FILES:
            for directory in (self.actual,self.expected):
                write_json(directory/name,self.data)

    def tearDown(self):
        self.scratch.cleanup()

    def test_frozen_replay_accepts_whitespace_but_rejects_changed_evidence(self):
        compare_expected(self.actual,self.expected)
        path = self.expected/CORE_FILES[0]
        path.write_text(json.dumps(self.data,separators=(',',':')),encoding='utf-8')
        compare_expected(self.actual,self.expected)
        changed = copy.deepcopy(self.data)
        changed['eta_coefficients']['A'][8] += 1
        write_json(path,changed)
        with self.assertRaises(ArithmeticError):
            compare_expected(self.actual,self.expected)

    def test_missing_extra_empty_and_invalid_evidence_fail_closed(self):
        with self.assertRaises(ArithmeticError):
            compare_expected(self.actual,self.actual)
        path = self.expected/CORE_FILES[0]
        path.unlink()
        with self.assertRaises(ArithmeticError):
            compare_expected(self.actual,self.expected)
        write_json(path,self.data)
        extra = self.expected/'unexpected.json'
        write_json(extra,self.data)
        with self.assertRaises(ArithmeticError):
            compare_expected(self.actual,self.expected)
        extra.unlink()
        for text in ('{}','{"status":"PASS","status":"FAIL"}','{"value":NaN}'):
            path.write_text(text,encoding='utf-8')
            with self.subTest(text=text),self.assertRaises((ValueError,ArithmeticError)):
                compare_expected(self.actual,self.expected)
        empty = self.expected.parent/'empty'
        empty.mkdir()
        with self.assertRaises(ArithmeticError):
            compare_expected(self.actual,empty)

    def test_boolean_integer_confusion_is_rejected(self):
        changed = copy.deepcopy(self.data)
        changed['schema_version'] = True
        write_json(self.expected/CORE_FILES[0],changed)
        with self.assertRaises(ArithmeticError):
            compare_expected(self.actual,self.expected)

    def test_CLI_rejects_empty_bound_and_refuses_evidence_overwrite(self):
        for args in (['--bound','6'],['--out',str(self.expected)]):
            result = subprocess.run([sys.executable,'-B','-O',str(ROOT/'scripts/verify.py'),*args],
                                    cwd=self.actual,capture_output=True,text=True)
            self.assertEqual(result.returncode,1,result.stdout+result.stderr)
            self.assertIn('SUN35_REPLAY_FAIL',result.stderr)


if __name__ == '__main__':
    unittest.main()
