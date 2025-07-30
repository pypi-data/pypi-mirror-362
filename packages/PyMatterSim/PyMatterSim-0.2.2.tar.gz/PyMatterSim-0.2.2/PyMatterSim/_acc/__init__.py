ENABLE_ACC = True
try:
    from . import acc
except ImportError as e:
    import warnings
    warnings.warn(
        f"Failed to load acceleration module 'acc', falling back to pure Python: {e}"
    )
    ENABLE_ACC = False
