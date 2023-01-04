import sqlite3
import pandas as pd

class Data_Shop_CatsnDogs:
    def __init__(self) -> None:
        self.conn = sqlite3.connect("./db0.db")

    def executeData(self, executeStr:str):
        cur = self.conn.cursor()
        try:
            cur.execute(executeStr)
            self.conn.commit()
            cur.close()
            return True
        except:
            cur.close()
            return False
        
    def queryAllDatas(self, queryStr:str) -> list:
        cur = self.conn.cursor()
        cur.execute(queryStr)
        data = cur.fetchall()
        cur.close()
        return data

    def queryManyDatas(self, queryStr, amount) -> list:
        cur = self.conn.cursor()
        cur.execute(queryStr)
        data = cur.fetchmany(amount)
        cur.close()
        return data

    def queryData(self, queryStr: str) -> object:
        cur = self.conn.cursor()
        cur.execute(queryStr)
        data = cur.fetchone()
        cur.close()
        return data

    def queryAllData(self) -> list:
        return self.queryManyDatas("select * from ShopData")

# df =db.queryManyDatas("select * from ShopData where loai='Chó'",5)
# for i in df:
#     # if i[2] == "Ba Tư":
#         print(i)

# import os

# Dogs = ["006934b7ef2e4b4990895879ad0f39e1", "370dfe3334cf4dc9be435e5524a91618"]
# Cats = ["00c888ec0534469bbc10a09d6e155264", "1d28760ae75148768b55d7672f4077cf", "04978864907747458f218ee11286f331"]



