## generateascii รหัสพิเศษ confirm email //ประยุคทำรหัสส่วนลด
import random
def GenerateTokentest(domain='http://localhost:8000/confirm/'):
    allcher = [chr(i) for i in range(65,91)]
    allcher.extend([chr(i) for i in range(97,123)])
    allcher.extend([str(i) for i in range(10)])
    emailtoken = ''
    for i in range(40):
        emailtoken += random.choice(allcher)

    url = domain + emailtoken
    return url

    

'''
allcher = []
for i in range(65,91):
    allcher.append(chr(i))
for i in range(97,123):
    allcher.append(chr(i))
for i in range(10):
    allcher.append(str(i))
print(allcher)
print("------------------------------------")
allcher2 = [chr(i) for i in range(65,91)]
allcher2.extend(chr(i) for i in range(97,123))
allcher2.extend(str(i) for i in range(10))
print(allcher2)
print("------------------------------------")
import string
print(list(string.ascii_letters))
'''
