import requests
import time
import io
import  RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep
from subprocess import call 


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(16,GPIO.IN)     

from config import TELEGRAM_SEND_MESSAGE_URL



class TelegramBot:       
        
    

  
    def __init__(self):
           

        self.chat_id = None
        self.text = None
        self.first_name = None
        """self.last_name = None"""


    def parse_webhook_data(self, data):
        

        message = data['message']

        self.chat_id = 1148706521
        self.incoming_message_text = message['text'].lower()
        self.first_name = message['from']['first_name']
        """self.last_name = message['from']['last_name']"""


    def action(self):
       

        success = None
        camera = PiCamera()

        if self.incoming_message_text == '/hello':
                for x in range(1):
                    self.outgoing_message_text = "Hello {}".format(self.first_name)
                    success = self.send_message()
                    break
            
      
        while True:
                i=GPIO.input(16)
                if i==0:           
                    for x in range(1):
                        print("Intruder detected")                        
                        self.outgoing_message_text = "Hello {} there is an intruder at your place".format(self.first_name)
                        success = self.send_message()
                        camera.capture('/home/pi/Desktop/image.jpg')
                        success = self.sendImage() 
                        camera.close()                       
                        success = self.takeVideo()
                        success = self.sendVideo()
                        GPIO.output(11, 1)
                        break                    
                
        return success       
   
        
    def send_message(self):
       

        res = requests.get(TELEGRAM_SEND_MESSAGE_URL.format(self.chat_id, self.outgoing_message_text))

        return True if res.status_code == 200 else False
        
        
    def sendImage(self):
        url = "https://api.telegram.org/bot1248764562:AAEGDQa5SuMASOg1ZLct15c5JZ8mCD2ZWJk/sendPhoto";
        files = {'photo': open('/home/pi/Desktop/image.jpg', 'rb')}
        data = {'chat_id' : self.chat_id}
        r= requests.post(url, files=files, data=data)
        print(r.status_code, r.reason, r.content)
        return True
        
    def sendVideo(self):
        url = "https://api.telegram.org/bot1248764562:AAEGDQa5SuMASOg1ZLct15c5JZ8mCD2ZWJk/sendVideo";
        files = {'video': open('/home/pi/Desktop/video.h264', 'rb')}
        data = {'chat_id' : self.chat_id}
        r= requests.post(url, files=files, data=data)
        print(r.status_code, r.reason, r.content)
        break
        return True      
        
    def takeVideo(self):
        while True:
            camera = PiCamera()
            camera.start_preview()
            camera.start_recording('/home/pi/Desktop/video.h264')
            sleep(1)
            camera.stop_recording()
            camera.stop_preview()
            camera.close()
            break
            return True
   

    @staticmethod
    def init_webhook(url):        

        requests.get(url)




