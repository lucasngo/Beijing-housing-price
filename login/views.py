from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from .models import *
import pickle
from datetime import date
import numpy as np
import requests
today = date.today()
d1=today.strftime("%d/%m/%Y")
day=int(d1[:2])
month=int(d1[3:5])
year=int(d1[8:])
model = pickle.load(open('./login/model_for_beijing_housing.sav', 'rb'))



def index(request):
    return render(request,"login/HomePage.html")

def form(request):
    if not request.user.is_authenticated:
        return render(request,'login/form.html')
    return HttpResponseRedirect(reverse('userinfo'))
    

def signin(request):
    return render(request, 'login/signin.html')

def userinfo(request,user_id):
    if request.method=="POST":
        fname=request.POST['firstname']
        lname=request.POST['lastname']
        username=request.POST['username']
        pw1=request.POST['pw1']
        pw2=request.POST['pw2']
        is_register=False
        if pw1!=pw2:
            return render(request,'login/form.html',{'pw1':pw1,'pw2':pw2,'is_register':is_register})
        else:
            try:
                match=Acc_user.objects.filter(username=username).count()
            except:
                match=0
            print('match =',match)
            if match==0:
                name = fname+' '+lname
                cust=Acc_user(name=name,username=username,pw=pw1)
                cust.save()
                
                user_id=Acc_user.objects.filter(username=username).values('id')
                # search=Acc_user.objects.get(pk=user_id).search
                # print('type:',type(search),len(search))
                # predict=Acc_user.objects.get(pk=user_id).predict
                # return render(request,'login/user.html',{'user_id':cust.id,'search':[],'predict':[]})
                return redirect('home',user_id=cust.id)
            else:   
                return render(request,'login/form.html',{'pw1':pw1,'pw2':pw2,'is_register':True})
    else:
        return render(request,'login/user.html',{'user_id':user_id})

def home(request,user_id):
    user=Acc_user.objects.get(pk=user_id)
    search=user.search.all()
    predict=user.predict.all()
    print(search,predict)
    return render(request,'login/user.html',{'user_id':user_id,'search':search,'predict':predict})

def signin_user(request):
    username=request.POST['username']
    pw1=request.POST['password']
    
    user = Acc_user.objects.filter(username = username, pw = pw1)
    print(type(user))
    if user.exists()==False:
        return render(request,'login/signin.html',{'boo':False})
    return redirect('home',user_id=user[0].id)

        

def addsearch(request,user_id):
    if request.method == 'POST':
        houses = list(request.POST.getlist('selected'))
        acc=Acc_user.objects.get(pk=user_id)
        for i in range(len(houses)):
            house=House.objects.get(pk=houses[i]) 
            acc.search.add(house)
            acc.save()
        return redirect('search',user_id=user_id)


def search(request,user_id):
    district_list=[(1,'Dongcheng'),(2,'Fengtai'),(3,'Pinggu'),(4,'Daxing'),(5,'Fangshan'),(6,'Changping'),(7,'Chaoyang'),(8,'haidian'),(9,'Shijingshan'),(10,'Xicheng'),(11,'Tongzhou'),(12,'Mentougou'),(13,'Shunyi')]
    subway_list=[(0,'more than 1km to the nearest subway'),(1,'less than 1km to the nearest subway')]
    elevator_list=[(0,'no elevator'),(1,'have elevator')]
    buildingType_list=[(1,'Tower'),(2,'bungalow'),(3,'combination of plate and tower'),(4,'plate')]
    buildingStructure_list=[(2,'mixed'),(3,'brick and wood'),(4,'brick and concrete'),(5,'steel'),(6,'steel-concrete composite')]
    return render(request,'login/search.html',{'user_id':user_id,'district':district_list,'subway':subway_list,'elevator':elevator_list,'buildingType':buildingType_list,'buildingStructure':buildingStructure_list,'empty_field':False})


def search_collect(request,user_id):
    district_list=[(1,'Dongcheng'),(2,'Fengtai'),(3,'Pinggu'),(4,'Daxing'),(5,'Fangshan'),(6,'Changping'),(7,'Chaoyang'),(8,'haidian'),(9,'Shijingshan'),(10,'Xicheng'),(11,'Tongzhou'),(12,'Mentougou'),(13,'Shunyi')]
    subway_list=[(0,'more than 1km to the nearest subway'),(1,'less than 1km to the nearest subway')]
    elevator_list=[(0,'no elevator'),(1,'have elevator')]
    buildingType_list=[(1,'Tower'),(2,'bungalow'),(3,'combination of plate and tower'),(4,'plate')]
    buildingStructure_list=[(2,'mixed'),(3,'brick and wood'),(4,'brick and concrete'),(5,'steel'),(6,'steel-concrete composite')]
    
    district=request.POST['district']
    subway=request.POST['subway']
    elevator=request.POST['elevator']
    buildingType=request.POST['buildingType']
    buildingStructure=request.POST['buildingStructure']
    square=request.POST['square']
    bedrooms=request.POST['bedroom']
    kitchen=request.POST['kitchen']
    livingRoom=request.POST['livingRoom']
    print([district,subway,elevator,buildingType,buildingStructure,square,bedrooms,kitchen,livingRoom])
    if '' in [district,subway,elevator,buildingType,buildingStructure,square,bedrooms,kitchen,livingRoom]:
        return render(request,'login/search.html',{'user_id':user_id,'district':district_list,'subway':subway_list,'elevator':elevator_list,'buildingType':buildingType_list,'buildingStructure':buildingStructure_list,'empty_field':True})


    house_filter=House.objects.filter(district=int(district),
                                    subway=int(subway),
                                    elevator=int(elevator),
                                    square__gte = int(int(square)*0.85),
                                    square__lte =int(int(square)*1.15),
                                    bedRoom = int(bedrooms),
                                    kitchen=int(kitchen),
                                    livingRoom=int(livingRoom))[:20]
    
    
    return render(request,'login/search_result.html',{'user_id':user_id,'search':house_filter,'district':district_list[int(district)-1][0]})

def predict(request,user_id):
    district=[(1,'Dongcheng'),(2,'Fengtai'),(3,'Pinggu'),(4,'Daxing'),(5,'Fangshan'),(6,'Changping'),(7,'Chaoyang'),(8,'haidian'),(9,'Shijingshan'),(10,'Xicheng'),(11,'Tongzhou'),(12,'Mentougou'),(13,'Shunyi')]
    subway=[(0,'more than 1km to the nearest subway'),(1,'less than 1km to the nearest subway')]
    elevator=[(0,'no elevator'),(1,'have elevator')]
    buildingType=[(1,'Tower'),(2,'bungalow'),(3,'combination of plate and tower'),(4,'plate')]
    buildingStructure=[(2,'mixed'),(3,'brick and wood'),(4,'brick and concrete'),(5,'steel'),(6,'steel-concrete composite')]
    renovationCondition=[(1,'other'),(2,'rough'),(3,'simplicity'),(4,'hard cover')]
    fiveYearsProperty=[(0,'Property less than 5 years'),(1,'Property for more than 5 years')]
    list_option=[('subway',subway),('elevator',elevator),('buildingType',buildingType),('buildingStructure',buildingStructure),('renovationCondition',renovationCondition),('fiveYearsProperty',fiveYearsProperty)]
    return render(request,'login/predict.html',{'user_id':user_id,'district':district,'subway':subway,'elevator':elevator,
                                                'buildingType':buildingType,'buildingStructure':buildingStructure,'renovationCondition':renovationCondition,'fiveYearsProperty':fiveYearsProperty})



def predict_result(request,user_id):
    district_dict={1:'Dongcheng',2:'Fengtai',3:'Pinggu',4:'Daxing',5:'Fangshan',6:'Changping',7:'Chaoyang',8:'haidian',9:'Shijingshan',10:'Xicheng',11:'Tongzhou',12:'Mentougou',13:'Shunyi'}
    house_number=request.POST['house_number']
    street=request.POST['street']
    district=int(request.POST['district'])
    subway=request.POST['subway']
    elevator=request.POST['elevator']
    buildingType=int(request.POST['buildingType'])
    buildingStructure=int(request.POST['buildingStructure'])
    square=int(request.POST['square'])
    bedrooms=int(request.POST['bedroom'])
    bathroom=int(request.POST['bathRoom'])
    kitchen=int(request.POST['kitchen'])
    livingRoom=int(request.POST['livingRoom'])
    renovationCondition=int(request.POST['renovationCondition'])
    fiveYearsProperty=int(request.POST['fiveYearsProperty'])
    age=int(request.POST['age'])
    ladderRatio=float(request.POST['ladderRatio'])
    floor=request.POST['floor']
    year_sold=request.POST['year_sold']

    address=str(house_number)+',+'+street+',+'+district_dict[int(district)]+',+'+'beijing'
    res=requests.get('https://maps.googleapis.com/maps/api/geocode/json',params={'address':address,'key':'AIzaSyDvPn47kFdnWa-nLOOsZM8qhcQN4EeBV6A'})
    data=res.json()
    longtitude=data['results'][0]['geometry']['location']['lng']
    latitude=data['results'][0]['geometry']['location']['lat']
    
    district_ml=[0]*13
    district_ml[district-1]=1

    buildingType_ml=[0]*4
    buildingType_ml[buildingType-1]=1

    buildingStructure_ml=[0]*6
    buildingStructure_ml[buildingStructure-1]=1

    renovationCondition_ml=[0]*4
    renovationCondition_ml[renovationCondition-1]=1

    user_house=[longtitude,latitude,square,bedrooms,livingRoom,kitchen,bathroom,floor,ladderRatio,elevator,fiveYearsProperty,subway,year_sold,month,day,age]
    user_house=user_house+buildingType_ml+buildingStructure_ml+renovationCondition_ml+district_ml

    user_house=np.array(user_house)
    user_house=user_house.reshape(1,-1)
    price1=model.predict(user_house)
    
    predict_house= Predict_house(Lng=longtitude,Lat= latitude,tradeTime= year_sold,totalPrice=price1[0]*square,price=price1[0],square=square,
                                bedRoom=bedrooms,livingRoom=livingRoom,kitchen=kitchen,bathRoom=bathroom,floor=floor,buildingType=buildingType,
                                renovationCondition=renovationCondition,buildingStructure=buildingStructure,ladderRatio=ladderRatio,elevator=elevator,
                                fiveYearsProperty=fiveYearsProperty,subway=subway,district=district,age=age)
    predict_house.save()
    acc=Acc_user.objects.get(pk=user_id)
    acc.predict.add(predict_house)
    acc.save()
    
    

    return  render(request,'login/predict_result.html',{'price':price1[0],'total_price':price1[0]*square})

