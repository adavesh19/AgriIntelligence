# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 21:46:27 2019

@author: PRATYUSH, Rahul, Somya, Abhay
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS, cross_origin
import numpy as np
import pandas as pd
from datetime import datetime
import requests
import crops
import random

# import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/ticker": {"origins": "http://localhost:port"}})

commodity_dict = {
    "arhar": "static/Arhar.csv",
    "bajra": "static/Bajra.csv",
    "barley": "static/Barley.csv",
    "copra": "static/Copra.csv",
    "cotton": "static/Cotton.csv",
    "sesamum": "static/Sesamum.csv",
    "gram": "static/Gram.csv",
    "groundnut": "static/Groundnut.csv",
    "jowar": "static/Jowar.csv",
    "maize": "static/Maize.csv",
    "masoor": "static/Masoor.csv",
    "moong": "static/Moong.csv",
    "niger": "static/Niger.csv",
    "paddy": "static/Paddy.csv",
    "ragi": "static/Ragi.csv",
    "rape": "static/Rape.csv",
    "jute": "static/Jute.csv",
    "safflower": "static/Safflower.csv",
    "soyabean": "static/Soyabean.csv",
    "sugarcane": "static/Sugarcane.csv",
    "sunflower": "static/Sunflower.csv",
    "urad": "static/Urad.csv",
    "wheat": "static/Wheat.csv"
}

annual_rainfall = [29, 21, 37.5, 30.7, 52.6, 150, 299, 251.7, 179.2, 70.5, 39.8, 10.9]
base = {
    "Paddy": 1245.5,
    "Arhar": 3200,
    "Bajra": 1175,
    "Barley": 980,
    "Copra": 5100,
    "Cotton": 3600,
    "Sesamum": 4200,
    "Gram": 2800,
    "Groundnut": 3700,
    "Jowar": 1520,
    "Maize": 1175,
    "Masoor": 2800,
    "Moong": 3500,
    "Niger": 3500,
    "Ragi": 1500,
    "Rape": 2500,
    "Jute": 1675,
    "Safflower": 2500,
    "Soyabean": 2200,
    "Sugarcane": 2250,
    "Sunflower": 3700,
    "Urad": 4300,
    "Wheat": 1350

}
commodity_list = []


class Commodity:

    def __init__(self, csv_name):
        self.name = csv_name
        dataset = pd.read_csv(csv_name)
        self.X = dataset.iloc[:, :-1].values
        self.Y = dataset.iloc[:, 3].values

        #from sklearn.model_selection import train_test_split
        #X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1, random_state=0)

        # Fitting decision tree regression to dataset
        from sklearn.tree import DecisionTreeRegressor
        depth = random.randrange(7,18)
        self.regressor = DecisionTreeRegressor(max_depth=depth)
        self.regressor.fit(self.X, self.Y)
        #y_pred_tree = self.regressor.predict(X_test)
        # fsa=np.array([float(1),2019,45]).reshape(1,3)
        # fask=regressor_tree.predict(fsa)

    def getPredictedValue(self, value):
        if value[1]>=2019:
            fsa = np.array(value).reshape(1, 3)
            #print(" ",self.regressor.predict(fsa)[0])
            return self.regressor.predict(fsa)[0]
        else:
            c=self.X[:,0:2]
            x=[]
            for i in c:
                x.append(i.tolist())
            fsa = [value[0], value[1]]
            ind = 0
            for i in range(0,len(x)):
                if x[i]==fsa:
                    ind=i
                    break
            #print(index, " ",ind)
            #print(x[ind])
            #print(self.Y[i])
            return self.Y[i]

    def getCropName(self):
        a = self.name.split('.')
        return a[0]


@app.route('/')
def index():
    context = {
        "top5": TopFiveWinners(),
        "bottom5": TopFiveLosers(),
        "sixmonths": SixMonthsForecast()
    }
    return render_template('index.html', context=context)


@app.route('/ai-farmer')
def ai_farmer():
    """AI Farmer Intelligence Dashboard"""
    top5  = TopFiveWinners()
    bot5  = TopFiveLosers()
    six   = SixMonthsForecast()
    # Build full commodity price list for the advisor
    current_month  = datetime.now().month
    current_year   = datetime.now().year
    current_rain   = annual_rainfall[current_month - 1]
    all_prices = []
    for c in commodity_list:
        cname = c.getCropName().split('/')[-1]
        base_p = base.get(cname, 1000)
        try:
            wpi = c.getPredictedValue([float(current_month), current_year, current_rain])
            price = round((wpi * base_p) / 100, 2)
        except:
            price = base_p
        all_prices.append({'name': cname, 'price': price, 'base': base_p})
    all_prices.sort(key=lambda x: -x['price'])
    context = {
        'top5': top5, 'bottom5': bot5, 'sixmonths': six,
        'all_prices': all_prices,
        'month': datetime.now().strftime('%B %Y'),
    }
    return render_template('ai_farmer.html', context=context)


@app.route('/commodity/<name>')
def crop_profile(name):
    try:
        max_crop, min_crop, forecast_crop_values = TwelveMonthsForecast(name)
        prev_crop_values   = TwelveMonthPrevious(name)

        # Build 3-element forecast tuples: [label, price, pct_change]
        fv_display = []
        base_price = float(forecast_crop_values[0][1]) if forecast_crop_values else 1.0
        for item in forecast_crop_values:
            price = float(item[1]) if item[1] else 0.0
            try:
                chg = round(((price - base_price) / base_price) * 100, 2) if base_price else 0.0
            except:
                chg = 0.0
            fv_display.append([item[0], round(price, 2), chg])

        forecast_x = [i[0] for i in fv_display]
        forecast_y = [i[1] for i in fv_display]
        forecast_changes = [i[2] for i in fv_display]
        previous_x = [i[0] for i in prev_crop_values]
        previous_y = [round(float(i[1]), 2) for i in prev_crop_values]
        current_price = CurrentMonth(name)
        crop_data = crops.crop(name)

        context = {
            "name":           name,
            "max_crop":       max_crop if max_crop else ["—", 0],
            "min_crop":       min_crop if min_crop else ["—", 0],
            "forecast_values":fv_display,
            "forecast_x":     str(forecast_x),
            "forecast_y":     forecast_y,
            "forecast_changes": forecast_changes,
            "previous_x":     previous_x,
            "previous_y":     previous_y,
            "current_price":  round(float(current_price), 2) if current_price else 0,
            "image_url":      crop_data[0] if crop_data else '',
            "prime_loc":      crop_data[1] if crop_data else '—',
            "type_c":         crop_data[2] if crop_data else '—',
            "export":         crop_data[3] if crop_data else '—',
        }
        return render_template('commodity.html', context=context)
    except Exception as e:
        import traceback; traceback.print_exc()
        # Safe fallback context — no data to display
        context = {
            "name": name, "max_crop": ["—", 0], "min_crop": ["—", 0],
            "forecast_values": [], "forecast_x": "[]", "forecast_y": [],
            "forecast_changes": [], "previous_x": [], "previous_y": [],
            "current_price": 0, "image_url": "", "prime_loc": "—",
            "type_c": "—", "export": "—",
        }
        return render_template('commodity.html', context=context)



@app.route('/api/all-crops')
def all_crops_api():
    """Return all 23 commodity names + current prices for the crop grid."""
    current_month = datetime.now().month
    current_year  = datetime.now().year
    current_rain  = annual_rainfall[current_month - 1]
    result = []
    for c in commodity_list:
        cname = c.getCropName().split('/')[-1]
        base_p = base.get(cname, 1000)
        try:
            wpi = c.getPredictedValue([float(current_month), current_year, current_rain])
            price = round((wpi * base_p) / 100, 2)
        except:
            price = base_p
        result.append({'name': cname, 'price': price})
    result.sort(key=lambda x: x['name'])
    return jsonify({'ok': True, 'crops': result})


@app.route('/ticker/<item>/<number>')
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def ticker(item, number):
    n = int(number)
    i = int(item)
    data = SixMonthsForecast()
    context = str(data[n][i])

    if i == 2 or i == 5:
        context = '₹' + context
    elif i == 3 or i == 6:

        context = context + '%'

    #print('context: ', context)
    return context



@app.route('/api/geocode')
def geocode():
    """Reverse-geocode GPS coords to village/taluk/district/state via OpenStreetMap Nominatim (free, no key)."""
    lat = request.args.get('lat', '')
    lon = request.args.get('lon', '')
    try:
        import urllib.request as ur, json
        url = (f"https://nominatim.openstreetmap.org/reverse"
               f"?format=json&lat={lat}&lon={lon}&addressdetails=1&zoom=14")
        req = ur.Request(url, headers={'User-Agent': 'AgriIntelligence/1.0'})
        data = json.loads(ur.urlopen(req, timeout=8).read())
        addr = data.get('address', {})
        result = {
            'village':  addr.get('village') or addr.get('hamlet') or addr.get('suburb') or addr.get('neighbourhood') or '',
            'taluk':    addr.get('county') or addr.get('subdistrict') or addr.get('town') or '',
            'district': addr.get('state_district') or addr.get('district') or addr.get('city') or '',
            'state':    addr.get('state', ''),
            'pincode':  addr.get('postcode', ''),
            'display':  data.get('display_name', ''),
            'full':     addr,
        }
        return jsonify({'ok': True, 'data': result})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})


@app.route('/api/weather')
def live_weather():
    """Fetch real-time weather from Open-Meteo (free, no API key required)"""
    lat = request.args.get('lat', 22.5)
    lon = request.args.get('lon', 78.9)
    try:
        import urllib.request as ur, json
        url = (f"https://api.open-meteo.com/v1/forecast"
               f"?latitude={lat}&longitude={lon}"
               f"&current=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m,weather_code"
               f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code"
               f"&timezone=Asia%2FKolkata&forecast_days=7")
        data = json.loads(ur.urlopen(url, timeout=6).read())
        return jsonify({'ok': True, 'data': data})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})


@app.route('/api/market/<name>')
def live_market(name):
    """Return live ML-predicted price + 30-day daily trend for any commodity"""
    try:
        name_l = name.lower()
        commodity = None
        for c in commodity_list:
            cname = c.getCropName().split('/')[-1].lower()
            if name_l == cname or name_l in cname or cname in name_l:
                commodity = c
                break
        if commodity is None:
            return jsonify({'ok': False, 'error': 'Commodity not found'})

        from datetime import timedelta
        now = datetime.now()
        base_name = name_l.capitalize()
        base_price = base.get(base_name, 1000)
        rainfall = annual_rainfall

        # 30-day daily prices
        trend = []
        for d in range(0, 30):
            dt = now + timedelta(days=d)
            m = dt.month
            y = dt.year
            r = rainfall[m - 1]
            try:
                wpi = commodity.getPredictedValue([float(m), y, r])
                price = round((wpi * base_price) / 100, 2)
            except:
                price = base_price
            trend.append({'date': dt.strftime('%d %b'), 'price': price})

        current_m = now.month
        current_y = now.year
        r_now = rainfall[current_m - 1]
        try:
            wpi_now = commodity.getPredictedValue([float(current_m), current_y, r_now])
            current_price = round((wpi_now * base_price) / 100, 2)
        except:
            current_price = base_price

        return jsonify({'ok': True, 'name': name_l, 'current_price': current_price, 'trend_30d': trend})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})



def TopFiveWinners():
    current_month = datetime.now().month
    current_year = datetime.now().year
    current_rainfall = annual_rainfall[current_month - 1]
    prev_month = current_month - 1
    prev_rainfall = annual_rainfall[prev_month - 1]
    current_month_prediction = []
    prev_month_prediction = []
    change = []

    for i in commodity_list:
        current_predict = i.getPredictedValue([float(current_month), current_year, current_rainfall])
        current_month_prediction.append(current_predict)
        prev_predict = i.getPredictedValue([float(prev_month), current_year, prev_rainfall])
        prev_month_prediction.append(prev_predict)
        change.append((((current_predict - prev_predict) * 100 / prev_predict), commodity_list.index(i)))
    sorted_change = change
    sorted_change.sort(reverse=True)
    # print(sorted_change)
    to_send = []
    for j in range(0, 5):
        perc, i = sorted_change[j]
        name = commodity_list[i].getCropName().split('/')[1]
        to_send.append([name, round((current_month_prediction[i] * base[name]) / 100, 2), round(perc, 2)])
    #print(to_send)
    return to_send


def TopFiveLosers():
    current_month = datetime.now().month
    current_year = datetime.now().year
    current_rainfall = annual_rainfall[current_month - 1]
    prev_month = current_month - 1
    prev_rainfall = annual_rainfall[prev_month - 1]
    current_month_prediction = []
    prev_month_prediction = []
    change = []

    for i in commodity_list:
        current_predict = i.getPredictedValue([float(current_month), current_year, current_rainfall])
        current_month_prediction.append(current_predict)
        prev_predict = i.getPredictedValue([float(prev_month), current_year, prev_rainfall])
        prev_month_prediction.append(prev_predict)
        change.append((((current_predict - prev_predict) * 100 / prev_predict), commodity_list.index(i)))
    sorted_change = change
    sorted_change.sort()
    to_send = []
    for j in range(0, 5):
        perc, i = sorted_change[j]
        name = commodity_list[i].getCropName().split('/')[1]
        to_send.append([name, round((current_month_prediction[i] * base[name]) / 100, 2), round(perc, 2)])
   # print(to_send)
    return to_send



def SixMonthsForecast():
    month1=[]
    month2=[]
    month3=[]
    month4=[]
    month5=[]
    month6=[]
    for i in commodity_list:
        crop=SixMonthsForecastHelper(i.getCropName())
        k=0
        for j in crop:
            time = j[0]
            price = j[1]
            change = j[2]
            if k==0:
                month1.append((price,change,i.getCropName().split("/")[1],time))
            elif k==1:
                month2.append((price,change,i.getCropName().split("/")[1],time))
            elif k==2:
                month3.append((price,change,i.getCropName().split("/")[1],time))
            elif k==3:
                month4.append((price,change,i.getCropName().split("/")[1],time))
            elif k==4:
                month5.append((price,change,i.getCropName().split("/")[1],time))
            elif k==5:
                month6.append((price,change,i.getCropName().split("/")[1],time))
            k+=1
    # Sort by percentage change (index 1) instead of raw absolute price (index 0)
    month1.sort(key=lambda x: x[1])
    month2.sort(key=lambda x: x[1])
    month3.sort(key=lambda x: x[1])
    month4.sort(key=lambda x: x[1])
    month5.sort(key=lambda x: x[1])
    month6.sort(key=lambda x: x[1])
    
    crop_month_wise=[]
    seen_best = set()
    seen_worst = set()
    
    for month_data in [month1, month2, month3, month4, month5, month6]:
        # Pick the lowest % change (worst) that hasn't been picked yet
        worst_idx = 0
        while worst_idx < len(month_data) and month_data[worst_idx][2] in seen_worst:
            worst_idx += 1
        if worst_idx >= len(month_data): worst_idx = 0  # Fallback
        
        # Pick the highest % change (best) that hasn't been picked yet
        best_idx = len(month_data) - 1
        while best_idx >= 0 and month_data[best_idx][2] in seen_best:
            best_idx -= 1
        if best_idx < 0: best_idx = len(month_data) - 1 # Fallback
            
        best = month_data[best_idx]
        worst = month_data[worst_idx]
        
        seen_best.add(best[2])
        seen_worst.add(worst[2])
        
        # Format expected by frontend: [time, best_change, best_name, best_price, worst_change, worst_name, worst_price]
        crop_month_wise.append([best[3], best[1], best[2], best[0], worst[1], worst[2], worst[0]])

   # print(crop_month_wise)
    return crop_month_wise

def SixMonthsForecastHelper(name):
    current_month = datetime.now().month
    current_year = datetime.now().year
    current_rainfall = annual_rainfall[current_month - 1]
    name = name.split("/")[1]
    name = name.lower()
    commodity = commodity_list[0]
    for i in commodity_list:
        if name == str(i):
            commodity = i
            break
    month_with_year = []
    for i in range(1, 7):
        if current_month + i <= 12:
            month_with_year.append((current_month + i, current_year, annual_rainfall[current_month + i - 1]))
        else:
            month_with_year.append((current_month + i - 12, current_year + 1, annual_rainfall[current_month + i - 13]))
    wpis = []
    current_wpi = commodity.getPredictedValue([float(current_month), current_year, current_rainfall])
    change = []

    for m, y, r in month_with_year:
        current_predict = commodity.getPredictedValue([float(m), y, r])
        wpis.append(current_predict)
        change.append(((current_predict - current_wpi) * 100) / current_wpi)

    crop_price = []
    for i in range(0, len(wpis)):
        m, y, r = month_with_year[i]
        x = datetime(y, m, 1)
        x = x.strftime("%b %y")
        crop_price.append([x, round((wpis[i]* base[name.capitalize()]) / 100, 2) , round(change[i], 2)])

   # print("Crop_Price: ", crop_price)
    return crop_price

def CurrentMonth(name):
    current_month = datetime.now().month
    current_year = datetime.now().year
    current_rainfall = annual_rainfall[current_month - 1]
    name = name.lower()
    commodity = commodity_list[0]
    for i in commodity_list:
        if name == str(i):
            commodity = i
            break
    current_wpi = commodity.getPredictedValue([float(current_month), current_year, current_rainfall])
    current_price = (base[name.capitalize()]*current_wpi)/100
    return current_price

def TwelveMonthsForecast(name):
    current_month = datetime.now().month
    current_year = datetime.now().year
    current_rainfall = annual_rainfall[current_month - 1]
    name = name.lower()
    commodity = commodity_list[0]
    for i in commodity_list:
        if name == str(i):
            commodity = i
            break
    month_with_year = []
    for i in range(1, 13):
        if current_month + i <= 12:
            month_with_year.append((current_month + i, current_year, annual_rainfall[current_month + i - 1]))
        else:
            month_with_year.append((current_month + i - 12, current_year + 1, annual_rainfall[current_month + i - 13]))
    max_index = 0
    min_index = 0
    max_value = 0
    min_value = 9999
    wpis = []
    current_wpi = commodity.getPredictedValue([float(current_month), current_year, current_rainfall])
    change = []

    for m, y, r in month_with_year:
        current_predict = commodity.getPredictedValue([float(m), y, r])
        if current_predict > max_value:
            max_value = current_predict
            max_index = month_with_year.index((m, y, r))
        if current_predict < min_value:
            min_value = current_predict
            min_index = month_with_year.index((m, y, r))
        wpis.append(current_predict)
        change.append(((current_predict - current_wpi) * 100) / current_wpi)

    max_month, max_year, r1 = month_with_year[max_index]
    min_month, min_year, r2 = month_with_year[min_index]
    min_value = min_value * base[name.capitalize()] / 100
    max_value = max_value * base[name.capitalize()] / 100
    crop_price = []
    for i in range(0, len(wpis)):
        m, y, r = month_with_year[i]
        x = datetime(y, m, 1)
        x = x.strftime("%b %y")
        crop_price.append([x, round((wpis[i]* base[name.capitalize()]) / 100, 2) , round(change[i], 2)])
   # print("forecasr", wpis)
    x = datetime(max_year,max_month,1)
    x = x.strftime("%b %y")
    max_crop = [x, round(max_value,2)]
    x = datetime(min_year, min_month, 1)
    x = x.strftime("%b %y")
    min_crop = [x, round(min_value,2)]

    return max_crop, min_crop, crop_price


def TwelveMonthPrevious(name):
    name = name.lower()
    current_month = datetime.now().month
    current_year = datetime.now().year
    current_rainfall = annual_rainfall[current_month - 1]
    commodity = commodity_list[0]
    wpis = []
    crop_price = []
    for i in commodity_list:
        if name == str(i):
            commodity = i
            break
    month_with_year = []
    for i in range(1, 13):
        if current_month - i >= 1:
            month_with_year.append((current_month - i, current_year, annual_rainfall[current_month - i - 1]))
        else:
            month_with_year.append((current_month - i + 12, current_year - 1, annual_rainfall[current_month - i + 11]))

    for m, y, r in month_with_year:
        current_predict = commodity.getPredictedValue([float(m), 2013, r])
        wpis.append(current_predict)

    for i in range(0, len(wpis)):
        m, y, r = month_with_year[i]
        x = datetime(y,m,1)
        x = x.strftime("%b %y")
        crop_price.append([x, round((wpis[i]* base[name.capitalize()]) / 100, 2)])
   # print("previous ", wpis)
    new_crop_price =[]
    for i in range(len(crop_price)-1,-1,-1):
        new_crop_price.append(crop_price[i])
    return new_crop_price

@app.route('/api/geocode')
def geocode_api():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    if not lat or not lon:
        return jsonify({"ok": False, "error": "Missing lat/lon"}), 400
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&zoom=14&addressdetails=1"
        headers = {'User-Agent': 'AgriIntelligence/1.0 (Contact: demo@example.com)'}
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status() 
        data = response.json()
        addr = data.get('address', {})
        
        village = addr.get('village') or addr.get('suburb') or addr.get('neighbourhood') or addr.get('town')
        taluk = addr.get('county') or addr.get('city_district') or addr.get('state_district')
        district = addr.get('state_district') or addr.get('county')
        state = addr.get('state')
        pincode = addr.get('postcode')
        
        return jsonify({
            "ok": True, 
            "data": {
                "village": village,
                "taluk": taluk,
                "district": district,
                "state": state,
                "pincode": pincode
            }
        })
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/weather')
def weather_api():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    if not lat or not lon:
        return jsonify({"ok": False, "error": "Missing lat/lon"}), 400
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=auto"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return jsonify({"ok": True, "data": data})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500
print("Loading ML models for 23 commodities...")
arhar = Commodity(commodity_dict["arhar"])
commodity_list.append(arhar)
bajra = Commodity(commodity_dict["bajra"])
commodity_list.append(bajra)
barley = Commodity(commodity_dict["barley"])
commodity_list.append(barley)
copra = Commodity(commodity_dict["copra"])
commodity_list.append(copra)
cotton = Commodity(commodity_dict["cotton"])
commodity_list.append(cotton)
sesamum = Commodity(commodity_dict["sesamum"])
commodity_list.append(sesamum)
gram = Commodity(commodity_dict["gram"])
commodity_list.append(gram)
groundnut = Commodity(commodity_dict["groundnut"])
commodity_list.append(groundnut)
jowar = Commodity(commodity_dict["jowar"])
commodity_list.append(jowar)
maize = Commodity(commodity_dict["maize"])
commodity_list.append(maize)
masoor = Commodity(commodity_dict["masoor"])
commodity_list.append(masoor)
moong = Commodity(commodity_dict["moong"])
commodity_list.append(moong)
niger = Commodity(commodity_dict["niger"])
commodity_list.append(niger)
paddy = Commodity(commodity_dict["paddy"])
commodity_list.append(paddy)
ragi = Commodity(commodity_dict["ragi"])
commodity_list.append(ragi)
rape = Commodity(commodity_dict["rape"])
commodity_list.append(rape)
jute = Commodity(commodity_dict["jute"])
commodity_list.append(jute)
safflower = Commodity(commodity_dict["safflower"])
commodity_list.append(safflower)
soyabean = Commodity(commodity_dict["soyabean"])
commodity_list.append(soyabean)
sugarcane = Commodity(commodity_dict["sugarcane"])
commodity_list.append(sugarcane)
sunflower = Commodity(commodity_dict["sunflower"])
commodity_list.append(sunflower)
urad = Commodity(commodity_dict["urad"])
commodity_list.append(urad)
wheat = Commodity(commodity_dict["wheat"])
commodity_list.append(wheat)
print("ML Models loaded.")

if __name__ == "__main__":
    app.run()





