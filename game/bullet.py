from pygame.math import Vector2

class Bullet:
    def __init__(self, _x, _y, _power, _waypoint):
        self.coords = Vector2(_x, _y)
        self.speed = 10
        self.power = _power
        self.color = 255, 255, 255
        self.size = 5 * self.power
        r = ((self.coords[0] - _waypoint[0])**2 + (self.coords[1] - _waypoint[1])**2)**0.5
        self.velocity = Vector2((_waypoint[0]-self.coords[0])/r, (_waypoint[1]-self.coords[1])/r)
    
    def move(self): #, socket, playerNumb
        self.coords += self.velocity * self.speed
        self.size -= 0.05

        # if not socket == None:
        #     socket.send('bulletMove-' + playerNumb + '-' + self.coords[0] + '-' + self.coords[1])

    def show(self, pygame, screen):
        pygame.draw.circle(screen, self.color, self.coords, self.size)