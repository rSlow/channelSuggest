import asyncio

from aiogram.types import ContentType, Message

from FSM.post_add import Start
from bot import dp
from handlers.start import start
from ORM.users import Dice
from keyboads.start import DiceKeyboard


@dp.message_handler(content_types=ContentType.DICE, state=Start.start)
async def dice(message: Message):
    await Start.dice.set()

    if message.dice.emoji in ("🎲", "🎯"):
        if message.dice.emoji == "🎲":
            await Dice.play_cube(user_id=message.from_user.id)
        elif message.dice.emoji == "🎯":
            await Dice.play_darts(user_id=message.from_user.id)

        user_value = message.dice.value
        await message.answer(
            text="Ну хорошо, давай поиграем...",
            reply_markup=DiceKeyboard.get_random_keyboard()
        )
        msg_dice = await message.answer_dice(
            emoji=message.dice.emoji,
        )
        bot_value = msg_dice.dice.value

        if user_value > bot_value:
            result_message = "Ну хорошо, ты выиграл. Но больше не балуйся!"
        elif user_value < bot_value:
            result_message = "И нечего баловаться! Ты все равно проиграл!!"
        else:
            result_message = "Давай ни тебе ни мне, и больше так не делай!"
        await asyncio.sleep(4)

    elif message.dice.emoji == "🏀":
        await Dice.play_basketball(user_id=message.from_user.id)
        match message.dice.value:
            case 1:
                result_message = "Нууу, братишка, надо тренироваться..."
            case 2:
                result_message = "Выскочил, мда... А могло быть красиво."
            case 3:
                result_message = f"Вот пусть он там и остается, не надо его доставать. " \
                                 f"И беспокоить меня по пустякам - тоже не надо."
            case 4:
                result_message = "Красивый унитазик :) Но лучше попадать чисто. А еще лучше - не заходить сюда!"
            case 5:
                result_message = "Чистенько. Молодец. Уходи на пике - не надо меня тут беспокоить. Лучше пост добавь."
            case _:
                raise ValueError("Unexpected dice value")
        await asyncio.sleep(4)

    elif message.dice.emoji == "🎰":
        await Dice.play_casino(user_id=message.from_user.id)
        match message.dice.value:
            case 1:
                result_message = "Этому гражданину напиток с бара за счёт заведения, быстро!"
            case 22:
                result_message = "Три вишенки - моё почтение!"
            case 43:
                result_message = "Три лимончика... осталось только коньяк и шоколадку найти..."
            case 64:
                result_message = "Ну тут без комментариев. Красавчик!"
            case _:
                result_message = "Без шансов. Давай когда-нибудь потом, хорошо?"
        await asyncio.sleep(3)

    elif message.dice.emoji == "⚽":
        await Dice.play_football(user_id=message.from_user.id)
        match message.dice.value:
            case 1:
                result_message = "Нууу, братишка, надо тренироваться..."
            case 2:
                result_message = "С таким пристрастием к штангам лучше в зал ходить!"
            case 3:
                result_message = "Ну еле-еле забил, но забил, спору нет."
            case 4:
                result_message = "Неплохо, неплохо, но можно лучше, давай тренируйся!"
            case 5:
                result_message = "вай вай вай, какая красота!"
            case _:
                raise ValueError("Unexpected dice value")
        await asyncio.sleep(4)

    else:
        result_message = "Не знаю такую игру, совсем. Узнаю - добавлю обязательно."

    await message.answer(text=result_message)
    await start(message=message, answer="А теперь серьезно, возвращаю тебя в главное меню.")
