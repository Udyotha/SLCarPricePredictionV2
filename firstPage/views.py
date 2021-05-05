from django.shortcuts import render
from django.http import HttpResponse
import numpy as np
import joblib
import pandas as pd

model= joblib.load('./models/random_forest_regression_model.pkl')




def index(request):
    context = {'a': 'HelloWorld'}
    return render(request, 'index.html', context)


def predict_price(request):
    print(request)
    if request.method == 'POST':
        temp={}

        temp['Year'] = request.POST.get('Year')
        temp['Mileage'] = request.POST.get('Mileage')
        temp['Engine_Capacity'] = request.POST.get('Engine_Capacity')
        temp['Transmission'] = request.POST.get('Transmission')
        temp['Fuel_Type'] = request.POST.get('Fuel_Type')
        temp['Brand'] = request.POST.get('Brand')

    Year = int(temp['Year'])
    Mileage = int(temp['Mileage'])
    Engine_Capacity = int(temp['Engine_Capacity'])
    Mileage2 = np.log(Mileage)
    Transmission = temp['Transmission']
    Fuel_Type = temp['Fuel_Type']
    Brand = temp['Brand']

    if (Fuel_Type == 'Petrol'):
        Fuel_Type_Petrol = 1
        Fuel_Type_Hybrid = 0
    else:
        Fuel_Type_Petrol = 0
        Fuel_Type_Hybrid = 1

    No_of_Years = 2021 - Year

    if (Transmission == 'Automatic'):
        Transmission_Auto = 1

    else:
        Transmission_Auto = 0

    if (Brand == 'Honda'):
        Brand_Honda = 1
        Brand_Toyota = 0
    else:
        Brand_Honda = 0
        Brand_Toyota = 1

    prediction = model.predict([[Mileage2, Engine_Capacity, No_of_Years, Transmission_Auto, Fuel_Type_Hybrid,
                                 Fuel_Type_Petrol, Brand_Honda, Brand_Toyota]])
    priceval1 = round(prediction[0])
    pricelakhs = round(priceval1/100000)

    priceval = "{:,}".format(priceval1)

    # testData=pd.DataFrame({'x':temp}).transpose()
    # priceval = reloadModel.predict(testData)[0]
    context = {'priceval': priceval, 'pricelakhs': pricelakhs}
    return render(request, 'index.html', context)
