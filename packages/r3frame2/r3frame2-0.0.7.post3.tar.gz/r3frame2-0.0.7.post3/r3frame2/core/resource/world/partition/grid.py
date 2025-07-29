from ....atom import R3atom, R3private
from ....globals import pg
from ....utils import div2_v2i, div_v2i, mul_v2, sub_v2, add_v2
import r3frame2 as r3

class R3gridPartition(R3atom):
    def __init__(
            self, world,
            pos: list[int],
            node_size: list[int],
            cell_size: list[int],
            grid_size: list[int],
            depth: int = 0,
        ) -> None:
        super().__init__()
        self.depth: int = depth
        self.world: r3.resource.R3world = world

        self.node_size: list[int] = [*map(int, node_size)]
        self.node_width: int = self.node_size[0]
        self.node_height: int = self.node_size[1]
        self.node_area: int = self.node_width * self.node_height

        self.cell_size: list[int] = [*map(int, cell_size)]
        self.cell_width: int = self.cell_size[0]
        self.cell_height: int = self.cell_size[1]
        self.cell_area: int = self.cell_width * self.cell_height
        
        # cells[cx, cy] = dict[tuple[int], list[R3entity]]
        # cells[cx, cy][nx, ny] = [entities...]
        self.loaded_cells: list[tuple[int]] = []
        self.cells: dict[tuple[int], dict[tuple[int], list[r3.resource.R3entity]]] = {}
        
        self.size: list[int] = [*map(int, grid_size)]
        self.width: int = self.size[0]
        self.height: int = self.size[1]
        self.area: int = self.width * self.height
        if self.size[0] > 0 and self.size[1] > 0:
            for cy in range(self.height):
                for cx in range(self.width):
                    cell_pos = (cx, cy)
                    self.cells[cell_pos] = {}
                    self.loaded_cells.append(cell_pos)
        
        self.cell_size_raw: list[int] = mul_v2(self.cell_size, self.node_size)
        self.size_raw: list[int] = mul_v2(self.cell_size_raw, self.size)
        
        self.pos: list[int] =  [*map(int, pos)]
        self.x: int = self.pos[0]
        self.y: int = self.pos[1]
        self.center: list[int] = add_v2(self.pos, div_v2i(self.size, 2))

        self._freeze()

    def cell_transform(self, pos: list[int|float]) -> tuple[int, int]:
        cell_pos = div2_v2i(sub_v2(pos, self.pos), mul_v2(self.cell_size, self.node_size))
        return tuple(cell_pos)
    
    def node_transform(self, pos: list[int|float]) -> tuple[int, int]:
        node_pos = div2_v2i(sub_v2(pos, self.pos), self.node_size)
        return tuple(node_pos)

    def insert(self, entity: "r3.resource.R3entity") -> None:
        cell_pos = self.cell_transform(entity.pos)
        node_pos = self.node_transform(entity.pos)

        if cell_pos not in self.cells:
            self.cells[cell_pos] = {}
            self.loaded_cells.append(cell_pos)

        cell = self.cells[cell_pos]

        if node_pos not in cell:
            cell[node_pos] = []

        node = cell[node_pos]
        if entity not in node:
            node.append(entity)

    @R3private
    def _insert(self, entity: "r3.resource.R3entity", cell_pos: list[int], node_pos: list[int]) -> None:
        if cell_pos not in self.cells:
            self.cells[cell_pos] = {}
            self.loaded_cells.append(cell_pos)

        cell = self.cells[cell_pos]

        if node_pos not in cell: cell[node_pos] = []

        node = cell[node_pos]
        if entity not in node:
            node.append(entity)

    @R3private
    def _remove(self, entity: "r3.resource.R3entity", cell_pos: list[int], node_pos: list[int]) -> None:
        if cell_pos[0] >= self.cell_size[0] or cell_pos[1] >= self.cell_size[1]\
        or node_pos[0] >= self.node_size[0] or node_pos[1] >= self.node_size[1]: return

        cell = self.cells[cell_pos]
        node = cell[node_pos]

        if entity in node:
            node.remove(entity)
            if not node:  # node empty
                del cell[node_pos]
            if not cell:  # cell empty
                del self.cells[cell_pos]
                if cell_pos in self.loaded_cells:
                    self.loaded_cells.remove(cell_pos)

    def remove(self, entity: "r3.resource.R3entity") -> None:
        if entity.pos[0] >= self.size_raw[0] or entity.pos[1] >= self.size_raw[1]: return

        cell_pos = self.cell_transform(entity.pos)
        node_pos = self.node_transform(entity.pos)

        cell = self.cells.get(cell_pos, None)
        if cell is None: return

        node = cell.get(node_pos, None)
        if node is None: return

        if entity in node:
            node.remove(entity)
            if not node:  # node empty
                del cell[node_pos]
            if not cell:  # cell empty
                del self.cells[cell_pos]
                if cell_pos in self.loaded_cells:
                    self.loaded_cells.remove(cell_pos)

    def query_node(self, pos: list[int|float]):
        if pos[0] >= self.size_raw[0] or pos[1] >= self.size_raw[1]: return tuple()

        cell = self.cells.get(self.cell_transform(pos), None)
        if cell is None: return tuple()
        
        node = cell.get(self.node_transform(pos), None)
        if node is None: return tuple()
        
        for entity in node: yield entity
        
    def query_neighbor_nodes(self, pos: list[int | float]):
        if pos[0] >= self.size_raw[0] or pos[1] >= self.size_raw[1]:
            return

        cx, cy = self.cell_transform(pos)
        nx, ny = self.node_transform(pos)

        cell = self.cells.get((cx, cy), None)
        if cell is None: return

        for dy in range(-1, 2):
            for dx in range(-1, 2):
                npos = (nx + dx, ny + dy)
                node = cell.get(npos, None)
                if node is None: continue

                for entity in node: yield entity

    def query_node_region(self, pos: list[int | float], size: list[int | float]):
        if pos[0] >= self.size_raw[0] or pos[1] >= self.size_raw[1]:
            return

        pos_end = add_v2(pos, size)

        cx0, cy0 = self.cell_transform(pos)
        cx1, cy1 = self.cell_transform(pos_end)

        for cy in range(cy0, cy1 + 1):
            for cx in range(cx0, cx1 + 1):
                cell = self.cells.get((cx, cy), None)
                if cell is None:
                    continue

                cell_world_pos = add_v2(self.pos, mul_v2([cx, cy], self.cell_size_raw))
                local_pos = sub_v2(pos, cell_world_pos)
                local_end = sub_v2(pos_end, cell_world_pos)

                nx0, ny0 = div2_v2i(local_pos, self.node_size)
                nx1, ny1 = div2_v2i(local_end, self.node_size)

                for ny in range(ny0, ny1 + 1):
                    for nx in range(nx0, nx1 + 1):
                        node = cell.get((nx, ny), None)
                        if node is None:
                            continue
                        for entity in node:
                            yield entity

    def query_cell(self, pos: list[int|float]):
        if pos[0] >= self.size_raw[0] or pos[1] >= self.size_raw[1]: return tuple()

        cell = self.cells.get(self.cell_transform(pos), None)
        if cell is None: return tuple()
        
        for node in cell:
            for entity in cell[node]:
                yield entity

    def query_neighbor_cells(self, pos: list[int|float]):
        if pos[0] >= self.size_raw[0] or pos[1] >= self.size_raw[1]: return
        
        cx, cy = self.cell_transform(pos)
        for dy in range(-1, 2, 1):
            for dx in range(-1, 2, 1):
                qpos = (dx + cx, dy + cy)
                cell = self.cells.get(qpos, None)
                if cell is None: continue

                for node in cell:
                    for entity in cell[node]:
                        yield entity
    
    def query_cell_region(self, pos: list[int | float], size: list[int | float]):
        if pos[0] >= self.size_raw[0] or pos[1] >= self.size_raw[1]: return

        cx0, cy0 = self.cell_transform(pos)
        cx1, cy1 = self.cell_transform(add_v2(pos, size))
        for cy in range(cy0, cy1 + 1):
            for cx in range(cx0, cx1 + 1):
                cell_pos = (cx, cy)
                cell = self.cells.get(cell_pos, None)
                if cell is None: continue

                for node in cell:
                    for entity in cell[node]:
                        yield entity

