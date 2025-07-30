from .globals import inspect
from .log import R3logger

def R3private(func):
    def wrapper(*args, **kwargs):
        caller = inspect.stack()[1].frame.f_globals.get("__name__")
        if not caller.startswith("r3frame2."):
            R3logger.warning(f"Internal Method, cannot call `{func.__name__}`: (caller){caller}")
            return
        return func(*args, **kwargs)
    return wrapper

class R3atom:
    def __init__(self) -> None:
        self._uid: int = id(self)
        self._flags: int = 0
        self._frozen: bool = 0
        
    def __setattr__(self, name, value):
        if hasattr(self, "_frozen"):
            if getattr(self, "_frozen") == 1:
                caller = inspect.stack()[1].frame.f_globals.get("__name__")
                if not caller.startswith("r3frame2."):
                    raise AttributeError("[R3atom] ERROR: attempted so mutate immutible object")
                else: return super().__setattr__(name, value)
            else: return super().__setattr__(name, value)
        else: return super().__setattr__(name, value)

    @property
    def flags(self) -> int:
        return self._flags
    
    @property
    def uid(self) -> int:
        return self._uid

    @R3private
    def _freeze(self) -> None:
        if self._frozen == 1: return
        else: self._frozen = 1

    @R3private
    def _unfreeze(self) -> None:
        if self._frozen == 0: return
        else: self._frozen = 0

    def swap_flag(self, rem: int, set: int) -> None:
        self.rem_flag(rem)
        self.set_flag(set)

    def set_flag(self, flag: int) -> None:
        if flag < 0 or not isinstance(flag, int): return
        self._unfreeze()
        self._flags |= flag
        self._freeze()

    def get_flag(self, flag: int) -> bool:
        if flag < 0 or not isinstance(flag, int): return
        return ((self._flags & flag) == flag)

    def rem_flag(self, flag: int) -> None:
        if flag < 0 or not isinstance(flag, int): return
        self._unfreeze()
        self._flags &= ~flag
        self._freeze()
