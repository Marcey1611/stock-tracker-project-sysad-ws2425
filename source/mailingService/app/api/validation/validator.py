from typing import Dict, Any, List
import logging

from entity.exceptions import BadRequestException

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


class Validator:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def validateData(self, productList: Dict[str, Any]) -> Dict[str, Any]:
        try:
            for product in productList:
                isDataValid = []
                isDataValid.append("productId" in product)
                isDataValid.append("productName" in product)
                isDataValid.append("productPicture" in product)
                isDataValid.append("productAmountAdded" in product)
                isDataValid.append("productAmountTotal"  in product)
                isDataValid.append(isinstance(product["productId"], int))
                isDataValid.append(isinstance(product["productName"], str))
                isDataValid.append(isinstance(product["productPicture"], str))
                isDataValid.append(isinstance(product["productAmountAdded"], int))
                isDataValid.append(isinstance(product["productAmountTotal"], int))
                isDataValid.append(len(product["productName"]) > 0)
                self.logger.info(isDataValid)
                self.logger.info(product)

                if False in isDataValid:
                    self.logger.error("Validation failed!")
                    raise BadRequestException()
            return productList
        except Exception:
            self.logger.error(f"Invalid data: {productList}")
            raise BadRequestException()

    def validateErrorMessage(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            errorMessageMissing = "errorMessage" not in data
            errorMessageInvalidType = not isinstance(data["errorMessage"], str)
            errorMessageEmpty = len(data["errorMessage"]) == 0
            if errorMessageMissing or errorMessageInvalidType or errorMessageEmpty:
                    raise BadRequestException()
        except Exception as exception:
            self.logger.error(f"Invalid data: {data}")
            raise BadRequestException()
