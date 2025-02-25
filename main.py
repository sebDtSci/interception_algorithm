import pygame
import numpy as np
from config import *
from interception import predict_interception

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

target_pos = np.array([100, 300], dtype=np.float64)
target_vel = np.array([2.5, 1.0], dtype=np.float64)  # Mouvement diagonal

interceptor_pos = np.array([600, 500], dtype=np.float64)
interceptor_angle = 0  # En radians

running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    target_pos += target_vel

    interception_point = predict_interception(target_pos, target_vel, interceptor_pos, INTERCEPTOR_SPEED)

    if interception_point is not None:
        # Calculer l'angle vers le point d'interception
        direction = interception_point - interceptor_pos
        target_angle = np.arctan2(direction[1], direction[0])

        # Ajuster progressivement l'angle de l'intercepteur
        angle_diff = (target_angle - interceptor_angle) % (2 * np.pi)
        if angle_diff > np.pi:
            angle_diff -= 2 * np.pi
        interceptor_angle += np.clip(angle_diff, -TURN_RATE, TURN_RATE)

        # Mettre à jour la position de l'intercepteur
        interceptor_pos += INTERCEPTOR_SPEED * np.array([np.cos(interceptor_angle), np.sin(interceptor_angle)])

    pygame.draw.circle(screen, RED, target_pos.astype(int), 10)

    pygame.draw.circle(screen, BLUE, interceptor_pos.astype(int), 10)

    # trajectoire d'interception
    if interception_point is not None:
        pygame.draw.circle(screen, WHITE, interception_point.astype(int), 5)
        pygame.draw.line(screen, WHITE, interceptor_pos.astype(int), interception_point.astype(int), 1)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()