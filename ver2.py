import pygame
import random


class Color:
    BLACK = (0,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)
    WHITE = (255,255,255)
    YELLOW = (255,255,0)
    
    OTHER = (225,204,79)
    
    @staticmethod
    def randcolor():
        return random.choice(Color.ALL)
        
    @staticmethod
    def _set_all():
        Color.ALL = [i[1] for i in Color.__dict__.items() if isinstance(i[1], tuple)]
        Color.ALL.remove(Color.WHITE)
    

class Card(pygame.sprite.Sprite):
    WIDTH = 120
    HEIGHT = 90
    STEP = 5
    
    def __init__(self,n):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface((Card.WIDTH, Card.HEIGHT))
        self.image.fill(Color.randcolor())
        
        self.rect = self.image.get_rect()
        
        x = Roulette.WIDTH / 2 + Roulette.OFFSET*(n+1) + Card.WIDTH * n
        if not x >= Roulette.WIDTH * 1.5:
            self.rect.x = x
        self.rect.y = Game.HEIGHT / 2 - Roulette.HEIGHT / 2 + Roulette.OFFSET
        
        self.image_x = self.rect.x
        
    def update(self):
        self.image_x += Card.STEP
        
        if not self.rect.x >= Roulette.RIGHT_END:
            self.rect.x += Card.STEP
            
        elif self.image_x >= Roulette.ALL_WIDTH:
            self.image_x -= Roulette.ALL_WIDTH
            self.rect.x = Roulette.WIDTH / 2 - Card.WIDTH + self.image_x#self.image_x 
    
class Roulette(pygame.sprite.Sprite):
    WIDTH = 400
    HEIGHT = 110
    OFFSET = 10
    MAX_CARDS = 5
    ALL_WIDTH = Card.WIDTH * MAX_CARDS
    
    RIGHT_END = WIDTH + WIDTH/2
    
    N = 5 #count of cards now
    
    def __init__(self, sc_width, sc_height):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.image.fill(Color.WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (sc_width/2, sc_height/2)
        
        self.cards = [Card(i) for i in range(self.N)]
        
    def update(self):
        for card in self.cards:
            card.update()

class Game:
    WIDTH = 800
    HEIGHT = 450
    FPS = 30
    
    def __init__(self):
        pygame.init()
        
        self.clock = pygame.time.Clock()
        
        self.set_sprites()
        self.set_window()
        
    def set_sprites(self):
        self.roulette = Roulette(self.WIDTH, self.HEIGHT)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.roulette)
        self.all_sprites.add(*self.roulette.cards)
        
    def draw_black_rects(self):
        pygame.draw.rect(self.screen, Color.BLACK, 
                        (Game.WIDTH - Roulette.WIDTH / 2,
                        Game.HEIGHT / 2 - Roulette.HEIGHT / 2 + Roulette.OFFSET,
                        Card.WIDTH+Roulette.OFFSET,
                        Card.HEIGHT))
                        
        pygame.draw.rect(self.screen, Color.BLACK, 
                        (Roulette.WIDTH / 2 - Card.WIDTH - Roulette.OFFSET,
                        Game.HEIGHT / 2 - Roulette.HEIGHT / 2 + Roulette.OFFSET,
                        Card.WIDTH+Roulette.OFFSET,
                        Card.HEIGHT))
            
    def set_window(self):
        #pygame.mixer.init()  # для звука
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Character roulette")
            
    def run(self):
        running = True
        while running:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        running = False
                        
            self.all_sprites.update()
                
            self.screen.fill(Color.BLACK)
            self.all_sprites.draw(self.screen)
            self.draw_black_rects()
            pygame.display.flip()


def run():
    Color._set_all()
    game = Game()
    game.run()
    
    
if __name__ == '__main__':
    run()