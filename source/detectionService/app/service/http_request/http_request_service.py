import copy
from typing import Dict

from api import api_rest_client_database
from entities.detection.product import Product
from entities.detection.track_manager import TrackerManager
from entities.http.database_models import DatabaseUpdateRequest
from service.detection.frame_codings import encode_frame
from service.detection.frame_drawings import draw_bounding_box


def init_database(frame,names):
    all_products: Dict[int, Product] = {}
    for index, name in enumerate(names.values()):
        all_products[index] = Product(name=name,amount=0,picture=None)
    http_database_request = DatabaseUpdateRequest(overall_picture=encode_frame(frame), products=all_products)
    return api_rest_client_database.update_database_products(http_database_request)


def generate_http_request(trackers: TrackerManager, annotated_frame, frame):
    http_database_request = DatabaseUpdateRequest(overall_picture=encode_frame(annotated_frame), products={})
    if frame is None:
        api_rest_client_database.update_database_products(http_database_request)
    else:
        http_database_request.products = generate_products(trackers, frame)
        api_rest_client_database.update_database_products(http_database_request)

def generate_products(trackers: TrackerManager, frame):
    from service.detection.frame_detecting import model_cls_names
    tmp_detected_objects = copy.deepcopy(trackers.detected_objects)
    all_products: Dict[int, Product] = {}
    detected_objects_list = list(tmp_detected_objects.values())
    while len(detected_objects_list) > 0:
        item = copy.deepcopy(detected_objects_list[0])
        product_frame = copy.deepcopy(frame)
        cls_list = [cls_item for cls_item in detected_objects_list if
                    item.get_cls_id() == cls_item.get_cls_id()]
        product_name = model_cls_names[item.get_cls_id()]
        product_amount = len(cls_list)
        for pic_item in cls_list:
            product_frame = draw_bounding_box(product_frame, pic_item)
            detected_objects_list.remove(pic_item)

        product_picture = encode_frame(product_frame)
        all_products[item.get_cls_id()] = Product(name=product_name, amount=product_amount,
                                                  picture=product_picture)
    return all_products
