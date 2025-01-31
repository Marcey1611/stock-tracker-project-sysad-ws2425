import logging
from typing import List
from fastapi import HTTPException

from database.databaseProvider import DatabaseProvider
from database.databaseTableModells import Products, OverallPicture
from entities.models import Request, MailResponse, AppResponse

class DatabaseService:
    database_provider = DatabaseProvider()

    def __init__(self):
        self.database_provider.init_db()
        self.logger = logging.getLogger(self.__class__.__name__)

    def update_products_amount(self, add: bool, request: Request):
        try:
            session = DatabaseService.database_provider.get_session()
            updated_products_dict = {}

            # Check if product id exists and update amount
            for id in request.products:
                product = session.query(Products).filter_by(product_id=id).first()

                # Raise HTTP-Exception if product doesn't exist
                if not product:
                    raise HTTPException(
                        status_code=404,
                        detail=id
                    )
 
                # Update product amount
                product.product_amount += 1 if add else -1 

                # Update product picture
                product.product_picture = request.pictures[id]

                # Update or append dictionary
                if product.product_id in updated_products_dict:
                    updated_products_dict[product.product_id].product_amount_total = product.product_amount
                    updated_products_dict[product.product_id].product_amount_changed += 1 if add else -1
                else:
                    updated_products_dict[product.product_id] = MailResponse(
                        product_id=product.product_id, 
                        product_name=product.product_name, 
                        product_amount_total=product.product_amount,
                        product_amount_changed=1 if add else -1
                    )

            # Update overall picture
            picture = session.query(OverallPicture).first()
            if picture:
                picture.overall_picture = request.overall_picture

            # Commit changes
            session.commit()
            
            return updated_products_dict
        
        except HTTPException as http_exception:
            session.rollback()
            self.logger.error(f"Error while searching for product: {http_exception}")
            raise http_exception
        
        except Exception as e:
            session.rollback()
            raise RuntimeError(f"An error occurred while updating products amount: {e}")
        
        finally:
            session.close()

    def reset_amounts(self):
        try:
            session = DatabaseService.database_provider.get_session()

            # Get all products
            products = session.query(Products).all()
            
            # Reset product amount and pictures
            for product in products:
                product.product_amount = 0
                product.product_picture = None
                
            # Reset overall picture
            picture = session.query(OverallPicture).first()
            if picture:
                picture.overall_picture = None

            # Commit changes 
            session.commit()
        
        except Exception as e:
            session.rollback()
            raise RuntimeError(f"An error occurred while reseting products amount: {e}")
        
        finally:
            session.close()

    def get_products(self) -> dict:
        try:
            products_dict = {}
            session = DatabaseService.database_provider.get_session()

            # Get all products
            products = session.query(Products).all()

            # Create dictionary with products
            for product in products:
                products_dict[product.product_id] = AppResponse(
                    product_id=product.product_id,
                    product_name=product.product_name,
                    product_picture=product.product_picture,
                    product_amount=product.product_amount
                )

            return products_dict

        except Exception as e:
            session.rollback()
            self.logger.error(f"Error while getting products: {e}")
            raise HTTPException(status_code=500, detail="Error while getting products")
        
        finally:
            session.close()
        
    def add_products(self, products: List[str]):
        try:
            session = DatabaseService.database_provider.get_session()

            # Create product classes in database
            for product in products:
                new_product = Products(
                    product_name=product,
                    product_picture=None,
                    product_amount=0
                    )

                session.add(new_product)

            session.add(OverallPicture(overall_picture=None))

            session.commit()
        
        except Exception as e:
            session.rollback()
            raise RuntimeError(f"An error occurred while creating products: {e}")
        
        finally:
            session.close()