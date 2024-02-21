import os
import sys
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///restaurants.db', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True)
    name = Column(String())
    price = Column(Integer)

    reviews = relationship("Review", back_populates="restaurant")
    customers = relationship("Customer", secondary="reviews", back_populates="restaurants")

    def get_reviews(self):
        return [review for review in self.reviews]

    def get_customers(self):
        return [customer for customer in self.customers]

    @classmethod
    def fanciest(cls):
        return session.query(cls).order_by(cls.price.desc()).first()

    def all_reviews(self):
        return [review.full_review() for review in self.reviews]

    def __repr__(self):
        return f'Restaurant: {self.name}'


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String())
    last_name = Column(String())

    reviews = relationship("Review", back_populates="customer")
    restaurants = relationship("Restaurant", secondary="reviews", back_populates="customers")

    def get_reviews(self):
        return [review for review in self.reviews]

    def get_restaurants(self):
        return [restaurant for restaurant in self.restaurants]

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def favorite_restaurant(self):
        highest_rating = 0
        favorite_restaurant = None
        for review in self.reviews:
            if review.star_rating > highest_rating:
                highest_rating = review.star_rating
                favorite_restaurant = review.restaurant
        return favorite_restaurant

    def add_review(self, restaurant, rating):
        new_review = Review(restaurant=restaurant, customer=self, star_rating=rating)
        session.add(new_review)
        session.commit()

    def delete_reviews(self, restaurant):
        for review in self.reviews:
            if review.restaurant == restaurant:
                session.delete(review)
        session.commit()

    def __repr__(self):
        return f'Customer: {self.first_name} {self.last_name}'


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    star_rating = Column(Integer)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    customer_id = Column(Integer, ForeignKey('customers.id'))

    restaurant = relationship("Restaurant", back_populates="reviews")
    customer = relationship("Customer", back_populates="reviews")

    def full_review(self):
        return f"Review for {self.restaurant.name} by {self.customer.full_name()}: {self.star_rating} stars."

    def get_customer(self):
        return self.customer

    def get_restaurant(self):
        return self.restaurant

    def __repr__(self):
        return f'Review: {self.star_rating} stars'
