import r3frame2 as r3

class Playground(r3.app.R3scene):
    def __init__(self, app):
        super().__init__(app)

    def init(self):
         # load an R3entity (0.0.1)
        self.database.load_entity("enemy", [200, 200], [8, 8], rgba=[0, 0, 255])
        self.database.load_entity("player", [100, 100], [16, 16], rgba=[255, 0, 0])

        # query said entity and toggle physics on it (0.0.5)
        self.enemy = self.database.query_entity("enemy")
        self.player = self.database.query_entity("player")

        # insert our entities into our world (0.0.7)
        self.world.insert(self.player)
        self.world.insert(self.enemy)
        
        # configure our entity physics (0.0.5)
        self.physics.toggle_transform(self.enemy)
        self.physics.toggle_transform(self.player)

        self.physics.toggle_collision(self.player, [0, 0], [16, 16])
        self.physics.toggle_collision(self.enemy, [0, 0], [8, 8])

    def exit(self): pass

    def events(self):
        # handle movement along the x-axis (0.0.1)
        if self.app.events.key_held(self.app.keyboard.A):
            self.physics.set_velocity(self.player, dx=-100)
        if self.app.events.key_held(self.app.keyboard.D):
            self.physics.set_velocity(self.player, dx=100)

        # handle movement along the y-axis (0.0.1)
        if self.app.events.key_held(self.app.keyboard.W):
            self.physics.set_velocity(self.player, dy=-100)
        if self.app.events.key_held(self.app.keyboard.S):
            self.physics.set_velocity(self.player, dy=100)

        # move our enemy using mouse right clicks (0.0.6)
        if self.app.events.mouse_pressed(self.app.mouse.RightClick):
            self.physics.move_to(self.enemy, self.app.mouse.pos.world, 100.0)

        # and lets move our camera using mouse left clicks (0.0.6)
        if self.app.events.mouse_pressed(self.app.mouse.LeftClick):
            self.camera.move_to(self.app.mouse.pos.world)

        # modify our camera viewport using the mouse wheel (0.0.6)
        if self.app.events.mouse_wheel_up: self.camera.zoom(-1)
        if self.app.events.mouse_wheel_down: self.camera.zoom(1)

        # lets initiate camera shake with left shift (0.0.6)
        if self.app.events.key_pressed(self.app.keyboard.LShift):
            self.camera.shake(4.0, 1.0)

        # move our camera along the x-axis using the left and right arrow keys (0.0.6)
        if self.app.events.key_held(self.app.keyboard.Left):
            self.camera.set_velocity(vx=-100)
        if self.app.events.key_held(self.app.keyboard.Right):
            self.camera.set_velocity(vx=100)

        # move our camera along the y-axis using the up and down arrow keys (0.0.6)
        if self.app.events.key_held(self.app.keyboard.Up):
            self.camera.set_velocity(vy=-100)
        if self.app.events.key_held(self.app.keyboard.Down):
            self.camera.set_velocity(vy=100)

    def update(self, dt: float): pass

    def render(self):
        # queue a render call for our player (0.0.7)
        self.renderer.queue(r3.resource.R3renderCall(0x0000, self.player.pos, self.player.surface))

        # queue a render call for our enemy (0.0.7)
        self.renderer.queue(r3.resource.R3renderCall(0x0000, self.enemy.pos, self.enemy.surface))

class PlaygroundApp(r3.app.R3app):
    def __init__(self):
        super().__init__(title="R3 Playground")

    def init(self):
        self.add_scene("playground", Playground)
        self.set_scene("playground")

    def exit(self): pass

def main() -> None:
    PlaygroundApp().run()

if __name__ == "__main__":
    main()
