import pygame
import time
from pygame.locals import *
import random


class Base(object):
    def __init__(self, screen_temp, x, y, image_name):
        self.x = x
        self.y = y
        self.screen = screen_temp
        self.image = pygame.image.load(image_name)


class BasePlane(Base):
    def __init__(self, screen_temp, x, y, image_name):
        Base.__init__(self, screen_temp, x, y, image_name)
        self.bullet_list = []  # 存储子弹

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))
        for bullet in self.bullet_list:
            bullet.display()
            bullet.move()
            if bullet.judge():  # 判断是否越界
                self.bullet_list.remove(bullet)


class HeroPlane(BasePlane):
    def __init__(self, screen_temp):
        BasePlane.__init__(self, screen_temp, 210, 700, "./feiji/hero1.png")

        self.hit = False
        self.bomb_list = []
        self.__create_images()
        self.image_num = 0
        self.image_index = 0

    def __create_images(self):
        self.bomb_list.append(pygame.image.load("./feiji/hero_blowup_n1.png"))
        self.bomb_list.append(pygame.image.load("./feiji/hero_blowup_n2.png"))
        self.bomb_list.append(pygame.image.load("./feiji/hero_blowup_n3.png"))
        self.bomb_list.append(pygame.image.load("./feiji/hero_blowup_n4.png"))

    def move_left(self):
        self.x -= 5

    def move_right(self):
        self.x += 5

    def fire(self):
        self.bullet_list.append(Bullet(self.screen, self.x, self.y))

    def display(self):
        BasePlane.display(self)
        if self.hit:
            self.screen.blit(self.bomb_list[self.image_index], (self.x, self.y))
            self.image_num += 1
            if self.image_num == 7:
                self.image_num = 0
                self.image_index += 1
            if self.image_index > 3:
                time.sleep(1)
                exit()
        else:
            self.screen.blit(self.image, (self.x, self.y))

    def bomb(self):
        self.hit =True
class EnmeyPlane(BasePlane):
    def __init__(self, screen_temp):
        BasePlane.__init__(self, screen_temp, 0, 0, "./feiji/enemy0.png")
        self.direction = "right"

    def fire(self):
        random_num = random.randint(1, 100)
        if random_num == 1 or random_num == 20:
            self.bullet_list.append(EnemyBullet(self.screen, self.x, self.y))

    def move(self):
        if self.direction == "right":
            self.x += 5
        elif self.direction == "left":
            self.x -= 5
        if self.x > 480 - 50:
            self.direction = "left"
        elif self.x < 0:
            self.direction = "right"


class BaseBullet(Base):

    def __init__(self, screen_temp, x, y, image_name):
        Base.__init__(self, screen_temp, x, y, image_name)

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))


class Bullet(BaseBullet):
    def __init__(self, screen_temp, x, y):
        BaseBullet.__init__(self, screen_temp, x + 40, y - 20, "./feiji/bullet.png")

    def move(self):
        self.y -= 20

    def judge(self):
        if self.y < 0:
            return True
        else:
            return False


class EnemyBullet(BaseBullet):
    def __init__(self, screen_temp, x, y):
        BaseBullet.__init__(self, screen_temp, x + 25, y + 40, "./feiji/bullet1.png")

    def move(self):
        self.y += 10

    def judge(self):
        if self.y > 852:
            return True
        else:
            return False


def key_control(hero):
    for event in pygame.event.get():
        if event.type == QUIT:
            print("exit")
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_a or event.key == K_LEFT:
                print("left")
                hero.move_left()

            elif event.key == K_d or event.key == K_RIGHT:
                print("right")
                hero.move_right()
            elif event.key == K_SPACE:
                print("space")
                hero.fire()
            elif event.key == K_b:
                print('b')
                hero.bomb()

#  创建窗口
def main():
    screen = pygame.display.set_mode((480, 852), 0, 32)
    background = pygame.image.load("./feiji/background.png")
    # 创建一个飞机图片

    hero = HeroPlane(screen)
    # 创建敌机
    enemy = EnmeyPlane(screen)
    num = 0
    while True:
        screen.blit(background, (0, 0))
        enemy.display()
        hero.display()
        key_control(hero)
        enemy.move()
        enemy.fire()
        pygame.display.update()
        if num == 50:
            pygame.display.update()
            num = 0
        else:
            num += 1


if __name__ == '__main__':
    main()
