from  fastapi import FastAPI,HTTPException,APIRouter,Depends,Header
from database.database import Sessionlocal
# from passlib.context import CryptContext
from src.schemas.product_order import OrderAll,ProductAll,productpass,orderid
from src.models.product import Product
from src.models.order import Order
from src.utils.token import get_token_product,get_token_product_by_id,decode_token_by_product_id
from src.utils.token import get_token_order_by_id,decode_token_by_order_id
from logs.log_config import logger



productOrder = APIRouter()

db = Sessionlocal()

#************************product**************************

#----------------------create product-------------------------

@productOrder.post("/create_product",response_model=ProductAll)
def create_product(products:ProductAll):
    logger.info("Creating a new product")
    
    new_customer= Product(
        name = products.name,
        price = products.price
    )
    logger.success("product is created.")
    logger.info("product adding to database.......")
    
    db.add(new_customer)
    logger.info("product loaded successfully")
    db.commit()
    logger.success("Product database has been saved successfully.")
    return new_customer

#-------------------------encode product--------------------------

@productOrder.get("/encode_product")
def encode_product(id : int ,name : str, price : int):
    access_token = get_token_product(id,name,price)
    return access_token

#----------------------encode id product--------------------------

@productOrder.get("/encode_product_id")
def encode_product_id(id : int ):
    logger.info("access token genereting....")
    access_token =get_token_product_by_id(id)
    logger.info("access token genereted.")
    logger.success("access token successfully.")
    return access_token


#----------------------decode id product--------------------------

@productOrder.get("/decode_id")
def decode_id(token : str):
    logger.info("decode product id using token.....")
    id = decode_token_by_product_id(token)
    logger.success("product id decode token successfully.")
    return id

#---------------------get by id product--------------------------


@productOrder.get("/get_product_by_id/{product_id}",response_model=ProductAll)
def get_product_by_id(product_id:int):
    logger.info("Accessing product by ID")
    
    db_product = db.query(Product).filter(Product.id == product_id ,Product.is_active == True).first()
    logger.success("retrieved product successfully")
    
    if db_product is  None:
        logger.error("product not found")
        raise HTTPException(status_code=404,detail="product not found")
    
    logger.info("product details retrieved successfully")
    return db_product


#------------------------get_product_by_id_token--------------------------------

# @productOrder.get("/get_product_by_id_token", response_model=ProductAll)
# def get_product_by_id_token(token: str):
#     product_id = decode_token_by_product_id(token)
#     db_product = db.query(Product).filter(Product.id == product_id, Product.is_active == True).first()
#     if db_product is None:
#         raise HTTPException(status_code=404, detail="Product not found")
#     return db_product

#-------depends------

@productOrder.get("/get_product_by_id_token_depends", response_model=ProductAll)
def get_product_by_id_token_depends(product_id=Depends(decode_token_by_product_id)):
    db_product = db.query(Product).filter(Product.id == product_id, Product.is_active == True).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

#---------header----------

@productOrder.get("/get_product_by_id_token_header", response_model=ProductAll)
def get_product_by_id_token_header(token=Header(...)):
    product_id = decode_token_by_product_id(token)
    db_product = db.query(Product).filter(Product.id == product_id, Product.is_active == True).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

#-----------------------get all product------------------------------    

@productOrder.get("/get_all_product",response_model=list[ProductAll])
def get_all_product():
    logger.info("Attempting to retrieve all product information.")
    db_product = db.query(Product).all()
    logger.success("employee retrieved succesfully")
    
    if db_product is  None:
        logger.error("product not found")
        raise HTTPException(status_code=404,detail="product not found")
    
    logger.success("product information retrieved successfully")
    return db_product

#-----------------------update product---------------------


@productOrder.put("/update_product",response_model=ProductAll)
def update_product(product_id:int,products:ProductAll):
    logger.info("access update product details using id")
    db_product = db.query(Product).filter(Product.id == product_id , Product.is_active == True).first()
    logger.info("retrieving product data from database")
    
    if db_product is  None:
        logger.info("product not found")
        raise HTTPException(status_code=404,detail="product not found")
    
    logger.info("Updating product details for product ID")
    
    db_product.name = products.name,
    db_product.price = products.price
    
    db.commit()
    logger.success("product details updated successfully for product ID")
    return db_product

#------------------------update token product-------------------------


# @productOrder.put("/update_product_token",response_model=ProductAll)
# def update_product_token(token:str,products:ProductAll):
#     user_id = decode_token_by_product_id(token)
#     db_product = db.query(Product).filter(Product.id == user_id , Product.is_active == True).first()
#     if db_product is  None:
#         raise HTTPException(status_code=404,detail="product not found")
    
#     db_product.name = products.name,
#     db_product.price = products.price
    
#     db.commit()
#     return db_product

#-------depends------

@productOrder.put("/update_product_token_depends",response_model=ProductAll)
def update_product_token_depends(products:ProductAll,user_id=Depends(decode_token_by_product_id)):
    db_product = db.query(Product).filter(Product.id == user_id , Product.is_active == True).first()
    if db_product is  None:
        raise HTTPException(status_code=404,detail="product not found")
    
    db_product.name = products.name,
    db_product.price = products.price
    
    db.commit()
    return db_product

#----------header-------------

@productOrder.put("/update_product_token_header",response_model=ProductAll)
def update_product_token_header(products:ProductAll,token=Header(...)):
    user_id = decode_token_by_product_id(token)
    db_product = db.query(Product).filter(Product.id == user_id , Product.is_active == True).first()
    if db_product is  None:
        raise HTTPException(status_code=404,detail="product not found")
    
    db_product.name = products.name,
    db_product.price = products.price
    
    db.commit()
    return db_product

#----------------------delete product--------------------------

@productOrder.delete("/delete_product")
def delete_product(product_id:str):
    logger.info("Attempting to delete product.")
    
    db_product = db.query(Product).filter(Product.id == product_id , Product.is_active == True).first()
    logger.info("retrieving product data from database")
    
    if db_product is None:
        logger.error("Product not found or inactive.")
        raise HTTPException(status_code=404,detail="product not found")
    
    db_product.is_active = False
    db_product.is_delete = True

    db.commit()
    logger.success("Product deleted successfully.")
    return {"message":"product deleted successfully"}

#--------------------------delete product token-----------------------------

# @productOrder.delete("/delete_product_token")
# def delete_product_token(token : str):
#     product_id = decode_token_by_product_id(token)
#     db_product = db.query(Product).filter(Product.id == product_id,Product.is_active == True).first()
#     if db_product is None:
#         raise HTTPException(status_code=404,detail="product not found")
    
#     db_product.is_active = False
#     db_product.is_delete = True
    
#     db.commit()
#     return "product delete successfully"

#-------depends------

@productOrder.delete("/delete_product_token_depends")
def delete_product_token_depends(product_id=Depends(decode_token_by_product_id)):
    db_product = db.query(Product).filter(Product.id == product_id,Product.is_active == True).first()
    if db_product is None:
        raise HTTPException(status_code=404,detail="product not found")
    
    db_product.is_active = False
    db_product.is_delete = True
    
    db.commit()
    return "product delete successfully"

#--------header----------

@productOrder.delete("/delete_product_token_header")
def delete_product_token_header(token = Header(...)):
    product_id = decode_token_by_product_id(token)
    db_product = db.query(Product).filter(Product.id == product_id,Product.is_active == True).first()
    if db_product is None:
        raise HTTPException(status_code=404,detail="product not found")
    
    db_product.is_active = False
    db_product.is_delete = True
    
    db.commit()
    return "product delete successfully"



#--------------------------reregister by token--------------------------


@productOrder.put("/reregister_product")
def reregister_product(token : str,product : productpass):
     logger.info("Attempting to reregister product using token")
    
     product_id = decode_token_by_product_id(token)
     logger.info("Decoded product ID from token")
     
     db_product = db.query(Product).filter(Product.id == product_id).first()
     logger.info("Checking if product exists in the database")
     
     if db_product is None :
         logger.error("Product not found")
         raise HTTPException (status_code=404,detail="product not found")
     
     if db_product.is_delete is True and db_product.is_active is False:
          if product.name == db_product.name:
             logger.info("Product found and matches the provided name. Reregistering product.")
             
             db_product.is_delete = False
             db_product.is_active = True
             
             db.commit()
             logger.success("Product reregistered successfully")
             return True
     
     logger.error("Invalid credentials provided")    
     raise HTTPException(status_code=404,detail="Invalid credentials")
 
 #-------depends------
 
@productOrder.put("/reregister_product_depends")
def reregister_product_depends(product : productpass,product_id=Depends(decode_token_by_product_id)):
     db_product = db.query(Product).filter(Product.id == product_id).first()
     if db_product is None :
         raise HTTPException (status_code=404,detail="product not found")
     
     if db_product.is_delete is True and db_product.is_active is False:
          if product.name == db_product.name:
             
             db_product.is_delete = False
             db_product.is_active = True
             
             db.commit()
             return True
         
     raise HTTPException(status_code=404,detail="Invalid credentials")
 
 #-----------header-------------

@productOrder.put("/reregister_product_header")
def reregister_product_header(product : productpass,token=Header(...)):
     product_id = decode_token_by_product_id(token)
     db_product = db.query(Product).filter(Product.id == product_id).first()
     if db_product is None :
         raise HTTPException (status_code=404,detail="product not found")
     
     if db_product.is_delete is True and db_product.is_active is False:
          if product.name == db_product.name:
             
             db_product.is_delete = False
             db_product.is_active = True
             
             db.commit()
             return True
         
     raise HTTPException(status_code=404,detail="Invalid credentials")

#*****************************order******************************

# ---------------------create order-----------------------

@productOrder.post("/create_order",response_model=OrderAll)
def create_order(orders:OrderAll):
    logger.info("Finding product id from product table")
    product_id = db.query(Product).filter(Product.id == Order.product_id,Product.is_active == True,Product.is_delete == False).first()
    
    if not product_id:
        logger.error("product id is not found")
        raise HTTPException(status_code=404)
    logger.info("my order is creating ........") 
    
    new_customer= Order(
        product_id = orders.product_id,
        quantity = orders.quantity
    )
    logger.success("my order is created.")
    logger.info("order is adding to database.....")
    db.add(new_customer)
    logger.success("order has loaded successfully")
    db.commit()
    logger.success("database has been saved successfuly.")
    return new_customer

#-------------------------encode order id------------------------------

@productOrder.get("/encode_order_id")
def encode_order(id : int):
    logger.info("Encoding order ID to generate access token.")
    
    access_token = get_token_order_by_id(id)
    logger.success("Order ID encoded successfully. Access token generated.")
    
    return access_token

@productOrder.get("/order_decode_id")
def order_decode_id(token : str):
    id = decode_token_by_order_id(token)
    return id

#-----------------------get by id order--------------------------------

@productOrder.get("/get_order_by_id",response_model=OrderAll)
def get_order_by_id(order_id:int):
    logger.info("Attempting to retrieve order by ID.")
    
    db_order = db.query(Order).filter(Order.id == order_id ,Order.is_active == True).first()
    logger.success("retrieved order successfully")
    
    if db_order is  None:
        logger.error("Order not found ")
        raise HTTPException(status_code=404,detail="order not found")
    
    logger.success("Order retrieved successfully.")
    return db_order

#---------------------get id by order token-------------------------------

# @productOrder.get("/get_order_by_id_token",response_model=OrderAll)
# def get_order_by_id_token(token: str):
#     order_id = decode_token_by_order_id(token)
#     db_order = db.query(Order).filter(Order.id == order_id,Order.is_active == True).first()
#     if db_order is None:
#         raise HTTPException(status_code=404,detail="order not found")
#     return db_order

 #-------depends------

@productOrder.get("/get_order_by_id_token_depeds",response_model=OrderAll)
def get_order_by_id_token_depends(order_id=Depends(decode_token_by_order_id)):
    db_order = db.query(Order).filter(Order.id == order_id,Order.is_active == True).first()
    if db_order is None:
        raise HTTPException(status_code=404,detail="order not found")
    return db_order

# header

@productOrder.get("/get_order_by_id_token_header",response_model=OrderAll)
def get_order_by_id_token_header(token= Header(...)):
    order_id = decode_token_by_order_id(token)
    db_order = db.query(Order).filter(Order.id == order_id,Order.is_active == True).first()
    if db_order is None:
        raise HTTPException(status_code=404,detail="order not found")
    return db_order

#----------------------get all order--------------------------

@productOrder.get("/get_all_order",response_model=list[OrderAll])
def get_all_order():
    logger.info("Attempting to retrieve all orders.")
    db_order = db.query(Order).all()
    logger.success("order retrieved succesfully")
    if db_order is  None:
        logger.error("order not found ")
        raise HTTPException(status_code=404,detail="order not found")
    return db_order

#---------------------- update order---------------------

@productOrder.put("/update_order",response_model=OrderAll)
def update_order(order_id:str,orders:OrderAll):
    logger.info("Attempting to update order.")
    
    db_order = db.query(Order).filter(Order.id == order_id , Order.is_active == True).first()
    logger.success("order retrieved succesfully")
    
    if db_order is  None:
        logger.error("Order not found ")
        raise HTTPException(status_code=404,detail="order not found")
    
    logger.info("Updating order details.")
    db_order.product_id = orders.product_id,
    db_order.quantity = orders.quantity
    
    db.commit()
    logger.success("Order updated successfully.")
    return db_order

#-------------------------update token order------------------------------

# @productOrder.put("/update_order_token",response_model=OrderAll)
# def update_order_token(token:str,orders:OrderAll):
#     order_id = decode_token_by_order_id(token)
#     db_order = db.query(Order).filter(Order.id == order_id , Order.is_active == True).first()
#     if db_order is  None:
#         raise HTTPException(status_code=404,detail="order not found")
    
#     db_order.product_id = orders.product_id,
#     db_order.quantity = orders.quantity
    
#     db.commit()
#     return db_order

#-------depends------

@productOrder.put("/update_order_token_depends",response_model=OrderAll)
def update_order_token_depends(orders : OrderAll ,order_id=Depends(decode_token_by_order_id)):
    
    db_order = db.query(Order).filter(Order.id == order_id , Order.is_active == True).first()
    if db_order is  None:
        raise HTTPException(status_code=404,detail="order not found")
    
    db_order.product_id = orders.product_id,
    db_order.quantity = orders.quantity
    
    db.commit()
    return db_order

#-----------header-----------

@productOrder.put("/update_order_token_header",response_model=OrderAll)
def update_order_token_header(orders:OrderAll,token=Header(...)):
    order_id = decode_token_by_order_id(token)
    db_order = db.query(Order).filter(Order.id == order_id , Order.is_active == True).first()
    if db_order is  None:
        raise HTTPException(status_code=404,detail="order not found")
    
    db_order.product_id = orders.product_id,
    db_order.quantity = orders.quantity
    
    db.commit()
    return db_order


#-----------------------delete order--------------------------


@productOrder.delete("/delete_order")
def delete_order(order_id:str):
    logger.info("Attempting to delete order.")
    
    db_order = db.query(Order).filter(Order.id == order_id , Order.is_active == True).first()
    logger.success("order retrieved succesfully")
    
    if db_order is None:
        logger.error("order not found")
        raise HTTPException(status_code=404,detail="order not found")
    
    logger.info("Marking order as inactive and deleted.")
    db_order.is_active = False
    db_order.is_delete = True

    db.commit()
    logger.success("order deleted successfully")
    return {"message":"order deleted successfully"}

#-----------------------delete order token------------------------------

# @productOrder.delete("/delete_order_token")
# def delete_order_token(token : str):
#     order_id = decode_token_by_order_id(token)
#     db_order = db.query(Order).filter(Order.id == order_id,Order.is_active == True).first()
#     if db_order is None:
#         raise HTTPException(status_code=404,detail="order not found")
    
#     db_order.is_active = False
#     db_order.is_delete = True
    
#     db.commit()
#     return "order deleted successfully"

#-------depends------

@productOrder.delete("/delete_order_token_depends")
def delete_order_token_depends(order_id=Depends(decode_token_by_order_id)):
    
    db_order = db.query(Order).filter(Order.id == order_id,Order.is_active == True).first()
    if db_order is None:
        raise HTTPException(status_code=404,detail="order not found")
    
    db_order.is_active = False
    db_order.is_delete = True
    
    db.commit()
    return "order deleted successfully"

#--------header----------

@productOrder.delete("/delete_order_token_header")
def delete_order_token_header(token=Header(...)):
    order_id = decode_token_by_order_id(token)
    db_order = db.query(Order).filter(Order.id == order_id,Order.is_active == True).first()
    if db_order is None:
        raise HTTPException(status_code=404,detail="order not found")
    
    db_order.is_active = False
    db_order.is_delete = True
    
    db.commit()
    return "order deleted successfully"

#-------------------------reregister order token---------------------------

@productOrder.put("/reregister_order")
def reregister_order(token:str, order:orderid):
    logger.info("Attempting to reregister order using token.")
    order_id = decode_token_by_order_id(token)
    logger.info("Decoded order ID from token.")
    
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order is None:
         logger.error("Order not found.")
         raise HTTPException (status_code=404,detail="order not found")
     
    if db_order.is_delete is True and db_order.is_active is False:
        if order.id == db_order.id:
             logger.info("Order found and matches the provided ID. Reregistering order.")
             
             db_order.is_delete = False
             db_order.is_active = True
             
             db.commit()
             logger.success("Order reregistered successfully.")
             return True    
         
    logger.error("Invalid credentials provided.")     
    raise HTTPException(status_code=404,detail="Invalid credentials")

#-------depends------

@productOrder.put("/reregister_order_depends")
def reregister_order_depends(order_id=Depends(decode_token_by_order_id)):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order is None:
         raise HTTPException (status_code=404,detail="order not found")
     
    if db_order.is_delete is True and db_order.is_active is False:
        
             db_order.is_delete = False
             db_order.is_active = True
             
             db.commit()
             return True    
         
    raise HTTPException(status_code=404,detail="Invalid credentials")

#--------header----------

@productOrder.put("/reregister_order_header")
def reregister_order_header(order:orderid,token=Header(...)):
    order_id = decode_token_by_order_id(token)
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order is None:
         raise HTTPException (status_code=404,detail="order not found")
     
    if db_order.is_delete is True and db_order.is_active is False:
        if order.id == db_order.id:
             
             db_order.is_delete = False
             db_order.is_active = True
             
             db.commit()
             return True    
         
    raise HTTPException(status_code=404,detail="Invalid credentials")

#-----------------------------create_bill--------------------------------------

@productOrder.get("/create_bill_amount")
def create_bill_amount(order_id : int):
    db_order = db.query(Order).filter(Order.id == order_id,Order.is_active == True).first()
    if db_order is None:
        raise HTTPException(status_code=404,detail="order not found")
    
    product_id = db_order.product_id
   
    db_product = db.query(Product).filter(Product.id == product_id,Product.is_active==True).first()
    
    if db_product is None:
        raise HTTPException(status_code=404,detail="product not found")
    
    order_id= db_product.price
    
    total = db_product.price * db_order.quantity
    
    return total

  

 


