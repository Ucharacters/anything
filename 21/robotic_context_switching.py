#python -m pip install watchdog
from watchdog.utils.dirsnapshot import DirectorySnapshot
from watchdog.utils.dirsnapshot import DirectorySnapshotDiff
import sched
import time
import os
import cv2
import sys
import uuid
import subprocess
#pip install --user pytesseract
import pytesseract
from time import localtime, strftime, monotonic
import random
import pickle
import speech_recognition as sr

##from send_to_telegram import send_to_telegram
##from send_to_telegram import download_file_from_telegram
#===
import json
import msvcrt
import urllib.request
import urllib.parse
#===
from text_mining_toolbox2 import getURLs
from text_mining_toolbox2 import getEmails

import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler,FileSystemEventHandler

class MyCustomEventHandler(FileSystemEventHandler):
       def on_any_event(self, event):
              pass
              #print (event.event_type, event.src_path)

       def on_closed(self, event):
              pass
               #print (event.event_type, event.src_path)
        
       def on_modified(self, event):
              pass
               #print (event.event_type, event.src_path)

       def on_deleted(self, event):
              pass
               #print (event.event_type, event.src_path)

       def on_moved(self, event):
              pass
               #print (event.event_type, event.src_path)

       def on_created(self, event):
              #print (event.event_type, event.src_path)
              filename, file_extension = os.path.splitext(event.src_path)
              print(strftime("%Y-%m-%dT%H:%M:%SZ", localtime()) +" "+"новый файл="+filename+file_extension)
              if file_extension==".jpg" or file_extension==".jpeg":
                     unique_name=str(uuid.uuid4())+".jpg"
                     os.rename(filename+file_extension, unique_name)
                     SafeMode("обработчик OCR", call_ocr_routine(unique_name))
              if file_extension==".pdf":
                     SafeMode("обработчик PDF", call_pdf_routine(filename+file_extension))
              if file_extension==".json":
                     with open(filename+file_extension, 'rb') as in_file:
                            file_contents=in_file.read().decode("utf-8")
                            #print("file_contents =" +str(file_contents))
                            is_email=getEmails(file_contents)
                            if len(is_email)>0:
                                   if len(file_contents)==len(is_email[0]):
                                          #print("строгое совпадение =" +str(is_email[0]))
                                          SafeMode("обработчик карты партнёра", call_отправить_карту_партнёра(is_email[0]))
                                          return
                     SafeMode("обработчик контекста робота", call_context_switching(file_contents))
                     SafeMode("обработчик JSON", call_json_routine(filename+file_extension))
              if file_extension==".html":
                     SafeMode("обработчик HTML", call_html_routine(filename+file_extension))        
              if file_extension==".xlsx" or file_extension==".xls":
                     SafeMode("обработчик XLS", call_xls_routine(filename+file_extension))
              if file_extension==".docx" or file_extension==".doc":
                     SafeMode("обработчик DOC", call_doc_routine(filename+file_extension))
              if file_extension==".opus" or file_extension==".ogg" or file_extension==".oga":
                     SafeMode("обработчик opus -> wav", call_process_audio(filename+file_extension))
              if file_extension==".wav":
                     SafeMode("обработчик Voice Notes", call_voice_notes_routine(filename+file_extension))                
              else:
                     SafeMode("обработчик контекста робота", call_context_switching(keeper.utterance))
#class MyCustomEventHandler


path = "V:/" 
event_handler = MyCustomEventHandler()
observer = Observer()
observer.schedule(event_handler, path, recursive=True)



        

#===

def rpa_eats_ai_for_breakfast_pickled(sampletext):
    loaded_model = pickle.load(open("model.pkl","rb"))
    loaded_vectorizer = pickle.load(open("vectorizer.pkl","rb"))
    
    actions = {  "1": "запрос_ставки_жд_тарифа",
                       "2": "сделай_перевод_с_английского",
                       "3": "напиши_письмо_на_русском",
                       "4": "напиши_письмо_на_английском",
                       "5": "найди_товар" }
        
    action_name = actions[str(loaded_model.predict(loaded_vectorizer.transform([sampletext]).toarray())[0])]
    return action_name



class KeeperObject():
    def __init__(self):
        self.utterance=""
        self.utterance_time=0
        self.context=""

keeper=KeeperObject()

def SafeMode(name, func):
    start = time.time()       
    print(strftime("%Y-%m-%dT%H:%M:%SZ", localtime()) +" "+name +"<=начало")
    try:
        func
        #return
    except Exception as e:
        print(" "*4+"error:", e)
        print(strftime("%Y-%m-%dT%H:%M:%SZ", localtime()) +" "+name +"<=ошибка выполнения !"+str(sys.exc_info()[1]))
        pass
    finally:
        print(strftime("%Y-%m-%dT%H:%M:%SZ", localtime()) +" "+name +"<=конец ("+str(time.time()-start  )[:6]+")")

def call_html_routine(filename):
    batchfile = os.path.join(path, filename)
    subprocess.call(['cmd', '/c', r"C:\Program Files\Google\Chrome\Application\chrome.exe", os.path.realpath(batchfile)])

def call_json_routine(filename):
    batchfile = os.path.join(path, filename)
    subprocess.call(['cmd', '/c', r"C:\Program Files\Google\Chrome\Application\chrome.exe", os.path.realpath(batchfile)])

def call_pdf_routine(filename):
    batchfile = os.path.join(path, filename)
    subprocess.call(['cmd', '/c', os.path.realpath(batchfile)])

def call_xls_routine(filename):
    batchfile = os.path.join(path, filename)
    subprocess.call(['cmd', '/c', os.path.realpath(batchfile)])

def call_doc_routine(filename):
    batchfile = os.path.join(path, filename)
    subprocess.call(['cmd', '/c', os.path.realpath(batchfile)])

def call_vbs_routine(filename):
    batchfile = os.path.join(path, filename)
    subprocess.call(['cmd', '/c', 'create pie chart.vbs'])

def call_ocr_routine(filename):
    custom_oem_psm_config = r'--oem 3 --psm 6'
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'#C:\Program Files\Tesseract-OCR
    #в названии файла не должно быть русских букв - Tesseract выдаст ошибку <class 'NoneType'> на print(type(img))
    img = cv2.imread(filename)
    if img is not None:
        #cv2.imshow('img', img)
        #cv2.waitKey(0)
        #print('================начинаем обработку========')
        print('===================rus===================')
        str_rus=pytesseract.image_to_string(img, lang='rus', config=custom_oem_psm_config)
        print(str_rus)
        print('===================rus===================')
        print('===================eng===================')
        str_eng=pytesseract.image_to_string(img, lang='eng', config=custom_oem_psm_config)
        print(str_eng)
        print('===================eng===================')
        with open(path+str(uuid.uuid4())+".html", 'wb') as new_file:
               new_file.write(str("<html><head></head><body><br><div style='font-family:Arial'>"+\
                                  "<table border='1' width='100%'><tr><td>"+str(str_rus)+"</td><td>"+str(str_eng)+"</td></tr></table>"+\
                                  "</div><br><br><iframe width='100%' height='500' frameborder='0' src = 'http://127.0.0.1:8000/docs#/default/'><br></iframe></html></body>").encode("utf-8"))
        if len(str_rus)>0:
              keeper.utterance=str_rus
              keeper.utterance_time=time.time()                    

    
def call_process_audio(filename):
    fullfilename, file_extension = os.path.splitext(filename)
    if subprocess.call(['cmd', '/c', r"C:\Users\User\Downloads\opus-tools-0.2-opus-1.3\opusdec.exe --quiet --rate 16000 --gain 5 --no-dither  --force-wav ", filename,filename[:-len(file_extension)]+".wav"]) !=0:
        print("error converting subprocess.call")
        #exit()
                   
def call_voice_notes_routine(filename):
       try:
              harvard = sr.AudioFile(filename)
              r = sr.Recognizer ()
              with harvard as source:
                     audio = r.record(source)

              thisistext_ru = r.recognize_google(audio,language='ru-RU')
              print('===================rus==================='+filename[-11:])
              print(thisistext_ru) #, show_all=True
              print('===================rus===================')
              thisistext_en = r.recognize_google(audio,language='en-EN')
              print('===================eng==================='+filename[-11:])
              print(thisistext_en) #, show_all=True
              print('===================eng===================')
              if len(thisistext_ru)>0:
                     keeper.utterance=thisistext_ru
                     keeper.utterance_time=time.time()       
              if len(thisistext_ru)==0:
                     thisistext_ru="-"
              with open(path+str(uuid.uuid4())+".html", 'wb') as new_file:
                     new_file.write(str("<html><head></head><body><br><div style='font-family:Arial'>"+\
                                                 "<table border='1' width='100%'><tr><td>"+str(thisistext_ru)+"</td><td>"+str(thisistext_en)+"</td></tr></table>"+\
                                                 "</div><button>"+str(rpa_eats_ai_for_breakfast_pickled(thisistext_ru))+"</button><br><br><iframe width='100%' height='500' frameborder='0' src = 'http://127.0.0.1:8000/docs#/default/'><br></iframe></html></body>").encode("utf-8"))

              SafeMode("обработчик контекста робота", call_context_switching(keeper.utterance))

       except:
              print("call_voice_notes_routine("+filename+") crashed"+str(sys.exc_info()[1]))
#def call_voice_notes_routine(filename):

def call_отправить_карту_партнёра(emailname):
       url="https://e.mail.ru/compose?To="+str(emailname.strip())#"+'&subject=карта партнёра «»"'
       subprocess.call(['cmd', '/c', r"C:\Program Files\Google\Chrome\Application\chrome.exe", url])
       import win32com.client
       import win32file
       import pythoncom

       # Отправка сообщения
       def sentHTMLmessageWithAttachments(to_address, subject, HTMLBody, to_name=''):
           # инициализируем объект outlook
           pythoncom.CoInitialize()
           objOutlook = win32com.client.Dispatch("Outlook.Application")
           objMail = objOutlook.CreateItem(0)
           objMail.to = to_address
           objMail.Subject = subject
           objMail.Body = "данные отправляемые"
           objMail.HTMLBody = HTMLBody#'<h2>HTML Message body</h2>' #this field is optional
           attachment  = r"I:\Desktop\Р.docx"
           objMail.Attachments.Add(attachment)
           objMail.Display() #    objMail.Send()

       sentHTMLmessageWithAttachments(str(emailname.strip()), "карта партнёра «»","")           

import nltk
import random
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer

BOT_CONFIG = {'intents':  ''}
texts = []
intent_names = []

for intent, intent_data in BOT_CONFIG['intents'].items():
    for example in intent_data['examples']:
        texts.append(example)
        intent_names.append(intent)

vectorizer = TfidfVectorizer(ngram_range=(2, 5), analyzer='char')
X = vectorizer.fit_transform(texts)
clf = LinearSVC()
clf.fit(X, intent_names)


def classify_intent(replica):
    intent = clf.predict(vectorizer.transform([replica]))[0]

    examples = BOT_CONFIG['intents'][intent]['examples']
    for example in examples:
        example = clear_text(example)
        if len(example) > 0:
            if abs(len(example) - len(replica)) / len(example) < 0.5:
                distance = nltk.edit_distance(replica, example)
                if len(example) and distance / len(example) < 0.5:
                    return intent

def get_answer_by_intent(intent):
    if intent in BOT_CONFIG['intents']:
        responses = BOT_CONFIG['intents'][intent]['responses']
        return random.choice(responses)


state_machine_processor_bot_metrics = {'intents': 0, 'generative': 0, 'stubs': 0}

def state_machine_processor_bot(replica):
    # NLU
    intent = classify_intent(replica)
    # правила
    if intent:
        answer = get_answer_by_intent(intent)
        if answer:
            state_machine_processor_bot_metrics['intents'] += 1
            return answer



    # заглушка
    answer = get_stub()
    state_machine_processor_bot_metrics['stubs'] += 1
    return [intent, answer]

def call_context_switching(sampletext):
       import nltk
       print(" "*4+"<="+str(sampletext))  
       sentences = [[word.lower() for word in nltk.word_tokenize(sentence)] for sentence in nltk.sent_tokenize(str(sampletext)) ]
       for sentence in range(0, len(sentences),5):
              print(" "*4+"=>"+" ".join(sentences[sentence]))
              keeper.context=state_machine_processor_bot(" ".join(sentences[sentence]))[0]
              print(" "*4+"<="+str(keeper.context))
              print(" "*8+"=>GET")              

##              #=================send to server=====================
##              import http.client
##              import mimetypes
####              import urllib.parse
####
####              def urlencode(str):
####                     return urllib.parse.quote(str)
####              def urldecode(str):
####                     return urllib.parse.unquote(str)
##              
##              import json
##              import msvcrt
##              import uuid       
##              import urllib.request
##              import urllib.parse
##              url = "http://127.0.0.1:5000"
##
##              def GetDataFromURL(site, method, payload):
##                     params = urllib.parse.urlencode(payload)
##                     if method=="GET":
##                            url = site+"?"+params
##                            with urllib.request.urlopen(url) as f:
##                                   return str(f.read().decode('utf-8')) #f.read().decode('utf-8')
##                     if method=="POST":
##                            params = params.encode('utf-8')
##                            req = urllib.request.Request(site,params )
##                            print(req)
##                            # Customize the header value:
##                            req.add_header('Content-Type', 'application/json')
##                            with urllib.request.urlopen(req) as response:
##                                   #print(json.load(response)['with']['thing'])
##                                   #print(response)
##                                   #print("GetDataFromURL <="+json.dumps(json.load(response)))
##                                   return json.load(response)
##
##              print(" "*8+"<="+GetDataFromURL("http://127.0.0.1:5000/utterances",
##                                       "GET",
##                                       {'utterance': " ".join(sentences[sentence]),
##                                        "intent":keeper.context,
##                                        'answer': state_machine_processor_bot(" ".join(sentences[sentence]))[1],
##                                       "guid": uuid.uuid4()
##                                        }))              
##              #=================send to server=====================
              
       if (time.time() - keeper.utterance_time) > 120:
              keeper.context=""
       print(strftime("%Y-%m-%dT%H:%M:%SZ", localtime()) +" contextname="+str(keeper.context)+", context age="+str(time.time() - keeper.utterance_time) )
        

observer.start()
print('================робот начал цикл=================')    
try:
    while True:
        time.sleep(5)
finally:
    observer.stop()
    observer.join()
    print('================робот закончил работать==========')    

#Different names for reusable RPA plugins include app, bot, solution, component, dashboard, workflow, skill, connector, asset, snippet, component, activity or plugin.
