from ....atom import R3atom
import r3frame2 as r3

class R3renderCall(R3atom):
    def __init__(
            self,
            mask: int,
            pos: list[float],
            surf: "r3.resource.R3surf",
            resource = None
        ) -> None:
        super().__init__()
        self.resource = resource

        self.mask: int = mask
        self.pos: list[float] = pos
        self.surf: r3.resource.R3surf = surf
        self._freeze()
