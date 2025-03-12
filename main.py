import pygame
import numpy as np
from config import *
from interception import predict_interception

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

start_button = pygame.Rect(50, 50, 80, 30)
reset_button = pygame.Rect(150, 50, 80, 30)
pause_button = pygame.Rect(250, 50, 80, 30)

running = True
simulation_running = False
paused = False

def reset_simulation():
    global target_pos, interceptor_pos, interceptor_angle, simulation_running, paused
    target_pos[:] = [100, 0]
    interceptor_pos[:] = [500, 500]
    interceptor_angle = 0
    simulation_running = False
    paused = False

target_pos = np.array([100, 0], dtype=np.float64)
target_vel = np.array([2.5, 1.0], dtype=np.float64)
interceptor_pos = np.array([500, 500], dtype=np.float64)
interceptor_angle = 0  # En radians

while running:
    screen.fill(BLACK)
    
    pygame.draw.rect(screen, (100, 200, 100), start_button)
    pygame.draw.rect(screen, (200, 100, 100), reset_button)
    pygame.draw.rect(screen, (100, 100, 200), pause_button)

    pygame.draw.circle(screen, RED, target_pos.astype(int), 10)
    pygame.draw.circle(screen, BLUE, interceptor_pos.astype(int), 10)
    
    font = pygame.font.Font(None, 30)
    screen.blit(font.render("Start", True, WHITE), (start_button.x +15, start_button.y + 10))
    screen.blit(font.render("Reset", True, WHITE), (reset_button.x +15, reset_button.y + 10))
    screen.blit(font.render("Pause", True, WHITE), (pause_button.x +15, pause_button.y + 10))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                simulation_running = True
                paused = False
            elif reset_button.collidepoint(event.pos):
                reset_simulation()
            elif pause_button.collidepoint(event.pos):
                paused = not paused
    
    if simulation_running and not paused:
        target_pos += target_vel
        interception_point = predict_interception(target_pos, target_vel, interceptor_pos, INTERCEPTOR_SPEED)
        
        if interception_point is not None:
            direction = interception_point - interceptor_pos
            target_angle = np.arctan2(direction[1], direction[0])
            
            angle_diff = (target_angle - interceptor_angle) % (2 * np.pi)
            if angle_diff > np.pi:
                angle_diff -= 2 * np.pi
            interceptor_angle += np.clip(angle_diff, -TURN_RATE, TURN_RATE)
            
            interceptor_pos += INTERCEPTOR_SPEED * np.array([np.cos(interceptor_angle), np.sin(interceptor_angle)])
            pygame.draw.circle(screen, WHITE, interception_point.astype(int), 5)
            pygame.draw.line(screen, WHITE, interceptor_pos.astype(int), interception_point.astype(int), 1)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
