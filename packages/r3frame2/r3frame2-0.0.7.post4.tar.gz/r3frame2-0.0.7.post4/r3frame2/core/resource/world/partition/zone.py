from ....atom import R3atom
from ....utils import div2_v2i, div_v2i, sub_v2, add_v2, mul_v2
import r3frame2 as r3

class R3zonePartition(R3atom):
    def __init__(
            self,
            cell_size: list[int] = [32, 32],
            zone_size: list[int] = [16, 16],
            zone_origin: list[int] = [0, 0]
    ) -> None:
        self.zone_origin: list[int] = [*map(int, zone_origin)]

        self.cell_width: int = int(cell_size[0])
        self.cell_height: int = int(cell_size[1])
        self.cell_size: list[int] = [*map(int, cell_size)]
        self.cell_area: int = self.cell_size[0] * self.cell_size[1]
        
        self.zone_width: int = int(cell_size[0] * zone_size[0])
        self.zone_height: int = int(cell_size[1] * zone_size[1])
        self.zone_size: list[int] = [*map(int, mul_v2(zone_size, cell_size))]
        self.zone_area: int = self.zone_size[0] * self.zone_size[1]

        self.loaded_zones: set[tuple[int]] = set()
        self.zones: dict[tuple[int], dict[tuple[int], set[r3.resource.R3entity]]] = {}


    def get_zone(self, pos: list[int | float]) -> tuple[int]:
        return tuple(div2_v2i(sub_v2(pos, self.zone_origin), self.zone_size))

    def get_zone_region(self, pos: list[int | float], size: list[int | float], xdir: int = 0, ydir: int = 0) -> list[tuple[int]]:
        top_left = pos
        bottom_right = sub_v2(add_v2(pos, size), [1, 1])

        region = []
        grid_pos0 = div2_v2i(top_left, self.zone_size)
        grid_pos1 = div2_v2i(bottom_right, self.zone_size)
        for y in range(grid_pos0[1] - ydir, grid_pos1[1] + ydir + 1):
            for x in range(grid_pos0[0] - xdir, grid_pos1[0] + xdir + 1):
                region.append((x, y))
        return tuple(region)


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


    def load_zone(self, pos: tuple[int]) -> None:
        if pos in self.loaded_zones: return
        self.zones[pos] = {}
        self.loaded_zones.add(pos)

    def unload_zone(self, pos: tuple[int]) -> None:
        if pos not in self.loaded_zones: return
        del self.zones[pos]
        self.loaded_zones.remove(pos)


    def load_cell(self, pos: list[int]) -> None:
        zone_pos = self.get_zone(mul_v2(pos, self.cell_size))

        if zone_pos not in self.loaded_zones:
            self.load_zone(zone_pos)

        zone = self.zones.get(zone_pos, None)
        if zone is None: return
        
        if pos not in zone:
            zone[pos] = set()

    def unload_cell(self, pos: list[int]) -> None:
        zone_pos = self.get_zone(mul_v2(pos, self.cell_size))

        zone = self.zones.get(zone_pos)
        if zone and pos in zone:
            del zone[pos]
            if len(zone) == 0:
                self.unload_zone(zone_pos)


    def insert(self, entity: "r3.resource.R3entity") -> None:
        entity.spatial.clear()
        region = self.get_cell_region(entity.pos, entity.size)
        for cell_pos in region:
            zone_pos = self.get_zone(mul_v2(cell_pos, self.cell_size))

            if zone_pos not in self.loaded_zones:
                self.load_zone(zone_pos)

            zone = self.zones.get(zone_pos, None)
            if zone is None: continue

            if cell_pos not in zone: self.load_cell(cell_pos)

            cell = zone.get(cell_pos, None)
            if cell is None: continue

            if entity not in cell:
                cell.add(entity)
                entity.spatial.add(cell_pos)

    def remove(self, entity: "r3.resource.R3entity") -> None:
        for cell_pos in entity.spatial:
            zone_pos = self.get_zone(mul_v2(cell_pos, self.cell_size))

            if zone_pos not in self.loaded_zones:
                self.load_zone(zone_pos)
                self.load_cell(cell_pos)

            zone = self.zones.get(zone_pos, None)
            if zone is None: continue

            cell = zone.get(cell_pos, None)
            if cell is None: continue

            if entity in cell:
                cell.remove(entity)

            if len(cell) == 0: self.unload_cell(cell_pos)
            if len(zone) == 0: self.unload_zone(zone_pos)
        entity.spatial.clear()


    def query_zone(self, pos: list[int | float]) -> set["r3.resource.R3entity"]:
        zone = self.zones.get(self.get_zone(pos), {})

        query = set()
        for cell in zone.values():
            query.update(cell)
        return query
    
    def query_zone_region(self, pos: list[int | float], size: list[int | float], xdir: int = 2, ydir: int = 2) -> tuple[set["r3.resource.R3entity"]]:
        region = self.get_zone_region(pos, size, xdir, ydir)
        query = set()

        for zone_pos in region:
            zone = self.zones.get(zone_pos, None)
            if zone is None: continue

            for cell in zone.values():
                query.update(cell)
        return query


    def query_cell(self, pos: list[int | float]) -> set["r3.resource.R3entity"]:
        zone = self.zones.get(self.get_zone(pos), None)
        if zone is None: return None
        return zone.get(self.get_cell(pos), set())
    
    def query_cell_region(self, pos: list[int | float], size: list[int | float], xdir: int = 2, ydir: int = 2) -> tuple[set["r3.resource.R3entity"]]:
        region = self.get_cell_region(pos, size, xdir, ydir)
        query = set()

        for cell_pos in region:
            zone_pos = self.get_zone(cell_pos)
            zone = self.zones.get(zone_pos, None)
            if zone is None: continue

            cell = zone.get(cell_pos, None)
            if cell is None: continue

            query.update(cell)
        return query


    def update(self, entity: "r3.resource.R3entity") -> None:
        new_cell_region = set(self.get_cell_region(entity.pos, entity.size))
        old_cell_region = entity.spatial
        
        if new_cell_region == old_cell_region: return
        
        self.remove(entity)
        self.insert(entity)
