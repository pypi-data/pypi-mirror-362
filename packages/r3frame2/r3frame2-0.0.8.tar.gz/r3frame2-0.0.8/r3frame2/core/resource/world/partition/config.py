from ....atom import R3atom

class R3gridConfig(R3atom):
    def __init__(
        self,
        cell_size: list[int] = [32, 32],
        world_origin: list[int] = [0, 0]
    ) -> None:
        super().__init__()
        self.cell_size: list[int] = cell_size
        self.world_origin: list[int] = world_origin
        self._freeze()

class R3zoneConfig(R3atom):
    def __init__(
        self,
        cell_size: list[int] = [32, 32],
        zone_size: list[int] = [16, 16],
        world_origin: list[int] = [0, 0]
    ) -> None:
        super().__init__()
        self.cell_size: list[int] = cell_size
        self.zone_size: list[int] = zone_size
        self.world_origin: list[int] = world_origin
        self._freeze()
