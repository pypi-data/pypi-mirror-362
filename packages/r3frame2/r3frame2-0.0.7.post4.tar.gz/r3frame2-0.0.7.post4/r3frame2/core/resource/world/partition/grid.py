from ....atom import R3atom
from ....utils import div2_v2i, div_v2i, sub_v2, add_v2
import r3frame2 as r3

class R3gridPartition(R3atom):
    def __init__(
            self,
            cell_size: list[int],
            grid_origin: list[int] = [0, 0]
    ) -> None:
        self.grid_origin: list[int] = [*map(int, grid_origin)]

        self.cell_width: int = int(cell_size[0])
        self.cell_height: int = int(cell_size[1])
        self.cell_size: list[int] = [*map(int, cell_size)]
        self.cell_area: int = self.cell_size[0] * self.cell_size[1]

        self.loaded_cells: set[tuple[int]] = set()
        self.cells: dict[tuple[int], set[r3.resource.R3entity]] = {}

    def get_cell(self, pos: list[int | float]) -> tuple[int]:
        return tuple(div2_v2i(sub_v2(pos, self.zone_origin), self.cell_size))
    
    def get_cell_region(self, pos: list[int | float], size: list[int | float], xdir: int = 0, ydir: int = 0) -> list[tuple[int]]:
        top_left = pos
        bottom_right = sub_v2(add_v2(pos, size), [1, 1])

        region = []
        grid_pos0 = div2_v2i(top_left, self.cell_size)
        grid_pos1 = div2_v2i(bottom_right, self.cell_size)
        for y in range(grid_pos0[1] - ydir, grid_pos1[1] + ydir + 1):
            for x in range(grid_pos0[0] - xdir, grid_pos1[0] + xdir + 1):
                region.append((x, y))
        return tuple(region)

    def load_cell(self, pos: list[int]) -> None:
        if pos in self.loaded_cells: return
        self.cells[pos] = set()
        self.loaded_cells.add(pos)

    def unload_cell(self, pos: list[int]) -> None:
        if pos not in self.loaded_cells: return
        del self.cells[pos]
        self.loaded_cells.remove(pos)

    def insert(self, entity: "r3.resource.R3entity") -> None:
        region = self.get_cell_region(entity.pos, entity.size)
        entity.spatial.clear()
        for cell_pos in region:
            if cell_pos not in self.loaded_cells:
                self.load_cell(cell_pos)

            cell = self.cells[cell_pos]
            if entity in cell: continue
            
            cell.add(entity)
            entity.spatial.add(cell_pos)

    def remove(self, entity: "r3.resource.R3entity") -> None:
        for cell_pos in entity.spatial:
            cell = self.cells.get(cell_pos, None)
            if cell is None: continue

            if entity in cell:
                cell.remove(entity)

            if len(cell) == 0: self.unload_cell(cell_pos)
        entity.spatial.clear()

    def query_cell(self, pos: list[int | float]) -> set["r3.resource.R3entity"] | set[None]:
        return self.cells.get(self.get_cell(pos), None)

    def query_cell_region(self, pos: list[int | float], size: list[int | float], xdir: int = 2, ydir: int = 2) -> tuple[set["r3.resource.R3entity"]]:
        region = self.get_cell_region(pos, size, xdir, ydir)
        cells = set()
        for cell_pos in region:
            cell = self.cells.get(cell_pos, None)
            if cell: cells.update(cell)
        return cells

    def update(self, entity: "r3.resource.R3entity") -> None:
        new_region = set(self.get_cell_region(entity.pos, entity.size))
        old_region = entity.spatial

        if new_region == old_region: return
        self.remove(entity)
        self.insert(entity)
