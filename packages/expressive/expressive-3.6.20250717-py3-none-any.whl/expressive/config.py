""" Copyright 2025 Russell Fordyce

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from collections import UserDict
from copy import deepcopy
from difflib import get_close_matches

import numpy
import sympy

from .messaging import warn


class UNSET:

    def __repr__(self):
        return "UNSET"

    def __deepcopy__(self, memo):
        # help maintain singleton as deepcopy will return the same object for `is` equality
        return self

    def __eq__(self, other):
        raise TypeError("compare instances with is, not ==")


# somewhat-dirty clobber name to help prevent new instances from accidentally being created
# NOTE new instances can still be created via `type(UNSET)()`
UNSET = UNSET()

# don't modify this directly, instead write to CONFIG
_CONFIG_DEFAULTS = {
    # warnings
    #   TODO consider if warnings should be in their namespaces or centralized?
    #   it's possible to do both and have some preference, but that also seems hellish

    # translate_simplify.parse
    # there's surely some global parsing choices that make sense for certain applications
    #   should `^` be translated to `**` Pow() or bitwise OR
    #   also warning about this (should there be a warning block?)

    # Sum() features
    # `Sum() is expressly an unevaluated summation
    # set to False to prevent this path, which first tries summation and may do other
    # simplifications on the inner function, always converting to a dedicated
    # function which loops over the given range, which may have symbolic (start,end)
    #
    # many `Sum()` instances can be converted to expressions, potentially avoiding a loop
    # of unknown length, such as here (where the range is not known in advance)
    #   >>> parse_expr("Sum(x, (x, a, b))").replace(Sum,summation)
    #  -a**2/2 + a/2 + b**2/2 + b/2
    # `Sum()` can always be replaced by `summation()`, which may produce a simpler expression
    # or the same or a simpler `Sum()` instance
    "translate_simplify.build.sum.try_algebraic_convert": True,
    # some simplifications result in a Piecewise, this controls if a resulting expr
    # which contains Piecewise is considered a successful simplification
    #   True   to immediately return and let the Piecewise be handled by a later
    #          `breakout_Piecewise_to_condition_block()` call
    #   False  result is ignored and continue to generate SumLoop
    "translate_simplify.build.sum.allow_piecewise_in_simplification": True,
    # warn users after N seconds if sum() simplification is taking an excessive amount of time
    # set the value
    #  - to some positive integer for a timeout in seconds
    #  - False to disable this and never spawn a thread
    #
    # as this spawns a new Thread, some users who are careful about their thread count
    # or are using some model that clashes with them may want to disable this
    # users can also simplify their `Sum()`s before passing them in
    # similarly, Windows users may find Thread generally problematic and wish to disable this
    # TODO this feels like it would be happier in a warnings meta-section
    # TODO this may make sense as part of a general simplifications thread or process
    #   (processes can be killed and benefit from `fork()`)
    "translate_simplify.build.sum.threaded_timeout_warn": 20,  # seconds, yes this is a huge default

    # data  # some data choices probably makes sense

    # per-instance builder settings
    # some autobuild tunables for users to disable the warnings
    "builder.autobuild.allow_autobuild": False,  # prefer never to autobuild
    "builder.autobuild.usage_warn_nag":  True,   # nag caller via warn() about using .build() instead
    # references specific to parallelization mode
    "builder.parallel_model.numba_parallel":    True,   # longer build times, but may improve performance
    "builder.parallel_model.allow_prange":      UNSET,  # decide based upon data ndim
    "builder.parallel_model.native_threadpool": False,  # FUTURE ignore numba parallelization

    # backend.numba
    # other backends?
    # perhaps .jit args
    #   "fastmath": True,
    #   "parallel": True,
    # needs for like distributing cached files on a network share?.. [ISSUE 24]
}

# mapper for renamed keys which returns a tuple
#  - noted key's new name
#  - new default hint: should be True, False, or a string hint
_RENAMED_KEYS_MAPPER = {
    "builder.allow_autobuild": ("builder.autobuild.allow_autobuild", "effectively the same default"),
}


class LegacyConfigMapper:

    def __init__(self, data_ref, constructed_path=""):
        self.data = data_ref
        self.constructed_path = constructed_path

    def __getitem__(self, key):
        constructed = f"{self.constructed_path}.{key}"
        try:
            return self.data[constructed]  # complete key match
        except KeyError:
            self.constructed_path = constructed
            return self

    def __setitem__(self, key, value):
        constructed = f"{self.constructed_path}.{key}"
        if constructed in self.data:  # only set when the key exists
            self.data[constructed] = value
            return
        raise KeyError(f"failed to set {constructed} (from {'key'}) to '{value}'")


def try_renamed_keys(key):
    """ see if user is referencing a key that's been renamed
        additionally hint if the default has changed
    """
    try:
        key_new, default_hint = _RENAMED_KEYS_MAPPER[key]
    except KeyError:  # key has not been renamed (normal path)
        return key
    # key has been renamed and might have a new default

    # basic message or embed extra details
    default_hint = "" if default_hint is None else f"({default_hint}) "
    warn(f"renamed key '{key}' is now '{key_new}' {default_hint} and may be removed in a future version")

    return key_new


# NOTE this is an unstable API for now which might change between versions
class ConfigWrapper(UserDict):  # FIXME is this still required to override methods vs subclassing dict?
    """ wrapper for config which can inject warnings and handle the legacy layout
         - key types (must be str)
         - keys flattened (originally a nested dict from v2.2.0)
         - schema checking (FUTURE)
        additionally, user can display all keys with `.display()`
    """
    def __init__(self, config=None):
        self._setup = True  # allow arbitrary setitem during
        # opportunity for users to create/control their own wrapped configs
        if config is None:
            # FUTURE consider a reset feature, though that seems like overkill
            config = deepcopy(_CONFIG_DEFAULTS)
        super().__init__(config)
        # self._config_default = config  # FUTURE consider option to reset
        self._setup = False

    def __getitem__(self, key):  # FUTURE `__getitem__(self, key, /)` when dropping 3.7 support
        # special-case keys used in the legacy nested config
        if key in {"warnings", "translate_simplify", "backend"}:
            warn("all keys must be flattened and dot-separated, legacy key retrieval will be removed in a future version")
            legacy_config = LegacyConfigMapper(self.data, key)
            return legacy_config
        if "." not in key:
            raise ValueError("all keys must be flattened and dot-separated")
        key = try_renamed_keys(key)
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError(f"keys must be str, but got {type(key)}:{repr(key)}")
        key = try_renamed_keys(key)
        if not self._setup and key not in self.data.keys():
            # try to get a key that's pretty close
            # 0.3 picked because it works for TestConfig.test_bad
            # the most-similar string will be first
            keys_partialmatch = get_close_matches(key, self.data.keys(), n=1, cutoff=0.3)  # list of strings or []
            block_partialmatch = "" if not keys_partialmatch else f"did you mean '{keys_partialmatch[0]}'? "
            raise KeyError(f"unknown key '{key}', {block_partialmatch}enumerate all keys with .display() or see config.py")
        # TODO opportunity for a full schema checker
        return super().__setitem__(key, value)

    def display(self):
        """ unstable API """
        keys = sorted(self.data.keys())
        width = max(len(k) for k in keys)  # get width to pad output
        return "\n".join(f"{key.ljust(width)} = {self.data[key]}" for key in keys)


# immediately use a wrapper to warn user about changes from 3.x
CONFIG = ConfigWrapper()


DTYPES_SUPPORTED = {
    # numpy.dtype("bool"):     1,
    numpy.dtype("uint8"):    8,
    numpy.dtype("uint16"):  16,
    numpy.dtype("uint32"):  32,
    numpy.dtype("uint64"):  64,
    numpy.dtype("int8"):     8,
    numpy.dtype("int16"):   16,
    numpy.dtype("int32"):   32,
    numpy.dtype("int64"):   64,
    numpy.dtype("float32"): 32,
    numpy.dtype("float64"): 64,
    # numpy.dtype("float128"): 128,  # not supported in Numba [ISSUE 65]
    numpy.dtype("complex64"):   64,
    numpy.dtype("complex128"): 128,
    # numpy.dtype("complex256"): 256,
}

# determine a sensible fill value when creating a result array
# only called when
#  - using indexing (indexers exists)
#  - result array wasn't passed (whatever content it has is used)
# see also DTYPES_SUPPORTED
DTYPES_FILLER_HINT = {
    # numpy.dtype("bool"):,  # FUTURE (probably fail hard and force filling)
    numpy.dtype("uint8"):  0,
    numpy.dtype("uint16"): 0,
    numpy.dtype("uint32"): 0,
    numpy.dtype("uint64"): 0,
    numpy.dtype("int8"):  -1,
    numpy.dtype("int16"): -1,
    numpy.dtype("int32"): -1,
    numpy.dtype("int64"): -1,
    numpy.dtype("float32"): numpy.nan,
    numpy.dtype("float64"): numpy.nan,
    numpy.dtype("complex64"):  numpy.nan,
    numpy.dtype("complex128"): numpy.nan,
}

# SymPy floating-point Atoms
SYMPY_ATOMS_FP = (
    # straightforward floats
    sympy.Float,
    # trancendental constants
    sympy.pi,
    sympy.E,
    # FUTURE general scipy.constants support
    # common floating-point functions
    sympy.log,
    sympy.exp,
    # sympy.sqrt,  # NOTE simplifies to Pow(..., Rational(1,2))
    # sympy.cbrt,  #   can be found with expr.match(cbrt(Wild('a')))
    # trig functions
    sympy.sin, sympy.asin, sympy.sinh, sympy.asinh,
    sympy.cos, sympy.acos, sympy.cosh, sympy.acosh,
    sympy.tan, sympy.atan, sympy.tanh, sympy.atanh,
    sympy.cot, sympy.acot, sympy.coth, sympy.acoth,
    sympy.sec, sympy.asec, sympy.sech, sympy.asech,
    sympy.csc, sympy.acsc, sympy.csch, sympy.acsch,
    sympy.sinc,
    sympy.atan2,
    # LambertW?  # FUTURE results in float or complex result [ISSUE 107]
)

SYMPY_ATOMS_PROMOTE = (
    sympy.Pow,  # at least promotes int32 -> int64
)
