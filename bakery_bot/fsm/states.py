from transitions import Machine


class BotStates:
    states = ['START', 'MAIN_MENU', 'NEW_CATEGORY_NAME', 'CATEGORY', 'PRODUCT', 'NEW_PRODUCT_NAME', 'NEW_PRODUCT_DESCRIPTION', 'NEW_PRODUCT_PHOTO', 'DELETE_PRODUCT']

    def __init__(self):
        self.machine = Machine(model=self, states=BotStates.states, initial='START')

        self.machine.add_transition(trigger='main_menu', source='START', dest='MAIN_MENU')

        self.machine.add_transition(trigger='new_category_name', source='MAIN_MENU', dest='NEW_CATEGORY_NAME')
        self.machine.add_transition(trigger='main_menu', source='NEW_CATEGORY_NAME', dest='MAIN_MENU')

        self.machine.add_transition(trigger='category', source='MAIN_MENU', dest='CATEGORY')
        self.machine.add_transition(trigger='main_menu', source='CATEGORY', dest='MAIN_MENU')

        self.machine.add_transition(trigger='new_product_name', source='CATEGORY', dest='NEW_PRODUCT_NAME')
        self.machine.add_transition(trigger='main_menu', source='NEW_PRODUCT_NAME', dest='MAIN_MENU')
        self.machine.add_transition(trigger='new_product_description', source='NEW_PRODUCT_NAME', dest='NEW_PRODUCT_DESCRIPTION')
        self.machine.add_transition(trigger='main_menu', source='NEW_PRODUCT_DESCRIPTION', dest='MAIN_MENU')
        self.machine.add_transition(trigger='new_product_photo', source='NEW_PRODUCT_DESCRIPTION', dest='NEW_PRODUCT_PHOTO')
        self.machine.add_transition(trigger='main_menu', source='NEW_PRODUCT_PHOTO', dest='MAIN_MENU')
        self.machine.add_transition(trigger='category', source='NEW_PRODUCT_PHOTO', dest='CATEGORY')

        self.machine.add_transition(trigger='product', source='CATEGORY', dest='PRODUCT')
        self.machine.add_transition(trigger='category', source='PRODUCT', dest='CATEGORY')

        self.machine.add_transition(trigger='delete_product', source='CATEGORY', dest='DELETE_PRODUCT')
        self.machine.add_transition(trigger='main_menu', source='DELETE_PRODUCT', dest='MAIN_MENU')

        for state in BotStates.states:
            if state != 'MAIN_MENU':
                self.machine.add_transition(trigger='back_to_main_menu', source=state, dest='MAIN_MENU')

    def is_START(self):
        return self.state == 'START'

    def is_MAIN_MENU(self):
        return self.state == 'MAIN_MENU'

    def is_CATEGORY(self):
        return self.state == 'CATEGORY'

    def is_PRODUCT(self):
        return self.state == 'PRODUCT'

    def is_NEW_CATEGORY_NAME(self):
        return self.state == 'NEW_CATEGORY_NAME'

    def is_NEW_PRODUCT_NAME(self):
        return self.state == 'NEW_PRODUCT_NAME'

    def is_NEW_PRODUCT_DESCRIPTION(self):
        return self.state == 'NEW_PRODUCT_DESCRIPTION'

    def is_NEW_PRODUCT_PHOTO(self):
        return self.state == 'NEW_PRODUCT_PHOTO'

    def is_DELETE_PRODUCT(self):
        return self.state == 'DELETE_PRODUCT'
