import pkgutil, importlib, single as _single

def load_plugins():
    for m in pkgutil.iter_modules(_single.__path__):
        importlib.import_module(f"{_single.__name__}.{m.name}")
