from dataclasses import dataclass

from entity.enums.action import Action

@dataclass
class MailData:
    product_id: int
    product_name: str
    product_amount_changed: int
    product_amount_total: int
    action: Action