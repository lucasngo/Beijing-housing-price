from django.db import models

class House(models.Model):
    url = models.CharField(max_length=64,blank=True)
    Lng = models.FloatField(blank=False)
    Lat = models.FloatField(blank=False)
    tradeTime=models.CharField(max_length=64,blank=False)
    totalPrice=models.FloatField(blank=False)
    price= models.FloatField(blank=False)
    square=models.FloatField(blank=False)
    bedRoom=models.IntegerField(blank=False)
    livingRoom=models.IntegerField(blank=False)
    kitchen=models.IntegerField(blank=False)
    bathRoom=models.IntegerField(blank=False)
    floor=models.IntegerField(blank=False)
    buildingType=models.IntegerField(blank=False)
    constructionTime=models.CharField(max_length=64,blank=False)
    renovationCondition=models.IntegerField(blank=False)
    buildingStructure=models.IntegerField(blank=False)
    ladderRatio=models.FloatField(blank=False)
    elevator=models.IntegerField(blank=False)
    fiveYearsProperty=models.IntegerField(blank=False)
    subway=models.IntegerField(blank=False)
    district=models.IntegerField(blank=False)

class Predict_house(models.Model):
    Lng = models.FloatField(blank=False)
    Lat = models.FloatField(blank=False)
    tradeTime=models.CharField(max_length=64,blank=False)
    totalPrice=models.FloatField(blank=False)
    price= models.FloatField(blank=False)
    square=models.FloatField(blank=False)
    bedRoom=models.IntegerField(blank=False)
    livingRoom=models.IntegerField(blank=False)
    kitchen=models.IntegerField(blank=False)
    bathRoom=models.IntegerField(blank=False)
    floor=models.IntegerField(blank=False)
    buildingType=models.IntegerField(blank=False)
    renovationCondition=models.IntegerField(blank=False)
    buildingStructure=models.IntegerField(blank=False)
    ladderRatio=models.FloatField(blank=False)
    elevator=models.IntegerField(blank=False)
    fiveYearsProperty=models.IntegerField(blank=False)
    subway=models.IntegerField(blank=False)
    district=models.IntegerField(blank=False)
    age=models.IntegerField(blank=False)

class Acc_user(models.Model):
    
    name=models.CharField(max_length=64)
    username=models.CharField(max_length=64)
    pw=models.CharField(max_length=64)
    search=models.ManyToManyField(House,blank=True,related_name='user')
    predict=models.ManyToManyField(Predict_house,blank=True,related_name='user')



    # user=models.ForeignKey(User,on_delete=models.CASCADE,blank=False,related_name='predict')
# class Predict(models.Model):
#     user_id=models.ForeignKey(User,on_delete=models.CASCADE,blank=False,related_name='predict')
#     house_id=models.ForeignKey(House,on_delete=models.CASCADE,blank=False)

# class Search(models.Model):
#     user_id=models.ForeignKey(User,on_delete=models.CASCADE,blank=False,related_name='search')
#     house_id=models.ForeignKey(House,on_delete=models.CASCADE,blank=False)





    
