import csv
import os
from login.models import * 
import pandas as pd

def main():
    df=pd.read_csv("/Users/ngoduclong/Documents/harvard_courses/HTML prog/beijing_housing_price_platform/beijing_housing_price_import.csv")
    list_df=[]
    for j in range(len(df['url'])):
        list_item=[]
        for i in list(df.columns):
            if type(df[i][j])== str:
                list_item.append(df[i][j])
            else:
                list_item.append(df[i][j].item())
            
        list_df.append(list_item)
    
    
    i=0
    
    for url, Lng, Lat, tradeTime, totalPrice,price,square,livingRoom,drawingRoom,kitchen,bathRoom,floor,buildingType, constructionTime, renovationCondition,buildingStructure, ladderRatio, elevator, fiveYearsProperty,subway, district in list_df:
        house = House(url=url, Lng=Lng, Lat=Lat, tradeTime=tradeTime, totalPrice=totalPrice,price=price,square=square ,bedRoom=livingRoom,livingRoom=drawingRoom,kitchen=kitchen,bathRoom=bathRoom,floor=floor, buildingType=buildingType, constructionTime=constructionTime, renovationCondition=renovationCondition,buildingStructure=buildingStructure, ladderRatio=ladderRatio, elevator=elevator, fiveYearsProperty=fiveYearsProperty,subway=subway, district=district)
        house.save()
        i+=1
        print('added',i)
        
    
main()
