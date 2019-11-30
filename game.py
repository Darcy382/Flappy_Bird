import pygame, sys
from pygame.locals import *
from post import Post
import itertools

pygame.init()

FPS = 30
fpsClock = pygame.time.Clock()

width = 400
height = 600
# set up the window
DISPLAYSURF = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird")

# Drawling
post_top = pygame.image.load('assets/post_top.png').convert_alpha()
post_bottom = pygame.image.load('assets/post_bottom.png').convert_alpha()
bird = pygame.image.load('assets/bird.png').convert_alpha()
bird_rect = bird.get_rect()
bird_rect.center = (width / 2 , height / 2)
font_name = pygame.font.match_font('arial')

# Vars
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
speed = [0, 1]
gravity = 2
post_speed = 3
post_spacing = 170
hit_leeway = 30
score = 0

post_width = post_top.get_rect().width
kill_range = range(int(width / 2 - bird_rect.width / 2 - post_width), int(width / 2 + bird_rect.width / 2))


# Functions
def jump():
    speed[1] = -15


def inter_through(alist):
    while True:
        for item in alist:
            yield item


def move_posts(posts):
    for post in posts:
        post.move_post(post_speed)


def check_for_next(obj1, obj2, obj3):
    posts_x = [post1.postx, post2.postx, post3.postx]
    if max(posts_x) < (width - post_spacing):
        return posts_x.index(min(posts_x))


def check_hit(post_list):
    for post in post_list:
        if post.postx in kill_range:
            if bird_rect.bottom - hit_leeway > post.bottom_y:
                print(bird_rect.bottom, post.bottom_y)
                end_game()
            elif bird_rect.top + hit_leeway < (post.top_y + 500):
                print(bird_rect.bottom, post.top_y)
                end_game()


def check_score(bird, post, current_score):
    if bird > post:
        return 1
    else:
        return 0


def end_game():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw():
    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(post_top, post1.top_tup)
    DISPLAYSURF.blit(post_bottom, post1.bottom_tup)
    DISPLAYSURF.blit(post_top, post2.top_tup)
    DISPLAYSURF.blit(post_bottom, post2.bottom_tup)
    DISPLAYSURF.blit(post_top, post3.top_tup)
    DISPLAYSURF.blit(post_bottom, post3.bottom_tup)
    DISPLAYSURF.blit(bird, bird_rect)
    draw_text(DISPLAYSURF, str(score), 75, width - 75, 20)


# Sets up posts, [ (top post left x, top post left y), (bottom post left x, bottom post left y]) ]
post1 = Post(1)
post2 = Post(2, width=width+post_spacing)
post3 = Post(2, width=width+post_spacing*2)
posts = inter_through([post1, post2, post3])
current_post = next(posts)

# the main game loop
running = True
while running:
    draw()
    bird_rect = bird_rect.move(speed)
    speed[1] += gravity

    move_posts([post1, post2, post3])
    # Resets posts
    check = check_for_next(post1, post2, post3)
    if check == 0:
        post1.reset()
    elif check == 1:
        post2.reset()
    elif check == 2:
        post3.reset()

    check_hit([post1, post2, post3])
    # Calc score
    new_score = check_score(bird_rect.left, current_post.postx, score)
    if new_score:
        score +=1
        current_post = next(posts)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                jump()

    #print(fpsClock.get_fps())
    pygame.display.update()
    fpsClock.tick(FPS)