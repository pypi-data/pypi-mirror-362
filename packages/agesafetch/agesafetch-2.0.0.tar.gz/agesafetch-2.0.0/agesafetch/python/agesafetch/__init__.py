"""
Re-export everything in the `agesafetch` module on the package's level.

The Python package name is "agesafetch", and since that just so happens
to be a directory in the workspace root (on account of this crate being
named the same), Maturin ≤ 1.8.3 detects a `mixed Rust/Python`_ project.

That, in turn, causes it to not generate its `default __init__.py`_, so
we need to create it ourselves to enable imports from just `agesafetch`.

.. _`default __init__.py`:
   https://www.maturin.rs/project_layout.html#pure-rust-project
.. _`mixed Rust/Python`:
   https://www.maturin.rs/project_layout.html#mixed-rustpython-project

SPDX-FileCopyrightText: Benedikt Vollmerhaus <benedikt@vollmerhaus.org>
SPDX-License-Identifier: MIT
"""
from .agesafetch import *

__doc__ = agesafetch.__doc__
if hasattr(agesafetch, '__all__'):
    __all__ = agesafetch.__all__
