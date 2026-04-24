# main.py
import pygame
import sys
from config import *
from environment import Environment
from agent import CarAgent

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT + 100)) # Extra space for status
    pygame.display.set_caption("Tesla Autonomous Simulation")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18, bold=True)

    env = Environment()
    car = CarAgent(env.start_pos, env.goal_pos)
    car.plan_path(env.obstacles)

    running = True
    sim_started = False
    status_msg = "SPACE: Start/Pause | R: Reset | O: Add Obstacle | T: Toggle Signal"

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    sim_started = not sim_started
                if event.key == pygame.K_t:
                    state = env.toggle_signal()
                    status_msg = f"Traffic Signal: {state}"
                if event.key == pygame.K_o:
                    # Random obstacle
                    import random
                    new_obs = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
                    if env.add_obstacle(new_obs):
                        status_msg = "New obstacle added!"
                        # Prompt re-plan if moving
                        if sim_started:
                            car.plan_path(env.obstacles)
                if event.key == pygame.K_r:
                    # Reset
                    env.reset_environment()
                    car = CarAgent(env.start_pos, env.goal_pos)
                    car.plan_path(env.obstacles)
                    sim_started = False
                    status_msg = "Simulation Reset!"

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Add obstacle on click
                x, y = event.pos
                if y < HEIGHT:
                    grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE
                    if env.add_obstacle((grid_x, grid_y)):
                        status_msg = f"Obstacle added at ({grid_x}, {grid_y})"
                        if sim_started:
                            car.plan_path(env.obstacles)

        # Update
        if sim_started:
            new_pos, state = car.move(env)
            if state == "REACHED_GOAL":
                status_msg = "🎯 Destination reached!"
                sim_started = False
            elif state == "BLOCKED_NO_PATH":
                 status_msg = "❌ No path available!"
                 sim_started = False
            elif state == "MOVING":
                 status_msg = f"Moving... ({new_pos})"
            elif state == "WAITING_SIGNAL":
                 status_msg = "🚦 Waiting for green signal..."

        # Draw
        screen.fill(COLOR_ROAD)

        # Draw Grid
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(screen, COLOR_GRID, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(screen, COLOR_GRID, (0, y), (WIDTH, y))

        # Draw Obstacles
        for obs in env.obstacles:
            pygame.draw.rect(screen, COLOR_OBSTACLE, (obs[0]*CELL_SIZE, obs[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw Path
        if car.path:
            for i in range(car.path_index, len(car.path) - 1):
                p1 = car.path[i]
                p2 = car.path[i+1]
                pygame.draw.line(screen, COLOR_PATH, 
                                 (p1[0]*CELL_SIZE + CELL_SIZE//2, p1[1]*CELL_SIZE + CELL_SIZE//2),
                                 (p2[0]*CELL_SIZE + CELL_SIZE//2, p2[1]*CELL_SIZE + CELL_SIZE//2), 4)

        # Draw Start & Goal
        pygame.draw.rect(screen, COLOR_START, (env.start_pos[0]*CELL_SIZE, env.start_pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, COLOR_GOAL, (env.goal_pos[0]*CELL_SIZE, env.goal_pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw Car
        pygame.draw.circle(screen, COLOR_CAR, (car.pos[0]*CELL_SIZE + CELL_SIZE//2, car.pos[1]*CELL_SIZE + CELL_SIZE//2), CELL_SIZE//3)

        # UI / Status Area
        pygame.draw.rect(screen, (220, 220, 220), (0, HEIGHT, WIDTH, 100))
        
        # Signal indicator
        sig_color = COLOR_SIGNAL_GREEN if env.signal_state == "GREEN" else COLOR_SIGNAL_RED
        pygame.draw.circle(screen, sig_color, (30, HEIGHT + 50), 15)
        
        txt_surf = font.render(status_msg, True, COLOR_TEXT)
        screen.blit(txt_surf, (60, HEIGHT + 40))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
