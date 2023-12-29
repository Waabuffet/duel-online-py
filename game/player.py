from bullet import Bullet
import pickle

class Player:

    def __init__(self, _color, _x, _y, _size):
        self.color = _color
        self.size = _size
        self.x = _x
        self.y = _y
        self.speed = 5
        self.bullets = []
        self.waypoint = 0
        self.numb = None

    def addSocket(self, socket):
        self.socket = socket
    
    def addPlayerNumb(self, _numb):
        self.numb = _numb

    def move(self):
        if (self.x + (self.size / 2)) < self.waypoint:
            self.x += self.speed
        else:
            self.x -= self.speed
        if not self.socket == None and not self.numb == None:
            self.socket.send('playerMove-' + self.numb + '-' + self.x)

    def teleport(self, _x):
        self.x = _x
    
    def addBullets(self, bullet):
        newBullet = pickle.loads(bullet)
        self.bullets.append(newBullet)

    def changeWaypoint(self, _x):
        self.waypoint = _x

    def shoot(self, mouse_pos, power, socket):
        newBullet = Bullet(self.x + (self.size / 2), self.y, power, mouse_pos)
        self.bullets.append(newBullet)
        if not self.numb == None:
            newBulletMessage = pickle.dumps(newBullet)
            msg = "bulletAdded-" + self.numb + "-" + newBulletMessage
            socket.send(msg)

    def isBulletInRange(self, bullet, width):
        if bullet.coords[0] <= 0 or bullet.coords[0] >= width: # or bullet.y <= 0 # this part will be the other player's screen
            return False
        return True
    def isBulletAlive(self, bullet):
        if bullet.size <= 0:
            return False
        return True

    def didBulletHitOtherPlayer(self, bullet, otherPlayer):
        if bullet.coords.x > otherPlayer.x and bullet.coords.x < (otherPlayer.x + otherPlayer.size) and bullet.coords.y > otherPlayer.y and bullet.coords.y < (otherPlayer.y + otherPlayer.size):
            return True
        return False

    def show(self, pygame, screen, screen_width, otherPlayer):
        for bullet in self.bullets:
            bullet.show(pygame, screen)
            bullet.move() #self.socket, self.numb
            if otherPlayer != None and self.socket != None:
                if self.didBulletHitOtherPlayer(bullet, otherPlayer):
                    pass
            if not self.isBulletInRange(bullet, screen_width) or not self.isBulletAlive(bullet):
                self.bullets.remove(bullet)
                break
        
        pygame.draw.rect(screen, self.color,(self.x, self.y, self.size, self.size))
