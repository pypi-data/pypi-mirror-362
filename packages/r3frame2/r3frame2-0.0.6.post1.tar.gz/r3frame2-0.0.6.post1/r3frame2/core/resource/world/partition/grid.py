from ....atom import R3atom
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
        self.cells: dict[tuple[int], dict[tuple[int], list[r3.resource.R3entity]]] = {}
        
        self.size: list[int] = [*map(int, grid_size)]
        self.width: int = self.size[0]
        self.height: int = self.size[1]
        self.area: int = self.width * self.height

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
        if entity.pos[0] >= self.size_raw[0] or entity.pos[1] >= self.size_raw[1]: return
        
        cell_pos = self.cell_transform(entity.pos)
        node_pos = self.node_transform(entity.pos)
        
        cell = self.cells.get(cell_pos, None)
        if cell is None:
            self.cells[cell_pos] = {}
            cell = self.cells[cell_pos]

        node = cell.get(node_pos, None)
        if node is None:
            cell[node_pos] = []
            node = cell[node_pos]

        if entity in node: return
        node.append(entity)
    
    def remove(self, entity: "r3.resource.R3entity") -> None:
        if entity.pos[0] >= self.size_raw[0] or entity.pos[1] >= self.size_raw[1]: return

        cell = self.cells.get(self.cell_transform(entity.pos), None)
        if cell is None: return
        
        node = cell.get(self.node_transform(entity.pos), None)
        if node is None: return

        if entity in node: node.remove(entity)

    def query_node(self, pos: list[int|float]):
        if pos[0] >= self.size_raw[0] or pos[1] >= self.size_raw[1]: return tuple()

        cell = self.cells.get(self.cell_transform(pos), None)
        if cell is None: return tuple()
        
        node = cell.get(self.node_transform(pos), None)
        if node is None: return tuple()
        
        for entity in node: yield entity
    
    def query_neighbor_nodes(self, pos: list[int | float]):
        wx, wy = pos
        if wx >= self.size_raw[0] or wy >= self.size_raw[1]: return

        query = []
        cx, cy = self.cell_transform(pos)
        nx, ny = self.node_transform(pos)

        for dy in range(-1, 2, 1):
            for dx in range(-1, 2, 1):
                qnx = nx + dx
                qny = ny + dy
                qcx = cx
                qcy = cy

                if qnx < 0:
                    qcx -= 1
                    qnx = self.cell_width - 1
                elif qnx >= self.cell_width:
                    qcx += 1
                    qnx = 0

                if qny < 0:
                    qcy -= 1
                    qny = self.cell_height - 1
                elif qny >= self.cell_height:
                    qcy += 1
                    qny = 0

                cell = self.cells.get((qcx, qcy), None)
                if cell is None: continue

                node = cell.get((qnx, qny), None)
                if node is None: continue

                for entity in node: yield entity

    def query_node_region(self, pos: list[int | float], size: list[int | float]):
        wx, wy = pos
        if wx >= self.size_raw[0] or wy >= self.size_raw[1]: return

        query = []
        cx0, cy0 = self.cell_transform(pos)
        cx1, cy1 = self.cell_transform(add_v2(pos, size))
        nx0, ny0 = self.node_transform(pos)
        nx1, ny1 = self.node_transform(add_v2(pos, size))

        for cy in range(cy0, cy1 + 1):
            for cx in range(cx0, cx1 + 1):
                cell = self.cells.get((cx, cy), None)
                if cell is None: continue

                for ny in range(self.cell_height):
                    for nx in range(self.cell_width):
                        ax = cx * self.cell_width + nx
                        ay = cy * self.cell_height + ny
                        if ax < nx0 or ax > nx1 or ay < ny0 or ay > ny1: continue

                        node = cell.get((nx, ny), None)
                        if node is None: continue
                        
                        for entity in node: yield entity

    def query_cell(self, pos: list[int|float]):
        if pos[0] >= self.size_raw[0] or pos[1] >= self.size_raw[1]: return tuple()

        cell = self.cells.get(self.cell_transform(pos), None)
        if cell is None: return tuple()
        
        for node in cell:
            for entity in cell[node]:
                yield entity

    def query_neighbor_cells(self, pos: list[int|float]):
        wx, wy = pos
        if wx >= self.size_raw[0] or wy >= self.size_raw[1]: return
        
        query = []
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
        wx, wy = pos
        if wx >= self.size_raw[0] or wy >= self.size_raw[1]: return

        query = {}
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

