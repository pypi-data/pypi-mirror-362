from ..atom import R3atom, R3private
from ..flags import R3flags
from ..log import R3logger
from ..globals import pg, math
import r3frame2 as r3

from r3frame2.core.resource.pipeline.render import R3renderPhase

class R3opaquePhase(R3renderPhase):
    mask: int = 0x0000
    
    def __init__(self) -> None:
        super().__init__("opaque")
    def execute(self, renderer: "r3.pipeline.R3renderer"):
        if renderer.get_flag(R3flags.renderer.Y_SORT):
            self.calls.sort(key=lambda call: call.pos[1])
            
        for call in self.calls:
            renderer.target.blit(call.surf.surface, renderer.camera.project(call.pos))
            renderer.blits += 1
        self.reset()

class R3renderer(R3atom):
    def __init__(
            self,
            app: "r3.app.R3app",
            world: "r3.resource.R3world",
            camera: "r3.pipeline.R3camera",
    ) -> None:
        super().__init__()
        self.app: r3.app.R3app = app
        self.world: r3.resource.R3world = world
        self.window: r3.app.R3window = app.window
        self.camera: r3.pipeline.R3camera = camera
        self.database: r3.resource.R3database = app.database

        self.blits: int = 0
        self.phases: list[r3.resource.pipeline.render.phase.R3renderPhase] = [
            R3opaquePhase()
        ]
        
        self.buffers: list[pg.Surface] = [pg.Surface(camera.viewport_size, pg.SRCALPHA) for _ in range(2)]
        self.target: pg.Surface = self.buffers.pop()

        self._freeze()

    def visible(self, pos: list[float], size: list[int]) -> bool:
        x, y = pos
        w, h = size
        vx, vy = self.camera.viewport_pos
        vw, vh = self.camera.viewport_size
        return (x + w >= vx and x <= vx + vw and y + h >= vy and y <= vy + vh)

    def queue(self, call: "r3.resource.R3renderCall") -> None:
        if not self.target: return
        if not isinstance(call, r3.resource.R3renderCall)\
        or not isinstance(call.surf, r3.resource.R3surf) \
        or not isinstance(call.pos, list): return
        
        if not self.visible(call.pos, call.surf.size): return

        for phase in self.phases:
            if phase.mask == call.mask:
                phase.queue(call)
                return

    @R3private
    def flush(self) -> None:
        if not self.target: return
        for phase in self.phases:
            phase.execute(self)
        
    @R3private
    def swap_buffers(self) -> None:
        if not len(self.buffers): return

        self.window.blit(pg.transform.scale(self.target, self.window.size), [0, 0])
        
        if self.camera.get_flag(R3flags.renderer.DIRTY_CAMERA):
            self.buffers = [pg.Surface(self.camera.viewport_size, pg.SRCALPHA) for _ in range(2)]
            self.camera.rem_flag(R3flags.renderer.DIRTY_CAMERA)
        else:
            self.buffers.insert(0, self.target)

        self.blits = 0
        self.target = self.buffers.pop()
        self.target.fill(self.window.color)
