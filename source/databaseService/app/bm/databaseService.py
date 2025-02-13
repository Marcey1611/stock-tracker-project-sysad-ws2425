from fastapi import HTTPException
from sqlalchemy import text
from typing import Dict
import logging

from database.databaseProvider import DatabaseProvider
from database.databaseTableModells import Products, OverallPicture
from entities.models import Request, MailResponse, AppResponse, Product

class DatabaseService:
    database_provider = DatabaseProvider()

    def __init__(self):
        self.database_provider.init_db()
        self.logger = logging.getLogger(self.__class__.__name__)

    def update_products(self, request: Request) -> Dict[int, MailResponse]:
        self.logger.info("Updating products.....................................................................................................................")
        try:
            self.logger.info("1")
            self.logger.info(request.products)
            self.logger.info("1.1")
            if not request.products == {}:
                if not next(iter(request.products.values())).picture:
                    self.intitalize_products(request)
                else:
                    return self.update_products_amount(request) 
            else:
                return self.update_products_amount(request) 
            self.logger.info("5")
            return None

        except Exception as e:
            self.logger.error(f"Database-Service: Error while updating products: {e}")
            raise RuntimeError(f"{e}")

    def intitalize_products(self, request: Request):
        try:
            session = DatabaseService.database_provider.get_session()

            session.query(Products).delete()
            session.execute(text("ALTER SEQUENCE products_id_seq RESTART WITH 1;"))

            # Create product classes in database
            for id in request.products:
                new_product = Products(
                    type_id=id,
                    name=request.products[id].name,
                    amount=request.products[id].amount,
                    picture=request.products[id].picture
                    )

                session.add(new_product)

            session.query(OverallPicture).delete()
            # Reset auto-increment sequence for overall_picture table and add new picture
            session.execute(text("ALTER SEQUENCE overall_picture_id_seq RESTART WITH 1;"))
            session.add(OverallPicture(picture=request.overall_picture))
            session.commit()
            self.logger.info("SUCCESS")
        
        except Exception as e:
            session.rollback()
            raise RuntimeError(f"Database-Service: Error while initializing tables: {e}")
        
        finally:
            session.close()

    def update_products_amount(self, request: Request) -> Dict[int, MailResponse]:
        try:
            updated_products = {}
            session = DatabaseService.database_provider.get_session()

            # Check if the amount of any product was reduced to zero
            products = session.query(Products).all()
            removed_products = [product for product in products if product.type_id not in request.products]
            for product in removed_products:
                if product.amount is not 0:
                    changed_amount = product.amount * -1
                    product.amount = 0
                    product.picture = None
                    session.commit()

                    updated_products[product.type_id] = MailResponse(
                                        id=product.type_id,
                                        name=product.name,
                                        amount=0,
                                        changed_amount=changed_amount
                    )

            # Check if product id exists and update amount
            for id in request.products:
                product = session.query(Products).filter_by(type_id=id).first()

                # Raise HTTP-Exception if product doesn't exist
                if not product:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Database-Service: Error couldn't find product with id {id}"
                    )
 
                if request.products[id].amount >= product.amount:
                    changed_amount = request.products[id].amount - product.amount
                else:
                    changed_amount = (product.amount - request.products[id].amount) * -1

                updated_products[id] = MailResponse(
                                    id=id,
                                    name=product.name,
                                    amount=product.amount,
                                    changed_amount=changed_amount
                )

                # Update product
                product.amount = request.products[id].amount 
                product.picture = request.products[id].picture

                session.commit()

            # Update overall picture or add one if it doesn't exist
            overall_picture = session.query(OverallPicture).first()
            if overall_picture:
                overall_picture.picture = request.overall_picture
            else:
                new_overall_picture = OverallPicture(picture=request.overall_picture)
                session.add(new_overall_picture)

            session.commit()
                
            return updated_products
        
        except Exception as e:
            session.rollback()
            raise RuntimeError(f"Database-Service: Error while updating products amount: {e}")
        
        finally:
            session.close()            

    def get_products(self) -> AppResponse:
        try:
            session = DatabaseService.database_provider.get_session()
            products = session.query(Products).all()
            overall_picture = session.query(OverallPicture).first()
            
            if not products or not overall_picture:
                raise HTTPException(
                    status_code=404, 
                    detail="Database-Service: No products available yet."
                )
                
            products_dict = {}
                
            for product in products:
                products_dict[product.type_id] = Product(
                    name=product.name,
                    amount=product.amount,
                    picture=product.picture
                )

            return AppResponse(
                products=products_dict,
                overall_picture=overall_picture.picture
            )

        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Database-Service: Error while getting products: {e}")
        
        finally:
            session.close()