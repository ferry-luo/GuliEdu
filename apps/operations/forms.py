from django import forms
from .models import UserAsk
from courses.models import CourseInfo
import re

class UserAskForm(forms.ModelForm): #ModelForm比Form牛逼。要求前端传参的参数名与表字段一致
    class Meta:
        model = UserAsk
        fields = ['name','course','phone']  #用UserAsk表的'name','course','phone'三个字段做验证
        # exclude = ['add_time']    #除了'add_time'字段，其他字段都要用来做验证

        #如果用到了所有的字段
        # fields = '__all__'

    #ModelForm有留口子给开发人员自定义验证规则，以写方法的形式
    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        com = re.compile('^1([358][0-9]|4[579]|66|7[0135678]|9[89])[0-9]{8}$')
        #用match()，从第一个字符开始匹配。search()，假设刚开始的字符不匹配，并不会停止往后匹配。故匹配手机号码的场景不用search()
        if com.match(phone):
            return phone
        else:
            raise forms.ValidationError("手机号码不合法")

    def clean_course(self):
        course = self.cleaned_data["course"]
        course_list = CourseInfo.objects.filter(name=course)
        if course_list:
            return course
        else:
            raise forms.ValidationError("系统无相应课程")

        '''
        for j in range(len(course_list)):
            # re.I 表示使匹配对大小写不敏感
            if re.search(course_list[j].name,course,re.I) is not None:
                return course
            else:
                raise forms.ValidationError("系统无相应课程")
        '''

class UserCommentForm(forms.Form):
    course = forms.IntegerField(required=True)
    content = forms.CharField(required=True,min_length=1,max_length=300)


