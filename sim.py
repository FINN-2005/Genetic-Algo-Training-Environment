from shapes import *



class run(APP):
    def setup(self):
        self.dt_speed_factor = 2
        self.group = Group([
            Rect(V2(APP.HW - 200,APP.HH - 100), V2(100,200), True),
            Circle(V2(APP.HW + 200,APP.HH), 100, 20, True),
            Propeller(V2(APP.HW, APP.HH))
        ])

        

    def update(self):
        # self.group.translate(V2(40,0) * self.dt)
        self.group.rotate(self.dt)
        # self.group.scale(0.9999)

    def draw(self):
        self.group.draw()


run()