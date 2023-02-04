from datetime import time as t
from random import choice


class TimeAnswer(str):
    morning_start = t(hour=6)
    dinner_start = t(hour=11)
    evening_start = t(hour=17)
    night_start = t(hour=23)

    def __init__(self, time: t):
        self.time = time

    def __str__(self):
        answer: str

        if self.time.hour >= self.evening_start.hour:
            answer = choice(Answer.evening)
        elif self.time.hour >= self.dinner_start.hour:
            answer = choice(Answer.dinner)
        elif self.time.hour >= self.morning_start.hour:
            answer = choice(Answer.morning)
        else:
            answer = choice(Answer.night)

        return answer

    def __repr__(self):
        return self.__str__()


class Answer:
    morning = [
        "Здрасьте здрасьте, с утра пораньше, вот тебе кнопочки.",
        "С добрым утром, жаворонок. Выбирай, что нужно.",
        "С утра надо бы и кофейку заварить сначала, а уж потом сюда заходить...",
        "Доброе утро, ненаглядный! Выбирай, что хочешь.",
        "Рады видеть ваше бодрое лицо в начале нового дня. Чего желаем?",
        "Тотальной победы над утренней ленью. Слушаю тебя...",
        "Готовь завтрак быстрее. А я тебя слушаю."
    ]
    dinner = [
        "Надеюсь, ты покушал уже. Добрый день.",
    ]
    evening = [
        "Добрейший вечерочек. Заваривай чай или кофе, тут уже что по вкусу...",
        "Вот так вот вечность пропадал и вдруг … прямо тут! Я в шоке! Добрый вечер, рад приветствовать.",
        "Ужин сам себя не съест, не забывай про него! Но если нужен я, то пожалуйста.",
    ]
    night = [
        "И чего мы не спим в такое время? Ладно, слушаю тебя...",
    ]
