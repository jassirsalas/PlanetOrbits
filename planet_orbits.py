import pygame, sys
import numpy as np

class Planet():
    def __init__(self, initial_state, radius, color=(255,255,255)):
        self.G = 39.478 # Gravitational constant [AU**3 year**-2 Msun**-1]
        self.M = 1.0 # Sun mass
        self.t = 0.0 # Time

        self.S0 = [*initial_state]
        self.scale = int(100 * initial_state[0])
        self.orbit = []
        
        self.size = int(np.sqrt(radius)/10)
        self.color = color
    
    def dSdt(self, S, t):
        r, rdot, theta, thetadot = S
    
        rddot = r*thetadot**2 - self.G*self.M/r**2
        thetaddot = -2*rdot*thetadot/r
        return rdot, rddot, thetadot, thetaddot

    def RK4(self, f, y, t, step):
        yn = y
        dt = step
        
        k1 = dt * np.array(f(y       , t       ))
        k2 = dt * np.array(f(y + k1/2, t + dt/2))
        k3 = dt * np.array(f(y + k2/2, t + dt/2))
        k4 = dt * np.array(f(y + k3  , t + dt  ))

        y = y + (k1 + 2*k2 + 2*k3 + k4)/6 

        return y

    def draw(self, x_planet, y_planet):
        pygame.draw.circle(screen, self.color, (x_planet, y_planet), self.size)

        if len(self.orbit) > 2:
            updated_orbit = []
            for pp in self.orbit:
                xx, yy = pp
                updated_orbit.append((xx, yy))

            pygame.draw.lines(screen, (115,115,115), False, (updated_orbit), 1)


    def update(self, dt):
        h = 1/dt
        
        self.S0 = self.RK4(self.dSdt, self.S0, self.t, h)

        self.t = self.t + h

        x_position = int(width//2 + self.scale*self.S0[0]*np.cos(self.S0[2]))
        y_position = int(height//2 + self.scale*self.S0[0]*np.sin(-self.S0[2]))

        self.orbit.append((x_position, y_position))
        if len(self.orbit) > 200:
            self.orbit.pop(0)
        
        self.draw(x_position, y_position)
        

# Pygame init
pygame.init()

# Screen
width, height = 600, 600
screen = pygame.display.set_mode((width, height))

# Clock
clock = pygame.time.Clock()

# star constants
r_sun = pygame.math.Vector2(width/2, height/2)

# Initial values for: r, r_dot, theta, theta_dot
S0_v = [0.72, 0.0, 0.0, 2.0*np.pi/0.61]
S0_e = [1.00, 0.0, 0.0, 2.0*np.pi/1.00]
S0_m = [1.52, 0.0, 0.0, 2.0*np.pi/1.88]
S0_j = [5.70, 0.0, 0.0, 2.0*np.pi/12.0]

planets = []
states = [S0_v, S0_e, S0_m]
radii = [6052, 6371, 3390] # Radius [km]
colors = [(218, 165, 32), (70, 130, 180), (188, 39, 50)]

for s_i, r_i, c_i in zip(states, radii, colors):
    planets.append(Planet(s_i, radius=r_i, color=c_i))


pg_font = pygame.font.SysFont('Tahoma', size=14)

t = 0.0
t_step = 30
dt_step = t_step

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    dt = clock.tick(t_step)
    
    # Draw
    screen.fill((0,0,0))
    
    for p in planets:
        p.update(dt_step)

    t = t + 1/(dt_step)

    # sun
    # pygame.draw.circle(screen, (255, 255, 255), (int(r_sun.x),int(r_sun.y)), 20)

    # Font
    img_font = pg_font.render(f"Time: {round(t, 1)} years", True, (255,255,255))
    screen.blit(img_font, (10, 10))
    
    # Update
    pygame.display.update()