# HTTP Requests

## [http_request_service.py](../../../../../../../source/detectionService/app/service/http_request/http_request_service.py)

### init_database
```python
def init_database(frame,names):
    all_products: Dict[int, Product] = {}
    for index, name in enumerate(names.values()):
        all_products[index] = Product(name=name,amount=0,picture=None)
    http_database_request = DatabaseUpdateRequest(overall_picture=encode_frame(frame), products=all_products)
    return api_rest_client_database.update_database_products(http_database_request)
```
When the first MQTT-Message arrives, the detection service then triggers this method to tell the [Database Service](../../../../database_service/Readme.md) which object it can detect.
To have an image in the [App/Web](../../../../flutter_app/Readme.md) before there is something to update, an overall picture is [encoded](../detection/Readme.md) and added.

### generate_http_request
```python
def generate_http_request(trackers: TrackerManager, annotated_frame, frame):
    http_database_request = DatabaseUpdateRequest(overall_picture=encode_frame(annotated_frame), products={})
    if frame is None:
        api_rest_client_database.update_database_products(http_database_request)
    else:
        http_database_request.products = generate_products(trackers, frame)
        api_rest_client_database.update_database_products(http_database_request)
```
This method does the [Database Service](../../../../database_service/Readme.md) call over the [api_rest_client_database](../../api/Readme.md) file .
Before it generates a [DatabaseUpdateRequest](../../entities/http/Readme.md).
Additionally, the overall picture will be [encoded](../detection/Readme.md) base64.

### generate_products
```python
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
```
In this methode all detected objects are transformed into products.
While doing so, it generates a product-class-frame which contains all bounding boxes from all Products with the same product id.
The bounding boxes are drawn by the [draw_bounding_box](../detection/Readme.md) method.
At the end, the frame will be base64 [encoded](../detection/Readme.md).