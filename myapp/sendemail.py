import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendthai(sendto,subj="ทดสอบส่งเมลลล์",detail="สวัสดี!\nคุณสบายดีไหม?\n"):

	myemail = 'ds42713@gmail.com'
	mypassword = "Golf42713129"
	receiver = sendto

	msg = MIMEMultipart('alternative')
	msg['Subject'] = subj
	msg['From'] = 'Admin mygameshop' 
	msg['To'] = receiver
	text = detail

	part1 = MIMEText(text, 'plain')
	msg.attach(part1)

	s = smtplib.SMTP('smtp.gmail.com:587')
	s.ehlo()
	s.starttls()

	s.login(myemail, mypassword)
	s.sendmail(myemail, receiver.split(','), msg.as_string())
	s.quit()


###########Start sending#############
## subject = 'ยืนยันการสมัคร My Game Shop'
## newmenber_name = ' โอ'
## content = '''สมัครสมาชิค My Game Shop เรียบร้อย กรุณายืนยัน email'''
## link = 'http://mygameshop.com'
## msg = ' สวัสดีคุณ {} \n\n {} Link : {}'.format(newmenber_name,content,link)

## sendthai('ds42713@gmail.com',subject,msg)

# หากต้องการส่งหลายคนสามารถใส่คอมม่าใน string ได้เลย เช่น 'loongTu1@gmail.com,loongTu2@gmail.com'


'''
-------------------------
ตั้งค่าให้เป็นสีเขียวก่อนส่ง แล้วลองรีเฟรชดู ( on )
https://myaccount.google.com/lesssecureapps
'''