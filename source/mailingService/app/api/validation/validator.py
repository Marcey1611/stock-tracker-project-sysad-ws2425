from typing import Dict, Any, List
import logging

from entity.exceptions import BadRequestException

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


class Validator:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def validateData(self, noError: bool, data: Dict[str, Any]) -> Dict[str, Any]:
        if not data:
            self.logger.error("Data is empty")
            raise BadRequestException()

        try:
            if noError:
                self.validateMailData(data)
            else:
                self.validateErrorMailData(data)
        except Exception as exception:
            self.logger.error(f"Invalid data: {data} - {str(exception)}")
            raise BadRequestException()

        return data

    def validateErrorMailData(self, data: Dict[str, Any]) -> None:
        required_fields = [
            "productId", "productName", "productPicture", 
            "productAmount", "productAmountTotal", "errorMessage"
        ]
        field_types = {
            "productId": int,
            "productName": str,
            "productPicture": str,
            "productAmountAdded": int,
            "productAmountTotal": int,
            "errorMessage": str,
        }
        self._validate_items(data, required_fields, field_types, check_non_empty=["productName", "errorMessage"])

    def validateMailData(self, data: Dict[str, Any]) -> None:
        required_fields = [
            "productId", "productName", "productPicture", 
            "productAmount", "productAmountTotal"
        ]
        field_types = {
            "productId": int,
            "productName": str,
            "productPicture": str,
            "productAmountAdded": int,
            "productAmountTotal": int,
        }
        self._validate_items(data, required_fields, field_types, check_non_empty=["productName"], check_absent=["errorMessage"])

    def _validate_items(
        self, 
        data: Dict[str, Any], 
        required_fields: List[str], 
        field_types: Dict[str, type], 
        check_non_empty: List[str] = None, 
        check_absent: List[str] = None
    ) -> None:
        check_non_empty = check_non_empty or []
        check_absent = check_absent or []

        for item in data.values():
            conditions = []

            conditions.append(all(field in item for field in required_fields))

            conditions.extend(
                field in item and isinstance(item[field], expected_type) 
                for field, expected_type in field_types.items()
            )

            conditions.extend(
                bool(item.get(field)) for field in check_non_empty
            )

            conditions.extend(
                field not in item for field in check_absent
            )

            if not all(conditions):
                self.logger.error(f"Invalid data: {item}")
                raise BadRequestException()
