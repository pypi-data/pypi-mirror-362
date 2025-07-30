from ....atom import R3atom, R3private
from ....flags import R3flags
from ....log import R3logger
import r3frame2 as r3

class R3renderPhase(R3atom):
    def __init__(self, tag: str) -> None:
        super().__init__()
        self.tag: str = tag
        self.calls: list[r3.resource.R3renderCall] = list()
        self._freeze()

    @R3private
    def queue(self, call: "r3.resource.R3renderCall") -> None:
        if not isinstance(call, r3.resource.R3renderCall): return
        self.calls.append(call)

    @R3private
    def execute(self, renderer: "r3.pipeline.R3renderer") -> None:
        if not isinstance(renderer, r3.pipeline.R3renderer): return
        R3logger.error(f"[R3renderer] phase must implement `execute()` method: (tag){self.tag}")
        return

    @R3private
    def reset(self) -> None:
        self.calls.clear()
