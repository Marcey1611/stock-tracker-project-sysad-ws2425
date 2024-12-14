from fastapi import HTTPException
from database.databaseProvider import DatabaseProvider
from entities.httpStatusEnum import httpStatusCode
from database.databaseTableModells import Products
from entities.UpdatedProductResponse import UpdatedProductResponse


# TODO: Rework exception handling and error messages


class DatabaseService:
    def __init__(self):
        self.databaseProvider = DatabaseProvider()
        self.databaseProvider.initDb()

    def updateProductsAmount(self, add: bool ,updatedProductIds: list[int]):
        try:
            session = self.databaseProvider.getSession()
            updatedProductsList = []

            # Check if product id exists and update amount
            for updatedProductId in updatedProductIds:
                product = session.query(Products).filter_by(productId=updatedProductId).first()

                # Raise HTTP-Exception if product doesn't exist
                if not product:
                    raise HTTPException(
                        status_code=httpStatusCode.CONFLICT,
                        detail=f"Product with id {updatedProductId} doesn't exist."
                        )
 
                # Update product amount
                if add:
                    product.amount += 1
                else:
                    product.amount -= 1

                # Append or update products to list 
                for updatedProduct in updatedProductsList:
                    if product.productId == updatedProduct.productId and add:
                        updatedProduct.productAmountAdded += 1
                    elif product.productId == updatedProduct.productId:
                        updatedProduct.productAmountAdded -= 1
                    else:
                        updatedProductsList.append(UpdatedProductResponse(
                            productId=product.productId, 
                            productName=product.productName, 
                            productPicture="", # TODO: Add product picture handling
                            productAmountTotal=product.productAmount,
                            productAmountAdded=1,
                            errorMessage=None,
                        ))
                        updatedProductsList.append(product)

            # Commit changes
            session.commit()
            
            return updatedProductsList
        
        except HTTPException as http_exception:
            session.rollback()
            raise http_exception
        
        except Exception as e:
            session.rollback()
            raise RuntimeError(f"An error occurred while updating products amount: {e}")
        
        finally:
            session.close()

    def resetAmounts(self):
        try:
            session = self.databaseProvider.getSession()

            # Get all products
            products = session.query(Products).all()
            
            # Reset product amount
            for product in products:
                product.amount = 0

            # Commit changes 
            session.commit()

            return httpStatusCode.OK
        
        except Exception as e:
            session.rollback()
            raise RuntimeError(f"An error occurred while reseting products amount: {e}")
        
        finally:
            session.close()

    def addProducts(self, products: list[str]):
        try:
            session = self.databaseProvider.getSession()

            # Create product classes in database
            for index, product in enumerate(products):
                newProduct = Products(
                    productId=index, 
                    productName=product,
                    productAmount=0
                    )

                session.add(newProduct)

            session.commit()
            return httpStatusCode.OK
        
        except Exception as e:
            session.rollback()
            raise RuntimeError(f"An error occurred creating product classes: {e}")
        
        finally:
            session.close()