project('sbmf', 'c', 'cython', version: '0.0.9')

# Find Python and required dependencies
py = import('python').find_installation(pure: false)
py_dep = py.dependency()

## Find numpy (taken from the sklearn and scipy build files)
incdir_numpy = meson.get_external_property('numpy-include-dir', 'not-given')
if incdir_numpy == 'not-given'
  incdir_numpy = run_command(py,
    [
      '-c',
      '''
import os
import numpy as np
try:
  incdir = os.path.relpath(np.get_include())
except Exception:
  incdir = np.get_include()
print(incdir)
'''
    ],
    check: true
  ).stdout().strip()
endif

inc_np = include_directories(incdir_numpy)
# Don't use the deprecated NumPy C API. Define this to a fixed version instead of
# NPY_API_VERSION in order not to break compilation for released SciPy versions
# when NumPy introduces a new deprecation.
numpy_no_deprecated_api = ['-DNPY_NO_DEPRECATED_API=NPY_1_9_API_VERSION']
np_dep = declare_dependency(include_directories: inc_np, compile_args: numpy_no_deprecated_api)

cython_args = ['-X boundscheck=False',
               '-X wraparound=False',
               '-X cdivision=True',
               '-X language_level=3']

# Build the extension module
py.extension_module('sparse',
                   'sbmf/sparse.pyx',
                   dependencies: [py_dep, np_dep],
                   install: true,
                   subdir: 'sbmf',
                   cython_args: cython_args)
