#!/usr/bin/env python
from decimal import Decimal
from hummingbot.core.event.events import PositionSide


# class PriceSize:
#     def __init__(self, price: Decimal, size: Decimal):
#         self.price: Decimal = price
#         self.size: Decimal = size

#     def __repr__(self):
#         return f"[ p: {self.price} s: {self.size} ]"


class Proposal:
    def __init__(self, market: str, dir: PositionSide, price: Decimal, size: Decimal):
        self.market: str = market
        self.dir: PositionSide = dir
        self.size: Decimal = size
        self.price: Decimal = price
        self.tp: Decimal = price + price * 0.02
        self.sl: Decimal = price - price * 0.01
        if dir == PositionSide.SHORT:
            tp = self.tp
            self.tp = self.sl
            self.sl = tp

    def __repr__(self):
        return f"{self.market} sir: {self.dir} price: {self.price} tp: {self.tp} sl: {self.sl}"

    def base(self):
        return self.market.split("-")[0]

    def quote(self):
        return self.market.split("-")[1]
