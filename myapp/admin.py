from django.contrib import admin
# from .models import Allproduct ,Profile #  //.model คือไฟล์ // allproduct คือชื่อclass
# Register your models here.
from .models import *

admin.site.site_header = 'My Game Shop'
admin.site.index_title = 'Main Admin'
admin.site.site_title = 'My Game Shop Admin'

class AllproductAdmin(admin.ModelAdmin):
    list_display = ['name','id','instock','price','quantity']
    list_editable = ['instock','quantity']

admin.site.register(Allproduct,AllproductAdmin)
admin.site.register(Profile)
admin.site.register(Cart)

class OrderListAdmin(admin.ModelAdmin):
    list_display = ['orderid','productname','total','quantity']


admin.site.register(OrderList ,OrderListAdmin)
admin.site.register(OrderPending)
admin.site.register(VerifyEmail)
admin.site.register(Category)