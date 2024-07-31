import pygame

vec = pygame.Vector2
GRAVITY_CONSTANT = 10.0
TRAIL_LIFE = 600
TRAIL_RADIUS = 2
DISPLAY_WIDTH = 1920
DISPLAY_HEIGHT = 1080
SCREEN_CENTER = vec((0, DISPLAY_HEIGHT / 2))


class Trail:
    def __init__(self, pos: vec, color: tuple):
        self.pos = pos
        self.color = color
        self.life = TRAIL_LIFE

    def update(self, surface: pygame.Surface, offset: vec) -> bool:
        if self.life <= 0:
            return True
        else:
            self.life -= 1
            value = self.life / TRAIL_LIFE
            r = self.color[0]
            g = self.color[1]
            b = self.color[2]
            new_r = int(r * value)
            new_g = int(g * value)
            new_b = int(b * value)
            self.color = (new_r, new_g, new_b)
            pygame.draw.circle(surface=surface, color=self.color, center=self.pos + offset, radius=TRAIL_RADIUS)
            return False


class Planet:
    def __init__(self, pos: vec, vel: vec, mass: float, radius: float, color: tuple):
        self.pos = pos
        self.vel = vel
        self.mass = mass
        self.radius = radius
        self.color = color

    def refresh(self, surface: pygame.Surface, offset: vec):
        pygame.draw.circle(surface=surface, color=self.color, center=self.pos + offset, radius=self.radius)

    def move(self, bounce: bool) -> Trail:
        previous_pos = self.pos.copy()
        self.pos += self.vel
        if bounce:
            if self.pos.x < 0 or self.pos.x > DISPLAY_WIDTH:
                self.vel.x = -self.vel.x
            if self.pos.y < 0 or self.pos.y > DISPLAY_HEIGHT:
                self.vel.y = -self.vel.y

        return Trail(pos=previous_pos, color=self.color)

    def calc_velocity(self, force: vec):
        self.vel += force / self.mass

    def calc_density(self) -> float:
        return self.mass / (self.radius ** 3)


def calculate_radius_from_mass(density: float, mass: float) -> float:
    return (mass / density) ** (1 / 3)


def calculate_force_between_planets(planet_a: Planet, planet_b: Planet) -> vec:
    distance_x = planet_a.pos.x - planet_b.pos.x
    distance_y = planet_a.pos.y - planet_b.pos.y
    distance = vec((distance_x, distance_y)).length()
    force_value = ((planet_a.mass * planet_b.mass) / (distance * distance)) * GRAVITY_CONSTANT
    force_vector = vec((distance_x, distance_y)).normalize()
    force_vector.scale_to_length(force_value)
    return -force_vector


def calculate_planet_forces(planet_list: list):
    for planet_a in planet_list:
        planet_a_force = vec((0, 0))
        for planet_b in planet_list:
            if planet_a is not planet_b:
                planet_a_force += calculate_force_between_planets(planet_a, planet_b)
        planet_a.calc_velocity(planet_a_force)


def calculate_center_of_mass(planet_list: list) -> vec:
    x_weighted = 0.0
    y_weighted = 0.0
    total_mass = 0.0
    for planet in planet_list:
        x_weighted += planet.pos.x * planet.mass
        y_weighted -= planet.pos.y * planet.mass
        total_mass += planet.mass
    return vec((x_weighted / total_mass, y_weighted / total_mass))


def combine_colors(a: tuple, b: tuple) -> tuple:
    c = [0, 0, 0]
    for i in range(3):
        new_a = a[i] / 255
        new_b = b[i] / 255
        c[i] = int((new_a + new_b) / 2 * 255)
    return tuple(c)


def check_collisions(planet_list: list) -> list:
    collisions_detected = True
    while(collisions_detected):
        collisions_detected = False
        for planet_a in planet_list:
            for planet_b in planet_list:
                if planet_a is not planet_b:
                    distance = (vec((planet_a.pos.x, planet_a.pos.y)) - vec((planet_b.pos.x, planet_b.pos.y))).length()
                    if distance < planet_a.radius + planet_b.radius:
                        total_mass = planet_a.mass + planet_b.mass
                        momentum = planet_a.vel * planet_a.mass + planet_b.vel * planet_b.mass
                        new_vel = momentum / total_mass
                        if planet_a.mass * 2 < planet_b.mass:
                            new_pos = planet_b.pos
                        elif planet_b.mass * 2 < planet_a.mass:
                            new_pos = planet_a.pos
                        else:
                            new_pos = (planet_a.pos + planet_b.pos) / 2
                        color_a = planet_a.color
                        color_b = planet_b.color
                        new_color = combine_colors(color_a, color_b)
                        new_density = (planet_a.calc_density() + planet_b.calc_density()) / 2
                        new_radius = calculate_radius_from_mass(new_density, total_mass)
                        planet_list.remove(planet_a)
                        planet_list.remove(planet_b)
                        planet_list.append(Planet(pos=new_pos, vel=new_vel, mass=total_mass, radius=new_radius, color=new_color))
                        collisions_detected = True
                        break
    return planet_list