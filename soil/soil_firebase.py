import serial
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import smtplib
from email.message import EmailMessage
import time


def send_mail(msg__):
	email_address = "muskannayani1707@gmail.com"
	email_password = "sjmpwylnfizhrstt"
	
	# create email
	msg = EmailMessage()
	msg['Subject'] = "Data"
	msg['From'] = email_address
	msg['To'] = "muskannayani8@gmail.com"
	msg.set_content(msg__)
	
	# send email
	count=0
	count=int(count)
	with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
		smtp.login(email_address, email_password)
		smtp.send_message(msg)
	
	time.sleep(3600)


cred = credentials.Certificate('C:\\Users\\Muskan\\Desktop\\IBM\\soil\\credit.json')
firebase_admin.initialize_app(cred, {
	'databaseURL': 'https://sensor-data-790b2-default-rtdb.firebaseio.com/'
})
ref = db.reference('/data')


ser = serial.Serial('COM5', 9600)

while True:
	line = ser.readline().decode('utf-8').rstrip()
	json_data = {
		'temperature': line.split('-')[0],
		'humadity': line.split('-')[1],
		'soilMoisture': line.split('-')[2]
	}
	ref.set(json_data)
	data = ref.get()
	
	print(data)
	if data !="":
		break
	# send_mail('Your distance is less then 20. Current distance is '+json_data['temperature'] +json_data['humadity']+json_data['soilMoisture'])
	# count=count+1
	# print(count)
	# if count>0:
	# 	break
	
send_mail('your data is '+json_data['temperature'] +json_data['humadity']+json_data['soilMoisture'])
ser.close()
