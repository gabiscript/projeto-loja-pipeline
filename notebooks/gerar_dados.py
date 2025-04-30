import random
from faker import Faker
import pandas as pd
from datetime import datetime

Faker.seed(0)
fake = Faker('en_US')
random.seed()    

category_products = {
    'Clothing': ['T-shirt', 'Jeans', 'Jacket', 'Sweater', 'Hat'],
    'Electronics': ['Smartphone', 'Laptop', 'Headphones', 'Camera', 'Smartwatch'],
    'Beauty': ['Shampoo', 'Conditioner', 'Face Cream', 'Lipstick', 'Nail Polish'],
    'Books': ['Fiction Novel', 'Cookbook', 'Science Book', 'Biography', 'Children\'s Book'],
    'Computers & Accessories': ['Laptop Stand', 'Mouse', 'Keyboard', 'Webcam', 'Monitor'],
    'Furniture': ['Sofa', 'Table', 'Chair', 'Bed', 'Bookshelf'],
    'Toys & Games': ['Action Figure', 'Puzzle', 'Board Game', 'Doll', 'RC Car'],
    'Sports & Outdoors': ['Tennis Racket', 'Basketball', 'Yoga Mat', 'Camping Tent', 'Fishing Rod']
}

def customer_creator():
    gender = random.choice(['F','M'])
    name = fake.first_name_female() if gender == 'F' else fake.first_name_male()
    last_name = fake.last_name()
    return{
            "gender": gender,
            "first_name": name,
            "last_name": last_name,
            "email": f"{name.lower()}.{last_name.lower()}@{fake.domain_name()}",
            "birth_date": fake.date_between_dates(date_start=datetime(1970,1,1), date_end=datetime(2007,12,30)),
            "country": fake.country(),
            "job": fake.job(),
            "phone_number": fake.phone_number(),
    }

def create_customers_df(n=101):
    customers = [customer_creator()for i in range(n)]
    df_customers = pd.DataFrame(customers)
    df_customers['customer_id']='CUST'+(df_customers.index+1).astype(str).str.zfill(3)
    return df_customers

def product_creator():
    category = random.choice(list(category_products.keys()))
    product = random.choice(category_products[category])
    return{
            "product_name": product,
            "category": category,
            "price": round(random.uniform(5.0, 500.0),2),
            "stock_quantity": random.randint(1,100),
            "brand": fake.company()
    }

def create_products_df(n=20):
    product = [product_creator()for i in range(n)]
    df_product = pd.DataFrame(product)
    df_product['product_id']='PROD'+(df_product.index+1).astype(str).str.zfill(3)
    return df_product

def order_creator(customer, df_product):

    product = df_product.sample(n=1).iloc[0]
    quantity = random.randint(1,5)
    order_date = fake.date_between_dates(date_start=datetime(2023,1,1), date_end=datetime(2024,12,30))
    total_price = round(product['price']*quantity, 2)

    return{
            "customer_id": customer['customer_id'],
            "product_id": product['product_id'],
            "quantity": quantity,
            "order_date": order_date,
            "total_price": total_price
    }

def create_orders_df(n=80, df_customers=None, df_product=None):
    orders = []
    for i in range(n):
        customer = df_customers.sample(n=1).iloc[0]
        num_orders=random.randint(1,5)
        for _ in range(num_orders):
            order = order_creator(customer, df_product)
            orders.append(order)
    df_orders = pd.DataFrame(orders)
    df_orders['order_id']='ORD'+(df_orders.index+1).astype(str).str.zfill(3)
    return df_orders

# Execução
df_customers = create_customers_df()
df_product = create_products_df()
df_orders = create_orders_df(df_customers=df_customers, df_product=df_product)

df_customers.to_csv('customers.csv', index=False)
df_product.to_csv('product.csv', index=False)
df_orders.to_csv('orders.csv', index=False)

# Exibe os 5 primeiros de cada
print(df_customers.head())
print(df_product.head())
print(df_orders.head())