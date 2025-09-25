from pygame_template import *


def rotate_point(point, center, angle):
    """Rotate a point around a center by angle (in radians)"""
    # Translate to origin
    x = point.x - center.x
    y = point.y - center.y
    
    # Rotate using trig
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    
    new_x = x * cos_a - y * sin_a
    new_y = x * sin_a + y * cos_a
    
    # Translate back
    return V2(new_x + center.x, new_y + center.y)



class Line:
    def __init__(self, start: V2, end: V2):
        self.start = start
        self.end = end
    
    def rotate(self, center, angle):
        self.start = rotate_point(self.start, center, angle)
        self.end = rotate_point(self.end, center, angle)
        return self
    
    def translate(self, pos: V2):
        self.start += pos
        self.end += pos

    def scale(self, center: V2, scale_factor):
        dist_a = self.start - center
        dist_b = self.end - center
        dist_a *= scale_factor
        dist_b *= scale_factor
        self.start = dist_a + center
        self.end = dist_b + center
    
    def draw(self, screen, lw):
        pygame.draw.line(screen, Color.white, self.start, self.end, lw)



class Shape(Sprite):
    def __init__(self,center=V2(APP.HW, APP.HH), *groups):
        super().__init__(*groups)

        self.lines = [ Line(center + V2(-50,0),center + V2(50,0)) ]     # defualt line

        self.center = V2(center)
        self.draw_center = False
        self.backup_center = self.center.copy()
        self.line_width = 1

    def draw(self, screen):
        for line in self.lines: line.draw(screen, self.line_width)
        if self.draw_center:
            pygame.draw.circle(screen, 'black', self.center, 7)
            pygame.draw.circle(screen, 'white', self.center, 5)

    def rotate(self, angle):
        for line in self.lines: line.rotate(self.center, angle)

    def translate(self, pos: V2):
        self.center += pos
        for line in self.lines: line.translate(pos)

    def scale(self, scale_factor):
        for line in self.lines: line.scale(self.center, scale_factor)


    def update(self, dt):
        ...



class Rect(Shape):
    def __init__(self, lt: V2, wh: V2, draw_center = False, *groups):
        center = lt + wh / 2
        super().__init__(center, *groups)
        
        self.pos = V2(lt)
        self.size = V2(wh)
        
        l, t, w, h = lt[0], lt[1], wh[0], wh[1]
        self.lines = [
            Line(V2(l, t), V2(l + w, t)),
            Line(V2(l + w, t), V2(l + w, t + h)),
            Line(V2(l + w, t + h), V2(l, t + h)),
            Line(V2(l, t + h), V2(l, t)),
        ]
        self.draw_center = draw_center



class Circle(Shape):
    def __init__(self, pos: V2, radius: float, num_of_segments = 10, draw_center = False, *groups):
        super().__init__(pos, *groups)
        self.draw_center = draw_center
        
        c, s, r = math.cos, math.sin, math.radians
        points = []
        angle_increment = 360.0 / num_of_segments        
        for i in range(num_of_segments):
            angle = i * angle_increment
            p = V2(c(r(angle))*radius, s(r(angle))*radius) + V2(pos)
            points.append(p)

        self.lines = []
        for i in range(0, len(points)):
            self.lines.append(Line(points[i], points[(i+1)%len(points)]))





class CustomShape(Shape):
    def __init__(self, center: V2, rel_lines: list[tuple[V2, V2]], *groups):
        super().__init__(center, *groups)
        
        self.rel_lines = rel_lines  # store definitions relative to center
        self.update_lines()

    def update_lines(self):
        self.lines = []
        for a, b in self.rel_lines:
            self.lines.append(Line(self.center + a, self.center + b))

    def rotate(self, angle):
        for line in self.lines:
            line.rotate(self.center, angle)

    def scale(self, scale_factor):
        for line in self.lines:
            line.scale(self.center, scale_factor)

class Propeller(Shape):
    def __init__(self, center: V2, blade_length=80, blade_width=20, num_blades=3, *groups):
        super().__init__(center, *groups)
        self.blades = []
        angle_inc = 2*math.pi/num_blades

        for i in range(num_blades):
            angle = i * angle_inc
            # rectangle blade in local space
            half_w = blade_width/2
            rect = [
                V2(-half_w, 0),
                V2(half_w, 0),
                V2(half_w, -blade_length),
                V2(-half_w, -blade_length),
            ]
            # rotate each point
            rect = [rotate_point(p, V2(0,0), angle) for p in rect]
            self.blades.append(rect)

        self.update_lines()

    def update_lines(self):
        self.lines = []
        for blade in self.blades:
            for i in range(len(blade)):
                self.lines.append(Line(self.center+blade[i], self.center+blade[(i+1)%len(blade)]))
