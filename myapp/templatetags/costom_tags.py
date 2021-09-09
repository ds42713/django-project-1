from django import template
#ใช้บนสุด {% load costom_tags %}

from ..models import * # .. ถอยหลังไป2ครั้ง

register = template.Library()

@register.simple_tag
def hello_tag():
    #นำไปใช้ {% hello_tag %}
    return '<----- Hello Tag ----->'

#นับสินค้าที่มีทั้งหมด
@register.simple_tag
def show_allproduct():
    count = Allproduct.objects.count()
    return count

@register.inclusion_tag('myapp/allcategory.html')
def all_category():
    cats = Category.objects.all()
    return {'allcats':cats}