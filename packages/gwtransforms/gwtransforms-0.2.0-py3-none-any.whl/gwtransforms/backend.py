try:
    import jax.numpy as np
    from jax.typing import ArrayLike

    backend = "jax"
    ArrayT = ArrayLike
except ImportError:
    try:
        import autograd.numpy as np

        backend = "autograd"
    except ImportError:
        import numpy as np

        backend = "numpy"
    from numpy.typing import NDArray

    ArrayT = NDArray

HAS_JAX = backend == "jax"
HAS_AUTOGRAD = backend == "autograd"
HAS_AUTODIFF = HAS_JAX or HAS_AUTOGRAD

__all__ = ["np", "backend", "HAS_JAX", "HAS_AUTOGRAD", "HAS_AUTODIFF", "ArrayT"]
