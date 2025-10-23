import math
import random
import pygame
from entites import (Tank,
                     Game,
                     Wall,
                     Enemy,
                     Button,
                     Bullet,
                     Explosion,
                     TempSprite
                     )

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 840
FPS = 30

pygame.init()
game = Game()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Battle Tanks Arena vs Bots")
pygame.display.set_icon(pygame.image.load('image/tank_icon.png'))
background_menu = pygame.image.load("image/menu.png")

battle_arena = pygame.Surface((780, 780))
ba_rect = battle_arena.get_rect()

portals = [(330, 0), (150, 0), (600, 0), (0, 60), (7, 60)]

pygame.mixer.init()
shot_sound = pygame.mixer.Sound("sound/shot.wav")
explosion_sound = pygame.mixer.Sound("sound/destroy.wav")

fontUI = pygame.font.Font(None, 30)
fontBig = pygame.font.Font(None, 70)
fontTitle = pygame.font.Font(None, 140)

# walls = pygame.sprite.Group()
# enemys = pygame.sprite.Group()
# explosions = pygame.sprite.Group()
#
# enemy = Enemy(battle_arena, 155, 0)
# enemys.add(enemy)
#
# enemys_background_location = [(x, y) for y in range(30, 421, 40) for x in range(820, 921, 40)]
# enemy_tank = pygame.image.load("image/enemy.png")
# enemy_image = pygame.transform.rotozoom(enemy_tank, 180, 30 / 32)
# enemys_background = [(enemy_image, item) for item in enemys_background_location]

users_background_location = [(x, y) for y in range(680, 731, 40) for x in range(820, 921, 40)]
user_tank = pygame.image.load("image/users_tank.png")
user_image = pygame.transform.rotozoom(user_tank, 0, 30 / 32)
game.users_background = [(user_image, item) for item in users_background_location]


def walls_coordinate_generation(window_rect):
    left = 40
    top = 40
    right = window_rect.width - 64
    bottom = window_rect.height - 64
    places = []
    while len(places) < 150:
        x = random.randrange(left, right + 1, 32)
        y = random.randrange(top, bottom + 1, 32)
        if (x, y) not in places:
            places.append((x, y))
    return places


def hit_reaction(only_tuple, objects_group, bckgr=None):
    for piece in only_tuple[:]:
        for obj in objects_group:
            if piece.image_rect.colliderect(obj.rect):
                explosion = Explosion(obj.rect.x, obj.rect.y, game.explosions, explosion_sound)
                only_tuple.remove(piece)
                objects_group.remove(obj)
                if type(piece.parent) == Tank:
                    game.score += 5

                if bckgr:
                    bckgr.pop()

                    if bckgr == game.enemys_background:
                        game.score += 50
                        game.enemy_count -= 1
                        if game.enemy_count <= 0:
                            game.new_stage()
                            game.my_tank.image_rect.midbottom = game.my_tank.field_rect.midbottom
                            game.my_tank.angle = 0
                            pygame.mixer.music.stop()
                break


def for_bullet_move(bullets=game.bullets, ba_rect=ba_rect):
    for bullet in bullets[:]:
        bullet.move()
        if not ba_rect.colliderect(bullet.image_rect):
            bullets.remove(bullet)


def for_bullets_blitme(bullets=game.bullets):
    for bullet in bullets:
        bullet.blitme()


def draw_UI(text, x, y):
    textUI = fontUI.render(text, 1, 'white')
    rect = textUI.get_rect(topleft=(x, y))
    screen.blit(textUI, rect)


def enemy_tank_control(my_tank=game.my_tank):
    for enemy in game.enemys:
        if my_tank.image_rect.y - 16 <= enemy.rect.y <= my_tank.image_rect.y + 16:
            if my_tank.image_rect.x - game.max_detection_distance < enemy.rect.x - 32 < my_tank.image_rect.x:
                enemy.angle = -90
                if random.randint(0, 9) == 5 and len(game.bullets_enemy) < 5:
                    bullet = Bullet(battle_arena, enemy, shot_sound)
                    game.bullets_enemy.append(bullet)
            if my_tank.image_rect.x + game.max_detection_distance > enemy.rect.x + 32 > my_tank.image_rect.x:
                enemy.angle = 90
                if random.randint(0, 9) == 5 and len(game.bullets_enemy) < 5:
                    bullet = Bullet(battle_arena, enemy, shot_sound)
                    game.bullets_enemy.append(bullet)

        if my_tank.image_rect.x - 16 <= enemy.rect.x <= my_tank.image_rect.x + 16:
            if my_tank.image_rect.y - game.max_detection_distance < enemy.rect.y < my_tank.image_rect.y:
                enemy.angle = 180
                if random.randint(0, 9) == 5 and len(game.bullets_enemy) < 5:
                    bullet = Bullet(battle_arena, enemy, shot_sound)
                    game.bullets_enemy.append(bullet)
            if my_tank.image_rect.y + game.max_detection_distance > enemy.rect.y > my_tank.image_rect.y:
                enemy.angle = 0
                if random.randint(0, 9) == 5 and len(game.bullets_enemy) < 5:
                    bullet = Bullet(battle_arena, enemy, shot_sound)
                    game.bullets_enemy.append(bullet)


# =====================================================================================================================
def game_loop():
    # game.running = True
    while game.running:

        game.timer += 1

        if not game.usertanks and game.users_background:
            game.my_tank = Tank(battle_arena)
            my_tank = game.my_tank
            game.usertanks.append(my_tank)

        # 1. обробка подій
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(game.bullets) < 5:
                    bullet = Bullet(battle_arena, my_tank, shot_sound)
                    game.bullets.append(bullet)
                if event.key == pygame.K_m:
                    game.paused_music = not game.paused_music
                    if game.paused_music:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()

        if game.timer == 1 and not game.is_gameover:
            pygame.mixer.music.load('sound/level_start.mp3')
            pygame.mixer.music.play()
            game.walls = pygame.sprite.Group()
            game.enemys = pygame.sprite.Group()
            game.explosions = pygame.sprite.Group()

            enemy = Enemy(battle_arena, 155, 0)
            game.enemys.add(enemy)

            enemys_background_location = [(x, y) for y in range(30, 421, 40) for x in range(820, 921, 40)]
            enemy_tank = pygame.image.load("image/enemy.png")
            enemy_image = pygame.transform.rotozoom(enemy_tank, 180, 30 / 32)
            game.enemys_background = [(enemy_image, item) for item in enemys_background_location]

            points = walls_coordinate_generation(ba_rect)

            for point in points:
                wall = Wall(battle_arena, point)
                game.walls.add(wall)

        if game.timer < 220 and not game.is_gameover:
            game.title_y += 3
            screen.fill((90, 90, 90))
            pygame.draw.rect(screen, 'black',
                             (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 200 + game.title_y, 600, 250))
            pygame.draw.rect(screen, 'orange',
                             (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 200 + game.title_y, 600, 250),
                             3)
            text = fontTitle.render('BATLE', 1, 'white')
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100 + game.title_y))
            screen.blit(text, rect)
            text = fontBig.render('TANKS ARENA', 1, 'white')
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20 + game.title_y))
            screen.blit(text, rect)
            text = fontUI.render(f'STAGE {game.stage}', 1, 'white')
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20 + game.title_y))
            screen.blit(text, rect)

        if game.timer >= 220 and game.timer <= 225 and not game.is_gameover:
            pygame.mixer.music.load("sound/soundtreck.mp3")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)

        if game.timer > 225 and not game.is_gameover:
            keys = pygame.key.get_pressed()
            my_tank.move(keys)

            portal = portals[random.randrange(5)]
            x, y = portal
            portal_rect = pygame.Rect(x, y, 32, 32)
            portal_sprite = TempSprite(portal_rect)
            if (not pygame.sprite.spritecollide(portal_sprite, game.enemys, False)
                    and len(game.enemys) < game.max_tanks_quantity
                    and len(game.enemys_background) >= game.max_tanks_quantity):
                new_enemy = Enemy(battle_arena, x, y)
                game.enemys.add(new_enemy)

            # 2. оновлення стану гри
            game.enemys.update()
            enemy_tank_control(my_tank)
            for_bullet_move(game.bullets)
            for_bullet_move(game.bullets_enemy)
            game.explosions.update()
            if game.score > game.hiscore:
                game.hiscore = game.score

            for wall in game.walls:
                if my_tank.image_rect.colliderect(wall):
                    my_tank.image_rect.x += my_tank.speed * int(math.sin(math.radians(my_tank.angle)))
                    my_tank.image_rect.y += my_tank.speed * int(math.cos(math.radians(my_tank.angle)))

            collisions = pygame.sprite.groupcollide(game.enemys, game.walls, False, False)
            for enemy in collisions:
                enemy.angle = enemy.turn()

            for ememy in game.enemys:
                for tank in pygame.sprite.spritecollide(ememy, game.enemys, False):
                    if ememy != tank:
                        tank.angle = tank.turn()
                        enemy.angle = enemy.turn()

            hit_reaction(game.bullets, game.walls)
            hit_reaction(game.bullets_enemy, game.walls)
            hit_reaction(game.bullets, game.enemys, bckgr=game.enemys_background)
            hit_reaction(game.usertanks, game.enemys)
            hit_reaction(game.bullets_enemy, game.usertanks, bckgr=game.users_background)

            if not game.users_background:
                game.is_gameover = True
                pygame.mixer.music.stop()
                game.timer = 5000

            # 3. оновлення екрана
            # 3.1 відмальовування фону
            battle_arena.fill((0, 0, 0))
            screen.fill((90, 90, 90))

            # 3.2 відмальовування об'єктів
            game.walls.draw(battle_arena)
            for_bullets_blitme(game.bullets)
            for_bullets_blitme(game.bullets_enemy)
            [my_tank.bliitme() for my_tank in game.usertanks]
            game.enemys.draw(battle_arena)
            game.explosions.draw(battle_arena)
            my_tank.bliitme()
            screen.blit(battle_arena, (30, 30))
            [screen.blit(*item) for item in game.enemys_background]
            [screen.blit(*item) for item in game.users_background]

            score_text = f"{game.score:09}"
            hiscore_text = f"{game.hiscore:09}"
            draw_UI("HISCORE", 820, 460)
            draw_UI(hiscore_text, 820, 490)
            draw_UI("SCORE", 820, 530)
            draw_UI(score_text, 820, 560)

            draw_UI(f"STAGE {game.stage}", 820, 600)

        if game.timer == 5000 and game.is_gameover:
            print("Game over!")

            text = fontTitle.render('GAME OVER', 1, 'white')
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, rect)

            pygame.mixer.music.load('sound/gameover.mp3')
            pygame.mixer.music.play()

        if game.timer == 5100 and game.is_gameover:
            game_menu()


        print(f"{game.timer=}, {game.enemy_count=}")
        # 3.3 оновлення дисплея
        pygame.display.flip()
        clock.tick(FPS)


def clearing():
    # game.timer = 0
    # game.score = 0
    # game.stage = 1
    game.bullets.clear()
    game.bullets_enemy.clear()
    game.users_background = [(user_image, item) for item in users_background_location]
    # game.running = True
    # # game.menu_running = False
    game.__init__()

def game_continue():
    # game.menu_running = False
    game.running = True
    game_loop()


button_start = Button(screen, 200, "NEW GAME", clearing, game_loop)
# button_continue = Button(screen, 320, "Continue", game_loop)
# # button_continue = Button(screen, 320, "Continue", game_continue)
button_exit = Button(screen, 440, "EXIT")


def game_menu():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            button_start.mouse_event(event)
            # button_continue.mouse_event(event)
            if button_exit.mouse_event(event):
                running = False

        screen.fill((16, 69, 79))
        screen.blit(background_menu, (0, 0))

        text = fontBig.render('BATTLE TANKS ARENA', 1, (35, 57, 55))
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20 ))

        screen.blit(text, rect)
        button_start.blitme()
        # button_continue.blitme()
        button_exit.blitme()

        pygame.display.flip()
        clock.tick(FPS)


# game_loop()
game_menu()

with open("hiscore.txt", 'w') as f:
    f.write(str(game.hiscore))

pygame.quit()
