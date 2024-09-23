import pygame
import math
import random

# Initialiser Pygame
pygame.init()

# Définir la taille de la fenêtre
screen_width = 1280
screen_height = 800

# Créer la fenêtre Pygame
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simulation du périphérique parisien")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Paramètres du cercle (périphérique)
circle_center = (screen_width // 2, screen_height // 2)  # Centre du cercle
circle_radius = 300  # Rayon du cercle (route)
car_radius = 10  # Taille des voitures

# Vitesse maximale en km/h (relatif)
MAX_SPEED_KMH = 70  # km/h

# Nombre de voitures
NUM_CARS = 50

# Angles des entrées et sorties
ENTRY_EXIT_ANGLES = [30, 150, 210, 330]  # Angles pour les bretelles

# Classe Car (Voiture)
class Car:
    def __init__(self, angle, speed, color=GREEN):
        self.angle = angle  # Angle de départ de la voiture
        self.speed = speed  # Vitesse angulaire (basée sur km/h)
        self.color = color
        self.x = 0
        self.y = 0
        self.next_car = None  # La voiture devant cette voiture
        self.on_exit = False  # Indique si la voiture est sur une bretelle

    def drive(self):
        """Simule le déplacement de la voiture le long de la trajectoire circulaire."""
        if self.on_exit:
            self.angle += 2  # Vitesse de la bretelle
            if self.angle >= 90:  # Simule une sortie de 90°
                self.on_exit = False  # Sortie terminée
                self.angle = 0  # Réinitialiser l'angle pour le chemin principal
        else:
            # Ralentir si une autre voiture est proche devant
            if self.next_car:
                distance = self.compute_distance(self.next_car)
                if distance < 40:  # Distance minimale pour ralentir
                    self.color = RED
                    self.speed = max(self.speed - 0.1, 1)  # Ralentir mais ne pas s'arrêter
                else:
                    self.color = GREEN
                    self.speed = min(self.speed + 0.05, MAX_SPEED_KMH / 60)  # Accélérer

            # Mettre à jour l'angle de la voiture
            self.angle = (self.angle + self.speed) % 360  # Garder l'angle entre 0 et 360°

        # Calculer la position de la voiture sur le cercle
        self.x = circle_center[0] + circle_radius * math.cos(math.radians(self.angle))
        self.y = circle_center[1] + circle_radius * math.sin(math.radians(self.angle))

        # Vérifier si la voiture doit sortir
        if random.random() < 0.01:  # Probabilité de sortie
            self.on_exit = True

    def compute_distance(self, other_car):
        """Calcule la distance angulaire entre deux voitures."""
        angle_diff = (other_car.angle - self.angle) % 360
        return angle_diff

    def draw(self, screen):
        """Affiche la voiture sur l'écran."""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), car_radius)  # Dessine la voiture

# Classe Road (Route)
class Road:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def draw(self, screen):
        """Dessine la route circulaire sur l'écran."""
        pygame.draw.circle(screen, BLACK, self.center, self.radius, 5)  # Cercle représentant le périphérique
        self.draw_entry_exit(screen)

    def draw_entry_exit(self, screen):
        """Dessine les bretelles d'entrée et de sortie."""
        for angle in ENTRY_EXIT_ANGLES:
            start_x = self.center[0] + self.radius * math.cos(math.radians(angle))
            start_y = self.center[1] + self.radius * math.sin(math.radians(angle))
            end_x = self.center[0] + (self.radius + 50) * math.cos(math.radians(angle))
            end_y = self.center[1] + (self.radius + 50) * math.sin(math.radians(angle))
            pygame.draw.line(screen, BLACK, (start_x, start_y), (end_x, end_y), 3)  # Dessine la bretelle

# Fonction principale
def main():
    clock = pygame.time.Clock()
    # Créer la route circulaire (périphérique)
    road = Road(circle_center, circle_radius)

    # Créer les voitures sur le périphérique avec des vitesses variables
    cars = []
    for i in range(NUM_CARS):
        angle = i * (360 / NUM_CARS)  # Répartir les voitures uniformément
        speed = (MAX_SPEED_KMH / 60) * random.uniform(0.5, 1)  # Vitesse initiale aléatoire
        car = Car(angle, speed)
        cars.append(car)

    # Lier chaque voiture à la suivante (pour savoir qui est devant)
    for i in range(NUM_CARS):
        cars[i].next_car = cars[(i + 1) % NUM_CARS]  # La voiture suivante dans la boucle

    running = True
    while running:
        # Gérer les événements Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Quitter avec Échap
                    running = False

        # Remplir l'écran de blanc avant de dessiner
        screen.fill(WHITE)

        # Exécuter la logique de chaque voiture
        for car in cars:
            car.drive()

        # Dessiner la route circulaire (périphérique)
        road.draw(screen)

        # Dessiner toutes les voitures
        for car in cars:
            car.draw(screen)

        # Mettre à jour l'affichage (double buffering)
        pygame.display.flip()

        # Limiter la vitesse de rafraîchissement à 60 FPS
        clock.tick(60)

    pygame.quit()

# Exécuter le programme
if __name__ == "__main__":
    main()
