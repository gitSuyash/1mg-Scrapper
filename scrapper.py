import requests
import pandas as pd
from bs4 import BeautifulSoup

def myScraper(scrape_url,total_pages):
    page_num = 1
    product_name=[]
    product_mrp =[]
    product_rate=[]
    product_rating=[]
    product_packing = []
    product_discount = []
    while True:
        if page_num > total_pages:
            break
        url = scrape_url+str(page_num)
        response = requests.get(url)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        product_container = html_soup.find_all('div',class_='style__container___1TL2R')
        for i in range(len(product_container)):
            product_name.append(product_container[i].find(class_='style__pro-title___2QwJy').text)
            try:
                product_mrp.append(product_container[i].find(class_='style__discount-price___25Bya').text)
            except AttributeError:
                product_mrp.append(None)
            try:
                product_rate.append(product_container[i].find(class_='style__price-tag___cOxYc').text)
            except AttributeError:
                product_rate.append(None)
            try:
                product_rating.append(product_container[i].find(class_='CardRatingDetail__weight-700___27w9q').text)
            except AttributeError:
                product_rating.append(None)
            try:
                product_packing.append(product_container[i].find(class_='style__pack-size___2JQG7').text)
            except AttributeError:
                product_packing.append(None)
            try:
                product_discount.append(product_container[i].find(class_='style__off-badge___2JaF-').text)
            except AttributeError:
                product_discount.append(None)
        page_num+=1
    data = pd.DataFrame({'Name':product_name,
                    'MRP':product_mrp,
                    'Rate':product_rate,
                     'Discount':product_discount,
                    'Ratings':product_rating,
                    'Packing':product_packing})
    return data

def clean_data(data):
    
    #Rate
    data['Rate']=data['Rate'].str.replace('MRP₹','')
    data['Rate'] = data['Rate'].str.replace('₹','')
    data['Rate']=data['Rate'].astype('float')
    
    # MRP
    data['MRP']=data['MRP'].str.replace('₹','')
    data['MRP'].fillna(data.loc[data['MRP'].isna(),'Rate'],inplace=True)
    data['MRP']=data['MRP'].astype('float')
    
    #Discount
    data['Discount'] = data['Discount'].str.replace('% off','')
    data['Discount'] = data['Discount'].replace('', None)
    data['Discount']=data['Discount'].astype('float')
    data['Discount'].fillna(0,inplace=True)
    
    return data

mask_data = myScraper('https://www.1mg.com/categories/coronavirus-prevention/protective-masks-277?filter=true&pageNumber=',20)
cleaned_mask_data = clean_data(mask_data)

sanitizer_data = myScraper('https://www.1mg.com/categories/coronavirus-prevention/sanitizers-handwash-products-296?filter=true&pageNumber=',24)
cleaned_sanitizer_data = clean_data(sanitizer_data)

oximeter_data = myScraper('https://www.1mg.com/categories/coronavirus-prevention/pulse-oximeters-825?filter=true&pageNumber=',3)
cleaned_oximeter_data = clean_data(oximeter_data)

disinfectant_data = myScraper('https://www.1mg.com/categories/coronavirus-prevention/disinfectants-226?filter=true&pageNumber=',5)
cleaned_disinfectant_data = clean_data(disinfectant_data)

immunity_data=myScraper('https://www.1mg.com/categories/coronavirus-prevention/boost-your-immunity-452?filter=true&pageNumber=',40)
cleaned_immunity_data = clean_data(immunity_data)

thermo_data = myScraper('https://www.1mg.com/categories/coronavirus-prevention/thermometers-device-298?filter=true&pageNumber=',5)
cleaned_thermo_data = clean_data(thermo_data)

chyawan_data = myScraper('https://www.1mg.com/categories/coronavirus-prevention/chyawanprash-709?filter=true&pageNumber=',3)
cleaned_chyawan_data = clean_data(chyawan_data)

cleaned_mask_data.to_csv('mask.csv',index=False)
cleaned_sanitizer_data.to_csv('sanitizer&handwash.csv',index=False)
cleaned_oximeter_data.to_csv('oximeter.csv',index=False)
cleaned_disinfectant_data.to_csv('disinfectant.csv',index=False)
cleaned_immunity_data.to_csv('immunity-items.csv',index=False)
cleaned_thermo_data.to_csv('thermometer.csv',index=False)
cleaned_chyawan_data.to_csv('chyawan.csv',index=False)