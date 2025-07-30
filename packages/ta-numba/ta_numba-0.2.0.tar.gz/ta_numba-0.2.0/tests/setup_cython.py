from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy

# Aggressive compiler optimization flags
extra_compile_args = [
    "-O3",                    # Maximum optimization
    "-ffast-math",           # Fast math operations (trade precision for speed)
    "-march=native",         # Optimize for current CPU architecture
    "-mtune=native",         # Tune for current CPU
    "-funroll-loops",        # Unroll loops for better performance
    "-fomit-frame-pointer",  # Omit frame pointer for extra register
    "-DNDEBUG",              # Disable debug assertions
    "-msse2",                # Enable SSE2 instructions
    "-msse3",                # Enable SSE3 instructions
    "-mssse3",               # Enable SSSE3 instructions
    "-msse4.1",              # Enable SSE4.1 instructions
    "-msse4.2",              # Enable SSE4.2 instructions
    "-mavx",                 # Enable AVX instructions if available
    "-mavx2",                # Enable AVX2 instructions if available
    "-fno-strict-aliasing",  # Avoid strict aliasing optimizations that can break
]

# Link-time optimization flags
extra_link_args = [
    "-O3",
    "-flto",                 # Link-time optimization
]

extensions = [
    Extension(
        "cython_indicators",
        ["cython_indicators.pyx"],
        include_dirs=[numpy.get_include()],
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
        define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")],  # Suppress numpy warnings
    )
]

setup(
    ext_modules = cythonize(
        extensions,
        compiler_directives={
            "language_level": 3,           # Use Python 3
            "boundscheck": False,          # Disable bounds checking
            "wraparound": False,           # Disable negative index wrapping
            "initializedcheck": False,     # Disable initialization checking
            "cdivision": True,             # Use C division (faster)
            "nonecheck": False,            # Disable None checking
            "overflowcheck": False,        # Disable overflow checking
            "embedsignature": False,       # Don't embed function signatures
            "optimize.use_switch": True,   # Use switch statements for optimization
            "optimize.unpack_method_calls": True,  # Optimize method calls
        },
        annotate=True,  # Generate HTML annotation files to see C code
    ),
    zip_safe=False,
)