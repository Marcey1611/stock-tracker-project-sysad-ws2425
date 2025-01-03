import logging
from typing import List
from fastapi import HTTPException

from database.databaseProvider import DatabaseProvider
from database.databaseTableModells import Products
from entities.models import MailResponse, AppResponse

class DatabaseService:
    databaseProvider = DatabaseProvider()

    def __init__(self):
        self.databaseProvider.initDb()
        self.logger = logging.getLogger(self.__class__.__name__)

    def updateProductsAmount(self, add: bool ,requestIds: List[int]) -> dict:
        try:
            session = DatabaseService.databaseProvider.getSession()
            updatedProductsDict = {}

            # Check if product id exists and update amount
            for id in requestIds:
                product = session.query(Products).filter_by(productId=id).first()

                # Raise HTTP-Exception if product doesn't exist
                if not product:
                    raise HTTPException(
                        status_code=404,
                        detail=id
                    )
 
                # Update product amount
                product.productAmount += 1 if add else -1 

                # Update or append dictionary
                if product.productId in updatedProductsDict:
                    updatedProductsDict[product.productId].productAmountTotal = product.productAmount
                    updatedProductsDict[product.productId].productAmountAdded += 1 if add else -1
                else:
                    updatedProductsDict[product.productId] = MailResponse(
                        productId=product.productId, 
                        productName=product.productName, 
                        productAmountTotal=product.productAmount,
                        productAmountAdded=1
                    )

            # Commit changes
            session.commit()
            
            return updatedProductsDict
        
        except HTTPException as http_exception:
            session.rollback()
            self.logger.error(f"Error while searching for product: {http_exception}")
            raise http_exception
        
        except Exception as e:
            session.rollback()
            raise RuntimeError(f"An error occurred while updating products amount: {e}")
        
        finally:
            session.close()

    def resetAmounts(self):
        try:
            session = DatabaseService.databaseProvider.getSession()

            # Get all products
            products = session.query(Products).all()
            
            # Reset product amount
            for product in products:
                product.productAmount = 0

            # Commit changes 
            session.commit()
        
        except Exception as e:
            session.rollback()
            raise RuntimeError(f"An error occurred while reseting products amount: {e}")
        
        finally:
            session.close()

    def getProducts(self) -> dict:
        try:
            productsDict = {}
            session = DatabaseService.databaseProvider.getSession()

            # Get all products
            products = session.query(Products).all()

            # Create dictionary with products
            for product in products:
                productsDict[product.productId] = AppResponse(
                    productId=product.productId,
                    productName=product.productName,
                    productPicture=None, # TODO: Send an actual picture
                    productAmount=product.productAmount
                )

            return productsDict

        except Exception as e:
            session.rollback()
            self.logger.error(f"Error while getting products: {e}")
            raise HTTPException(status_code=500, detail="Error while getting products")
        
        finally:
            session.close()
        
    def addProducts(self, products: List[str]):
        try:
            session = DatabaseService.databaseProvider.getSession()

            # Create product classes in database
            for index, product in enumerate(products):
                newProduct = Products(
                    productId=index, 
                    productName=product,
                    productAmount=0
                    )

                session.add(newProduct)

            session.commit()
        
        except Exception as e:
            session.rollback()
            raise RuntimeError(f"An error occurred while creating products: {e}")
        
        finally:
            session.close()