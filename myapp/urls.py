# urls.py
from django.urls import path, include 
from .views import *
# * คือ import ทั้งหมด
# from .views import Home, About, Contact ,Playstation5 ,AddProduct ,Product ,Register
# .views คือ ไฟล์views 
# Home คือ ฟังชั่น Home ในไฟล์ views.py # * คือ import ทั้งหมด

urlpatterns = [
    path('', Home,name='home-page'),
    path('about/', About,name='about-page'),
    path('contact/', Contact,name='contact-page'),
    path('playstation5/', Playstation5,name='playstation5-page'),
    path('addproduct/', AddProduct, name='addproduct-page'),
    path('allproduct/', Product, name='allproduct-page'),
    path('register/', Register, name='register-page'),
    path('addtocart/<int:pid>/', AddtoCart, name='addtocart-page'),
    path('mycart/', MyCart, name='mycart-page'),
    path('mycart/edit/', MyCartEdit, name='mycartedit-page'),
    path('checkout/', Checkout, name='checkout-page'),
    path('orderlist/' ,OrderListPage  ,name='orderlist-page'),
    path('allorderlist/' ,AllOrderListPage  ,name='allorderlist-page'),
    path('uploadslip/<str:orderid>/', UploadSlip, name='uploadslip-page'),
    path('updatestatus/<str:orderid>/<str:status>/',UpdatePaid ,name='updatestatus'),
    path('updatetracking/<str:orderid>/' ,UpdateTracking ,name='updatetracking'),
    path('myorder/<str:orderid>/',MyOrder ,name='myorder-page'),
    path('confirm/<str:token>/', Confirm ,name='confirm-email'),
    path('graph/', PieChart, name='graph-page'),
    path('category/<int:code>/', ProductCategory, name='category-page'),
    path('testmd/', TestMd, name='testmd-page'),
    path('product/<int:productid>/', ProductDetail, name='detail-page'),
    path('editproduct/<int:productid>/', EditProduct, name='editproduct-page'),

    #### API ####
    path('api/product/',AllproductAPI,name='api-product'),
    #path('api/product/<int:pid>',ProductDetailAPI,name='api-productdetail'),


    path('api/product/<int:pid>/',api_get_product,name='api-productdetail'),
    path('api/product/create',api_post_product,name='api-product-post'), #ห้ามใส่ / ข้างหลัง
    path('api/product/update/<int:pid>',api_update_product,name='api-product-update'), #ห้ามใส่ / ข้างหลัง
    path('api/product/delete/<int:pid>',api_delete_product,name='api-product-delete'),
]
