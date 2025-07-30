from contextlib import contextmanager

@contextmanager
def optional_dependencies():
    try:
        yield None
    except ImportError as e:
        msg = f'La librería "{e.name}" no se incluye como dependencia por defecto. \
                Intentar: poetry add {e.name} | pip install {e.name}'
        raise ImportError(msg)