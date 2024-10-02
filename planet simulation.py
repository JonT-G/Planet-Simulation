import pygame
import math
#import random
pygame.init()

# Window dimensions
width, height = 800, 800
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Planet Simulation")

# Colors
White = (255, 255, 255)
Yellow = (255, 255, 0)
Blue = (100, 149, 237)
Red = (188, 39, 50)
Dark_Grey = (80, 78, 81)
Black = (0, 0, 0)
Orange = (255, 165, 0)

# Font for distance text
FONT = pygame.font.SysFont("comicsans", 16)

# Planet class to represent each planet in the system
class Planet:
    AU = 149.6e6 * 1000  # Astronomical unit in meters
    G = 6.67428e-11  # Gravitational constant
    Scale = 200 / AU  # 1 AU = 100 pixels
    Timestep = 3600 * 24  # 1 day in seconds
    
    def __init__(self, x, y, radius, color, mass, name=""):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.orbit = []
        self.sun = False
        self.name = name
        self.distance_to_sun = 0
        self.x_vel = 0
        self.y_vel = 0

    # Draws the planet and its orbit on the window
    def draw(self, win):
        # Convert planet's position from AU to pixel coordinates
        x = self.x * self.Scale + width / 2
        y = self.y * self.Scale + height / 2
        
        # Draw orbit line if it has more than 2 points
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                orbit_x, orbit_y = point
                orbit_x = orbit_x * self.Scale + width / 2
                orbit_y = orbit_y * self.Scale + height / 2
                updated_points.append((orbit_x, orbit_y))
            pygame.draw.lines(window, self.color, False, updated_points, 2)

        # Display distance to the sun for planets that are not the sun
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun / 1000, 1)}km", 1, White)
            window.blit(distance_text, (x - distance_text.get_width() / 2, y - self.radius + 20))
            
        # Display the name of the planet above it
        name_text = FONT.render(self.name, 1, White)
        window.blit(name_text, (x - name_text.get_width() / 2, y - self.radius - 20))  # 20 pixels above the planet

        # Draw the planet itself
        pygame.draw.circle(win, self.color, (x, y), self.radius)

    # Calculate the gravitational attraction between two planets
    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    # Update the planet's position based on gravitational forces from other planets
    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.Timestep
        self.y_vel += total_fy / self.mass * self.Timestep

        self.x += self.x_vel * self.Timestep
        self.y += self.y_vel * self.Timestep
        self.orbit.append((self.x, self.y)) 

"""
# Function to add stars in the background
def draw_stars(win):
    for _ in range(200):
        star_x = random.randint(0, width)
        star_y = random.randint(0, height)
        pygame.draw.circle(win, White, (star_x, star_y), 1)  # Draw small white dots
"""

# Main function to run the simulation
def main():
    run = True
    clock = pygame.time.Clock()

    # Create the sun and planets
    sun = Planet(0, 0, 30, Yellow, 1.98892 * 10**30, "Sun")
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, Blue, 5.9742 * 10**24, "Earth")
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, Red, 6.39 * 10**23, "Mars")
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8, Dark_Grey, 3.30 * 10**23, "Mercury")
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, White, 4.8685 * 10**24, "Venus")
    venus.y_vel = -35.02 * 1000

    planets = [sun, earth, mars, mercury, venus]

    while run:
        clock.tick(60) 
        window.fill(Black)  

        # Draw stars in the background
        #draw_stars(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)  
            planet.draw(window)  

        # Draw sun glow effect
        pygame.draw.circle(window, (255, 255, 100, 50), (width / 2, height / 2), 20)  # The glow of the sun
        pygame.draw.circle(window, (255, 255, 150, 50), (width / 2, height / 2), 20)

        pygame.display.update()  

    pygame.quit()

main()
