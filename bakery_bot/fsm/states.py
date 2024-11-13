from transitions import Machine
from transitions.core import MachineError

from config.logging_config import logger


class BotStates:
    """
    Defines the states and transitions for the bot's finite state machine (FSM)
    """

    states = [
        "START",
        "MAIN_MENU",
        "NEW_CATEGORY_NAME",
        "CATEGORY",
        "PRODUCT",
        "NEW_PRODUCT_NAME",
        "NEW_PRODUCT_DESCRIPTION",
        "NEW_PRODUCT_PHOTO",
        "DELETE_PRODUCT",
    ]

    def __init__(self, **kwargs):
        self.state = kwargs.get("state", "START")
        self.product_name = kwargs.get("product_name", None)
        self.product_description = kwargs.get("product_description", None)
        self.category_name = kwargs.get("category_name", None)
        self.machine = Machine(model=self, states=BotStates.states, initial="START")

        self.machine.add_transition(
            trigger="main_menu", source="START", dest="MAIN_MENU"
        )

        self.machine.add_transition(
            trigger="new_category_name", source="MAIN_MENU", dest="NEW_CATEGORY_NAME"
        )
        self.machine.add_transition(
            trigger="main_menu", source="NEW_CATEGORY_NAME", dest="MAIN_MENU"
        )

        self.machine.add_transition(
            trigger="category", source="MAIN_MENU", dest="CATEGORY"
        )
        self.machine.add_transition(
            trigger="main_menu", source="CATEGORY", dest="MAIN_MENU"
        )

        self.machine.add_transition(
            trigger="new_product_name", source="CATEGORY", dest="NEW_PRODUCT_NAME"
        )
        self.machine.add_transition(
            trigger="main_menu", source="NEW_PRODUCT_NAME", dest="MAIN_MENU"
        )
        self.machine.add_transition(
            trigger="new_product_description",
            source="NEW_PRODUCT_NAME",
            dest="NEW_PRODUCT_DESCRIPTION",
        )
        self.machine.add_transition(
            trigger="main_menu", source="NEW_PRODUCT_DESCRIPTION", dest="MAIN_MENU"
        )
        self.machine.add_transition(
            trigger="new_product_photo",
            source="NEW_PRODUCT_DESCRIPTION",
            dest="NEW_PRODUCT_PHOTO",
        )
        self.machine.add_transition(
            trigger="main_menu", source="NEW_PRODUCT_PHOTO", dest="MAIN_MENU"
        )
        self.machine.add_transition(
            trigger="category", source="NEW_PRODUCT_PHOTO", dest="CATEGORY"
        )

        self.machine.add_transition(
            trigger="product", source="CATEGORY", dest="PRODUCT"
        )
        self.machine.add_transition(
            trigger="category", source="PRODUCT", dest="CATEGORY"
        )

        self.machine.add_transition(
            trigger="delete_product", source="CATEGORY", dest="DELETE_PRODUCT"
        )
        self.machine.add_transition(
            trigger="main_menu", source="DELETE_PRODUCT", dest="MAIN_MENU"
        )
        self.machine.add_transition(
            trigger="back_to_main_menu", source="*", dest="MAIN_MENU"
        )

    def trigger_event(self, event):
        try:
            getattr(self, event)()
        except MachineError as e:
            logger.error(f"FSM error: {e}")

    def to_json(self):
        return {
            "state": self.state,
            "product_name": self.product_name,
            "product_description": self.product_description,
            "category_name": self.category_name,
        }

    def load(self, **kwargs):
        self.state = kwargs.get("state", "START")
        self.product_name = kwargs.get("product_name", None)
        self.product_description = kwargs.get("product_description", None)
        self.category_name = kwargs.get("category_name", None)

    def is_start(self):
        return self.state == "START"

    def is_main_menu(self):
        return self.state == "MAIN_MENU"

    def is_category(self):
        return self.state == "CATEGORY"

    def is_product(self):
        return self.state == "PRODUCT"

    def is_new_category_name(self):
        return self.state == "NEW_CATEGORY_NAME"

    def is_new_product_name(self):
        return self.state == "NEW_PRODUCT_NAME"

    def is_new_product_description(self):
        return self.state == "NEW_PRODUCT_DESCRIPTION"

    def is_new_product_photo(self):
        return self.state == "NEW_PRODUCT_PHOTO"

    def is_delete_product(self):
        return self.state == "DELETE_PRODUCT"
