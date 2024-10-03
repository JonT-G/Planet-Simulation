import pygame
import math
import random
pygame.init()

# Window dimensions
width, height = 1800, 900
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Planet Simulation")

# Colors used
White = (255, 255, 255)
Yellow = (255, 255, 0)
Blue = (100, 149, 237)
Red = (188, 39, 50)
Dark_Grey = (80, 78, 81)
Black = (0, 0, 0)
Orange = (255, 165, 0)
Light_Grey = (200, 200, 200)

# Planet class to represent each planet in the system
class Planet:
    AU = 149.6e6 * 1000  # Astronomical unit in meters
    G = 6.67428e-11  # Gravitational constant
    Scale = 90 / AU  # 1 AU = 100 pixels
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
    def draw(self, win, x_offset=0, y_offset=0):
        
        # Font for distance text
        FONT = pygame.font.SysFont("comicsans", 16)
        
        # Convert planet's position from AU to pixel coordinates
        x = self.x * self.Scale + width / 2 + x_offset
        y = self.y * self.Scale + height / 2 + y_offset
        
        # Draw orbit line
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                orbit_x, orbit_y = point
                orbit_x = orbit_x * self.Scale + width / 2 + x_offset
                orbit_y = orbit_y * self.Scale + height / 2 + y_offset
                updated_points.append((orbit_x, orbit_y))
            pygame.draw.lines(window, self.color, False, updated_points, 2)

        # Display distance to the sun for planets expect sun of course 
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun / 1000, 1)}km", 1, White)
            window.blit(distance_text, (x - distance_text.get_width() / 2, y - self.radius + 20))
            
        # Display the name of the planet above it
        name_text = FONT.render(self.name, 1, White)
        window.blit(name_text, (x - name_text.get_width() / 2, y - self.radius - 20))  # 20 pixels to get name above the planet

        # Draw the planets itself
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


# Function to add stars in the background
def draw_stars(win):
    for _ in range(200):
        star_x = random.randint(0, width)
        star_y = random.randint(0, height)
        pygame.draw.circle(win, White, (star_x, star_y), 1) 

# Main function to run the simulation
def main():
    run = True
    clock = pygame.time.Clock()
    paused = False
    is_dragging = False
    x_offset = 0
    y_offset = 0
    last_mouse_pos = (0, 0)
    
    
    # Create the sun and planets
    sun = Planet(0, 0, 25, Yellow, 1.98892 * 10**30, "Sun")
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, Blue, 5.9742 * 10**24, "Earth")
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, Red, 6.39 * 10**23, "Mars")
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8, Dark_Grey, 3.30 * 10**23, "Mercury")
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, White, 4.8685 * 10**24, "Venus")
    venus.y_vel = -35.02 * 1000
    
    jupiter = Planet(-5.2 * Planet.AU, 0, 28, Orange, 1.898 * 10**27, "Jupiter")
    jupiter.y_vel = 13.06 * 1000

    saturn = Planet(-9.58 * Planet.AU, 0, 24, Light_Grey, 5.683 * 10**26, "Saturn")
    saturn.y_vel = 9.68 * 1000

    uranus = Planet(-19.22 * Planet.AU, 0, 20, Light_Grey, 8.681 * 10**25, "Uranus")
    uranus.y_vel = 6.80 * 1000

    neptune = Planet(-30.05 * Planet.AU, 0, 20, Light_Grey, 1.024 * 10**26, "Neptune")
    neptune.y_vel = 5.43 * 1000

    planets = [sun, earth, mars, mercury, venus, jupiter, saturn, uranus, neptune]
    
  
    while run:
        clock.tick(60)  
        window.fill(Black)  
     
        #Draw stars in the background
        draw_stars(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                    is_dragging = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    is_dragging = True
                    last_mouse_pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # doing this is so it lets go when leftclick is up, and does not follow the mouse
                    is_dragging = False 
            elif event.type == pygame.MOUSEMOTION:
                if is_dragging:
                    mouse_pos = pygame.mouse.get_pos()
                    x_offset += mouse_pos[0] - last_mouse_pos[0]
                    y_offset += mouse_pos[1] - last_mouse_pos[1]
                    last_mouse_pos = mouse_pos
        
        for planet in planets:
            if not paused:
                planet.update_position(planets) 
            planet.draw(window, x_offset, y_offset) 
            
            # Draw sun glow effect
            #pygame.draw.circle(window, (255, 255, 100, 50), (width // 2, height // 2), 60)  
            #pygame.draw.circle(window, (255, 255, 150, 50), (width // 2, height // 2), 90)

            if paused:
                is_dragging = False
                draw_stars(window) == paused
                # Create a translucent surface for the "Paused" text
                overlay = pygame.Surface(window.get_size(), pygame.SRCALPHA) 
                overlay.fill((0, 0, 0, 70))
            
                # Render the "Paused" text
                font = pygame.font.SysFont("rockwell", 55)
                pause_text = font.render("Paused", True, (255, 255, 255))
            
                # Center the text relative to the current view
                overlay.blit(pause_text, (width // 2 - pause_text.get_width() // 2, 
                                         height // 2 - pause_text.get_height() // 2 - 35)) # 35 test and try number to make it go futher up the y-axes

                
                # Display description for distances
                description_font = pygame.font.SysFont("rockwell", 35)
                desc_text = "Distance from the sun:"
                description_surface = description_font.render(desc_text, True, (255, 255, 255))
                overlay.blit(description_surface, (10, height - 540))

                # Display planet information (distances) adjusted with the view offsets
                info_font = pygame.font.SysFont("rockwell", 35)
                y_offset_text = height - 500
            
                for planet in planets:
                    distance_FS = planet.distance_to_sun / 1000
                    info_text = f"{planet.name}: {distance_FS:,.2f}km"
                    info_surface = info_font.render(info_text, True, (255, 255, 255))

                    # Display the text starting at y_offset_text and moving down for each planet
                    overlay.blit(info_surface, (10, y_offset_text))

                    y_offset_text += 40 # Keeps moving down to display the rest of the planets 

                # Apply the all things when paused
                window.blit(overlay, (0, 0))
            

        pygame.display.update()

    pygame.quit()

main()

