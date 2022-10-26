import os
from decimal import Decimal

from peewee import *

db = SqliteDatabase(f'database1.db', pragmas={'foreign_keys': 1})


class BaseModel(Model):
    class Meta:
        database = db


class Data(BaseModel):
    trade_type = CharField(max_length=64)
    payment = CharField(max_length=64)
    price = CharField(max_length=64)


db.create_tables([Data])


def load_data(data):
    with db.transaction() as txn:
        for trade_type, payment, price in data:
            try:
                data_in_db = Data.select().where((Data.trade_type == trade_type) & (Data.payment == payment))[0]
                if data_in_db.price != price:
                    data_in_db.price = price
                    data_in_db.save()
            except:
                Data.create(trade_type=trade_type, payment=payment, price=price)
        txn.commit()


def get_course1(trade_type, payment):
    for i in Data.select():
        print(i)
    a = Data.select().where((Data.trade_type == trade_type) & (Data.payment == payment))
    print(a)
    return Decimal(Data.select(Data.price).where((Data.trade_type == trade_type) & (Data.payment == payment))[0].price)


def get_course(trade_type, payment_name):
    data = [['BUY', 'RosBankNew', '64.97000'], ['BUY', 'TinkoffNew', '65.03000'], ['BUY', 'QIWI', '65.49000'], ['SELL', 'KaspiBank', '472.11000'], ['SELL', 'ForteBank', '470.10000'], ['SELL', 'BankofGeorgia', '2.77000'], ['SELL', 'TBCbank', '2.77000'], ['SELL', 'LIBERTYBANK', '2.65000'], ['SELL', 'Uzcard', '11370.00000'], ['SELL', 'PermataMe', '15594.00000']]
    names_bank = {
        'Сбер (RUB)': 'RosBankNew',
        'Тинькофф (RUB)': 'TinkoffNew',
        'QIWI (RUB)': 'QIWI',
        'Kaspi Bank (KZT)': 'KaspiBank',
        'Forte Bank (KZT)': 'ForteBank',
        'Bank of Georgia (GEL)': 'BankofGeorgia',
        'TBC Bank (GEL)': 'TBCbank',
        ' Liberty Bank (GEL)': 'LIBERTYBANK',
        'UZCARD (UZS)': 'Uzcard',
        'Индонезия (IDR)': 'PermataMe'
    }
    payment = names_bank[payment_name]
    for i in data:
        if i[0] == trade_type and i[1] == payment:
            return Decimal(i[2])
    # a = Data.select().where((Data.trade_type == trade_type) & (Data.payment == payment))
    # print(a)
    # return Decimal(Data.select(Data.price).where((Data.trade_type == trade_type) & (Data.payment == payment))[0].price)


if __name__ == '__main__':
    pass
