import xadmin
from .models import *

class CityInfoXadmin(object):
    list_display = ['name','add_time']
    model_icon = 'fa fa-bath'


class OrgInfoXadmin(object):
    list_display = ['image', 'name','course_num','study_num','love_num','click_num','category','cityinfo']
    model_icon = 'fa fa-gift'
    style_fields = {'detail':'ueditor'} #告诉它我要把detail这个字段设为ueditor富文本编辑器


class TeacherInfoXadmin(object):
    list_display = ['image', 'name', 'work_year', 'work_position', 'click_num', 'age', 'gender', 'love_num']


xadmin.site.register(CityInfo,CityInfoXadmin)
xadmin.site.register(OrgInfo,OrgInfoXadmin)
xadmin.site.register(TeacherInfo,TeacherInfoXadmin)