from typing import Dict, Any
import logging

from entity.exceptions.bad_request_exception import BadRequestException
from entity.enums.action import Action

class Validator:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def validate_data(self, product_list):
        self.logger.info("Validating mail data...")
        try:
            if len(product_list) < 1:
                self.logger.error("No products provided!")
                raise BadRequestException()
            
            check_added_or_removed = 0
            for product in product_list:
                is_data_valid = []

                is_data_valid.append("product_id" in product)
                is_data_valid.append("product_name" in product)
                is_data_valid.append("product_amount_total" in product)
                is_data_valid.append("product_amount_changed" in product)

                is_data_valid.append(isinstance(product["product_id"], int))
                is_data_valid.append(isinstance(product["product_name"], str))
                is_data_valid.append(isinstance(product["product_amount_total"], int))
                is_data_valid.append(isinstance(product["product_amount_changed"], int))
                is_data_valid.append(len(product["product_name"]) > 0)

                check_added_or_removed += 1 if product["product_amount_changed"] > 0 else -1
                if False in is_data_valid:
                    self.logger.error(f"Validation failed: {product}")
                    raise BadRequestException()
                
            if len(product_list) != check_added_or_removed and len(product_list) != check_added_or_removed*-1:
                self.logger.error(f"Added/Removed check failed! It isn't allowed to mix added and removed products in one request. {check_added_or_removed}")
                raise BadRequestException()
            action = Action.ADDED if check_added_or_removed > 0 else Action.DELETED
            return product_list, action
        
        except Exception:
            self.logger.error(f"Invalid data: {product_list}")
            raise BadRequestException()

    def validate_error_message(self, request_data):
        try:
            self.logger.info(request_data)
            is_data_valid = []
            is_data_valid.append("error_message" in request_data)
            is_data_valid.append(isinstance(request_data["error_message"], str))
            is_data_valid.append(len(request_data["error_message"]) > 0)
            if False in is_data_valid:
                self.logger.error("Validation failed!")
                raise BadRequestException()
            return request_data
        
        except Exception:
            self.logger.error(f"Invalid data: {request_data}")
            raise BadRequestException()
