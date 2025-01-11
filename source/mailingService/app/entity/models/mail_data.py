from entity.enums.action import Action

class MailData:
    def __init__(self, product_id: int, product_name: str, product_amount_changed: int, product_amount_total: int, action: Action):
        self.__product_id = product_id
        self.__product_name = product_name
        self.__product_amount_changed = product_amount_changed
        self.__product_amount_total = product_amount_total
        self.__action = action


    def get_product_id(self) -> int:
        return self.__product_id
    
    def get_product_name(self) -> str:
        return self.__product_name
    
    def get_action(self) -> Action:
        return self.__action
    
    def get_product_amount_changed(self) -> int:
        return self.__product_amount_changed
    
    def get_product_amount_total(self) -> int:
        return self.__product_amount_total