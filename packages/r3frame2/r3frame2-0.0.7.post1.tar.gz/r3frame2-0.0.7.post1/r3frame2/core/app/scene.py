from ..atom import R3atom
from ..globals import pg
# from ..utils import 
import r3frame2 as r3

class R3scene(R3atom):
    def __init__(
            self,
            app: "r3.app.R3app",
            world_node_size: list[int] = [32, 32],
            world_cell_size: list[int] = [16, 16],
            world_size: list[int] = [8, 8], # defaults to 4096x4096px 32 pixelsx/node * 16 nodes/cell * 8 cells/axis
            world_origin: list[int] = [0, 0]
    ) -> None:
        super().__init__()
        self.app: r3.app.R3app = app
        self.database: r3.resource.R3database = app.database

        self.world: r3.resource.R3world = r3.resource.R3world(world_node_size, world_cell_size, world_size, world_origin)
        self.physics: r3.pipeline.R3physics = r3.pipeline.R3physics(app, self.world)
        
        self.ui: r3.pipeline.R3ui = r3.pipeline.R3ui(app)
        self.camera: r3.pipeline.R3camera = r3.pipeline.R3camera(app)
        self.renderer: r3.pipeline.R3renderer = r3.pipeline.R3renderer(app, self.world, self.camera)

    def exit(self) -> None: raise NotImplementedError
    def init(self) -> None: raise NotImplementedError
    def events(self) -> None: raise NotImplementedError

    def update(self, dt: float) -> None: raise NotImplementedError
    def tick(self) -> None: pass

    def render(self) -> None: raise NotImplementedError
