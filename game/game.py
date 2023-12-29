from cgi import test
import sys, pygame, asyncio, websockets
from player import Player

testing=True
gameStarted=False
size = width, height = 2000, 1500
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
blue = 0, 0, 255
player_size = 100
timer = 0
messageToShow = ''#"timer: " + str(timer)
buttonHeld = False
maxPower = 12
initBulletPower = 5
bulletPower = initBulletPower
powerAddFrameCount = 100

# socket config
socketProtocol = 'ws'
socketHost = 'localhost'
socketPort = '8123'
socket = None

pygame.init()
screen = pygame.display.set_mode(size)

player = Player(red, size[0] / 2, size[1] - player_size, player_size)
otherPlayer = None
my_font = pygame.font.SysFont('Comic Sans MS', 30)

async def connectToSocket():
    async with websockets.connect(socketProtocol + "://" + socketHost + ":" + socketPort) as websocket:
        global socket, player, otherPlayer, blue, size
        socket = websocket
        player.addSocket(socket)
        # await websocket.send("Hello world!")
        msg = await websocket.recv()
        msgDetails = msg.split('-')
        match msgDetails[0]:
            case 'init':
                if player.numb == None:
                    otherPlayer = Player(blue, size[0] / 2, size[1], player_size)
                    otherPlayer.addPlayerNumb(msgDetails[1])
                else:
                    player.addPlayerNumb(msgDetails[1])
            case 'playerMove':
                if player.numb != None:
                    if otherPlayer.numb == msgDetails[1]:
                        otherPlayer.teleport(msgDetails[2])
            case 'bulletAdded':
                if player.numb != None:
                    if otherPlayer.numb == msgDetails[1]:
                        otherPlayer.addBullets(msgDetails[2])
            # case 'bulletMove':
            #     pass

asyncio.run(connectToSocket())

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if gameStarted or testing:
            if event.type == pygame.MOUSEMOTION:
                mouse_position = pygame.mouse.get_pos()
                player.changeWaypoint(mouse_position[0]) # we only need the x 
            if event.type == pygame.MOUSEBUTTONDOWN:
                buttonHeld = True
            if event.type == pygame.MOUSEBUTTONUP:
                buttonHeld = False
                mouse_position = pygame.mouse.get_pos()
                player.shoot(mouse_position, bulletPower, socket)
                timer = 0
                bulletPower = initBulletPower

    # messageToShow = 'Bullets: ' + str(len(player.bullets))
    if buttonHeld:
        timer += 1
        if timer == powerAddFrameCount and bulletPower < maxPower:
            timer = 0
            bulletPower += 1
    messageToShow = 'Power: ' + str(bulletPower)
    text_surface = my_font.render(messageToShow, False, white)
    screen.fill(black)
    player.show(pygame, screen, size[0], otherPlayer)
    player.move()
    if otherPlayer != None:
        otherPlayer.show(pygame, screen, size[0], None)
    screen.blit(text_surface, (size[0] / 2, 200))
    pygame.display.update()