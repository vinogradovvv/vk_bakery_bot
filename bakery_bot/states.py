from transitions import Machine


class BotStates:
    states = ['START', 'MAIN_MENU', 'CATEGORY', 'PRODUCT']

    def __init__(self):
        self.machine = Machine(model=self, states=BotStates.states, initial='START')

        self.machine.add_transition(trigger='go_to_main_menu', source='START', dest='MAIN_MENU')
        self.machine.add_transition(trigger='select_category', source='MAIN_MENU', dest='CATEGORY')
        self.machine.add_transition(trigger='select_product', source='CATEGORY', dest='PRODUCT')
        self.machine.add_transition(trigger='go_back_to_main_menu', source='PRODUCT', dest='MAIN_MENU')

    def is_START(self):
        return self.state == 'START'

    def is_MAIN_MENU(self):
        return self.state == 'MAIN_MENU'

    def is_CATEGORY(self):
        return self.state == 'CATEGORY'

    def is_PRODUCT(self):
        return self.state == 'PRODUCT'
