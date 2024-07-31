import sys
import pygame
from pygame.locals import *
import ctypes
ctypes.windll.user32.SetProcessDPIAware()

from entities import (Planet, vec, calculate_planet_forces, check_collisions, DISPLAY_WIDTH, DISPLAY_HEIGHT,
                      calculate_center_of_mass, SCREEN_CENTER, print_debug_values, COLORS, Info)

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
is_physics_enabled = True

# test data
Planets = []
Trails = []
Planets.append(Planet(pos=vec((2000, 1000)), vel=vec((8, 0)), mass=1000.0, color=COLORS["Red"]))
Planets.append(Planet(pos=vec((2000, 900)), vel=vec((-8, 0)), mass=1000.0, color=COLORS["Blue"]))
Planets.append(Planet(pos=vec((2000, 100)), vel=vec((2.5, 0)), mass=100.0, color=COLORS["Grey"]))

center_of_mass_pos = vec((0, 0))
view_id = 0
views_amount = 0
view_offset = vec((0, 0))
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
            elif event.key == K_SPACE:
                is_physics_enabled = not is_physics_enabled
            elif event.key == K_TAB:
                view_id += 1

    display_surface.fill((0, 0, 0))
    views_amount = len(Planets) + 1
    if view_id > views_amount:
        view_id = 0

    if is_physics_enabled:
        calculate_planet_forces(Planets)
        Planets = check_collisions(Planets)

        center_of_mass_pos = calculate_center_of_mass(Planets)

        for trail in Trails:
            is_flagged_for_deletion = trail.update()
            if is_flagged_for_deletion:
                Trails.remove(trail)

        for planet in Planets:
            new_trail = planet.move(bounce_screen)
            Trails.append(new_trail)

    if view_id == 0:
        view_offset = vec((0, 0))
    elif view_id == 1:
        view_offset = center_of_mass_pos - SCREEN_CENTER
    else:
        for index, planet in enumerate(Planets):
            if index == view_id - 2:
                view_offset = planet.pos - SCREEN_CENTER
                break

    for planet in Planets:
        planet.refresh(display_surface, view_offset)
    for trail in Trails:
        trail.refresh(display_surface, view_offset)

    Info.draw_center_of_mass(center_of_mass_pos - view_offset, display_surface)

    # debug
    print_debug_values([f"Trails: {len(Trails)}",
                        f"Planets: {len(Planets)}",
                        f"Center of mass: {center_of_mass_pos.x:.0f}, {center_of_mass_pos.y:.0f}",
                        f"Physics: {is_physics_enabled}",
                        f"View_id: {view_id}"],
                       font=standard_font, surface=display_surface)

    # refresh screen
    pygame.display.update()

    # wait for tick to next frame
    FramePerSec.tick(FPS)
