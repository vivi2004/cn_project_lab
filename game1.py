import pygame
import socket
import pickle
from sys import exit

# UDP setup
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('<SERVER_IP>', 9999)  # Replace with actual server IP
client_socket.setblocking(False)

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Fighting Club")
clock = pygame.time.Clock()

# Load assets
sky_surface = pygame.image.load('Sky.png').convert()
ground_surface = pygame.image.load('ground.png').convert()

# Player 1 animations
player1_walk = [
    pygame.image.load('Player/player_walk_1.png').convert_alpha(),
    pygame.image.load('Player/player_walk_2.png').convert_alpha()
]
player1_attack = pygame.image.load('Player/player_stand.png').convert_alpha()
player1_jump = pygame.image.load('Player/jump.png').convert_alpha()

player1_index = 0
player1_surface = player1_walk[player1_index]
player1_rect = player1_surface.get_rect(midbottom=(100, 300))

# Player 2 animations
player2_walk = [
    pygame.transform.flip(player1_walk[0], True, False),
    pygame.transform.flip(player1_walk[1], True, False)
]
player2_attack = pygame.transform.flip(player1_attack, True, False)
player2_jump = pygame.transform.flip(player1_jump, True, False)
player2_index = 0
player2_surface = player2_walk[player2_index]
player2_rect = player2_surface.get_rect(midbottom=(700, 300))

# States
gravity = 1
jump_velocity = 0
is_jumping = False
is_attacking = False
attack_timer = 0
ground_level = 300

# Player 2 state (from server)
player2_state = {
    "x": 700,
    "y": 300,
    "is_jumping": False,
    "is_attacking": False,
    "moving": False,
    "frame": 0
}

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()
    moving = False

    # Player 1 movement
    if keys[pygame.K_LEFT]:
        player1_rect.x -= 5
        moving = True
    elif keys[pygame.K_RIGHT]:
        player1_rect.x += 5
        moving = True

    if player1_rect.left < 0:
        player1_rect.left = 0
    if player1_rect.right > 800:
        player1_rect.right = 800

    # Player 1 jump
    if keys[pygame.K_UP] and not is_jumping:
        is_jumping = True
        jump_velocity = -15

    if is_jumping:
        player1_surface = player1_jump
        player1_rect.y += jump_velocity
        jump_velocity += gravity
        if player1_rect.bottom >= ground_level:
            player1_rect.bottom = ground_level
            is_jumping = False
            jump_velocity = 0

    # Player 1 attack
    if keys[pygame.K_SPACE] and not is_attacking:
        is_attacking = True
        attack_timer = 10

    if is_attacking:
        player1_surface = player1_attack
        attack_timer -= 1
        if attack_timer <= 0:
            is_attacking = False
    elif moving and not is_jumping:
        player1_index += 0.1
        if player1_index >= len(player1_walk):
            player1_index = 0
        player1_surface = player1_walk[int(player1_index)]
    elif not is_jumping:
        player1_surface = player1_walk[0]

    # --- Receive Player 2 state from server ---
    try:
        data, _ = client_socket.recvfrom(1024)
        player2_state = pickle.loads(data)
    except BlockingIOError:
        pass

    # Apply received Player 2 state
    player2_rect.x = player2_state['x']
    player2_rect.y = player2_state['y']
    if player2_state["is_jumping"]:
        player2_surface = player2_jump
    elif player2_state["is_attacking"]:
        player2_surface = player2_attack
    elif player2_state["moving"]:
        player2_index = player2_state["frame"] % len(player2_walk)
        player2_surface = player2_walk[int(player2_index)]
    else:
        player2_surface = player2_walk[0]

    # Drawing
    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 300))
    screen.blit(player1_surface, player1_rect)
    screen.blit(player2_surface, player2_rect)

    pygame.display.update()
    clock.tick(60)
