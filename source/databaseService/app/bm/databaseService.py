from typing import List, Dict
from fastapi import HTTPException

from database.databaseProvider import DatabaseProvider
from database.databaseTableModells import Products, OverallPicture
from entities.models import Request, MailResponse, AppResponse, Product

class DatabaseService:
    database_provider = DatabaseProvider()

    def __init__(self):
        self.database_provider.init_db()

    def intitalize_products(self, request: Request):
        try:
            session = DatabaseService.database_provider.get_session()

            session.query(Products).delete()

            # Create product classes in database
            for id in request.products:
                new_product = Products(
                    name=request.products[id].name,
                    amount=request.products[id].amount,
                    picture=request.products[id].picture
                    )

                session.add(new_product)

            session.add(OverallPicture(picture=request.overall_picture))
            session.commit()
        
        except Exception as e:
            session.rollback()
            raise RuntimeError(f"Database-Service: Error while initializing tables: {e}")
        
        finally:
            session.close()

    def update_products_amount(self, request: Request, add: bool) -> dict:
        try:
            updated_products = {}
            session = DatabaseService.database_provider.get_session()

            # Check if product id exists and update amount
            for id in request.products:
                product = session.query(Products).filter_by(id=id).first()

                # Raise HTTP-Exception if product doesn't exist
                if not product:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Database-Service: Error couldn't find product with id {id}"
                    )
 
                # Add updated product to mail response
                if add:
                    changed_amount = request.products[id].amount - product.amount
                else:
                    changed_amount = product.amount - request.products[id].amount

                updated_products[id] = MailResponse(
                                    id=id,
                                    name=product.name,
                                    amount=product.amount,
                                    changed_amoun=changed_amount
                )

                # Update product
                product.amount = request.products[id].amount 
                product.picture = request.products[id].pictures

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

    def reset_amounts(self):
        try:
            session = DatabaseService.database_provider.get_session()
            products = session.query(Products).all()
            overall_picture = session.query(OverallPicture).first()

            if not products or not overall_picture:
                raise HTTPException(
                    status_code=404, 
                    detail="Database-Service: No products or overall picture found"
                )
            
            # Reset product amount and pictures
            for product in products:
                product.product_amount = 0
                product.product_picture = None
                
            # Reset overall picture
            overall_picture = session.query(OverallPicture).first()
            if overall_picture:
                overall_picture.overall_picture = None

            # Commit changes 
            session.commit()
        
        except Exception as e:
            session.rollback()
            raise RuntimeError(f"Database-Service: Error while reseting products amount: {e}")
        
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
                    detail="Database-Service: No products or  found"
                )
                
            products_dict = {}
                
            for product in products:
                products_dict[product.id] = Product(
                    name=product.product_name,
                    picture=product.product_picture,
                    amount=product.product_amount
                )

            return AppResponse(
                product=products_dict,
                overall_picture=overall_picture
            )

        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail="Error while getting products")
        
        finally:
            session.close()