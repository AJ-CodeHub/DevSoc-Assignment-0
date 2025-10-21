import pygame, sys, random

pygame.init()
pygame.display.set_mode()
pygame.mixer.init()
pygame.font.init()
hit_sound1 = pygame.mixer.Sound("hit1.mp3")
hit_sound2 = pygame.mixer.Sound("hit2.mp3")
score_sound = pygame.mixer.Sound("Score.mp3")

paddle = pygame.image.load("paddle.png").convert_alpha()
paddle = pygame.transform.scale(paddle, (100, 100))

paddle1 = pygame.image.load("paddle1.png").convert_alpha()
paddle1 = pygame.transform.scale(paddle1, (100, 100))

ball_pic = pygame.image.load("Ball.png").convert_alpha()
ball_pic = pygame.transform.scale(ball_pic, (40, 40))

player_score = 0
opponent_score = 0
game_font = pygame.font.Font(None, 74)



def ball_animation():
    global ball_speed_x, ball_speed_y
    global player_score, opponent_score
    
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
        hit_sound2.play()
    
    if ball.left <= 0:
        player_score += 1
        ball_start()
        score_sound.play()

    if ball.right >= screen_width:
        opponent_score += 1
        ball_start()
        score_sound.play()


    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1
        hit_sound1.play()


def player_animation():
    player.y += player_speed

    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def opponent_animation():
    opponent.y += opponent_speed

    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

def ball_start():
    global ball_speed_x, ball_speed_y
    ball_speed_x = 7 * random.choice((1,-1))
    ball_speed_y = 7 * random.choice((1,-1))

    ball.center = (screen_width/2, screen_height/2)
    ball_speed_y *= random.choice((1,-1))
    ball_speed_x *= random.choice((1,-1))

def draw_dashed_line(surface, color, start_pos, end_pos, width=6, dash_length=20, gap_length=10):
    x1, y1 = start_pos
    x2, y2 = end_pos

    y = y1
    while y < y2:
        pygame.draw.line(surface, color, (x1, y), (x1, min(y + dash_length, y2)), width)
        y += dash_length + gap_length

def start_screen():
    screen.blit(bg_start, (0, 0))

    # title_text = game_font.render("PONG", True, (255, 255, 255))
    # prompt_text = game_font.render("Press SPACE to start", True, (200, 200, 200))

    # screen.blit(title_text, (screen_width/2 - title_text.get_width()/2, screen_height/2 - 100))
    # screen.blit(prompt_text, (screen_width/2 - prompt_text.get_width()/2, screen_height/2 + 50))



# General setup
pygame.init()
clock = pygame.time.Clock()

# Main Window
screen_width = 1440
screen_height = 850
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Pong')

bg = pygame.image.load("bg.png").convert()
bg = pygame.transform.scale(bg, (screen_width, screen_height))

bg_start = pygame.image.load("PONG.png").convert()
bg_start = pygame.transform.scale(bg_start, (screen_width, screen_height))

# Colors
light_grey = (200,200,200)
bg_color = pygame.Color('grey12')

# Game Rectangles
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10,100)
opponent = pygame.Rect(10, screen_height / 2 - 70, 10,100)

# Game Variables
ball_speed_x = 7 * random.choice((1,-1))
ball_speed_y = 7 * random.choice((1,-1))
player_speed = 0
opponent_speed = 0

game_state = "start"

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_state == "start":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = "play"
                ball_start() 

    if game_state == "start":
        start_screen()
        pygame.display.flip()
        clock.tick(60)
        continue

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
            player_speed -= 1 
    elif keys[pygame.K_DOWN]:
        player_speed += 1

    if keys[pygame.K_w]:
        opponent_speed -= 1
    elif keys[pygame.K_s]:
        opponent_speed += 1

    player_speed *= 0.95
    opponent_speed *= 0.95

    ball_speed_x += 0.005*(abs(ball_speed_x)/ball_speed_x)
    ball_speed_y += 0.005*(abs(ball_speed_y)/ball_speed_y)

    # Game Logic
    ball_animation()
    player_animation()
    opponent_animation()


    # Visuals 
    screen.blit(bg, (0, 0))
    screen.blit(paddle1, (player.x - 8, player.y))
    screen.blit(paddle, (opponent.x - 8, opponent.y))
    screen.blit(ball_pic, ball)
    draw_dashed_line(screen, light_grey, (screen_width // 2, 0), (screen_width // 2, screen_height), width=8, dash_length=25, gap_length=15)


    player_text = game_font.render(f"{player_score}", True, light_grey)
    opponent_text = game_font.render(f"{opponent_score}", True, light_grey)

    screen.blit(opponent_text, (screen_width/2 - 60 - 30*(len(str(opponent_score))-1), 50))
    screen.blit(player_text, (screen_width/2 + 30, 50))


    pygame.display.flip()
    clock.tick(60)
