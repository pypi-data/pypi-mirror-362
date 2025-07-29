from ...atom import R3atom
from ...globals import pg
from ...utils import div_v2i
import r3frame2 as r3

class R3world(R3atom):
    def __init__(
            self,
            node_size: list[int] = [32, 32],
            cell_size: list[int] = [16, 16],
            world_size: list[int] = [8, 8],
            world_origin: list[int] = [0, 0]
        ) -> None:
        super().__init__()
        self.ecs: r3.resource.R3ecs = r3.resource.R3ecs()

        self.node_size: list[int] = [*map(int, node_size)]
        self.cell_size: list[int] = [*map(int, cell_size)]
        
        self.size: list[int] = [*map(int, world_size)]
        self.width: int = self.size[0]
        self.height: int = self.size[1]
        self.area: int = self.width * self.height
        self.center: list[int] = div_v2i(self.size, 2)

        self.partition: r3.resource.R3gridPartition = r3.resource.R3gridPartition(self, world_origin, node_size, cell_size, world_size)
        self._freeze()
        
    def _write_to_disk(self) -> None: pass
    def _read_from_disk(self) -> None: pass

    def cell_transform(self, pos: list[int|float] = None) -> list[int]:
        return self.partition.cell_transform(pos)
    def node_transform(self, pos: list[int|float] = None) -> list[int]:
        return self.partition.node_transform(pos)

    def query(self, entity: "r3.resource.R3entity", pos: list[int|float] = None) -> tuple | None:
        return self.partition.query_node(entity.pos)
    
    def insert(self, entity: "r3.resource.R3entity", pos: list[int|float] = None) -> None:
        self.partition.insert(entity)
    def remove(self, entity: "r3.resource.R3entity", pos: list[int|float] = None) -> None:
        self.partition.remove(entity)
