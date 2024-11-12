from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def add_delete_category_button(keyboard: VkKeyboard):
    keyboard.add_button("Удалить категорию", color=VkKeyboardColor.NEGATIVE)
    # keyboard.add_line()
    return keyboard


def add_delete_product_button(keyboard: VkKeyboard):
    keyboard.add_button("Удалить продукт", color=VkKeyboardColor.NEGATIVE)
    # keyboard.add_line()
    return keyboard
