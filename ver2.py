import pygame
import random

class Characters:
    NAMES = {"Лес": ["ЛесЧерт1", "ЛесЧерт2"],
        "Вода": ["ВодаЧерт1", "ВодаЧерт2"],
        "Камни": ["КамниЧерт1", "КамниЧерт2"],
        "Болото": ["БолотоЧерт1", "БолотоЧерт2"],
        "Равнины": ["РавниныЧерт1", "РавниныЧерт2"],
        "Пустыня": ["ПустыняЧерт1", "ПустыняЧерт2"],
        "Пустошь": ["ПустошьЧерт1", "ПустошьЧерт2"]}
        
    COLORS = {name: color for name, color in zip(NAMES, (
        (139, 148, 32), (97, 154, 198), (204, 206, 201),
        (93, 87, 45), (132, 124, 40), (246, 215, 39),
        (203, 120, 68)
        ))}
        
    @staticmethod
    def delete_name(name):
        del Characters.NAMES[name]
        
    @staticmethod
    def shuffle():
        names = [i for i in Characters.NAMES]
        random.shuffle(names)
        Characters.NAMES = {name: Characters.NAMES[name] for name in names}
        
    @staticmethod
    def get_names():
        data = []
        Characters.shuffle()
        for name in Characters.NAMES:
            data.append((Characters.NAMES[name][0], Characters.COLORS[name]))
            data.append((Characters.NAMES[name][1], Characters.COLORS[name]))
            
        for i in range(14-len(data)):
            name = random.choice(list(Characters.NAMES))
            data.append((Characters.NAMES[name][0], Characters.COLORS[name]))
            data.append((Characters.NAMES[name][1], Characters.COLORS[name]))
            
        return data

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
        
class Game:
    WIDTH = 800
    WIDHTDIV2 = WIDTH / 2
    
    HEIGHT = 450
    HEIGHTDIV2 = HEIGHT / 2
    FPS = 60
    
    def __init__(self):
        pygame.init()
        
        self.clock = pygame.time.Clock()
        self.button = None
        
        self.set_sprites()
        self.set_window()
        
    def set_sprites(self):
        #Rect -> x,y, width, height
        self.roulette = Roulette(self.WIDTH, self.HEIGHT)
        self.black_squares = [
            pygame.Rect(
                0,
                Game.HEIGHTDIV2 - Roulette.HEIGHTDIV2, 
                Game.WIDHTDIV2 - Roulette.WIDHTDIV2, 
                Roulette.HEIGHT), 
            pygame.Rect(
                Game.WIDHTDIV2 + Roulette.WIDHTDIV2,
                Game.HEIGHTDIV2 - Roulette.HEIGHTDIV2,
                Game.WIDHTDIV2 - Roulette.WIDHTDIV2,
                Roulette.HEIGHT)
        ]
        
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.roulette)
        self.all_sprites.add(*self.roulette.cards)
        
    def draw_black_squares(self):
        pygame.draw.rect(self.screen, Color.GREEN, self.black_squares[0])
        pygame.draw.rect(self.screen, Color.YELLOW, self.black_squares[1])
            
    def set_window(self):
        #pygame.mixer.init()  # для звука
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Character roulette")
        
    def draw_all(self):
        self.all_sprites.update()   
        
        self.screen.fill((14, 123, 53))
        
        self.all_sprites.draw(self.screen)
        pygame.draw.line(self.screen, (230, 10, 10), 
            [Game.WIDHTDIV2, Game.HEIGHTDIV2 - Roulette.HEIGHTDIV2], 
            [Game.WIDHTDIV2, Game.HEIGHTDIV2 + Roulette.HEIGHTDIV2], 3)
        #self.draw_black_squares()
        
        pygame.display.flip()
            
    def run(self):
        running = True
        while running:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        running = False
                        
            self.draw_all()
        
class Roulette(pygame.sprite.Sprite):
    WIDTH = 400
    WIDHTDIV2 = WIDTH / 2
    
    HEIGHT = 110
    HEIGHTDIV2 = HEIGHT / 2
    
    OFFSET = 10
    
    RIGHT_END = WIDTH + WIDTH/2
    START_LEFT = Game.WIDHTDIV2 - WIDHTDIV2
    
    N = 14 #count of cards now
    
    
    
    def __init__(self, sc_width, sc_height):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.image.fill(Color.WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (sc_width/2, sc_height/2)
        
        Roulette.ALL_WIDTH = Card.WIDTH * Roulette.N + Roulette.OFFSET * (Roulette.N+1)
        
        data = Characters.get_names()
        
        self.cards = [Card(i, data[i][0],data[i][1]) for i in range(Roulette.N)]
        
    def update(self):    
        if Card.STEP > 0:
            for card in self.cards:
                card._update()
            
            #Card.STEP -= 0.01
            
class Card(pygame.sprite.Sprite):
    WIDTH = 120
    HEIGHT = 90
    STEP = 5
    
    def __init__(self,n, text, color):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface((Card.WIDTH, Card.HEIGHT))
        self.image.fill(color)
        
        self.text = text
        
        self.rect = self.image.get_rect()
        
        self.rect.x = Roulette.START_LEFT + Roulette.OFFSET*(n+1) + Card.WIDTH * n
        self.rect.y = Game.HEIGHTDIV2 - Roulette.HEIGHTDIV2 + Roulette.OFFSET
        
        self.image_x = self.rect.x - Roulette.WIDHTDIV2
        
    def _update(self):
        self.rect.x += Card.STEP
        if self.rect.x - Roulette.START_LEFT >= Roulette.ALL_WIDTH:
            self.rect.x = Roulette.ALL_WIDTH - self.rect.x

def run():
    Color._set_all()
    game = Game()
    game.run()
    
    
if __name__ == '__main__':
    run()