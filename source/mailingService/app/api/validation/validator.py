from typing import Dict, Any
import logging

from entity.exceptions.bad_request_exception import BadRequestException

class Validator:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def validate_data(self, product_list) -> Dict[str, Any]:
        self.logger.debug("test")
        try:
            if len(product_list) < 1:
                self.logger.error("No products provided!")
                raise BadRequestException()
            for product in product_list:
                is_data_valid = []

                is_data_valid.append("productId" in product)
                is_data_valid.append("productName" in product)
                is_data_valid.append("productAmountTotal" in product)
                is_data_valid.append("productAmountAdded" in product)

                is_data_valid.append(isinstance(product["productId"], int))
                is_data_valid.append(isinstance(product["productName"], str))
                is_data_valid.append(isinstance(product["productAmountTotal"], int))
                is_data_valid.append(isinstance(product["productAmountAdded"], int))
                is_data_valid.append(len(product["productName"]) > 0)

                if False in is_data_valid:
                    self.logger.error("Validation failed!")
                    raise BadRequestException()
            return product_list
        
        except Exception:
            self.logger.error(f"Invalid data: {product_list}")
            raise BadRequestException()

    def validate_error_message(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            is_data_valid = []
            is_data_valid.append("errorMessage" in request_data)
            is_data_valid.append(isinstance(request_data["errorMessage"], str))
            is_data_valid.append(len(request_data["errorMessage"]) > 0)
            if False in is_data_valid:
                self.logger.error("Validation failed!")
                raise BadRequestException()
            return request_data
        
        except Exception:
            self.logger.error(f"Invalid data: {request_data}")
            raise BadRequestException()
