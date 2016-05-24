from taxidata.models import Taxi
#from django.db.models import Q
import random

def exportJson():
    """docstring for exportJson"""
    jsonData = '['
    oTaxies = Taxi.objects.all()
    for ot in oTaxies:
        jsonData += '{"location":%d, "timeField": %d, "peoples": %d, "taxies": %d},'%(ot.location, ot.timeField, ot.peoples, ot.taxies)
        pass
    jsonData = jsonData[:-1]
    jsonData += ']'
    
    f = open('taxidata.json', 'w')
    f.write(jsonData)
    f.close()
    
    pass


def randomData():
    """generate random data into databases"""
    print 'random data is making...'
    
    oTaxies = Taxi.objects.all()
    for ot in oTaxies:
        ot.delete()
        pass
    busyTime = [8,9,18,19,20]
    busiLocation = [1,2,3,4,5]
    
    maxp = 20
    maxt = 18
    minp = 5
    mint = 4
    
    for location in range(1, 21):
        if location in busiLocation:
            maxp1 = 100
            maxt1 = 30
            minp1 = 30
            mint1 = 10
        else:
            maxp1 = 0
            maxt1 = 0
            minp1 = 0
            mint1 = 0
        for timeField in range(24):
            if timeField in busyTime:
                maxp2 = 100
                maxt2 = 30
                minp2 = 30
                mint2 = 10
            else:
                maxp2 = 0
                maxt2 = 0
                minp2 = 0
                mint2 = 0
            oTaxi = Taxi()
            oTaxi.location = location
            oTaxi.timeField = timeField
            oTaxi.peoples = random.randint(minp+minp1+minp2, maxp+maxp1+maxp2)
            oTaxi.taxies = random.randint(mint+mint1+mint2,maxt+maxt1+maxt2)
            oTaxi.save()