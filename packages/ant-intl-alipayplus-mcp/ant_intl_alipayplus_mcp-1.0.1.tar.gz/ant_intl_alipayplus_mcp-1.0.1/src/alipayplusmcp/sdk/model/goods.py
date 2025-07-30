#!/usr/bin/env python
# -*- coding: utf-8 -*-
from alipayplusmcp.sdk.model.amount import Amount


class Goods(object):
    def __init__(self):
        self.__reference_goods_id = None
        self.__goods_name = None
        self.__goods_category = None
        self.__goods_unit_amount = None  # type:Amount
        self.__goods_quantity = None

    @property
    def reference_goods_id(self):
        return self.__reference_goods_id

    @reference_goods_id.setter
    def reference_goods_id(self, value):
        self.__reference_goods_id = value

    @property
    def goods_name(self):
        return self.__goods_name

    @goods_name.setter
    def goods_name(self, value):
        self.__goods_name = value

    @property
    def goods_category(self):
        return self.__goods_category

    @goods_category.setter
    def goods_category(self, value):
        self.__goods_category = value

    @property
    def goods_unit_amount(self):
        return self.__goods_unit_amount

    @goods_unit_amount.setter
    def goods_unit_amount(self, value):
        self.__goods_unit_amount = value

    @property
    def goods_quantity(self):
        return self.__goods_quantity

    @goods_quantity.setter
    def goods_quantity(self, value):
        self.__goods_quantity = value


    def to_aps_dict(self):
        params = dict()
        if hasattr(self, "reference_goods_id") and self.reference_goods_id:
            params['referenceGoodsId'] = self.reference_goods_id

        if hasattr(self, "goods_name") and self.goods_name:
            params['goodsName'] = self.goods_name

        if hasattr(self, "goods_category") and self.goods_category:
            params['goodsCategory'] = self.goods_category

        if hasattr(self, "goods_unit_amount") and self.goods_unit_amount:
            params['goodsUnitAmount'] = self.goods_unit_amount

        if hasattr(self, "goods_quantity") and self.goods_quantity:
            params['goodsQuantity'] = self.goods_quantity

        return params
