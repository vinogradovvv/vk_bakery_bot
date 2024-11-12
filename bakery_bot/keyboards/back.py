from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def gen_back_keyboard():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("Назад", color=VkKeyboardColor.NEGATIVE)
    return keyboard


def add_back_button(keyboard: VkKeyboard):
    keyboard.add_button("Назад", color=VkKeyboardColor.NEGATIVE)
    # keyboard.add_line()
    return keyboard
