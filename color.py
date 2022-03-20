from random import choice


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
        return choice(Color.ALL)
        
    @staticmethod
    def _set_all():
        Color.ALL = [i[1] for i in Color.__dict__.items() if isinstance(i[1], tuple)]
        Color.ALL.remove(Color.WHITE)