import pygame
import random
import sys
import math

# ============================================================
# INITIALIZATION
# ============================================================

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 400, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Jumpscare Edition")

clock = pygame.time.Clock()
FPS = 60


# ============================================================
# COLORS
# ============================================================

WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 100, 255)
BLACK = (0, 0, 0)


# ============================================================
# PLAYER SETTINGS
# ============================================================

bird_x = 50
bird_y = HEIGHT // 2

bird_radius = 15

gravity = 0.3
velocity = 0
jump_strength = -7


# ============================================================
# PIPE SETTINGS
# ============================================================

pipe_width = 70
pipe_gap = 150
pipe_speed = 3

pipes = []

score = 0


# ============================================================
# FONTS
# ============================================================

font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 80)
timer_font = pygame.font.SysFont(None, 60)


# ============================================================
# ASSETS
# ============================================================

# ------------------------------------------------------------
# PLAYER PNG
# ------------------------------------------------------------

player_img = pygame.image.load(
    "pngwing.com (2).png"
).convert_alpha()

player_img = pygame.transform.scale(
    player_img,
    (40, 40)
)


# ------------------------------------------------------------
# ENEMY PNG
# ------------------------------------------------------------

enemy_img = pygame.image.load(
    "Creepy-Transparent.png"
).convert_alpha()

enemy_img = pygame.transform.scale(
    enemy_img,
    (60, 60)
)


# ------------------------------------------------------------
# JUMPSCARE IMAGE
# ------------------------------------------------------------

jumpscare_img = pygame.image.load(
    "The Smiling Man.jpg"
).convert_alpha()

jumpscare_img = pygame.transform.scale(
    jumpscare_img,
    (WIDTH, HEIGHT)
)


# ------------------------------------------------------------
# JUMPSCARE SOUND
# ------------------------------------------------------------

jumpscare_sound = pygame.mixer.Sound(
    "sound_effects75-robotic_jumpscare-485532.mp3"
)


# ------------------------------------------------------------
# GLITCH SOUND
# ------------------------------------------------------------

glitch_sound = pygame.mixer.Sound(
    "dragon-studio-glitch-effect-1-397982.wav"
)


# ------------------------------------------------------------
# NORMAL SOUNDTRACK
# ------------------------------------------------------------

soundtrack = pygame.mixer.Sound(
    "02. Hill Zone.mp3"
)


# ------------------------------------------------------------
# GLITCH SOUNDTRACK
# ------------------------------------------------------------

glitch_soundtrack = pygame.mixer.Sound(
    "dragon-studio-glitch-effect-1-397982.wav"
)


# ------------------------------------------------------------
# HORROR SOUNDTRACK
# ------------------------------------------------------------

sonic_drowned = pygame.mixer.Sound(
    "05. Death Chase (Drowning).mp3"
)


# ============================================================
# GAME STATES
# ============================================================

dark_theme = False

pipes_disabled = False

spikes_active = False

spike_height = 40

show_run_text = False
run_blink = 0


# ============================================================
# CHASE MODE
# ============================================================

chase_mode = False

# Enemy position
enemy_x = WIDTH + 150
enemy_y = HEIGHT // 2

# Enemy sangat lambat
enemy_speed = 0.45

enemy_radius = 22


# ============================================================
# 14 SECOND TIMER
# ============================================================

CHASE_DURATION = 14000

chase_start_time = 0

chase_finished = False


# ============================================================
# SURVIVED SCREEN
# ============================================================

survived_screen = False


# ============================================================
# DRAW PLAYER
# ============================================================

def draw_bird(x, y):

    screen.blit(
        player_img,
        (
            int(
                x
                - player_img.get_width() / 2
            ),
            int(
                y
                - player_img.get_height() / 2
            )
        )
    )


# ============================================================
# DRAW ENEMY
# ============================================================

def draw_enemy(x, y):

    screen.blit(
        enemy_img,
        (
            int(
                x
                - enemy_img.get_width() / 2
            ),
            int(
                y
                - enemy_img.get_height() / 2
            )
        )
    )


# ============================================================
# DRAW PIPES
# ============================================================

def draw_pipes(pipes):

    color = RED if dark_theme else GREEN

    for pipe in pipes:

        pygame.draw.rect(
            screen,
            color,
            pipe[0]
        )

        pygame.draw.rect(
            screen,
            color,
            pipe[1]
        )


# ============================================================
# DRAW SPIKES
# ============================================================

def draw_spikes():

    spike_width = 20

    for i in range(
        0,
        WIDTH,
        spike_width
    ):

        points = [
            (i, HEIGHT),

            (
                i + spike_width // 2,
                HEIGHT - spike_height
            ),

            (
                i + spike_width,
                HEIGHT
            )
        ]

        pygame.draw.polygon(
            screen,
            RED,
            points
        )


# ============================================================
# PIPE COLLISION
# ============================================================

def check_collision(
    bird_y,
    pipes
):

    # --------------------------------------------------------
    # TOP SCREEN
    # --------------------------------------------------------

    if (
        bird_y - bird_radius <= 0
    ):
        return True


    # --------------------------------------------------------
    # BOTTOM SCREEN
    # --------------------------------------------------------

    if (
        bird_y + bird_radius >= HEIGHT
    ):
        return True


    # --------------------------------------------------------
    # PIPES
    # --------------------------------------------------------

    for pipe in pipes:

        if pipe[0].collidepoint(
            bird_x,
            bird_y
        ):
            return True

        if pipe[1].collidepoint(
            bird_x,
            bird_y
        ):
            return True


    return False


# ============================================================
# SPIKE COLLISION
# ============================================================

def check_spike_collision(
    x,
    y
):

    return (
        y + bird_radius
        >= HEIGHT - spike_height
    )


# ============================================================
# ENEMY COLLISION
# ============================================================

def check_enemy_collision():

    distance = math.hypot(
        bird_x - enemy_x,
        bird_y - enemy_y
    )

    return (
        distance
        <= bird_radius + enemy_radius
    )


# ============================================================
# SHOW SCORE
# ============================================================

def show_score(score):

    score_text = font.render(
        f"Score:{score}",
        True,
        WHITE
    )

    screen.blit(
        score_text,
        (10, 10)
    )


# ============================================================
# JUMPSCARE
# ============================================================

def jumpscare():

    # --------------------------------------------------------
    # STOP ALL MUSIC
    # --------------------------------------------------------

    soundtrack.stop()

    glitch_soundtrack.stop()

    sonic_drowned.stop()


    # --------------------------------------------------------
    # SHOW JUMPSCARE
    # --------------------------------------------------------

    screen.blit(
        jumpscare_img,
        (0, 0)
    )


    # --------------------------------------------------------
    # PLAY JUMPSCARE SOUND
    # --------------------------------------------------------

    jumpscare_sound.play()


    pygame.display.update()

    pygame.time.delay(2000)


# ============================================================
# GAME OVER
# ============================================================

def show_game_over(score):

    game_over_text = font.render(
        "GAME OVER",
        True,
        WHITE
    )

    score_text = font.render(
        f"Final Score:{score}",
        True,
        WHITE
    )


    screen.blit(
        game_over_text,
        (
            WIDTH // 2
            - game_over_text.get_width() // 2,
            HEIGHT // 2 - 40
        )
    )


    screen.blit(
        score_text,
        (
            WIDTH // 2
            - score_text.get_width() // 2,
            HEIGHT // 2 + 10
        )
    )


    pygame.display.update()

    pygame.time.delay(2000)


# ============================================================
# GLITCH TRANSITION
# ============================================================

def glitch_transition():

    # --------------------------------------------------------
    # GLITCH SOUND
    # --------------------------------------------------------

    glitch_sound.play()

    glitch_soundtrack.play()


    # --------------------------------------------------------
    # GLITCH VISUAL
    # --------------------------------------------------------

    for i in range(10):

        random_color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )

        screen.fill(
            random_color
        )

        pygame.display.update()

        pygame.time.delay(50)


    # --------------------------------------------------------
    # STOP GLITCH
    # --------------------------------------------------------

    glitch_soundtrack.stop()


    # --------------------------------------------------------
    # START HORROR MUSIC
    # --------------------------------------------------------

    sonic_drowned.play(-1)


# ============================================================
# SURVIVED SCREEN
# ============================================================

def draw_survived_screen():

    screen.fill(BLACK)


    # --------------------------------------------------------
    # SURVIVED TEXT
    # --------------------------------------------------------

    survived_text = big_font.render(
        "SURVIVED!",
        True,
        WHITE
    )


    survived_x = (
        WIDTH // 2
        - survived_text.get_width() // 2
    )


    survived_y = (
        HEIGHT // 2
        - survived_text.get_height() // 2
        - 30
    )


    screen.blit(
        survived_text,
        (
            survived_x,
            survived_y
        )
    )


    # --------------------------------------------------------
    # SCORE
    # --------------------------------------------------------

    score_text = font.render(
        f"Score: {score}",
        True,
        WHITE
    )


    score_x = (
        WIDTH // 2
        - score_text.get_width() // 2
    )


    screen.blit(
        score_text,
        (
            score_x,
            HEIGHT // 2 + 45
        )
    )


    # --------------------------------------------------------
    # CONTINUE TEXT
    # --------------------------------------------------------

    continue_text = font.render(
        "Press SPACE to continue",
        True,
        RED
    )


    continue_x = (
        WIDTH // 2
        - continue_text.get_width() // 2
    )


    screen.blit(
        continue_text,
        (
            continue_x,
            HEIGHT - 70
        )
    )


# ============================================================
# RESET GAME
# ============================================================

def reset_game():

    global bird_x
    global bird_y
    global velocity
    global pipes
    global score

    global dark_theme
    global spikes_active

    global show_run_text
    global run_blink

    global pipes_disabled

    global chase_mode
    global enemy_x
    global enemy_y

    global chase_start_time
    global chase_finished

    global survived_screen


    # --------------------------------------------------------
    # PLAYER
    # --------------------------------------------------------

    bird_x = 50

    bird_y = HEIGHT // 2

    velocity = 0


    # --------------------------------------------------------
    # PIPES
    # --------------------------------------------------------

    pipes = []


    # --------------------------------------------------------
    # SCORE
    # --------------------------------------------------------

    score = 0


    # --------------------------------------------------------
    # THEME
    # --------------------------------------------------------

    dark_theme = False


    # --------------------------------------------------------
    # SPIKES
    # --------------------------------------------------------

    spikes_active = False


    # --------------------------------------------------------
    # RUN
    # --------------------------------------------------------

    show_run_text = False

    run_blink = 0


    # --------------------------------------------------------
    # PIPES
    # --------------------------------------------------------

    pipes_disabled = False


    # --------------------------------------------------------
    # CHASE
    # --------------------------------------------------------

    chase_mode = False

    enemy_x = WIDTH + 150

    enemy_y = HEIGHT // 2


    # --------------------------------------------------------
    # TIMER
    # --------------------------------------------------------

    chase_start_time = 0

    chase_finished = False


    # --------------------------------------------------------
    # SURVIVED
    # --------------------------------------------------------

    survived_screen = False


    # --------------------------------------------------------
    # STOP MUSIC
    # --------------------------------------------------------

    soundtrack.stop()

    glitch_soundtrack.stop()

    sonic_drowned.stop()


# ============================================================
# GAME VARIABLES
# ============================================================

running = True

main_menu = True

game_active = False

menu_time = 0


# ============================================================
# MAIN GAME LOOP
# ============================================================

while running:


    # ========================================================
    # SURVIVED SCREEN
    # ========================================================

    if survived_screen:

        draw_survived_screen()

        pygame.display.update()


        for e in pygame.event.get():

            if e.type == pygame.QUIT:

                running = False

                pygame.quit()

                sys.exit()


            if (
                e.type == pygame.KEYDOWN
                and e.key == pygame.K_SPACE
            ):

                survived_screen = False

                game_active = False

                main_menu = True


        clock.tick(FPS)

        continue


    # ========================================================
    # BACKGROUND
    # ========================================================

    if dark_theme:

        screen.fill(
            (10, 10, 10)
        )

    else:

        screen.fill(
            BLACK
        )


    # ========================================================
    # MAIN MENU
    # ========================================================

    if main_menu:

        title = font.render(
            "Flappy Bird Jumpscare",
            True,
            WHITE
        )


        start_text = font.render(
            "Press SPACE to start",
            True,
            WHITE
        )


        screen.blit(
            title,
            (
                WIDTH // 2
                - title.get_width() // 2,
                HEIGHT // 3
            )
        )


        screen.blit(
            start_text,
            (
                WIDTH // 2
                - start_text.get_width() // 2,
                HEIGHT // 2
            )
        )


        # ----------------------------------------------------
        # MENU BIRD ANIMATION
        # ----------------------------------------------------

        menu_time += 0.05


        menu_bird_y = (
            HEIGHT // 2
            + int(
                math.sin(menu_time)
                * 20
            )
        )


        draw_bird(
            WIDTH // 2,
            menu_bird_y
        )


        pygame.display.update()


        # ----------------------------------------------------
        # MENU EVENTS
        # ----------------------------------------------------

        for e in pygame.event.get():

            if e.type == pygame.QUIT:

                running = False

                pygame.quit()

                sys.exit()


            if (
                e.type == pygame.KEYDOWN
                and e.key == pygame.K_SPACE
            ):

                reset_game()

                main_menu = False

                game_active = True


    # ========================================================
    # GAME ACTIVE
    # ========================================================

    elif game_active:


        # ====================================================
        # EVENTS
        # ====================================================

        for e in pygame.event.get():

            if e.type == pygame.QUIT:

                running = False

                pygame.quit()

                sys.exit()


            if (
                e.type == pygame.KEYDOWN
                and e.key == pygame.K_SPACE
            ):

                velocity = jump_strength


        # ====================================================
        # BIRD PHYSICS
        # ====================================================

        velocity += gravity

        bird_y += velocity


        # ====================================================
        # NORMAL PIPE MODE
        # ====================================================

        if not chase_mode:


            # ------------------------------------------------
            # SPAWN PIPE
            # ------------------------------------------------

            if (
                not pipes_disabled
                and (
                    len(pipes) == 0
                    or pipes[-1][0].x
                    < WIDTH - 200
                )
            ):

                h = random.randint(
                    100,
                    400
                )


                top_pipe = pygame.Rect(
                    WIDTH,
                    0,
                    pipe_width,
                    h
                )


                bottom_pipe = pygame.Rect(
                    WIDTH,
                    h + pipe_gap,
                    pipe_width,
                    HEIGHT
                    - h
                    - pipe_gap
                )


                pipes.append(
                    (
                        top_pipe,
                        bottom_pipe
                    )
                )


            # ------------------------------------------------
            # MOVE PIPES
            # ------------------------------------------------

            new_pipes = []


            for p in pipes:

                p[0].x -= pipe_speed

                p[1].x -= pipe_speed


                if (
                    p[0].x + pipe_width > 0
                ):

                    new_pipes.append(p)


                else:

                    # ========================================
                    # SCORE
                    # ========================================

                    score += 1


                    # ========================================
                    # SCORE > 20
                    # ========================================

                    if (
                        score > 20
                        and not dark_theme
                    ):

                        dark_theme = True

                        soundtrack.play(
                            -1,
                            fade_ms=2000
                        )


                    # ========================================
                    # SCORE == 30
                    # ========================================

                    if (
                        score == 30
                        and not pipes_disabled
                    ):

                        # ------------------------------------
                        # STOP NORMAL SOUNDTRACK
                        # ------------------------------------

                        soundtrack.fadeout(
                            1000
                        )


                        # ------------------------------------
                        # DELETE PIPES
                        # ------------------------------------

                        pipes = []

                        new_pipes = []

                        pipes_disabled = True


                        # ------------------------------------
                        # CENTER PLAYER
                        # ------------------------------------

                        bird_x = WIDTH // 2

                        bird_y = HEIGHT // 2

                        velocity = 0


                        # ------------------------------------
                        # RUN TEXT
                        # ------------------------------------

                        show_run_text = True

                        run_blink = 0


                        # ------------------------------------
                        # GLITCH
                        # ------------------------------------

                        glitch_transition()


                        # ------------------------------------
                        # START CHASE
                        # ------------------------------------

                        chase_mode = True


                        # ------------------------------------
                        # ENEMY POSITION
                        # ------------------------------------

                        enemy_x = WIDTH + 150

                        enemy_y = random.randint(
                            100,
                            HEIGHT - 100
                        )


                        # ------------------------------------
                        # START TIMER
                        # ------------------------------------

                        chase_start_time = (
                            pygame.time.get_ticks()
                        )

                        chase_finished = False


            pipes = new_pipes


        # ====================================================
        # CHASE MODE
        # ====================================================

        if chase_mode:


            # =================================================
            # TIMER
            # =================================================

            elapsed_time = (
                pygame.time.get_ticks()
                - chase_start_time
            )


            remaining_time = max(
                0,
                CHASE_DURATION
                - elapsed_time
            )


            remaining_seconds = math.ceil(
                remaining_time / 1000
            )


            # =================================================
            # ENEMY MOVEMENT
            # =================================================

            dx = bird_x - enemy_x

            dy = bird_y - enemy_y


            distance = math.hypot(
                dx,
                dy
            )


            if distance > 0:

                enemy_x += (
                    dx
                    / distance
                    * enemy_speed
                )


                enemy_y += (
                    dy
                    / distance
                    * enemy_speed
                )


            # =================================================
            # TIMER DISPLAY
            # =================================================

            timer_text = timer_font.render(
                str(remaining_seconds),
                True,
                RED
            )


            timer_x = (
                WIDTH // 2
                - timer_text.get_width() // 2
            )


            timer_y = 15


            screen.blit(
                timer_text,
                (
                    timer_x,
                    timer_y
                )
            )


            # =================================================
            # ENEMY COLLISION
            # =================================================

            if check_enemy_collision():

                jumpscare()

                print(
                    "Perished"
                )

                game_active = False

                main_menu = True


            # =================================================
            # 14 SECONDS FINISHED
            # =================================================

            if (
                remaining_time <= 0
                and not chase_finished
            ):

                chase_finished = True


                # --------------------------------------------
                # STOP HORROR MUSIC
                # --------------------------------------------

                sonic_drowned.fadeout(
                    1000
                )


                # --------------------------------------------
                # STOP CHASE
                # --------------------------------------------

                chase_mode = False


                # --------------------------------------------
                # HIDE RUN
                # --------------------------------------------

                show_run_text = False


                # --------------------------------------------
                # SURVIVED SCREEN
                # --------------------------------------------

                survived_screen = True


                # --------------------------------------------
                # STOP PLAYER
                # --------------------------------------------

                velocity = 0


                # --------------------------------------------
                # RESET ENEMY
                # --------------------------------------------

                enemy_x = WIDTH + 150

                enemy_y = HEIGHT // 2


        # ====================================================
        # DRAW PIPES
        # ====================================================

        if not chase_mode:

            draw_pipes(
                pipes
            )


        # ====================================================
        # DRAW SPIKES
        # ====================================================

        if spikes_active:

            draw_spikes()


        # ====================================================
        # DRAW PLAYER
        # ====================================================

        draw_bird(
            bird_x,
            bird_y
        )


        # ====================================================
        # DRAW ENEMY
        # ====================================================

        if chase_mode:

            draw_enemy(
                enemy_x,
                enemy_y
            )


        # ====================================================
        # SCORE
        # ====================================================

        show_score(
            score
        )


        # ====================================================
        # RUN TEXT
        # ====================================================

        if (
            show_run_text
            and chase_mode
        ):

            run_blink += 1


            # ------------------------------------------------
            # BLINK
            # ------------------------------------------------

            if (
                run_blink // 15
            ) % 2 == 0:

                run_text = big_font.render(
                    "RUN!",
                    True,
                    RED
                )


                # ------------------------------------------------
                # CENTER HORIZONTAL
                # ------------------------------------------------

                run_x = (
                    WIDTH // 2
                    - run_text.get_width() // 2
                )


                # ------------------------------------------------
                # BOTTOM SCREEN
                # ------------------------------------------------

                run_y = (
                    HEIGHT
                    - run_text.get_height()
                    - 20
                )


                screen.blit(
                    run_text,
                    (
                        run_x,
                        run_y
                    )
                )


        # ====================================================
        # NORMAL COLLISION
        # ====================================================

        if not chase_mode:


            # ------------------------------------------------
            # PIPE / WALL COLLISION
            # ------------------------------------------------

            if (
                not dark_theme
                and check_collision(
                    bird_y,
                    pipes
                )
            ):

                if score <= 20:

                    show_game_over(
                        score
                    )

                    print(
                        "Game Over! Score:",
                        score
                    )

                else:

                    jumpscare()

                    print(
                        "Game Over (Jumpscare)! Score:",
                        score
                    )


                game_active = False

                main_menu = True


            # ------------------------------------------------
            # SPIKE COLLISION
            # ------------------------------------------------

            if (
                spikes_active
                and check_spike_collision(
                    bird_x,
                    bird_y
                )
            ):

                jumpscare()

                print(
                    "Game Over (Spike)! Score:",
                    score
                )

                game_active = False

                main_menu = True


        # ====================================================
        # UPDATE DISPLAY
        # ====================================================

        pygame.display.update()


    # ========================================================
    # FPS
    # ========================================================

    clock.tick(FPS)


# ============================================================
# QUIT
# ============================================================

pygame.quit()
