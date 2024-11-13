from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def gen_back_keyboard() -> VkKeyboard:
    """
    Generates a back keyboard with a single 'Назад' button.
    Returns:
        VkKeyboard: The generated keyboard with a 'Назад' button.
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("Назад", color=VkKeyboardColor.NEGATIVE)
    return keyboard


def add_back_button(keyboard: VkKeyboard) -> VkKeyboard:
    """
    Adds a 'back' button to the provided keyboard.
    Args:
        keyboard (VkKeyboard): The keyboard to which the 'Назад' button will be added.
    Returns:
        VkKeyboard: The keyboard with the added 'Назад' button.
    """
    keyboard.add_button("Назад", color=VkKeyboardColor.NEGATIVE)
    # keyboard.add_line()
    return keyboard
