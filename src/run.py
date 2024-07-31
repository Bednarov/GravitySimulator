import sys
import pygame
from pygame.locals import *

from entities import (Planet, vec, calculate_planet_forces, check_collisions, DISPLAY_WIDTH, DISPLAY_HEIGHT,
                      calculate_center_of_mass, SCREEN_CENTER)

pygame.init()
print(f"\n\nGravity")
print("by Grzegorz Bednarczyk\n\n")

# setup pygame elements
FramePerSec = pygame.time.Clock()
display_surface = pygame.display.set_mode(size=(DISPLAY_WIDTH, DISPLAY_HEIGHT), flags=pygame.SCALED, vsync=1)
standard_font = pygame.font.SysFont("Arial", 24)
pygame.display.set_caption("Gravity")
FPS = 60
bounce_screen = False


# fonts
COLORS = {
    "White": (255, 255, 255),
    "Grey": (128, 128, 128),
    "Red": (255, 0, 0),
    "Green": (0, 255, 0),
    "Blue": (0, 0, 255),
    "DarkGrey": (50, 50, 50)
}

# test data
Planets = []
Trails = []
Planets.append(Planet(pos=vec((950, 100)), vel=vec((4, 0)), mass=1.0, radius=5.0, color=COLORS["Red"]))
Planets.append(Planet(pos=vec((500, 500)), vel=vec((0, -8)), mass=1000.0, radius=20.0, color=COLORS["White"]))
Planets.append(Planet(pos=vec((950, 300)), vel=vec((-4, -5)), mass=1.0, radius=5.0, color=COLORS["Green"]))
Planets.append(Planet(pos=vec((950, 330)), vel=vec((6, 0)), mass=0.03, radius=2.0, color=COLORS["Grey"]))
Planets.append(Planet(pos=vec((1300, 10)), vel=vec((0, 0)), mass=10.0, radius=5.0, color=COLORS["Green"]))
Planets.append(Planet(pos=vec((600, 500)), vel=vec((1, 7)), mass=1000.0, radius=20.0, color=COLORS["White"]))

while True:
    # read keys
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # check keyboard
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

    display_surface.fill((0, 0, 0))

    calculate_planet_forces(Planets)
    Planets = check_collisions(Planets)
    new_offset = calculate_center_of_mass(Planets)

    for index, trail in enumerate(Trails):
        is_flagged_for_deletion = trail.update(display_surface, new_offset + SCREEN_CENTER)
        if is_flagged_for_deletion:
            Trails.remove(trail)

    for planet in Planets:
        new_trail = planet.move(bounce_screen)
        Trails.append(new_trail)
        planet.refresh(display_surface, new_offset + SCREEN_CENTER)

    # debug
    text_y = 10
    text = standard_font.render(f"Trails: {len(Trails)}", True, COLORS["White"])
    text_rect = text.get_rect(topleft=(10, text_y))
    display_surface.blit(text, text_rect)
    text_y += text_rect.h + 1
    text = standard_font.render(f"Planets: {len(Planets)}", True, COLORS["White"])
    text_rect = text.get_rect(topleft=(10, text_y))
    display_surface.blit(text, text_rect)

    # refresh screen
    pygame.display.update()

    # wait for tick to next frame
    FramePerSec.tick(FPS)
