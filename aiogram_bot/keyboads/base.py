from aiogram.types import ReplyKeyboardMarkup


class TypeInterface:
    iterable = list | tuple
    double_iterable = list[iterable] | tuple[iterable]
    buttons_list_type = iterable | double_iterable


class BaseKeyboard(ReplyKeyboardMarkup):
    """
    Use this class as base for your keyboard classes.
    Override class-attribute `buttons_list` to
    You can override to your values the default parameters, such as:
        - resize_keyboard
        - row_width
    """

    resize_keyboard: bool = True
    row_width: int = 2
    input_field_placeholder: str | None = None
    add_on_main_button: bool = True
    on_main_button = "На главную ◀"

    buttons_list: TypeInterface.buttons_list_type | None = None

    def __init__(self):
        super(BaseKeyboard, self).__init__(
            resize_keyboard=self.resize_keyboard,
            row_width=self.row_width,
            input_field_placeholder=self.input_field_placeholder
        )

        if self.buttons_list is not None:
            self._process_buttons_list(self.buttons_list)

        if self.add_on_main_button:
            self.insert(self.on_main_button)

    def _process_buttons_list(self, buttons_list: TypeInterface.buttons_list_type):
        for buttons_row in buttons_list:
            if type(buttons_row) == TypeInterface.iterable:
                _row = []
                for button in buttons_row:
                    _row.append(button)
                self.add(*_row)
            else:
                self.add(*buttons_list)
                return
