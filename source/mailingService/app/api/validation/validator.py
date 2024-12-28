from typing import Dict, Any
import logging

from entity.exceptions import BadRequestException
from entity.enums import Action

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

class Validator:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def validateData(self, productList: Dict[str, Any], action: Action) -> Dict[str, Any]:
        try:
            if len(productList) < 1:
                self.logger.error("Got empty product list!")
                raise BadRequestException()
            for product in productList:
                isDataValid = []

                isDataValid.append("productId" in product)
                isDataValid.append("productName" in product)
                isDataValid.append("productAmountAdded" in product)
                isDataValid.append("productAmountTotal"  in product)

                isDataValid.append(isinstance(product["productId"], int))
                isDataValid.append(isinstance(product["productName"], str))
                isDataValid.append(isinstance(product["productAmountAdded"], int))
                isDataValid.append(isinstance(product["productAmountTotal"], int))
                isDataValid.append(len(product["productName"]) > 0)

                if False in isDataValid:
                    self.logger.error("Validation failed!")
                    raise BadRequestException()
            return productList
        
        except Exception:
            self.logger.error(f"Invalid data: {productList}")
            raise BadRequestException()

    def validateErrorMessage(self, requestData: Dict[str, Any]) -> Dict[str, Any]:
        try:
            isDataValid = []
            isDataValid.append("errorMessage" in requestData)
            isDataValid.append(isinstance(requestData["errorMessage"], str))
            isDataValid.append(len(requestData["errorMessage"]) > 0)
            if False in isDataValid:
                    self.logger.error("Validation failed!")
                    raise BadRequestException()
            return requestData
        
        except Exception:
            self.logger.error(f"Invalid data: {requestData}")
            raise BadRequestException()
