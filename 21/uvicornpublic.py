#!/usr/bin/python3
# -*- coding: utf-8 -*-

from typing import Optional#, Enum
from fastapi import FastAPI
from pydantic import BaseModel
import csv
import win32com.client
import win32file
import re
import os
import time
import datetime
import uuid
import sys
import pythoncom
from fastapi.middleware.cors import CORSMiddleware

минимальная_вагонная_норма_загрузки={
"11005":" по грузоподъёмности",
"12008":" по грузоподъёмности",
"13000":"53",
"14003":" по грузоподъёмности",
"15006":" по грузоподъёмности",
"16009":"53",
"17001":" по грузоподъёмности",
"18004":" по грузоподъёмности",
"21007":"43",
"22007":"35",
"23002":"26",
"24005":"29",
"31009":"34",
"41000":"28",
"42003":"25",
"43006":"51",
"44009":"кр, пв-50, пл-20",
"51002":"25",
"52005":"25",
"53008":"33",
"54000":"35",
"61004":"10",
"62007":"10",
"63006":"10",
"71006":"15",
"72009":"21",
"73001":"17",
"74004":"17",
"75007":"22",
"76003":"22",
"77002":"40",
"78005":"47",
"81008":"44 <5>",
"82000":"44 <5>",
"91008":"44",
"92002":"44 <5>",
"93005":"пв, пл - 44 <5>",
"94008":"38",
"101004":"кр, пв-40, пл-33",
"102007":"кр, пв-40, пл-33",
"103007":"18",
"111006":"кр, пв-40, пл-33",
"112009":"22",
"121008":"26",
"122000":"42",
"123003":"25",
"124006":"25",
"125009":"31",
"126001":"20",
"127004":"13",
"131009":"41",
"132002":"40",
"133005":"18",
"141001":" по грузоподъёмности",
"142004":" по грузоподъёмности",
"151003":" по грузоподъёмности",
"152006":" по грузоподъёмности",
"153009":"53",
"161005":"кр, пв- по грузоподъёмности <2>, пл-46",
"171007":"44",
"181009":"40",
"182001":"40",
"191000":"50",
"201005":"50",
"211007":"50",
"212009":"50",
"213002":"50",
"214005":"50",
"215008":"50",
"221009":"50",
"222001":"50",
"223004":"50",
"224007":"50",
"225006":"50",
"226002":"26",
"231000":"кр, пв- по грузоподъёмности, пл-46",
"232003":"кр, пв- по грузоподъёмности, пл-46",
"233006":"кр, пв- по грузоподъёмности, пл-46",
"234009":"40",
"235001":"кр, пв- по грузоподъёмности, пл-46",
"236004":"кр, пв- по грузоподъёмности, пл-46",
"241002":"кр, пв- по грузоподъёмности, пл-46",
"242005":"кр, пв- по грузоподъёмности, пл-46",
"243008":"кр, пв- по грузоподъёмности, пл-46",
"244000":" по грузоподъёмности",
"245003":" по грузоподъёмности",
"246006":" по грузоподъёмности",
"251004":"кр, пв-58, пл-46",
"252007":"50",
"253008":"кр, пв- по грузоподъёмности, пл-46",
"254002":"58",
"255005":"58",
"256008":"15",
"261006":"15",
"262009":"50",
"263001":"50",
"264004":"44",
"265007":"27",
"266005":"52",
"267002":"45",
"268005":"20",
"271008":"кр, пв- по грузоподъёмности, пл-46",
"281000":" по грузоподъёмности",
"291001":"кр, пв- по грузоподъёмности, пл-46",
"292004":"кр, пв- по грузоподъёмности, пл-46",
"301006":"кр, пв- по грузоподъёмности, пл-46",
"302009":"кр, пв- по грузоподъёмности, пл-46",
"303001":"кр, пв- по грузоподъёмности, пл-46",
"304004":"52",
"311008":" по грузоподъёмности",
"312000":" по грузоподъёмности",
"313003":" по грузоподъёмности",
"314006":" по грузоподъёмности",
"315009":"60",
"316001":"51",
"321000":"59",
"322002":" по грузоподъёмности",
"323005":"44 <2>",
"324008":" по грузоподъёмности",
"331001":" по грузоподъёмности",
"332004":"49",
"333007":"41",
"341003":"кр, пв- по грузоподъёмности, пл-46",
"351005":"21",
"361007":"21",
"362000":"17",
"371009":"21",
"381000":"14",
"391002":"12",
"401007":"20",
"402000":"12",
"403002":"11",
"404005":"21",
"405008":"14",
"411009":"38",
"412001":"38",
"413004":"15",
"414007":"43",
"415008":"19",
"416002":"29",
"417005":"27",
"418008":"29",
"421000":"",
"422003":"",
"423006":"",
"431002":" по грузоподъёмности",
"432005":" по грузоподъёмности",
"433008":" по грузоподъёмности",
"434000":" по грузоподъёмности",
"435003":" по грузоподъёмности",
"436006":" по грузоподъёмности",
"441004":"25",
"442007":"20",
"443000":"46",
"451006":"55",
"452009":"20",
"453001":"23",
"454004":"29",
"461008":"43",
"462000":"17",
"463003":"20",
"464006":"30",
"465009":"45",
"466001":"39",
"467004":"39",
"471001":"55",
"472002":"45",
"473005":"55",
"474008":"19",
"475000":"45",
"481001":"52",
"482004":"55",
"483007":"52",
"484009":"52",
"485002":"52",
"486005":"32",
"487008":" по грузоподъёмности",
"488000":"39",
"489003":"52",
"501008":" по грузоподъёмности",
"502000":" по грузоподъёмности",
"503003":" по грузоподъёмности",
"504006":" по грузоподъёмности",
"505009":" по грузоподъёмности",
"511002":"25",
"512002":"25",
"513005":"25",
"514008":"29",
"515000":"55",
"516003":"29",
"517006":"18",
"521001":" по грузоподъёмности",
"531003":" по грузоподъёмности",
"541005":"56",
"542008":"52",
"551007":"20",
"552001":"20",
"553002":"42",
"554005":"42",
"555008":"18",
"556000":"31",
"561009":"21",
"562001":"27",
"563004":"31",
"564007":"21",
"571000":"18",
"572003":"50",
"573006":"50",
"574009":"51",
"581002":"40",
"582005":"31",
"583008":"24",
"584000":"40",
"591004":"40",
"592007":"40",
"593000":"40",
"594002":"37",
"595005":"40",
"601009":"52",
"602001":"40",
"611000":"54",
"621002":"19",
"622005":"19",
"623008":"26",
"624000":"10",
"625003":"10",
"626006":"19",
"631004":"25",
"632007":"18",
"633001":"12",
"634002":"12",
"635005":"14",
"641006":"18",
"651008":"39",
"652000":"48",
"653003":"17",
"654006":"13",
"661003":"22",
"662002":"22",
"671001":"16",
"681003":"16",
"682006":"30",
"683009":"11",
"684001":"30",
"685004":"14",
"691005":"10",
"692008":"20",
"693000":"10 <4>",
"711001":"39",
"712004":"39",
"713007":"39",
"721003":"32",
"722006":"32",
"723009":"52",
"724001":"52",
"725004":"32",
"726007":"52",
"731005":"52",
"732012":"52",
"741007":"32",
"742003":"52",
"751009":"39",
"752001":"35",
"753004":"52",
"754007":"35",
"755000":"39",
"756002":"39",
"757005":"40",
"758008":"40"
    }

  
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    None
]

app.add_middleware(
    CORSMiddleware,
##    allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

##class ModelName(str, Enum):
##    alexnet = "alexnet"
##    resnet = "resnet"
##    lenet = "lenet"




class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

@app.put("/itemiiis/{item_id}")
async def create_item(item_id: int, item: Item):#, model:ModelName):
    return {"item_id": item_id, **item.dict()}

@app.get("/")
def read_root():
    try:
        uniqueid=uuid.uuid4()
        return { "status":"ok", "guid": uniqueid, "help":"http://127.0.0.1:8000/docs#/default/"}
    except:
        return { "status":"exception", "guid": uniqueid}
    
@app.get("/description.xml")
def read_description_xml():
    try:
        uniqueid=uuid.uuid4()
        IP = "192.168.88.107" # Bind to IP
        HTTP_PORT = 1901 # HTTP-port to serve icons and xml
        DESCRIPTION_XML = """<?xml version="1.0"?>
        <root xmlns="urn:schemas-upnp-org:device-1-0">
                <specVersion>
                        <major>1</major>
                        <minor>0</minor>
                </specVersion>
                <URLBase>http://{}:{}/</URLBase>
                <device>
                        <deviceType>urn:schemas-upnp-org:device:Basic:1</deviceType>
                        <friendlyName>Philips hue Bridge Router</friendlyName>
                        <manufacturer>Sagen</manufacturer>
                        <manufacturerURL>http://github.com/sagen</manufacturerURL>
                        <modelDescription>Philips hue Personal Wireless Lighting Bridge Router</modelDescription>
                        <modelName>Philips hue bridge 2012 Router</modelName>
                        <modelNumber>929000226503</modelNumber>
                        <modelURL>http://www.meethue.com</modelURL>
                        <serialNumber>nope</serialNumber>
                        <UDN>uuid:2f402f80-da50-11e1-9b23-nydalenlys</UDN>
                        <serviceList>
                                <service>
                                        <serviceType>(null)</serviceType>
                                        <serviceId>(null)</serviceId>
                                        <controlURL>(null)</controlURL>
                                        <eventSubURL>(null)</eventSubURL>
                                        <SCPDURL>(null)</SCPDURL>
                                </service>
                        </serviceList>
                        <presentationURL>index.html</presentationURL>
                        <iconList>
                                <icon>
                                        <mimetype>image/png</mimetype>
                                        <height>48</height>
                                        <width>48</width>
                                        <depth>24</depth>
                                        <url>hue_logo_0.png</url>
                                </icon>
                                <icon>
                                        <mimetype>image/png</mimetype>
                                        <height>120</height>
                                        <width>120</width>
                                        <depth>24</depth>
                                        <url>hue_logo_3.png</url>
                                </icon>
                        </iconList>
                </device>
        </root>
        """.format(IP, HTTP_PORT).replace("\n", "").replace("  ", " ")#.replace("\n", "\r\n")
        return bytes(DESCRIPTION_XML, "latin1")
    except:
        return { "status":"exception", "guid": uniqueid}
    


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.get("/ite/")
def read_item(item_id: Optional[str] = None, name: Optional[str] = None, price: Optional[str] = None):
    with open('del2.csv', 'w', newline='') as csvfile:
        writer  = csv.writer(csvfile, delimiter=';',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['item_id', 'name', 'price'])
        writer.writerow([str(item_id), str(name), str(price)])
    return {"item_id": item_id, "name": name}



@app.get("/fe/")
def uvi_frontend(item_id: Optional[str] = None):
    with open(r'C:\Users\User\Downloads\uvicornserver_frontend.html', 'r') as bodyfile:
        return bodyfile.read()

@app.get("/fe2fa/")
def uvi_2fa(totp: str):
    """
    Script that produces the same TOTP codes as the Google Authenticator App\n
    make one here https://dan.hersam.com/tools/gen-qr-code.php
    """
    import hmac, base64, struct, hashlib, time, json, os

    def get_hotp_token(secret, intervals_no):
            """This is where the magic happens."""
            key = base64.b32decode(normalize(secret), True) # True is to fold lower into uppercase
            msg = struct.pack(">Q", intervals_no)
            h = bytearray(hmac.new(key, msg, hashlib.sha1).digest())
            o = h[19] & 15
            h = str((struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000)
            return prefix0(h)

    def get_totp_token(secret):
            """The TOTP token is just a HOTP token seeded with every 30 seconds."""
            return get_hotp_token(secret, intervals_no=int(time.time())//30)

    def normalize(key):
            """Normalizes secret by removing spaces and padding with = to a multiple of 8"""
            k2 = key.strip().replace(' ','')
            # k2 = k2.upper()	# skipped b/c b32decode has a foldcase argument
            if len(k2)%8 != 0:
                    k2 += '='*(8-len(k2)%8)
            return k2

    def prefix0(h):
            """Prefixes code with leading zeros if missing."""
            if len(h) < 6:
                    h = '0'*(6-len(h)) + h
            return h

    try:
        uniqueid=uuid.uuid4()
        print("\n==============================Поступил запрос==============================")
        if get_totp_token("XP") ==totp:
            print("==============================Подпись правильная==============================\n")
            print("==============================Поступил запрос==============================\n")
            return { "status":"ok", "guid": uniqueid, "result":"Подпись правильная"}
        else:
            print("==============================Подпись неправильная==============================\n")
            print("==============================Поступил запрос==============================\n")
            return { "status":"ok", "guid": uniqueid, "result":"Подпись неправильная"}
    except:
        print("===========================Запрос не обработан==============================\n")
        return { "status":"exception", "guid": uniqueid}
    

def работа_с_личным_кабинетом_ржд(station_from, station_to, freight, package, weight, car_type, car_owner):
    import rpa as roboticsa
    try:
        print("\n==============================Поступил запрос==============================")
        roboticsa.init()
        roboticsa.wait(2)
        roboticsa.url('https://cargolk.rzd.ru/services/calculator')
        roboticsa.wait(30)
        roboticsa.type('//*[@id="station_from"]', str(station_from))
        roboticsa.wait(2)
        roboticsa.type('//*[@id="station_to"]', str(station_to))
        roboticsa.wait(2)
        roboticsa.type('//*[@id="freight"]', str(freight))#Наименование груза
        roboticsa.wait(2)
        roboticsa.type('//*[@id="package"]', str(package))
        roboticsa.wait(2)
        roboticsa.type('//*[@id="weight"]', str(weight))
        roboticsa.type('//*[@id="car-type"]', str(car_type))
        roboticsa.wait(2)
        roboticsa.type('//*[@id="car-owner"]', str(car_owner))
        roboticsa.wait(2)
        #roboticsa.close()
        uniqueid=uuid.uuid4()
        print("==============================Поступил запрос==============================\n")
        return reply
    except:
        return { "status":"exception", "guid": uniqueid}

def работа_с_документом_ms_word(where_to_put,itemi):
    import requests
    import json
    

    USERAGENT_HEADER = """Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) \
    AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.101 Safari/537.11"""
    ACCEPT_HEADER = """text/html,application/xhtml+xml,application/xml;q=0.9,\
    */*;q=0.8"""


    def simple_http_get(url, headers=None):
        default_headers = {
            'Accept': ACCEPT_HEADER,
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Language': 'en-US,en;q=0.8',
            'User-Agent': USERAGENT_HEADER
        }
        default_headers.update(headers or {})
        req = requests.get(url, headers=default_headers)
        return req.text

    print(" try работа_с_документом_ms_word(where_to_put,itemi):")
    if itemi is None:
        itemi = " "
    workingdirectory = r"I:\Desktop\2021"
    import win32com.client
    import win32file
    from datetime import datetime
    import re
    #============================MorphAnalyzer
    import pymorphy2
    morph = pymorphy2.MorphAnalyzer()
    #По умолчанию используется словарь для русского языка; 

##    butyavka = morph.parse('бутявка')[0]
##
##
##    #Получив объект Parse, можно просклонять слово, используя его метод Parse.inflect():
##    print(butyavka.inflect({'gent'}) ) # нет кого? (родительный падеж)
##
##    #письмо datv дательный Кому? Чему?  
##    print(morph.parse('Генеральный')[0].inflect({'sing', 'datv'}).word )
##    print(morph.parse('директор')[0].inflect({'sing', 'datv'}).word )
##
##    #в лице gent родительный Кого? Чего? 
##    print(morph.parse('Генеральный')[0].inflect({'sing', 'gent'}).word)
##    print(morph.parse('директор')[0].inflect({'sing', 'gent'}).word)
##
##
##    position_phrase="Старший исполнительный директор"
##    position_phrase_inflected=""
##    for single_word in position_phrase.split(" "):
##        position_phrase_inflected+=morph.parse(single_word)[0].inflect({'sing', 'datv'}).word+" "
##
##    print(position_phrase_inflected[0:1].upper()+position_phrase_inflected[1:])
    #============================MorphAnalyzer
    arr_all_files=[0]
    for file in win32file.FindFilesW(workingdirectory+"\*.doc*", Transaction=None ):
        if not re.search("[0-9][0-9][0-9]", str(file[8][0:3])) is None:
            arr_all_files.append(int(str(file[8][0:3])))
                
    pythoncom.CoInitialize()            
    Word = win32com.client.Dispatch("Word.Application")
    Word.Visible = True
    Word.DisplayAlerts = False
    objDocument = Word.Documents.Open(workingdirectory+"\\"+where_to_put) 
    #Заменяем метки на значения из ячеек request['data']
    objDocument.Bookmarks["DocNumber"].Range.Text = str(max(arr_all_files)+1)
    objDocument.Bookmarks["DocDate"].Range.Text = str(datetime.strftime(datetime.now(),"%d.%m.%Y"))
    if itemi is not None:
        #Данный код запрашивает ИНН и готовит письмо с реквизитами...
        request=json.loads(simple_http_get("https://api.checko.ru/json?object=organization&key=hakZwNakig1eEoF3o6augQ&ogrn=&inn="+str(itemi)+"&kpp=&source=false"))
        objDocument.Bookmarks["CompanyName"].Range.Text = str(request['data']['name'])
        position_phrase=str(request['data']['leaders'][0]['post'])
        position_phrase_inflected=""
        for single_word in position_phrase.split(" "):
            position_phrase_inflected+=morph.parse(single_word)[0].inflect({'sing', 'datv'}).word+" "

        objDocument.Bookmarks["JobTitle"].Range.Text = str(position_phrase_inflected[0:1].upper()+position_phrase_inflected[1:]) #str(request['data']['leaders'][0]['post'])
        #print(str(request['data']['leaders'][0]['name']).split(" ")[2][-4:] )
        greeting=["",""]    
        if str(request['data']['leaders'][0]['name']).split(" ")[2][-4:] in ["ович","евич"]:
            greeting[0]="Уважаемый "
            greeting[1]="г-ну "
        if str(request['data']['leaders'][0]['name']).split(" ")[2][-4:] in ["овна","евна"]:
            greeting[0]="Уважаемая "
            greeting[1]="г-же "            
        objDocument.Bookmarks["FullName"].Range.Text = greeting[1]+\
        str(request['data']['leaders'][0]['name']).split(" ")[0]+" "+\
        str(request['data']['leaders'][0]['name']).split(" ")[1][:1]+\
        "."+str(request['data']['leaders'][0]['name']).split(" ")[2][:1]+"."
        objDocument.Bookmarks["PatronimicName"].Range.Text = greeting[0]+str(" ".join(request['data']['leaders'][0]['name'].split(" ")[1:]))
#работа_с_документом_ms_word():

def создание_простого_договора(инн_продавца, инн_покупателя):
    import requests
    import json
    import pymorphy2
    morph = pymorphy2.MorphAnalyzer()

    def simple_http_get(url, headers=None):
        USERAGENT_HEADER = """Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) \
        AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.101 Safari/537.11"""
        ACCEPT_HEADER = """text/html,application/xhtml+xml,application/xml;q=0.9,\
        */*;q=0.8"""        
        default_headers = {
            'Accept': ACCEPT_HEADER,
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Language': 'en-US,en;q=0.8',
            'User-Agent': USERAGENT_HEADER
        }
        default_headers.update(headers or {})
        req = requests.get(url, headers=default_headers)
        return req.text


  
    if len(инн_продавца) in [10,12] and len(инн_покупателя) in [10,12] :
        print(инн_продавца)
        print(инн_покупателя)
        #Запрашиваем ИНН продавца
        request=json.loads(simple_http_get("https://api.checko.ru/json?object=organization&key=hakZwNakig1eEoF3o6augQ&ogrn=&inn="+str(инн_продавца)+"&kpp=&source=false"))
        phrase_inflected=""
        phrase_inflected+=str(request['data']['name'])
        phrase_inflected+=", именуемое в дальнейшем изложении «Продавец», в лице "
        #реквизиты 
        at_the_end_details="«Продавец» "+str(request['data']['name'])+\
                            "Местонахождение: "+str(request['data'] ['location']['legal_address'])+\
                            " ОГРН "+str(request['data']['ogrn'])+\
                            " ИНН "+str(request['data'][ 'inn'])+" / КПП "+str(request['data'][ 'kpp'])+\
                            " ОКПО "+str(request['data'][ 'okpo'])
        #в лице
        at_the_end_phrase="«Продавец» "+str(request['data']['leaders'][0]['post'])
        for single_word in str(request['data']['leaders'][0]['post']).split(" "):
            position_one=morph.parse(single_word)[0].inflect({'sing', 'gent'}).word
            phrase_inflected+=position_one[0:1].upper()+position_one[1:]+" "
    
        #ФИО
        at_the_end_phrase+=" "+str(request['data']['leaders'][0]['name']).split(" ")[0]+" "+\
        str(request['data']['leaders'][0]['name']).split(" ")[1][:1]+\
        "."+str(request['data']['leaders'][0]['name']).split(" ")[2][:1]+". ___________"           
        for single_word in str(request['data']['leaders'][0]['name']).split(" "):
            position_one=morph.parse(single_word)[0].inflect({'sing', 'gent'}).word
            phrase_inflected+=position_one[0:1].upper()+position_one[1:]+" "
            
        phrase_inflected+=", действующего на основании Устава, с одной стороны и "
        time.sleep(5)
        #Запрашиваем ИНН покупателя
        request=json.loads(simple_http_get("https://api.checko.ru/json?object=organization&key=hakZwNakig1eEoF3o6augQ&ogrn=&inn="+str(инн_покупателя)+"&kpp=&source=false"))
        phrase_inflected+=str(request['data']['name'])
        phrase_inflected+=", именуемое в дальнейшем изложении «Покупатель», в лице "
        #реквизиты 
        at_the_end_details+="«Покупатель» "+str(request['data']['name'])+\
                            "Местонахождение: "+str(request['data'] ['location']['legal_address'])+\
                            " ОГРН "+str(request['data']['ogrn'])+\
                            " ИНН "+str(request['data'][ 'inn'])+" / КПП "+str(request['data'][ 'kpp'])+\
                            " ОКПО "+str(request['data'][ 'okpo'])        
        #в лице
        at_the_end_phrase+="«Покупатель» "+str(request['data']['leaders'][0]['post'])        
        for single_word in str(request['data']['leaders'][0]['post']).split(" "):
            position_one=morph.parse(single_word)[0].inflect({'sing', 'gent'}).word
            phrase_inflected+=position_one[0:1].upper()+position_one[1:]+" "
    
        #ФИО
        at_the_end_phrase+=" "+str(request['data']['leaders'][0]['name']).split(" ")[0]+" "+\
        str(request['data']['leaders'][0]['name']).split(" ")[1][:1]+\
        "."+str(request['data']['leaders'][0]['name']).split(" ")[2][:1]+". ___________"                              
        for single_word in str(request['data']['leaders'][0]['name']).split(" "):
            position_one=morph.parse(single_word)[0].inflect({'sing', 'gent'}).word
            phrase_inflected+=position_one[0:1].upper()+position_one[1:]+" "
            
        phrase_inflected+=", действующего на основании Устава, с другой стороны, совместно именуемые «Стороны» заключили настоящее дополнительное соглашение о нижеследующем:"
        return phrase_inflected+at_the_end_details+at_the_end_phrase
#создание_простого_договора_ms_word():
        
# Отправка сообщения
def sentHTMLmessageWithAttachments(to_address, subject, HTMLBody, to_name=''):
    # инициализируем объект outlook
    print("1 sentHTMLmessageWithAttachments")
    pythoncom.CoInitialize()
    #print("2 sentHTMLmessageWithAttachments")
    objOutlook = win32com.client.Dispatch("Outlook.Application")
    #print("3 sentHTMLmessageWithAttachments")
    objMail = objOutlook.CreateItem(0)
    #print("4 sentHTMLmessageWithAttachments")
    objMail.to = to_address
    objMail.Subject = subject
    objMail.BodyFormat = 2
    objMail.ReplyRecipients.Add("")
    objMail.HTMLBody = HTMLBody#'<h2>HTML Message body</h2>' #this field is optional
    attachment  = r'C:\Windows\Temp\структурированные_данные.csv'
    objMail.Attachments.Add(attachment)
    objMail.Display() #    objMail.Send()
#def sentHTMLmessageWithAttachments(to_address, subject, HTMLBody, to_name=''):

@app.get("/запрос_справки_о_товаре")
def запрос_справки_о_товаре(товар: str, страна: str, экспорт_либо_импорт: str, Наименование_организации: Optional[str] = None, Наименование_товара: Optional[str] = None, Заявляемая_таможенная_процедура: Optional[str] = None, Страна_отправления: Optional[str] = None, Страна_назначения: Optional[str] = None, Страна_происхождения_товара: Optional[str] = None, Описание_товара: Optional[str] = None, Фото_товара: Optional[str] = None, Область_применения_и_назначение_товара: Optional[str] = None):
    """ запрос справки о товаре в 
    эксп_имп - направление экспорт либо импорт
    
	1. Наименование организации с указанием реквизитов;
	2. Наименование товара (в том числе торговое/коммерческое);
	3. Заявляемая таможенная процедура;
	4. Страна отправления/назначения, страна происхождения товара;
	5. Описание товара, в том числе техническая документация, паспорта качества, ГОСТы, ТУ, сертификаты;
	6. Фото товара;
	7. Область применения и назначение товара;
    
    """
    try:
        uniqueid=uuid.uuid4()
        print("\n==============================Поступил запрос==============================")
        sentHTMLmessageWithAttachments(to_address="", subject='дать справку о товаре',HTMLBody="Уважаемые господа,<br><br>ООО «» просит Вас дать справку на "+str(экспорт_либо_импорт)+":<br><br>Товар: "+str(товар)+"<br>Страна: "+str(страна)+"<br><br>--<br>С уважением,<br><p> <font color='white'>"+str(uniqueid)+"</font></p>", to_name='')        
        print("==============================Поступил запрос==============================\n")
        return { "status":"ok", "guid": uniqueid}
    except:
        print("===========================Запрос не обработан==============================\n")
        return { "status":"exception", "guid": uniqueid}

@app.get("/запрос_поставщику_rus")
def запрос_поставщику_rus(инн: Optional[str] = None):
    try:
        uniqueid=uuid.uuid4()
        print("\n==============================Поступил запрос==============================")
        работа_с_документом_ms_word("шаблон-RFP-RUS.doc",инн)
        print("==============================Поступил запрос==============================\n")
        return { "status":"ok", "item": инн, "guid": uniqueid}
    except:
        print("===========================Запрос не обработан==============================\n")
        return { "status":"exception", "guid": uniqueid}


@app.get("/запрос_поставщику_eng")
def запрос_поставщику_eng(инн: Optional[str] = None):
    try:
        uniqueid=uuid.uuid4()
        print("\n==============================Поступил запрос==============================")
        работа_с_документом_ms_word("шаблон-RFP-ENG.doc",инн)
        print("==============================Поступил запрос==============================\n")
        return { "status":"ok", "item": инн, "guid": uniqueid}
    except:
        print("===========================Запрос не обработан==============================\n")
        return { "status":"exception", "guid": uniqueid}

@app.get("/предложение_клиенту_rus")
def предложение_клиенту_rus(инн: Optional[str] = None):
    try:
        uniqueid=uuid.uuid4()
        print("\n==============================Поступил запрос==============================")
        работа_с_документом_ms_word("шаблон-FCO-RUS.doc",инн)
        print("==============================Поступил запрос==============================\n")
        return { "status":"ok", "item": инн, "guid": uniqueid}
    except:
        print("===========================Запрос не обработан==============================\n")
        return { "status":"exception", "guid": uniqueid}

@app.get("/предложение_клиенту_eng")
def предложение_клиенту_eng(инн: Optional[str] = None):
    try:
        uniqueid=uuid.uuid4()
        print("\n==============================Поступил запрос==============================")
        работа_с_документом_ms_word("шаблон-FCO-ENG.doc",инн)
        print("==============================Поступил запрос==============================\n")
        return { "status":"ok", "item": инн, "guid": uniqueid}
    except:
        print("===========================Запрос не обработан==============================\n")
        return { "status":"exception", "guid": uniqueid}

from fastapi import BackgroundTasks, FastAPI



@app.get("/запрос_ставки_жд_тарифа")
def запрос_ставки_жд_тарифа(тип_вагона:str, код_груза:str, станция_отправления:str,станция_назначения: str, тариф: str, background_tasks: BackgroundTasks):
    try:
        uniqueid=uuid.uuid4()
        #console = sys.stdout
        print("==============================Поступил запрос==============================\n"+str(тип_вагона)+":"+str(код_груза)+":"+str(станция_отправления)+":"+str(станция_назначения)+":"+str(тариф)+":"+str(uniqueid)+"\n==============================Поступил запрос==============================")
        #sys.stdout = console
        with open(r'C:\Windows\Temp\структурированные_данные.csv', 'w', newline='') as csvfile:
            writer  = csv.writer(csvfile, delimiter=';',quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['тип вагона', 'код груза', 'станция отправления', 'станция назначения', 'тариф', 'guid'])
            writer.writerow([str(тип_вагона), str(код_груза), str(станция_отправления), str(станция_назначения), str(тариф), str(uniqueid)])

        with open(r'I:\DataProjects\workflow\структурированные_данные.csv', 'a', newline='') as csvfile:
            writer  = csv.writer(csvfile, delimiter=';',quotechar='"', quoting=csv.QUOTE_MINIMAL)
            #writer.writerow(['тип вагона', 'код груза', 'станция отправления', 'станция назначения', 'тариф', 'guid'])
            writer.writerow([str(тип_вагона), str(код_груза), str(станция_отправления), str(станция_назначения), str(тариф), str(uniqueid)])
           
##        with open(r"C:\Users\User\Downloads\exchange.txt") as fp:
##            message = fp.read() #текстовый файл сохранять в формате анси

        str_минимальная_вагонная_норма_загрузки=""
        if str(код_груза).split(" ")[-1:][0] in минимальная_вагонная_норма_загрузки:
            str_минимальная_вагонная_норма_загрузки="<br>Минимальная вагонная норма загрузки: "+минимальная_вагонная_норма_загрузки[str(код_груза).split(" ")[-1:][0]]+" тонн"
##            print(str_минимальная_вагонная_норма_загрузки)            

        adressees=[]
##        print(str(тип_вагона))
        if str(тип_вагона)=="крытые грузовые вагоны" or str(тип_вагона)=="крытый грузовой вагон":
            adressees=[]


           #работа_с_личным_кабинетом_ржд(станция_отправления, "самур", код_груза, "Мешок, многослойный мешок 5-50 кг", "68000", тип_вагона, "Арендованный")
        elif str(тип_вагона)=="зерновоз" or str(тип_вагона)=="зерновозы":
            adressees=[]
            #работа_с_личным_кабинетом_ржд(станция_отправления, "самур", код_груза, "Насыпь", "68000", "зерновозы", "Арендованный")
        elif str(тип_вагона)=="цистерны" or str(тип_вагона)=="цистерна":
            adressees=[]
        elif str(тип_вагона)=="платформы" or str(тип_вагона)=="платформа":
            adressees=[]            
        elif str(тип_вагона)=="полувагоны" or str(тип_вагона)=="полувагон":
            adressees=[]            
            #работа_с_личным_кабинетом_ржд(станция_отправления, "самур", код_груза, "Налив", "68000", "цистерны", "Арендованный")
        else:
            print('неправильно указан тип вагона')
            return { "status":"exception", "guid": uniqueid, "description":"неправильно указан тип вагона"}


                
        for emadress in  adressees:
            background_tasks.add_task(sentHTMLmessageWithAttachments,
                                      to_address=emadress,
                                      subject='дать комплексную ставку',
                                      HTMLBody="Уважаемые господа,<br><br>"+\
                                      "ООО «» просит Вас сообщить комплексную ставку* на перевозку:<br><br>"+\
                                      "Станция отправления: "+str(станция_отправления)+\
                                      " <br>Станция назначения: "+str(станция_назначения)+\
                                      "<br>Код груза: "+str(код_груза)+\
                                      "<br>Тип вагона: "+str(тип_вагона)+\
                                      str_минимальная_вагонная_норма_загрузки+\
                                      "<br><br>* Ставку оперирования просим указать полностью до станции назначения,<br> а гружёный тариф "+str(тариф)+"<br><br>--<br>С уважением,<br>ген. директор ООО «»<br>ович <br>.ru/ <br>+7 <br>+7 <br>+7  (факс)<br><br>ИНН <br><p> <font color='white'>"+str(uniqueid)+"</font></p>", to_name='')        
        print("===========================Запрос обработан нормально==============================\n")
        return { "status":"ok", "guid": uniqueid, "message": "Messages will be sent in the background"}
    except Exception:
        import traceback
        import sys
        print(traceback.format_exc())
        print(sys.exc_info()[2])
        print("===========================Запрос не обработан==============================\n")
        return { "status":"exception", "guid": uniqueid}
    
    


@app.get("/данные_для_подписания_контракта/")
def данные_для_подписания_контракта(полное_наименование: str, сокращенное_наименование: str, наименование_на_английском: str, вид_деятельности: str, телефон: str, факс: str, электронная_почта: str, инн: str, кпп: str, юридический_адрес: str, почтовый_адрес: str, валюта_платежа: str, банковские_реквизиты_банк: str, банковские_реквизиты_бик: str, банковские_реквизиты_расчётный_счёт: str, банковские_реквизиты_корреспондентский_счёт: str, руководитель_ф_и_о_: str, подписант_ф_и_о_: str, подписант_ф_и_о__в_родительном_падеже: str, подписант_должность: str, подписант_должность_в_родительном_падеже: str, подписант_документ_основание: str):
    try:
        uniqueid=uuid.uuid4()
        return { "status":"ok", "guid": uniqueid}
    except:
        return { "status":"exception", "guid": uniqueid}

@app.get("/преамбула_простого_договора/")
def преамбула_простого_договора(инн_продавца: str, инн_покупателя: str):
    try:
        uniqueid=uuid.uuid4()
        return { "status":"ok", "text":str(создание_простого_договора(инн_продавца, инн_покупателя)), "guid": uniqueid}
    except:
        return { "status":"exception", "guid": uniqueid}
    

print("==============================Server started==============================")
print("====Читай документацию по адресу           http://127.0.0.1:8000/docs#/default       ======")



