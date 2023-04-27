from django.shortcuts import render
from django.views.decorators.cache import cache_control                                                        
import pandas as pd                                                      
from sklearn import preprocessing                                        
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
from django.shortcuts import render, redirect
from django.contrib import messages
from cropAnalysis.models import Users
import hashlib

# Create your views here.
def dashboard(request):
    return render(request,'dashboard.html')
def dashboard1(request):
    return render(request,'dashboard1.html')
def home(request):
    return render(request, 'signup.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
	del request.session["Current_User"]
	return redirect('/login/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    auth = 0
    # if request.session['valid_user'] != 1:
    #     return redirect('/login/')
    # else:
    #     pass
    if request.method == 'POST':
        uname = request.POST['uname']
        password = hashlib.md5(request.POST['password'].encode())
        password = password.hexdigest()
        auth = Users.objects.filter(username=uname, password=password).count()
        if auth == 1:
            data = Users.objects.filter(username=uname, password=password)
            for val in data:
                request.session['Current_User'] = val.username
            request.session['valid_user'] = 1
            
            return redirect('/ds/')
        
        else:
            messages.info(request, 'Wrong Credentials..')
            return redirect('/login/')

    return render(request, 'login.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def putData(request):
    return render(request, 'soil_data.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def register(request):
    if request.method == 'POST':
        u = request.POST['uname']
        pass1 = request.POST['password']
        pass2 = request.POST['c_password']
        enc_pass = hashlib.md5(request.POST['password'].encode())
        enc_pass = enc_pass.hexdigest()
        Email=request.POST['email']
       # print(u,pass1,pass2,Email)
        if pass1 == pass2:
            if Users.objects.filter(username=u).exists():
                messages.info(request, 'Username already taken')
                print('Username already taken')
            else:
                try:
                    a = Users(username=u, email=Email, password=enc_pass)
                    a.save()
                    print(a)
                    return redirect('/login/')
                except:
                    print("Data not Inserted")
                    
        else:
            messages.info(request, 'Password do not match')
            print('Password do not match')
    else:
        pass
    return render(request, 'signup.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def process(request):
    #nitrogen_content, phosphorus_content, potassium_content, temperature_content, humidity_content, ph_content, rainfall = 0
    if request.method == "POST":
        nitrogen_content = request.POST['nitrogen']                                          
        phosphorus_content = request.POST['phosphorus']                                                                                                   
        potassium_content =  request.POST['potassium']                                                                                                    
        temperature_content = request.POST['temperature']                                                                                                     
        humidity_content = request.POST['humidity']                                                                                                   
        ph_content =  request.POST['ph']                                                                                                       
        rainfall = request.POST['rainfall']

        nitrogen_content = int(nitrogen_content)
        phosphorus_content = int(phosphorus_content)
        potassium_content = int(potassium_content)
        temperature_content = int(temperature_content)
        humidity_content = int(humidity_content)
        ph_content = float(ph_content)
        rainfall = int(rainfall)
        

# C:\Users\Muskan\Desktop\IBM\IBM\Agriculture//
        excel = pd.read_excel('Crop.xlsx', header = 0)     
                                                            

        le = preprocessing.LabelEncoder()                                         
        crop = le.fit_transform(list(excel["CROP"]))                              

                                                            
        NITROGEN = list(excel["NITROGEN"])                                        
        PHOSPHORUS = list(excel["PHOSPHORUS"])                                    
        POTASSIUM = list(excel["POTASSIUM"])                                      
        TEMPERATURE = list(excel["TEMPERATURE"])                                  
        HUMIDITY = list(excel["HUMIDITY"])                                        
        PH = list(excel["PH"])                                                    
        RAINFALL = list(excel["RAINFALL"])                                        


        features = list(zip(NITROGEN, PHOSPHORUS, POTASSIUM, TEMPERATURE, HUMIDITY, PH, RAINFALL))                     
        features = np.array([NITROGEN, PHOSPHORUS, POTASSIUM, TEMPERATURE, HUMIDITY, PH, RAINFALL])                    

        features = features.transpose()                                                                                
       # print(features.shape)                                                                                          
        #print(crop.shape)                                                                                              

        model = KNeighborsClassifier(n_neighbors=3)                                                                    
        model.fit(features, crop)                                                                                      
    
        


        
        predict1 = np.array([nitrogen_content,phosphorus_content, potassium_content, temperature_content, humidity_content, ph_content, rainfall])  
        #   print(predict1)                                                                                                                             
        predict1 = predict1.reshape(1,-1)                                                                              
        #  print(predict1)                                                                                                
        predict1 = model.predict(predict1)                                                                             
        # print(predict1)                                                                                                
        crop_name = str()
        if predict1 == 0:                                                                                              
            crop_name = 'Apple(सेब)'
        elif predict1 == 1:
            crop_name = 'Banana(केला)'
        elif predict1 == 2:
            crop_name = 'Blackgram(काला चना)'
        elif predict1 == 3:
            crop_name = 'Chickpea(काबुली चना)'
        elif predict1 == 4:
            crop_name = 'Coconut(नारियल)'
        elif predict1 == 5:
            crop_name = 'Coffee(कॉफ़ी)'
        elif predict1 == 6:
            crop_name = 'Cotton(कपास)'
        elif predict1 == 7:
            crop_name = 'Grapes(अंगूर)'
        elif predict1 == 8:
            crop_name = 'Jute(जूट)'
        elif predict1 == 9:
            crop_name = 'Kidneybeans(राज़में)'
        elif predict1 == 10:
            crop_name = 'Lentil(मसूर की दाल)'
        elif predict1 == 11:
            crop_name = 'Maize(मक्का)'
        elif predict1 == 12:
            crop_name = 'Mango(आम)'
        elif predict1 == 13:
            crop_name = 'Mothbeans(मोठबीन)'
        elif predict1 == 14:
            crop_name = 'Mungbeans(मूंग)'
        elif predict1 == 15:
            crop_name = 'Muskmelon(खरबूजा)'
        elif predict1 == 16:
            crop_name = 'Orange(संतरा)'
        elif predict1 == 17:
            crop_name = 'Papaya(पपीता)'
        elif predict1 == 18:
            crop_name = 'Pigeonpeas(कबूतर के मटर)'
        elif predict1 == 19:
            crop_name = 'Pomegranate(अनार)'
        elif predict1 == 20:
            crop_name = 'Rice(चावल)'
        elif predict1 == 21:
            crop_name = 'Watermelon(तरबूज)'

        
        print(crop_name)
        dict1={
            'name':crop_name
        }

        return render(request, 'crop.html', dict1)
    else:
        return redirect('/putdata/')
    
    
        