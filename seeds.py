from sqlalchemy.orm import sessionmaker
from lib.models import Restaurant, Customer, Review, engine


Session = sessionmaker(bind=engine)
session = Session()


restaurants_data = [
    {"name": "Restaurant A", "price": 2},
    {"name": "Restaurant B", "price": 3},

]

customers_data = [
    {"first_name": "John", "last_name": "Doe"},
    {"first_name": "Jane", "last_name": "Smith"},

]

reviews_data = [
    {"restaurant_id": 1, "customer_id": 1, "star_rating": 4},
    {"restaurant_id": 2, "customer_id": 2, "star_rating": 5},
    
]


restaurants = [Restaurant(**data) for data in restaurants_data]
session.add_all(restaurants)
session.commit()


customers = [Customer(**data) for data in customers_data]
session.add_all(customers)
session.commit()


reviews = [Review(**data) for data in reviews_data]
session.add_all(reviews)
session.commit()


session.close()
