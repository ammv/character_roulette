import pygame
import random

class Characters:
    NAMES = {"Лес": ["Аурены", "Ведьмы"],   # green
        "Озера": ["Русалки", "Амфибии"],       # blue
        "Горы": ["Гномы", "Инженеры"],# grey
        "Болото": ["Алхимики", "Дарклинги"], #black
        "Равнины": ["Культисты", "Полурослики"], # коричневый
        "Пустыня": ["Кочевники", "Факиры"],   # yellow
        "Пустошь": ["Маги Хаоса", "Гиганты"]}
        
    COLORS = {name: color for name, color in zip(NAMES, (
        (139, 148, 32), (97, 154, 198), (204, 206, 201),
        (93, 87, 45), (132, 124, 40), (246, 215, 39),
        (203, 120, 68)
        ))}
        
    @staticmethod
    def delete_name(name):
        for key in Characters.NAMES:
            if name in Characters.NAMES[key]: 
                frac = key
                break
                
        del Characters.NAMES[frac]
        
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
    
    GREEN2 = (14, 123, 53)
    
    OTHER = (225,204,79)
    
    ROULETTE_BORDER = (138, 127, 142)
    CARD_BORDER = (167, 110, 25)
    
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
        pygame.font.init()
        
        Game.CARD_FONT = pygame.font.Font(None, 24)
        Game.WINNER_FONT = pygame.font.Font(None, 36)
        
        self.winner_title = Game.WINNER_FONT.render("Ваш персонаж:", True, Color.BLACK)
        
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
                self.roulette.rect.y, 
                Game.WIDHTDIV2 - Roulette.WIDHTDIV2, 
                Roulette.HEIGHT), 
            pygame.Rect(
                Game.WIDHTDIV2 + Roulette.WIDHTDIV2,
                self.roulette.rect.y,
                Game.WIDHTDIV2 - Roulette.WIDHTDIV2,
                Roulette.HEIGHT)
        ]
        
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.roulette)
        self.all_sprites.add(*self.roulette.cards)
        
    def draw_winner(self):
        self.screen.blit(self.winner_title, (
            Game.WIDHTDIV2-Game.WINNER_FONT.size("Ваш персонаж:")[0]/2,
            Game.HEIGHTDIV2-Game.WINNER_FONT.size("Ваш персонаж:")[1]/2-25))
            
        self.screen.blit(self.roulette.text_winner, (
            Game.WIDHTDIV2-Game.WINNER_FONT.size(self.roulette.winner)[0]/2,
            Game.HEIGHTDIV2-Game.WINNER_FONT.size(self.roulette.winner)[1]/2 +   
            Game.WINNER_FONT.size("Ваш персонаж:")[1]/2 + 5))
        
    def draw_hiding_squares(self):
        pygame.draw.rect(self.screen, Color.GREEN2, self.black_squares[0])
        pygame.draw.rect(self.screen, Color.GREEN2, self.black_squares[1])
            
    def set_window(self):
        #pygame.mixer.init()  # для звука
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Character roulette")
        
    def draw_text_on_cards(self):
        for card in self.roulette.cards:
            self.screen.blit(card.text, card.get_text_pos())
            
    def draw_lines(self):
        #center red line in roulette
        pygame.draw.line(self.screen, (230, 10, 10), 
            self.roulette.rect.midtop, 
            self.roulette.rect.midbottom, 3)
            
        #roulette border
        pygame.draw.lines(self.screen, Color.ROULETTE_BORDER, True, 
            [self.roulette.rect.topleft, self.roulette.rect.topright,
            self.roulette.rect.bottomright, self.roulette.rect.bottomleft], 3)
            
    def draw_cards_border(self):
        for card in self.roulette.cards:
            pygame.draw.lines(self.screen, Color.CARD_BORDER, True, 
            [card.rect.topleft, card.rect.topright,
            card.rect.bottomright, card.rect.bottomleft], 1)
        
    def draw_all(self):
        if not self.roulette.end:
            self.all_sprites.update()
            self.screen.fill(Color.GREEN2)
               
        else:
            self.screen.fill(Color.GREEN2)
            self.draw_winner()
        
        self.all_sprites.draw(self.screen)
        self.draw_cards_border()
        self.draw_text_on_cards()
            
        self.draw_hiding_squares()
        self.draw_lines()
        
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
    
    HEIGHT = 100
    HEIGHTDIV2 = HEIGHT / 2
    
    OFFSET = 5
    
    RIGHT_END = WIDTH + WIDTH/2
    START_LEFT = Game.WIDHTDIV2 - WIDHTDIV2
    
    STEP = 25 + random.randint(5, 15)
    K = 0.995
    
    N = 14 #count of cards now   
    
    def __init__(self, sc_width, sc_height):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.image.fill(Color.WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (sc_width/2, sc_height/4)
        
        Roulette.ALL_WIDTH = Card.WIDTH * Roulette.N + Roulette.OFFSET * (Roulette.N+1)
        
        data = Characters.get_names()
        
        self.cards = [Card(i, data[i][0],data[i][1]) for i in range(Roulette.N)]
        
        self.end = False
        
    def get_winner_character(self):
        for card in self.cards:
            if card.rect.x < Game.WIDHTDIV2 < card.rect.topright[0]:
                Characters.delete_name(card.raw_text)
                return card.raw_text
                
    def stop(self):
        self.winner = self.get_winner_character()
        self.text_winner = Game.WINNER_FONT.render(self.winner, True, Color.BLACK)
        self.end = True
        
    def update(self):    
        if Roulette.STEP > 1:
            for card in self.cards:
                card._update()
            Roulette.STEP *= Roulette.K
            Roulette.K -= random.random() / 100000
        else:
            self.stop()
        
            
class Card(pygame.sprite.Sprite):
    WIDTH = 120
    HEIGHT = 90
    
    def __init__(self,n, text, color):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface((Card.WIDTH, Card.HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        
        self.text = Game.CARD_FONT.render(text, True, Color.BLACK)
        self.raw_text = text
        self.text_size = Game.CARD_FONT.size(text)
        self.text_size = self.text_size[0] / 2, self.text_size[1] / 2
        
        self.rect.x = Roulette.START_LEFT + Roulette.OFFSET*(n+1) + Card.WIDTH * n
        self.rect.y = Game.HEIGHTDIV2/4 + Roulette.OFFSET*2
        
    def get_text_pos(self):
        x = self.rect.center[0] - self.text_size[0]
        y = self.rect.center[1] - self.text_size[1]
        return (x,y)
        
    def _update(self):
        self.rect.x += Roulette.STEP
        if self.rect.x >= Roulette.ALL_WIDTH:
            self.rect.x = self.rect.x  - Roulette.ALL_WIDTH

def run():
    Color._set_all()
    game = Game()
    game.run()
    
    
if __name__ == '__main__':
    run()