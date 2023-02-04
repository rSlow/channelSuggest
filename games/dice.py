class DiceGame:
    def __init__(self, emoji: str, value: int):
        self.emoji = emoji
        self.value = value

    def football(self):
        match self.value:
            case 1:
                return "Нууу, братишка, надо тренироваться..."
            case 2:
                return "С таким пристрастием к штангам лучше в зал ходить!"
            case 3:
                return "Ну еле-еле забил, но забил, спору нет."
            case 4:
                return "Неплохо, неплохо, но можно лучше, давай тренируйся!"
            case 5:
                return "вай вай вай, какая красота!"

    def basketball(self):
        match self.value:
            case 1:
                return "Нууу, братишка, надо тренироваться..."
            case 2:
                return "С таким пристрастием к штангам лучше в зал ходить!"
            case 3:
                return "Ну еле-еле забил, но забил, спору нет."
            case 4:
                return "Неплохо, неплохо, но можно лучше, давай тренируйся!"
            case 5:
                return "вай вай вай, какая красота!"

    def casino(self):
        match self.value:
            case 1:
                return "Этому гражданину напиток с бара за счёт заведения, быстро!"
            case 22:
                return "Три вишенки - моё почтение!"
            case 43:
                return "Три лимончика... осталось только коньяк и шоколадку найти..."
            case 64:
                return "Ну тут без комментариев. Красавчик!"
            case _:
                return "Без шансов. Давай когда-нибудь потом, хорошо?"
