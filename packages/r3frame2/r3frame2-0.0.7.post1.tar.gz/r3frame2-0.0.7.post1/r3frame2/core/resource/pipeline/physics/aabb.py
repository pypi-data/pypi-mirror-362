from ....atom import R3atom
from ....globals import pg
from ....utils import add_v2, div_v2, div2_v2
import r3frame2 as r3

# aabb data container
# R3database.aabb[key] -> R3aabb
class R3aabb(R3atom):
    def __init__(
            self,
            entity: "r3.resource.R3entity",
            pos: list[int] = [0, 0],
            size: list[int] = [32, 32],
    ) -> None:
        super().__init__()
        self.entity: "r3.resource.R3entity" = entity
        self.pos: list[int] = pos[:]
        self.size: list[int] = size[:]
        self._freeze()
    
    @property
    def rect(self) -> pg.Rect:
        return pg.Rect(add_v2(self.entity.pos, self.pos), self.size)

    @property
    def x(self) -> float:
        return self.entity.pos[0] + self.pos[0]
    @property
    def y(self) -> float:
        return self.entity.pos[1] + self.pos[1]
    
    @property
    def center_left(self) -> list[float]:
        return [(self.entity.pos[0] + self.pos[0]), (self.entity.pos[1] + self.pos[1]) + (self.size[1] / 2)]
    
    @property
    def center_right(self) -> list[float]:
        return [(self.entity.pos[0] + self.pos[0]) + self.size[0], (self.entity.pos[1] + self.pos[1]) + (self.size[1] / 2)]
    
    @property
    def center_top(self) -> list[float]:
        return [(self.entity.pos[0] + self.pos[0]) + (self.size[0] / 2), (self.entity.pos[1] + self.pos[1])]
    
    @property
    def center_bottom(self) -> list[float]:
        return [(self.entity.pos[0] + self.pos[0]) +  + (self.size[0] / 2), (self.entity.pos[1] + self.pos[1]) + self.size[1]]
    
    @property
    def top_left(self) -> float:
        return [(self.entity.pos[0] + self.pos[0]), (self.entity.pos[1] + self.pos[1])]
    
    @property
    def top_right(self) -> float:
        return [(self.entity.pos[0] + self.pos[0]) + self.size[0], (self.entity.pos[1] + self.pos[1])]
    
    @property
    def bottom_left(self) -> float:
        return [(self.entity.pos[0] + self.pos[0]), (self.entity.pos[1] + self.pos[1]) + self.size[1]]
    
    @property
    def bottom_right(self) -> float:
        return [(self.entity.pos[0] + self.pos[0]) + self.size[0], (self.entity.pos[1] + self.pos[1]) + self.size[1]]
    
    @property
    def width(self) -> float:
        return self.size[0]
    @property
    def height(self) -> float:
        return self.size[1]
    @property
    def area(self) -> float:
        return self.size[0] * self.size[1]
