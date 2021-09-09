from django.shortcuts import render ,redirect
from django.http import HttpResponse
# httpResponse คือ ฟังชั่นสำหรับทำให้โชว์ข้อความหน้าเว็ปได้
from django.core.files.storage import FileSystemStorage
# FileSystemStorage อัพโหลดตัวไฟล์ไปเก็บไว้ในโปรเจค
from django.contrib.auth.decorators import login_required
# เช็คlogin
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,login
from datetime import datetime
from django.core.paginator import Paginator 
#สำหรับทำสินค้าหลายหน้า


######### API  #######
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
#######################

############# admin ##########
def CheckNotAdmin(request):
    if request.user.profile.usertype != 'admin':
        return True
    else:
        return False

#############################

###### ไฟล์ส่งemail #####
from .sendemail import *

####### send email test ########
def EmailConfirm(email,name,token):
    subject = 'ยืนยันการสมัคร My Game Shop'
    newmenber_name = name
    content = '''สมัครสมาชิก My Game Shop เรียบร้อย กรุณายืนยัน email'''
    ##### generateascii รหัสพิเศษ confirm email#####
    #link = 'http://mygameshop.com/confirm/sadl13k1as231dla34'
    link = token

    msg = ' สวัสดีคุณ {} \n\n {} Link : {}'.format(newmenber_name,content,link)

    sendthai(email,subject,msg)
    #######################
######################

##### generateascii รหัสพิเศษ confirm email #####
import random
def GenerateToken(domain='http://localhost:8000/confirm/'):
    allcher = [chr(i) for i in range(65,91)]
    allcher.extend([chr(i) for i in range(97,123)])
    allcher.extend([str(i) for i in range(10)])
    emailtoken = ''
    for i in range(40):
        emailtoken += random.choice(allcher)

    url = domain + emailtoken
    return (url,emailtoken)

def Confirm(request,token): #confirm email
    try:
        check = VerifyEmail.objects.get(token=token)
        status = 'found'
        check.approved = True
        check.save()
        context = {'status':status,'username':check.user.username,'name':check.user.first_name}
    except:
        status = 'notfound'
        context = {'status':status}
     
    return render(request, 'myapp/confirm.html',context)
##########################

###### LINE NOTIFY #####
from songline import Sendline
token = 'x2DZaxIvgJyifTCqFj5fVAtaied2NtGZk20tesyY3Wo'
messenger = Sendline(token)
########################


########### markdown  ##############
import markdown as md

def TestMd(request):
    text = '[Test Header](www.youtube.com)'
    print(md.markdown(text, extensions=['markdown.extensions.fenced_code']))
    context = {'text':text}
    return render(request, 'myapp/testmd.html', context)

#############################


def Home(request):
    product = Allproduct.objects.all().order_by('id')[:3] 
    #ดึงข้อมูลลงตัวแปร .order_by('id') คือเรียงตามid .reverse()คือย้อนกลับในที่นี้คือid
    preorder = Allproduct.objects.filter(quantity__lte=0)
    #เชคค่าpreorder ว่ามีค่าเท่าไร
    #quantity__lte=0 หาค่าที่ quantity <= 0 // lte คือ <=
    #quantity__gt=0 หาค่าที่ quantity > 0 // gt คือ >
    #quantity__gte=10 หาค่าที่ quantity >= 10 // gt คือ >=

    context = {'product':product,'preorder':preorder}

    return render(request, 'myapp/home.html' ,context)

    #return HttpResponse('<h1>Hello world</h1>') 

def About(request):
    return render(request, 'myapp/about.html' )

def Contact(request):
    return render(request, 'myapp/contact.html')

def Playstation5(request):
    return render(request, 'myapp/playstation5.html')

def AddProduct(request):

    category = Category.objects.all()

    if request.user.profile.usertype != 'admin':
        return redirect('home-page')

    if request.method == 'POST': #and request.FILES['imageupload']: 
        # request.FILES['imageupload'] เช็คว่า อัพโหลดimageไหม
        data = request.POST.copy()
        name = data.get('name')
        price = data.get('price')
        detail = data.get('detail')
        imageurl = data.get('imageurl')
        quantity = data.get('quantity')
        unit = data.get('unit')

        cat = data.get('category')
        cat = Category.objects.get(catname=cat)

        new = Allproduct()
        new.name = name
        new.price = price
        new.detail = detail
        new.imageurl = imageurl
        new.quantity = quantity
        new.unit = unit
        
        # ไม่สามารถsaveได้เลย
        new.catname = cat  

        ########## save image ################
        try:
            file_image = request.FILES['imageupload']
            file_image_name = request.FILES['imageupload'].name.replace(' ','')
            fs = FileSystemStorage()
            filename = fs.save(file_image_name,file_image)
            upload_file_url = fs.url(filename)
            new.image = upload_file_url[6:]  #[6:] 6 = media เพื่อให้ได้ชื่อไฟล์รูปอย่างเดียว
        except:
            new.image = '/default-image.png' #ถ้าไม่มีการอัพโหลดจะดึงค่านี้มาใช้งาน
        ###################################
        
        new.save() 

    context = {'category':category}
    return render(request, 'myapp/addproduct.html',context)

def Product(request):
    
    product = Allproduct.objects.all().order_by('id').reverse() 
    #ดึงข้อมูลลงตัวแปร .order_by('id') คือเรียงตามid .reverse()คือย้อนกลับในที่นี้คือid

    #ทำรายการหลายหน้า โดยให้แสดงผลจำนวนนึง
    paginator = Paginator(product,3) # 1หน้า แสดง3รายการ
    page = request.GET.get('page') # http://localhost:8000/allproduct/?page=2 
    #เอาค่า จาก?page=2 คือ2
    product = paginator.get_page(page) #มาเฉพาะหน้าที่2จากตัวแปรpage

    context = {'product':product}
    return render(request, 'myapp/allproduct.html',context)

def ProductCategory(request,code):
    select = Category.objects.get(id=code)
    product = Allproduct.objects.filter(catname=select).order_by('id').reverse() 
    #ดึงข้อมูลลงตัวแปร .order_by('id') คือเรียงตามid .reverse()คือย้อนกลับในที่นี้คือid

    #ทำรายการหลายหน้า โดยให้แสดงผลจำนวนนึง
    paginator = Paginator(product,3) # 1หน้า แสดง3รายการ
    page = request.GET.get('page') # http://localhost:8000/allproduct/?page=2 
    #เอาค่า จาก?page=2 คือ2
    product = paginator.get_page(page) #มาเฉพาะหน้าที่2จากตัวแปรpage

    context = {'product':product,'catname':select.catname}
    return render(request, 'myapp/allproductcat.html',context)

def Register(request):
    if request.method == 'POST':
        data = request.POST.copy()
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')
        
        newuser = User()
        newuser.username = email
        newuser.email = email
        newuser.first_name = first_name
        newuser.last_name = last_name
        newuser.set_password(password) #password ต้องใช้ set
        newuser.save()

        profile = Profile()
        profile.user = User.objects.get(username=email) # User มาจากไฟล์ models.py
        profile.save()

       
        token,token_code = GenerateToken()
        EmailConfirm(email,first_name,token)
        getuser = User.objects.get(username=email)
        addverify = VerifyEmail()
        addverify.user = getuser
        addverify.token = token_code
        addverify.save()

        user = authenticate(username=email ,password=password)
        login(request,user)
        #from django.contrib.auth import authenticate ,login
        #auto Login

    return render(request, 'myapp/register.html')
        
def AddtoCart (request ,pid):

    username = request.user.username
    user = User.objects.get(username=username)
    check = Allproduct.objects.get(id=pid)

    try: # เวลาที่ตัวสินค้ามีซ้ำ
        newcart = Cart.objects.get(user=user,productid=str(pid)) #Product check
        newquan = newcart.quantity + 1
        newcart.quantity = newquan
        calculate = newcart.price * newquan
        newcart.total = calculate
        
        newcart.save()

        count = Cart.objects.filter(user=user)
        count = sum([ c.quantity for c in count])
        updatequan = Profile.objects.get(user=user)
        updatequan.cartquan = count
        updatequan.save()
        return redirect('allproduct-page')

    except: # เวลาที่ตัวสินค้ามี ไม่ ซ้ำ
        newcart = Cart()
        newcart.user = user
        newcart.productid = pid
        newcart.productname = check.name
        newcart.price = int(check.price) #แปลงเป็นint
        newcart.quantity = 1
        calculate = int(check.price) * 1
        newcart.total = calculate

        newcart.save()

        count = Cart.objects.filter(user=user)
        count = sum([ c.quantity for c in count])
        updatequan = Profile.objects.get(user=user)
        updatequan.cartquan = count
        updatequan.save()
        return redirect('allproduct-page')

def MyCart(request):
    
    username = request.user.username
    user = User.objects.get(username=username)
    context = {}
    if request.method == 'POST':
        #ใช้สำหรับการลบค่า
        data = request.POST.copy()
        productid = data.get('productid') # mycart.html ตรงname
        item = Cart.objects.get(user=user,productid=productid)
        item.delete()
        context['status'] = 'delete'

        #updatequan คือจำนวนสินค้ารวมทั้งหมด
        count = Cart.objects.filter(user=user)
        count = sum([ c.quantity for c in count])
        updatequan = Profile.objects.get(user=user)
        updatequan.cartquan = count
        updatequan.save()


    mycart = Cart.objects.filter(user=user)
    count = sum([ c.quantity for c in mycart])
    total = sum([ c.total for c in mycart])


    context['mycart'] = mycart
    context['count'] = count
    context['total'] = total
    return render(request, 'myapp/mycart.html', context)

def MyCartEdit(request):   
    # เชคว่า userไหนเข้าระบบ
    username = request.user.username
    user = User.objects.get(username=username)
    context = {}

    if request.method == 'POST':
        data = request.POST.copy()

        if data.get('clear') == 'clear': # ปุ่มลบทั้งหมด
            Cart.objects.filter(user=user).delete()
            updatequan = Profile.objects.get(user=user)
            updatequan.cartquan = 0
            updatequan.save()
            
            return redirect('mycart-page')
        
        editlist = []
        for k,v in data.items(): # mycartedit เก็บค่ามา2ตัว คือ k=pd_{{pd.productid}} v={{pd.quantity}}
            
            if k[:2] == 'pd': # เชค2ตัวแรกว่าเป็น pd รึป่าว จากpd_{{pd.productid}} mycart
                pid = int(k.split('_')[1]) # _ ไว้ใช้แยกค่าออกจากกัน
                dt = [pid,int(v)]
                editlist.append(dt)
      #  print('EDITLIST :',editlist) [[9,10],[3,8]] ตัวแรกคือ productid ตัวหลังคือจำนวน quan

        for ed in editlist:
            edit = Cart.objects.get(productid=ed[0],user=user) # นำ [pid,int(v)] มาใช้เฉพาะตัวแรก pid //userเพื่อยืนยันตน
            edit.quantity = ed[1] #ตัวหลังคือจำนวน quan
            calculate = edit.price * edit.quantity #edit.quantity = ed[1] คำนวนราคาใหม่
            edit.total = calculate 
            edit.save()

        count = Cart.objects.filter(user=user)
        count = sum([ c.quantity for c in count])
        updatequan = Profile.objects.get(user=user)
        updatequan.cartquan = count
        updatequan.save()
        
        return redirect('mycart-page')

    mycart = Cart.objects.filter(user=user)
    context['mycart'] = mycart

    return render(request, 'myapp/mycartedit.html', context)

def Checkout(request):
    username = request.user.username
    user = User.objects.get(username=username)
    if request.method == 'POST':
        data = request.POST.copy()
        name = data.get('name')
        tel = data.get('tel')
        address = data.get('address')
        shipping = data.get('shipping')
        payment = data.get('payment')
        other = data.get('other')
        page = data.get('page')

        if page == 'information': #ส่งข้อมูลจาก checkout1
            context = {}
            context['name'] = name
            context['tel'] = tel
            context['address'] = address
            context['shipping'] = shipping
            context['payment'] = payment
            context['other'] = other

            mycart = Cart.objects.filter(user=user)
            count = sum([ c.quantity for c in mycart])
            total = sum([ c.total for c in mycart])

            context['mycart'] = mycart
            context['count'] = count
            context['total'] = total
            return render(request, 'myapp/checkout2.html', context)

        if page == 'confirm':
            print('confirm')
            mycart = Cart.objects.filter(user=user)
            mid = str(user.id).zfill(3)
            dt = datetime.now().strftime('%Y%m%d%H%M%S') # www.strftime.org
            orderid = 'OD' + mid + dt
           
            productorder = ''
            producttotal = 0


            for pd in mycart:
                order = OrderList()
                order.orderid = orderid
                order.productid = pd.productid
                order.productname = pd.productname
                order.price = pd.price
                order.quantity = pd.quantity
                order.total = pd.total
                order.save()

                productorder = productorder + '- {}\n'.format(pd.productname) #รายการสินค้า
                producttotal += pd.total

            ####### send LINE ######
            texttoline = 'OrderID : {}\n---\nรายการสินค้า\n{}ยอดรวม : {:,.2f} บาท\n({})'.format(orderid,productorder,producttotal,name)
            if producttotal > 10000:
                messenger.sticker(14,1,texttoline)
            else:
                messenger.sendtext(texttoline)
            #################

            odp = OrderPending()
            odp.orderid = orderid
            odp.user = user
            odp.name = name
            odp.tel = tel
            odp.address = address 
            odp.shipping = shipping
            odp.payment = payment
            odp.other = other
            odp.save()

            Cart.objects.filter(user=user).delete()
            updatequan = Profile.objects.get(user=user)
            updatequan.cartquan = 0
            updatequan.save()
            return redirect('mycart-page')

    return render(request, 'myapp/checkout1.html')

def OrderListPage(request):
    username = request.user.username
    user = User.objects.get(username=username)
    context = {}

    order = OrderPending.objects.filter(user=user)

    for od in order:
        orderid = od.orderid
        odlist = OrderList.objects.filter(orderid=orderid)
        '''
        odlist
            -object (1)
                -orderid : OD1033134
                -product : playstation5
                -total : 16900
            -object (2)
                -orderid : OD1033134
                -product : playstation4
                -total : 12900
            -object (3)
                -orderid : OD1033135
                -product : playstation5
                -total : 16900
        '''
        total = sum([ c.total for c in odlist])
        od.total = total #สร้างตัว totalจำลองเฉพาะ
        count = sum([ c.quantity for c in odlist])
        
        if od.shipping == 'ems':
            shipcost = sum([50 if i == 0 else 10 for i in range(count)]) 
        #รวมค่าส่ง ชิ้นแรก50 ชิ้นต่อไป10บาท
        else:
            shipcost = sum([30 if i == 0 else 10 for i in range(count)])
        #รวมค่าส่ง ชิ้นแรก30 ชิ้นต่อไป10บาท

        if od.payment == 'cod':
            shipcost += 20
        od.shipcost = shipcost


    context['allorder'] = order

    return render(request, 'myapp/orderlist.html',context)
 
def AllOrderListPage(request):
    context = {}

    order = OrderPending.objects.all()

    for od in order:
        orderid = od.orderid
        odlist = OrderList.objects.filter(orderid=orderid)
        total = sum([ c.total for c in odlist])
        od.total = total #สร้างตัว totalจำลองเฉพาะ
        
        count = sum([ c.quantity for c in odlist])
        
        if od.shipping == 'ems':
            shipcost = sum([50 if i == 0 else 10 for i in range(count)]) 
        #รวมค่าส่ง ชิ้นแรก50 ชิ้นต่อไป10บาท
        else:
            shipcost = sum([30 if i == 0 else 10 for i in range(count)])
        #รวมค่าส่ง ชิ้นแรก30 ชิ้นต่อไป10บาท
        if od.payment == 'cod':
            shipcost += 20
        od.shipcost = shipcost
    
    #ทำรายการหลายหน้า โดยให้แสดงผลจำนวนนึง
    paginator = Paginator(order,20) # 1หน้า แสดง20รายการ
    page = request.GET.get('page') # http://localhost:8000/allproduct/?page=2 
    #เอาค่า จาก?page=2 คือ2
    order = paginator.get_page(page) #มาเฉพาะหน้าที่2จากตัวแปรpage

    context['allorder'] = order # ใช้ชื่อ key

    return render(request, 'myapp/allorderlist.html',context)

def UploadSlip(request, orderid):

    if request.method == 'POST' and request.FILES['slip']:
        data = request.POST.copy()
        sliptime = data.get('sliptime')
        price = data.get('price')

        update = OrderPending.objects.get(orderid=orderid)
        update.sliptime = sliptime
        ########## save image ################
        file_image = request.FILES['slip']
        file_image_name = request.FILES['slip'].name.replace(' ','')
        print('FILE_IMAGE: ',file_image)
        print('IMAGE_NAME: ',file_image_name)
        fs = FileSystemStorage()
        filename = fs.save(file_image_name,file_image)
        upload_file_url = fs.url(filename)
        update.slip = upload_file_url[6:]  #[6:] 6 = media เพื่อให้ได้ชื่อไฟล์รูปอย่างเดียว
        ###################################
        
        update.save() 

    odlist = OrderList.objects.filter(orderid=orderid)
    total = sum([ c.total for c in odlist])
    oddetail = OrderPending.objects.get(orderid=orderid)
    # คำนวนค่าส่งตามประเภทการส่ง
    count = sum([ c.quantity for c in odlist])
    if oddetail.shipping == 'ems':
        shipcost = sum([50 if i == 0 else 10 for i in range(count)]) 
        #รวมค่าส่ง ชิ้นแรก50 ชิ้นต่อไป10บาท
    else:
        shipcost = sum([30 if i == 0 else 10 for i in range(count)])
        #รวมค่าส่ง ชิ้นแรก30 ชิ้นต่อไป10บาท

    if oddetail.payment == 'cod':
        shipcost += 20

    context = { 'orderid':orderid ,
                'total':total ,
                'shipcost':shipcost ,
                'grandtotal':total+shipcost ,
                'oddetail':oddetail ,
                'count':count
              }



    return render(request, 'myapp/uploadslip.html' ,context)

def UpdatePaid(request,orderid,status):

    if request.user.profile.usertype != 'admin':
        return redirect('home-page')

    order = OrderPending.objects.get(orderid=orderid)
    if status == 'confirm':
        order.paid = True
        order.confirmed = True
        odlist = OrderList.objects.filter(orderid=orderid)
        for od in odlist:
            product = Allproduct.objects.get(id=od.productid)
            product.quantity = product.quantity - od.quantity
            product.save()


    elif status == 'cancel':
        order.paid = False
        order.confirmed = False
    order.save()

    return redirect('allorderlist-page')

def UpdateTracking(request,orderid):
    if request.user.profile.usertype != 'admin':
        return redirect('home-page')


    if request.method == 'POST':
        order = OrderPending.objects.get(orderid=orderid)
        data = request.POST.copy()
        trackingnumber = data.get('trackingnumber')
        order.trackingnumber = trackingnumber
        order.save()
        return redirect('allorderlist-page')

    order = OrderPending.objects.get(orderid=orderid)
    odlist = OrderList.objects.filter(orderid=orderid)

    total = sum([ c.total for c in odlist])
    order.total = total

    count = sum([ c.quantity for c in odlist])
        
    if order.shipping == 'ems':
        shipcost = sum([50 if i == 0 else 10 for i in range(count)]) 
        #รวมค่าส่ง ชิ้นแรก50 ชิ้นต่อไป10บาท
    else:
        shipcost = sum([30 if i == 0 else 10 for i in range(count)])
        #รวมค่าส่ง ชิ้นแรก30 ชิ้นต่อไป10บาท
    if order.payment == 'cod':
        shipcost += 20
    order.shipcost = shipcost
    

    context = {'orderid':orderid 
              ,'order':order
              ,'odlist':odlist
              ,'total':total
              ,'count':count}

    return render(request, 'myapp/updatetracking.html',context)

def MyOrder(request,orderid):
    username = request.user.username
    user = User.objects.get(username=username)

    order = OrderPending.objects.get(orderid=orderid)
    #เช็คว่าเป็นของตัวเองไหม
    if user != order.user:
        return redirect('allproduct-page')

    odlist = OrderList.objects.filter(orderid=orderid)

    total = sum([ c.total for c in odlist])
    order.total = total
    count = sum([ c.quantity for c in odlist])
        
    if order.shipping == 'ems':
        shipcost = sum([50 if i == 0 else 10 for i in range(count)]) 
        #รวมค่าส่ง ชิ้นแรก50 ชิ้นต่อไป10บาท
    else:
        shipcost = sum([30 if i == 0 else 10 for i in range(count)])
        #รวมค่าส่ง ชิ้นแรก30 ชิ้นต่อไป10บาท
    if order.payment == 'cod':
        shipcost += 20
    order.shipcost = shipcost

    context = {'order':order
              ,'odlist':odlist
              ,'total':total
              ,'count':count}

    return render(request, 'myapp/myorder.html',context)
    
def PieChart(request):
    product = Allproduct.objects.all()

    pdname = []
    pdquan = []

    for pd in product[:5]:
        pdname.append(pd.name)
        pdquan.append(pd.quantity)
    
    context = {'pdname':str(pdname),'pdquan':pdquan}
    return render(request , 'myapp/graph.html' , context)

def ProductDetail(request,productid):
    product = Allproduct.objects.get(id=productid)
    context = {'product':product}
    return render(request, 'myapp/productdetail.html', context)

@login_required
def EditProduct(request,productid):

    Check = CheckNotAdmin(request) ## ส่งค่า Bool เพื่อเช็คว่าเป็นadminหรือไม่
    if Check:
        return redirect('home-page')

    product = Allproduct.objects.get(id=productid)
    category = Category.objects.all()
    
    if request.method == 'POST': #and request.FILES['imageupload']: 
        # request.FILES['imageupload'] เช็คว่า อัพโหลดimageไหม
        data = request.POST.copy()
        name = data.get('name')
        price = data.get('price')
        detail = data.get('detail')
        imageurl = data.get('imageurl')
        quantity = data.get('quantity')
        unit = data.get('unit')
        
        # ดึงMOdelsเข้ามา *** ForeignKey
        cat = data.get('category')
        cat = Category.objects.get(catname=cat)
       
        instock_check = data.get('instock')

        product.name = name
        product.price = price
        product.detail = detail
        product.imageurl = imageurl
        product.quantity = quantity
        product.unit = unit
        # ไม่สามารถsaveได้เลย
        product.catname = cat  

        # instock เอาค่ามาแปลงเป็น boolean
        if instock_check == 'instock_true':
            product.instock = True
        else:
            product.instock = False     
        

        ########## edit image ################
        print('FILE :',[request.FILES])
        if 'imageupload' in request.FILES: 
            file_image = request.FILES['imageupload']
            file_image_name = request.FILES['imageupload'].name.replace(' ','')
            print('FILE_IMAGE: ',file_image)
            print('IMAGE_NAME: ',file_image_name)
            fs = FileSystemStorage()
            filename = fs.save(file_image_name,file_image)
            upload_file_url = fs.url(filename)
            product.image = upload_file_url[6:]  #[6:] 6 = media เพื่อให้ได้ชื่อไฟล์รูปอย่างเดียว
        else:
            print('no')
        ###################################       
        product.save() 

    product = Allproduct.objects.get(id=productid)
    context = {'product':product,'category':category}
    return render(request, 'myapp/editproduct.html', context)



###### API ######

# ,​json_dumps_params={'ensure_ascii': False}
# ,​json_dumps_params={'ensure_ascii': False}

def AllproductAPI(request):
    product = Allproduct.objects.all()
    serializer = AllproductSerializer(product, many=True  ) #if product is list put (many=True)
    return JsonResponse(serializer.data, safe=False )

def ProductDetailAPI(request,pid):
    product = Allproduct.objects.get(id=pid)
    serializer = AllproductSerializer(product) #if product is list put (many=True)
    return JsonResponse(serializer.data )

#rest_framework api

@api_view(['GET'])
def api_get_product(request,pid):
    product = Allproduct.objects.get(id=pid)
    if request.method == 'GET':
        serializer = AllproductSerializer(product)
        return Response(serializer.data)

@api_view(['POST'])
def api_post_product(request):
    if request.method == 'POST':
        serializer = AllproductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def api_update_product(request,pid):
    if request.method == 'PUT':
        product = Allproduct.objects.get(id=pid)
        serializer = AllproductSerializer(product,data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            data['message'] = 'อัพเดตข้อมูลแล้ว'

            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
        
@api_view(['DELETE'])
def api_delete_product(request,pid):
    if request.method == 'DELETE' :
        product = Allproduct.objects.get(id=pid)
        delete = product.delete()
        data = {}
        if deleted:
            data['message'] = 'ลบข้อมูลเรียบร้อยแล้ว'
            return Response(data=data,status=status.HTTP_200_OK)
        else:
            data['message'] = 'ลบข้อมูลไม่สำเร็จ'
            return Response(data=data,status=status.HTTP_404_NOT_FOUND)

###########