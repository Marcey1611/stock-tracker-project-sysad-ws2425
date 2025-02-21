# http
## database_models.py
### DatabaseUpdateRequest
```python
class DatabaseUpdateRequest(BaseModel):
    products: Dict[int, Product]
    overall_picture: str
```
This is the class that is to make a request to the [Database Service](../../../../database_service/Readme.md).

### DatabaseUpdateResponse
```python
class DatabaseUpdateResponse(BaseModel):
    status_code: int
```
This class is there to receive the response from the [Database Service](../../../../database_service/Readme.md).
## product.py
```python
class Product(BaseModel):
    name: str
    amount: int
    picture: str | None = None
```
This is the class used in the DatabaseUpdateRequest for the objects.