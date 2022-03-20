import pygame
import random

from time import sleep
from characters import Characters
from color import Color

        
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
        
        self.set_window()
        self.set_sprites()
        self.set_button()
        
        self.spins = 0
        
    def set_window(self):
        #pygame.mixer.init()  # для звука
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Character roulette")
        
    def set_button(self):
        self.button_img = pygame.image.load("button.jpg")
        self.button_img.convert()
        
        self.button = self.button_img.get_rect(center=(Game.WIDHTDIV2, Game.HEIGHT*0.75))
        
    def button_click(self):
        if len(Characters.NAMES) == 0:
            self.running = False
            
        else:
            if self.spins > 0:
                self.set_sprites()
                
            self.spins += 1
            self.roulette.spin = True
        
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
            
        try:
            self.screen.blit(self.roulette.text_winner, (
                Game.WIDHTDIV2-Game.WINNER_FONT.size(self.roulette.winner)[0]/2,
                Game.HEIGHTDIV2-Game.WINNER_FONT.size(self.roulette.winner)[1]/2 +   
                Game.WINNER_FONT.size("Ваш персонаж:")[1]/2 + 5))
        except:
            print(self.roulette.winner)
            input("Ожидаю Enter")
            
    def draw_button(self):
        self.screen.blit(self.button_img, self.button)
        
    def draw_hiding_squares(self):
        pygame.draw.rect(self.screen, Color.GREEN2, self.black_squares[0])
        pygame.draw.rect(self.screen, Color.GREEN2, self.black_squares[1])
        
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
        if self.roulette.spin:
            self.all_sprites.update()
            self.screen.fill(Color.GREEN2)
               
        elif self.roulette.end:
            self.screen.fill(Color.GREEN2)
            self.draw_winner()
            self.draw_button()
            
        else:
            self.screen.fill(Color.GREEN2)
            self.draw_button()
        
        self.all_sprites.draw(self.screen)
        
        self.draw_cards_border()
        self.draw_text_on_cards()
            
        self.draw_hiding_squares()
        self.draw_lines()
            
    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button.collidepoint(event.pos):
                        self.button_click()
                        
            self.draw_all()
            pygame.display.flip()
        
class Roulette(pygame.sprite.Sprite):
    WIDTH = 600
    WIDHTDIV2 = WIDTH / 2
    
    HEIGHT = 100
    HEIGHTDIV2 = HEIGHT / 2
    
    OFFSET = 5
    
    RIGHT_END = WIDTH + WIDTH/2
    START_LEFT = Game.WIDHTDIV2 - WIDHTDIV2
    
    N = 14 # количество карт
    
    def __init__(self, sc_width, sc_height):
        pygame.sprite.Sprite.__init__(self)
        
        self.calculate_steps()
        
        self.image = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.image.fill(Color.WHITE)
        
        self.rect = self.image.get_rect()
        self.rect.center = (sc_width/2, sc_height/4)
        
        Roulette.ALL_WIDTH = Card.WIDTH * Roulette.N + Roulette.OFFSET * Roulette.N
        
        # инициализация карт
        data = Characters.get_names()
        self.cards = [Card(i, data[i][0],data[i][1]) for i in range(Roulette.N)]
        
        self.spin = False
        
        self.end = False
        
    def calculate_steps(self):
        '''
            Коэффицент для замедления прокрутки рулетки
        '''
        STEP = 25 + random.randint(0, 20)
        
        k = 0.995
        
        STEPS = [STEP]
        
        while STEP > 1:
            STEP *= k
            k -= random.random() / 100000
            STEPS.append(STEP)
            
        Roulette.STEPS = STEPS
        
    def get_winner_character(self):
        winner = None
        for card in self.cards:
            if card.rect.x < Game.WIDHTDIV2 < card.rect.topright[0]:
                Characters.delete_name(card.raw_text)
                winner = card.raw_text
                
        if winner == None:
            for i in range(0, Roulette.N-1):
                card1 = self.cards[i]
                card2 = self.cards[i+1]
                
                if card1.rect.bottomright[0] < Game.WIDHTDIV2 < card2.rect.bottomleft[0]:
                    d1 = abs(card1.rect.bottomright[0]-WIDHTDIV2)
                    d2 = abs(card2.rect.bottomleft[0]-WIDHTDIV2)
                    
                    if d1 > d2:
                        winner = card2.raw_text
                    else:
                        winner = card1.raw_text
                        
        return winner
                
    def stop(self):
        self.winner = self.get_winner_character()
        self.text_winner = Game.WINNER_FONT.render(self.winner, True, Color.BLACK)
        self.spin = False
        self.end = True
        
    def update(self):
        if Roulette.STEPS:
            for card in self.cards:
                card._update()
            Roulette.STEPS.pop(0)
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
        self.rect.bottomright = (self.rect.bottomright[0] + Roulette.STEPS[0], self.rect.bottomright[1])
        if self.rect.bottomright[0] >= Roulette.ALL_WIDTH:
            self.rect.bottomright = (self.rect.bottomright[0] - Roulette.ALL_WIDTH, self.rect.bottomright[1])

def run():
    Color._set_all()
    game = Game()
    game.run()
    
    
if __name__ == '__main__':
    run()
