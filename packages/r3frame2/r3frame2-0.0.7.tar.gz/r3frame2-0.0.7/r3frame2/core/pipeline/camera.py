from ..atom import R3atom, R3private
from ..flags import R3flags
from ..log import R3logger
from ..globals import pg, random
from ..utils import add_v2, sub_v2, div_v2, mag_v2
import r3frame2 as r3

class R3camera(R3atom):
    def __init__(
            self,
            app: "r3.app.R3app",
    ) -> None:
        super().__init__()
        self.app: r3.app.R3app = app
        self.window: r3.app.R3window = app.window
        self.database: r3.resource.R3database = app.database

        self.deadzone: float = 4.0

        self.shake_timer: float = 0.0
        self.shake_intensity: float = 1.0
        self.shake_offset: list[float] = [0.0, 0.0]

        self.damp_value: float = 1.0
        self.damp_threshold: float = 5.0
        self.velocity: list[float] = [0.0, 0.0]

        self.viewport_pos: list[float] = [0.0, 0.0]
        self.viewport_size: list[float] = [(app.window.size[0] // 2),(app.window.size[1] // 2)]
        self.viewport_scale: list[float] = [
            app.window.size[0] / self.viewport_size[0],
            app.window.size[1] / self.viewport_size[1]]

        self._freeze()

    @property
    def viewport_width(self) -> float:
        return self.viewport_size[0]
    @property
    def viewport_height(self) -> float:
        return self.viewport_size[1]
    @property
    def viewport_area(self) -> float:
        return self.viewport_size[0] * self.viewport_size[1]

    @property
    def viewport_x(self) -> float:
        return self.viewport_pos[0]
    @property
    def viewport_y(self) -> float:
        return self.viewport_pos[1]
    @property
    def viewport_center(self) -> list[float]:
        return add_v2(self.viewport_pos, div_v2(self.viewport_size, 2))

    def shake(self, intensity: float, time: float = 0.5) -> None:
        if not isinstance(time, (int, float))\
        or not isinstance(intensity, (int, float)):
            return

        self.shake_intensity = intensity
        self.shake_timer = time

    def project(self, pos: list[float]) -> list[float]:
        if not isinstance(pos, list): return pos
        return sub_v2(pos, sub_v2(self.viewport_pos, self.shake_offset))

    def zoom(self, delta: float) -> None:
        # scale zoom delta by 10% vp size
        delta *= min(self.viewport_size) * 0.1

        self.viewport_size[1] = min(self.window.size[1], max(self.window.size[1] / 4, self.viewport_size[1] + delta))
        self.viewport_size[0] = self.viewport_size[1] * self.window.aspect

        self.viewport_scale = [
            self.window.size[0] / self.viewport_size[0],
            self.window.size[1] / self.viewport_size[1]]
        
        self.set_flag(R3flags.renderer.DIRTY_CAMERA)


    def move_to(self, pos: list[float]) -> None:
        diff = sub_v2(pos, self.viewport_center)
        dist = mag_v2(diff)
        if int(dist) <= self.deadzone: return
        self.velocity[0] = diff[0]
        self.velocity[1] = diff[1]

    def set_velocity(self, vx: float=None, vy: float=None) -> None:
        if isinstance(vx, (int, float)): self.velocity[0] = vx
        if isinstance(vy, (int, float)): self.velocity[1] = vy


    @R3private
    def update(self, dt: float) -> None:
        self.viewport_pos[0] += self.velocity[0] * dt
        self.viewport_pos[1] += self.velocity[1] * dt

        self.velocity[0] *= (1 - self.damp_value * dt)
        self.velocity[1] *= (1 - self.damp_value * dt)

        if abs(self.velocity[0]) < self.damp_threshold: self.velocity[0] = 0.0
        if abs(self.velocity[1]) < self.damp_threshold: self.velocity[1] = 0.0
        
        if self.shake_timer > 0.0:
            self.shake_offset = [random.uniform(-1, 1) * self.shake_intensity,
                                 random.uniform(-1, 1) * self.shake_intensity]
            self.shake_timer -= dt
        else:
            self.shake_timer = 0.0
            self.shake_intensity = 0.0
            self.shake_offset = [0.0, 0.0]
        
