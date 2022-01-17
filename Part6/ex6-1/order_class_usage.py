from abc import ABC, abstractclassmethod, abstractmethod
from collections import namedtuple

Customer = namedtuple('Customer','name fidelity')

class LineItem:

    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price
    
    def total(self):
        return self.price * self.quantity

class Order: #콘텍스트

    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion
    
    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total
    
    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion.discount(self)
        return self.total() - discount
    
    def __repr__(self) -> str:
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())

class Promotion(ABC): # 전략: 추상 베이스 클래스

    @abstractmethod
    def discount(self, order):
        """할인액을 구체적인 숫자로 반환한다."""

class FidelityPromo(Promotion): # 첫 번째 구체적인 전략
    """충성도 포인트가 1000점 이상인 고객에게 전체 5% 할인 적용 """

    def discount(self, order):
        return order.total() * .05 if order.customer.fidelity >= 1000 else 0

class BulkItemPromo(Promotion): # 두 번째 구체적인 전략
    """20개 이상의 동일 상품을 구입하면 10% 할인 적용"""

    def discount(self, order):
        discount =0
        for item in order.cart:            
            if item.quantity >= 20:            
                discount += item.total() * .1
        return discount

class LargeOrderPromo(Promotion): # 세 번째 구체적인 전략
    """10종류 이상의 상품을 구입하면 전체 7% 할인 적용"""

    def discount(self, order):
        distinct_items = {item.product for item in order.cart}
        if len(distinct_items) >= 10:
            return order.total() * .07
        return 0

""" 위 클래스를 사용하는 예"""
joe = Customer('John Doe', 0)
ann = Customer('Ann Smith', 1100)
cart = [LineItem('banana', 4, .5),
        LineItem('apple', 10, 1.5),
        LineItem('watermellon', 5, 5.0)]

print(Order(joe, cart, FidelityPromo()))
print(Order(ann, cart, FidelityPromo()))

banana_cart = [LineItem('banana', 30, .5),
               LineItem('apple', 10, 1.5)]

print(Order(joe, banana_cart, BulkItemPromo()))

long_order = [LineItem(str(item_code), 1, 1.0)
              for item_code in range(10)]

print(Order(joe, long_order, LargeOrderPromo()))
print(Order(joe, cart, LargeOrderPromo()))

