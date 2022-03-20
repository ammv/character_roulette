from random import shuffle, choice


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
        shuffle(names)
        Characters.NAMES = {name: Characters.NAMES[name] for name in names}
        
    @staticmethod
    def get_names():
        data = []
        Characters.shuffle()
        for name in Characters.NAMES:
            data.append((Characters.NAMES[name][0], Characters.COLORS[name]))
            data.append((Characters.NAMES[name][1], Characters.COLORS[name]))
            
        for i in range(14-len(data)):
            name = choice(list(Characters.NAMES))
            data.append((Characters.NAMES[name][0], Characters.COLORS[name]))
            data.append((Characters.NAMES[name][1], Characters.COLORS[name]))
            
        return data
