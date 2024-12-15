from typing import Dict, Any
import logging

from entity.exceptions import BadRequestException

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

class Validator:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def validateData(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            productIdMissing = "productId" not in data
            productNameMissing = "productName" not in data
            productPictureMissing = "productPicture" not in data
            productIdInvalidType = not isinstance(data["productId"], int)
            productNameInvalidType = not isinstance(data["productName"], str)
            productPictureInvalidType = not isinstance(data["productPicture"], str)
            productNameEmpty = len(data["productName"]) == 0

            if productIdMissing or productNameMissing or productPictureMissing or productIdInvalidType or productNameInvalidType or productPictureInvalidType or productNameEmpty:
                self.logger.error(f"Invalid data: {data}")
                raise BadRequestException()
            
            return data
        except Exception as exception:
            self.logger.error(f"Invalid data: {data}")
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