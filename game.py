import pygame
import sys
import random
import os

# initiate pygame
pygame.init()
clock = pygame.time.Clock()
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Astronaut")

# load images and fonts
bgImg1 = pygame.image.load("images/background1.png")
bgImg1_1 = pygame.image.load("images/background1_1.png")
bgImg1_2 = pygame.image.load("images/background1_2.png")
bgImg1_3 = pygame.image.load("images/background1_3.png")
bgImg2 = pygame.image.load("images/background2.png")
bgImg2_1 = pygame.image.load("images/background2_1.png")
bgImg2_2 = pygame.image.load("images/background2_2.png")
bgImg2_3 = pygame.image.load("images/background2_3.png")
bgImg3 = pygame.image.load("images/background3.png")
bgImg3_1 = pygame.image.load("images/background3_1.png")
bgImg3_2 = pygame.image.load("images/background3_2.png")
bgImg3_3 = pygame.image.load("images/background3_3.png")
bgImgs = ((bgImg1, bgImg1_1, bgImg1_2, bgImg1_3),
          (bgImg2, bgImg2_1, bgImg2_2, bgImg2_3),
          (bgImg3, bgImg3_1, bgImg3_2, bgImg3_3))
playerImg = pygame.image.load("images/player.png")
fireImg = pygame.image.load("images/fire.png")
pipeImg = pygame.image.load("images/pipe.png")
font = pygame.font.Font("fonts/menu.TTF", 32)
largeFont = pygame.font.Font("fonts/menu.TTF", 64)
smallFont = pygame.font.Font("fonts/menu.TTF", 28)
DATA_FILE = "data/highest_score.txt"

# constant
UP_FORCE = 8.5
GRAVITY = 0.9
PIPE_SPEED = 8.0
PIPE_INTERVAL = 1500
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 100, 100)
COLOR_YELLOW = (255, 255, 200)
COLOR_BLUE = (50, 255, 255)
SCORE_STEP = 50
BACKGROUND_UPGRADE_STEP = SCORE_STEP * 10
BACKGROUND_INTERVAL_FRAMES = 5

# game variables
newRecord = False
score = 0
highestScore = 0


class Background:
    def __init__(self):
        self.movement = 0
        self.backgroundImg = bgImgs
        self.row = 0
        self.col = 0
        self.interval = BACKGROUND_INTERVAL_FRAMES
        self.upgradeFlag = False

    def render(self):
        self.movement -= 2
        if self.movement <= -1164:
            self.movement = 0
        screen.blit(self.backgroundImg[self.row][int(self.col)], (self.movement, 0))
        screen.blit(self.backgroundImg[self.row][int(self.col)], (self.movement + 1164, 0))

    def upgrade_background(self):
        if self.upgradeFlag:
            self.col += (1 / self.interval)
            if self.col % 4 < 0.01:
                self.col = 0
                self.row = (self.row + 1) % 3
                self.upgradeFlag = False

    def trigger_upgrade(self):
        if get_score() % BACKGROUND_UPGRADE_STEP == 0:
            self.upgradeFlag = True


class Player:
    def __init__(self):
        self.gravity = GRAVITY
        self.movement = 0
        self.y = SCREEN_HEIGHT / 2
        self.img = playerImg
        self.fire = fireImg
        self.rect = self.img.get_rect(center=(300, self.y))
        self.fireRect = self.fire.get_rect(midtop=(300, self.y + 10))

    def render(self):
        self.movement += self.gravity
        self.y += self.movement
        self.rect.centery = self.y
        screen.blit(self.img, self.rect)

    def move_upward(self):
        self.movement = -UP_FORCE

    def eject_fire(self):
        self.fireRect.centery = self.y + 20
        screen.blit(self.fire, self.fireRect)


class Pipes:
    def __init__(self):
        self.pipes = []
        self.bottomImg = pipeImg
        self.topImg = pygame.transform.flip(self.bottomImg, False, True)

    def create(self):
        gap = random.randint(120, 250)
        top = random.randint(0, 300)
        bottom = top + gap
        topRect = self.topImg.get_rect(midbottom=(SCREEN_WIDTH + 100, top))
        bottomRect = self.bottomImg.get_rect(midtop=(SCREEN_WIDTH + 100, bottom))
        self.pipes.append((bottomRect, 0))
        self.pipes.append((topRect, 1))

    def render(self):
        for pipe in self.pipes:
            pipe[0].centerx -= PIPE_SPEED
            if pipe[1] == 0:
                screen.blit(self.bottomImg, pipe[0])
            else:
                screen.blit(self.topImg, pipe[0])


def check_collision(avatar, objects):
    """
    check if avatar collides with objects or screen boundary
    :param avatar: Player object
    :param objects: Pipes object
    :return: None
    """
    if avatar.y <= -40 or avatar.y >= SCREEN_HEIGHT + 40:
        return True
    for obj in objects.pipes:
        if avatar.rect.colliderect(obj[0]):
            return True
    return False


def get_score():
    """
    get current score of the player
    :return: int
    """
    return max(0, score - SCORE_STEP)


def save_highest_score():
    """
    save the highest score into the DATA_FILE ("data/highest_score.txt")
    :return: None
    """
    with open(DATA_FILE, "w") as fout:
        fout.write(str(highestScore))


def read_highest_score():
    """
    read the highest score from the DATA_FILE ("data/highest_score.txt")
    :return:
    """
    if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE):
        with open(DATA_FILE) as fin:
            return int(fin.read())
    return 0


def render_menu():
    """
    render text of the menu page before the game start
    :return: None
    """
    title = largeFont.render("FLAPPY ASTRONAUT", True, COLOR_BLUE)
    titleRect = title.get_rect(center=(504, 179))
    screen.blit(title, titleRect)
    title = largeFont.render("FLAPPY ASTRONAUT", True, COLOR_RED)
    titleRect = title.get_rect(center=(500, 175))
    screen.blit(title, titleRect)
    startText = font.render(">>>>> PRESS SPACE TO JUMP <<<<<", True, COLOR_WHITE)
    startTextRect = startText.get_rect(center=(500, 240))
    screen.blit(startText, startTextRect)
    startText = smallFont.render("START (PRESS S)", True, COLOR_YELLOW)
    startTextRect = startText.get_rect(center=(500, 325))
    screen.blit(startText, startTextRect)
    quitText = smallFont.render("QUIT (PRESS Q)", True, COLOR_YELLOW)
    quitTextRect = quitText.get_rect(center=(500, 370))
    screen.blit(quitText, quitTextRect)


def render_header():
    """
    render score as the header of the playground when game started
    :return: None
    """
    startText = font.render("SCORE: " + str(get_score()), True, COLOR_WHITE)
    startTextRect = startText.get_rect(topleft=(15, 10))
    screen.blit(startText, startTextRect)


def render_endpage():
    """
    render the text of the end page after game is over
    :return: None
    """
    if newRecord:
        scoreText = largeFont.render("NEW RECORD: " + str(get_score()), True, COLOR_WHITE)
        scoreTextRect = scoreText.get_rect(center=(504, 154))
        screen.blit(scoreText, scoreTextRect)
        scoreText = largeFont.render("NEW RECORD: " + str(get_score()), True, COLOR_RED)
        scoreTextRect = scoreText.get_rect(center=(500, 150))
        screen.blit(scoreText, scoreTextRect)
    else:
        scoreText = largeFont.render("YOUR SCORE: " + str(get_score()), True, COLOR_WHITE)
        scoreTextRect = scoreText.get_rect(center=(504, 154))
        screen.blit(scoreText, scoreTextRect)
        scoreText = largeFont.render("YOUR SCORE: " + str(get_score()), True, COLOR_BLUE)
        scoreTextRect = scoreText.get_rect(center=(500, 150))
        screen.blit(scoreText, scoreTextRect)
    scoreTextRect = scoreText.get_rect(center=(500, 150))
    screen.blit(scoreText, scoreTextRect)
    highestScoreText = font.render("HIGHEST SCORE: " + str(highestScore) + " (RESET R)", True, COLOR_YELLOW)
    highestScoreTextRect = highestScoreText.get_rect(center=(500, 250))
    screen.blit(highestScoreText, highestScoreTextRect)
    startText = font.render("RESTART (PRESS S)", True, COLOR_WHITE)
    startTextRect = startText.get_rect(center=(500, 300))
    screen.blit(startText, startTextRect)
    quitText = font.render("QUIT (PRESS Q)", True, COLOR_WHITE)
    quitTextRect = quitText.get_rect(center=(500, 350))
    screen.blit(quitText, quitTextRect)


def main():
    global newRecord, score, highestScore
    highestScore = read_highest_score()
    gameStart = False
    gamePrepare = False
    gameOver = False
    fireDelay = 0
    background = Background()
    player = None
    pipes = None
    PIPE_TIMER = pygame.USEREVENT
    pygame.time.set_timer(PIPE_TIMER, PIPE_INTERVAL)

    # game loop
    while True:
        background.render()
        if not gameStart:
            render_menu()
        elif not gameOver:
            if fireDelay > 0:
                player.eject_fire()
                fireDelay -= 1
            player.render()
            pipes.render()
            render_header()
            if not gamePrepare:
                background.upgrade_background()
            if check_collision(player, pipes):
                gameOver = True
                player = None
                pipes = None
                if get_score() > highestScore:
                    highestScore = get_score()
                    newRecord = True
                save_highest_score()
        else:
            render_endpage()

        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if not gameStart:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_s:
                        gameStart = True
                        gamePrepare = True
                        newRecord = False
                        background = Background()
                        player = Player()
                        pipes = Pipes()
                elif not gameOver:
                    if event.key == pygame.K_SPACE:
                        player.move_upward()
                        fireDelay = 10
                else:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_s:
                        gameOver = False
                        gamePrepare = True
                        newRecord = False
                        score = 0
                        background = Background()
                        player = Player()
                        pipes = Pipes()
                    if event.key == pygame.K_r:
                        score = 0
                        highestScore = 0
                        save_highest_score()
            elif event.type == PIPE_TIMER and gameStart and not gameOver:
                pipes.create()
                score += SCORE_STEP
                if not gamePrepare:
                    background.trigger_upgrade()
                gamePrepare = False

        pygame.display.update()
        clock.tick(120)


if __name__ == "__main__":
    main()
