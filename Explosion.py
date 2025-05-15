#Danke für die Bilder russs123 [Github]
class Explosion:
    def __init__(self, x, y):
        
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f"BilderExplosion/exp{num}.png") # Ordner mit den Bildern
            img = pygame.transform.scale(img, (100, 100))
            self.images.append(img)
