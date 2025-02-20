from fastapi import HTTPException
from sqlalchemy import text
from typing import Dict
import logging

from database.database_provider import DatabaseProvider
from database.database_table_modells import Products, OverallPicture
from entities.models import Request, MailResponse, AppResponse, Product

class DatabaseService:
    database_provider = DatabaseProvider()

    def __init__(self):
        self.database_provider.init_db()
        self.logger = logging.getLogger(self.__class__.__name__)

    def update_products(self, request: Request) -> Dict[int, MailResponse]:
        try:
            # Check if request is initialization or update
            if request.products and all(product.picture is None for product in request.products.values()):
                self.intitalize_products(request)
                return {}
            else:
                return self.update_products_amount(request)

        except Exception as e:
            self.logger.error(f"Error while updating products: {e}")
            raise RuntimeError(f"{e}")

    def intitalize_products(self, request: Request):
        try:
            with DatabaseService.database_provider.get_session() as session:
                # Delete all elements from products and overall_picture tables
                session.execute(text("""
                    DELETE FROM products;
                    ALTER SEQUENCE products_id_seq RESTART WITH 1;
                    DELETE FROM overall_picture;
                    ALTER SEQUENCE overall_picture_id_seq RESTART WITH 1;
                """))

                # Add new products
                new_products = [
                    Products(
                        type_id=id,
                        name=product.name,
                        amount=product.amount,
                        picture=product.picture
                    ) for id, product in request.products.items()
                ]
                session.add_all(new_products)

                # Add new overall_picture
                session.add(OverallPicture(picture=request.overall_picture))

                session.commit()
                self.logger.info(f"Successfully initialized:\n\nProducts\n{request.products}\n\nOverall-Picture\n{request.overall_picture}\n")

        except Exception as e:
            self.logger.error(f"Error while initializing tables: {e}")
            raise RuntimeError(f"Database-Service: Error while initializing tables: {e}")

    def update_products_amount(self, request: Request) -> Dict[int, MailResponse]:
        updated_products = {}
        try:
            with DatabaseService.database_provider.get_session() as session:
                product_ids = set(request.products.keys())
                products_in_db = session.query(Products).filter(Products.type_id.in_(product_ids)).all()

                # Check if request has Ids which are not in db
                if product_ids - {product.type_id for product in products_in_db}:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Database-Service: Error couldn't find product with id {id}"
                    )

                # Set amount zero if product is not in request
                removed_products = session.query(Products).filter(~Products.type_id.in_(product_ids)).all()
                for product in removed_products:
                    if product.amount != 0:
                        updated_products[product.type_id] = MailResponse(
                            id=product.type_id,
                            name=product.name,
                            amount=0,
                            changed_amount=-product.amount
                        )
                        product.amount = 0
                        product.picture = None

                self.logger.info(f"Successfully removed:\n\nProducts\n{updated_products}\n")    

                # Update products
                for product_in_db in products_in_db:
                    changed_amount = request.products[product_in_db.type_id].amount - product_in_db.amount

                    product_in_db.amount = request.products[product_in_db.type_id].amount 
                    product_in_db.picture = request.products[product_in_db.type_id].picture

                    if changed_amount != 0:
                        updated_products[id] = MailResponse(
                                            id=product_in_db.type_id,
                                            name=product_in_db.name,
                                            amount=product_in_db.amount,
                                            changed_amount=changed_amount
                        )

                # Update overall picture
                overall_picture = session.query(OverallPicture).first()
                if overall_picture.picture:
                    overall_picture.picture = request.overall_picture
                else:
                    session.add(OverallPicture(picture=request.overall_picture))

                session.commit()
                
            self.logger.info(f"Successfully updated:\n\nProducts\n{request.products}\n\nOverall-Picture\n{request.overall_picture}\n")    
            return updated_products
        
        except HTTPException as e:
            self.logger.error(e)
            raise e
        except Exception as e:
            self.logger.error(f"Error while updating products amount: {e}")
            raise RuntimeError(f"Database-Service: Error while updating products amount: {e}")           

    def get_products(self) -> AppResponse:
        try:
            with DatabaseService.database_provider.get_session() as session:
                products = session.query(Products).all()
                overall_picture = session.query(OverallPicture).first()

                if not products or not overall_picture:
                    raise HTTPException(
                        status_code=404, 
                        detail="Database-Service: No products available yet."
                    )

                products_dict = {
                    product.type_id: Product(
                        name=product.name,
                        amount=product.amount,
                        picture=product.picture
                    ) 
                    for product in products
                }

                return AppResponse(
                    products=products_dict,
                    overall_picture=overall_picture.picture
                )

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database-Service: Error while getting products: {e}")