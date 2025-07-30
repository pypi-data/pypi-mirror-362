import sys
import types
import logging
import pkgutil
from importlib import import_module
from typing import Set, Optional, Union


class LazyModuleLoader:
    """
    A utility to lazily load submodules and avoid circular imports.

    Parameters
    ----------
    parent_module : str
        The fully qualified name of the module (e.g., 'is_matrix_forge.led_matrix').

    submodules : Optional[Set[str]]
        A set of submodules to lazily load. If not provided, it will be auto-discovered.

    fallback_module : Optional[str]
        Optional fallback module to delegate attribute lookups to.

    enable_logging : bool
        Enable logging for import errors.
    """

    def __init__(
        self,
        parent_module: str,
        submodules: Optional[Set[str]] = None,
        fallback_module: Optional[str] = None,
        enable_logging: bool = True
    ):
        self.module_name = parent_module
        self.submodules = submodules or self._discover_submodules()
        self.fallback_module = fallback_module
        self.enable_logging = enable_logging
        self.logger = logging.getLogger(__name__)
        self._install()

    def _discover_submodules(self) -> Set[str]:
        try:
            module = import_module(self.module_name)
            path = module.__path__
            return {name for _, name, is_pkg in pkgutil.iter_modules(path)}
        except Exception as e:
            if self.enable_logging:
                self.logger.error(f"Error discovering submodules for '{self.module_name}': {e}")
            return set()

    def _install(self):
        mod = sys.modules[self.module_name]
        mod.__getattr__ = self.__getattr__
        mod.__dir__ = self.__dir__
        mod.__all__ = sorted(self.submodules)

    def __getattr__(self, name):
        if name in self.submodules:
            try:
                full_name = f"{self.module_name}.{name}"
                module = import_module(full_name)
                sys.modules[full_name] = module
                return module
            except ImportError as e:
                if self.enable_logging:
                    self.logger.error(f"Failed to import submodule '{name}': {e}")
                raise
        elif self.fallback_module:
            base = import_module(self.fallback_module)
            try:
                return getattr(base, name)
            except AttributeError as e:
                if self.enable_logging:
                    self.logger.error(
                        f"Fallback '{self.fallback_module}' has no attribute '{name}': {e}"
                    )
                raise
        else:
            raise AttributeError(f"Module '{self.module_name}' has no attribute '{name}'")

    def __dir__(self):
        return sorted(set(sys.modules[self.module_name].__dict__) | self.submodules)

