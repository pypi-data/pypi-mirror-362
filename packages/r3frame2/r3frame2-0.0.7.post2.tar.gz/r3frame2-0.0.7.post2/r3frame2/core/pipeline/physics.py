from ..atom import R3atom, R3private
from ..status import R3status
from ..log import R3logger
from ..utils import sub_v2, norm_v2, mag_v2, equal_arrays
import r3frame2 as r3

class R3physics(R3atom):
    def __init__(
            self,
            app: "r3.app.R3app",
            world: "r3.resource.R3world",
    ) -> None:
        super().__init__()
        self._meta: dict = {
            "_count": 0,
        }

        self.damp_value = 4
        self.damp_threshold = 0.8
        
        self.app: r3.app.R3app = app
        self.world: r3.resource.R3world = world
        self.database: r3.resource.R3database = app.database
        
        self._command_buffer_max: int = 16
        self.transform_data: dict[r3.resource.R3entity, list] = { k: v for k,v in self._meta.items() }
        self.collision_data: dict[r3.resource.R3entity, r3.resource.R3aabb] = { k: v for k,v in self._meta.items() }
        
        self._freeze()

    @R3private
    def _valid_entity(self, cache: dict, entity: "r3.resource.R3entity") -> int:
        if not isinstance(entity, r3.resource.R3entity):
            return R3status.physics.ENTITY_INVALID
        if not cache.get(entity, 0):
            return R3status.physics.ENTITY_NOT_FOUND
        else: return R3status.physics.ENTITY_FOUND


    def toggle_transform(self, entity: "r3.resource.R3entity") -> int:
        if self._valid_entity(self.transform_data, entity) == R3status.physics.ENTITY_FOUND:
            self.transform_data.pop(entity)
            R3logger.debug(f"[R3physics] toggled entity physics off: (entity){entity.tag}")
            return R3status.physics.ENTITY_FOUND
        elif self._valid_entity(self.transform_data, entity) == R3status.physics.ENTITY_NOT_FOUND:
            self.transform_data[entity] = [entity, [0.0, 0.0], [], self.world.cell_transform(entity.pos), self.world.node_transform(entity.pos)]
            R3logger.debug(f"[R3physics] toggled entity physics on: (entity){entity.tag}")
            return R3status.physics.ENTITY_FOUND
        else:
            R3logger.error(f"[R3physics] entity not found: (entity){entity.tag}")
            return R3status.physics.ENTITY_NOT_FOUND

    def toggle_collision(self, entity: "r3.resource.R3entity", pos: list[int] = None, size: list[int] = None) -> int:
        if self._valid_entity(self.collision_data, entity) == R3status.physics.ENTITY_FOUND:
            self.database.unload_aabb(f"{entity.tag}.aabb")
            self.collision_data.pop(entity)
            R3logger.debug(f"[R3physics] toggled entity collision off: (entity){entity.tag}")
            return R3status.physics.ENTITY_FOUND
        elif self._valid_entity(self.collision_data, entity) == R3status.physics.ENTITY_NOT_FOUND:
            if not isinstance(pos, list) or not isinstance(size, list):
                self.database.unload_aabb(f"{entity.tag}.aabb")
                return R3status.physics.ENTITY_NOT_FOUND

            self.database.load_aabb(f"{entity.tag}.aabb", entity, pos, size)
            self.collision_data[entity] = [entity, self.database.query_aabb(f"{entity.tag}.aabb")]
            R3logger.debug(f"[R3physics] toggled entity collision on: (entity){entity.tag}")
            return R3status.physics.ENTITY_FOUND
        else:
            R3logger.error(f"[R3physics] entity not found: (entity){entity.tag}")
            return R3status.physics.ENTITY_NOT_FOUND


    def get_velocity(self, entity: "r3.resource.R3entity") -> list[float]:
        if self._valid_entity(self.transform_data, entity) != R3status.physics.ENTITY_FOUND:
            R3logger.error(f"[R3physics] entity not found: (entity){entity.tag}")
            return
        else: return self.transform_data[entity][1][0]

    def get_direction(self, entity: "r3.resource.R3entity") -> list[float]:
        if self._valid_entity(self.transform_data, entity) != R3status.physics.ENTITY_FOUND:
            R3logger.error(f"[R3physics] entity not found: (entity){entity.tag}")
            return
        else: return [(self.transform_data[entity][1][0] > 0) - (self.transform_data[entity][1][0] < 0),
                      (self.transform_data[entity][1][1] > 0) - (self.transform_data[entity][1][1] < 0)]


    def move_to(self, entity: "r3.resource.R3entity", pos: list[int|float], speed: int|float, stop: int|float = 4.0, flush: bool = True, center: bool = True) -> None:
        if not self._valid_entity(self.transform_data, entity): return
        if len(self.transform_data[entity][2]) == self._command_buffer_max: return
        if not isinstance(speed, (int, float)): return
        if not isinstance(stop, (int, float)): return
        if not isinstance(pos, list): return
        
        if flush: self.transform_data[entity][2].clear()

        self.transform_data[entity][2].append([speed, pos, stop, center])

    def set_velocity(self, entity: "r3.resource.R3entity", dx: int|float = None, dy: int|float = None) -> None:
        if self._valid_entity(self.transform_data, entity) != R3status.physics.ENTITY_FOUND:
            R3logger.error(f"[R3physics] entity not found: (entity){entity.tag}")
        else:
            if dx is not None: self.transform_data[entity][1][0] = dx
            if dy is not None: self.transform_data[entity][1][1] = dy


    # TODO: SAABB narrow-phase rejection filter
    # TODO: TOI resolver (Ray vs AABB / Minkowski Difference)
    @R3private
    def _aabbx(self, entity: "r3.resource.R3entity") -> bool:
        if self._valid_entity(self.collision_data, entity) != R3status.physics.ENTITY_FOUND:
            return
        vel = self.transform_data[entity][1]
        a1 = self.collision_data[entity][1]
        r1 = a1.rect
        for entity2 in self.world.partition.query_neighbor_nodes(entity.pos):
            if entity2 == entity: continue
            if self._valid_entity(self.collision_data, entity2) != R3status.physics.ENTITY_FOUND:
                continue
            a2 = self.collision_data[entity2][1]
            if r1.colliderect(a2.rect):
                if vel[0] > 0:
                    r1.right = a2.rect.left
                    entity.pos[0] = r1.x + (a2.rect.left - r1.right)
                elif vel[0] < 0:
                    r1.left = a2.rect.right
                    entity.pos[0] = r1.x + (a2.rect.right - r1.left)
                vel[0] = 0

    @R3private
    def _aabby(self, entity: "r3.resource.R3entity") -> bool:
        if self._valid_entity(self.collision_data, entity) != R3status.physics.ENTITY_FOUND:
            return
        vel = self.transform_data[entity][1]
        a1 = self.collision_data[entity][1]
        r1 = a1.rect
        for entity2 in self.world.partition.query_neighbor_nodes(entity.pos):
            if entity2 == entity: continue
            if self._valid_entity(self.collision_data, entity2) != R3status.physics.ENTITY_FOUND:
                continue
            a2 = self.collision_data[entity2][1]
            if r1.colliderect(a2.rect):
                if vel[1] < 0:
                    r1.bottom = a2.rect.top
                    entity.pos[1] = r1.y + (a2.rect.bottom - r1.top)
                elif vel[1] > 0:
                    r1.top = a2.rect.bottom
                    entity.pos[1] = r1.y + (a2.rect.top - r1.bottom)
                vel[1] = 0


    @R3private
    def update(self, dt: float) -> None:
        entities = tuple(self.transform_data[e] for e in self.transform_data if e not in self._meta)
        for entity, vel, cmds, cell, node in entities:
            if len(cmds) > 0:   # evaluate the "move to" command buffer
                speed, pos, stop, center = cmds[0]
                
                diff = sub_v2(pos, entity.center if center else entity.pos)
                direction = norm_v2(diff)
                dist = mag_v2(diff)
                
                if int(dist) <= int(stop):
                    cmds.pop(0)
                else:
                    dirx, diry = direction
                    vel[0] = dirx * speed
                    vel[1] = diry * speed

            vel[0] *= (1 - self.damp_value * dt)
            vel[1] *= (1 - self.damp_value * dt)

            if abs(self.transform_data[entity][1][0]) < self.damp_threshold: vel[0] = 0
            if abs(self.transform_data[entity][1][1]) < self.damp_threshold: vel[1] = 0

            entity.pos[0] += vel[0] * dt
            self._aabbx(entity)
            entity.pos[1] += vel[1] * dt
            self._aabby(entity)
            
            # partition updates
            new_node = self.world.node_transform(entity.pos)
            if new_node and not equal_arrays(node, new_node):
                self.transform_data[entity][4] = new_node
                new_cell = self.world.cell_transform(entity.pos)
                if new_cell and not equal_arrays(cell, new_cell):
                    self.transform_data[entity][3] = new_cell
                
                # TODO: refactor partition insertion/removal logic to accept
                # position as a param for elimination of the try/except block
                try:
                    self.world.partition.cells[cell][node].remove(entity)
                except: pass
                self.world.partition.insert(entity)
