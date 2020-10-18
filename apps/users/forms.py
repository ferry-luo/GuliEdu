
from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile,EmailVerifyCode

class UserRegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True,min_length=6,max_length=16,error_messages={
        "required":"密码必须填写",
        "min_length":"密码至少6位",
        "max_length":"密码最多16位"
    })
    captcha = CaptchaField()



class UserLoginForm(forms.Form):
    username = forms.EmailField(required=True)
    password = forms.CharField(required=True,min_length=6,max_length=16,error_messages={
        "required":"密码必须填写",
        "min_length":"密码至少6位",
        "max_length":"密码最多16位"
    })

class UserForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField()

class UserResetForm(forms.Form):
    password = forms.CharField(required=True,min_length=6,max_length=16,error_messages={
        'required':'密码必须填写',
        'min_length':'密码至少6位',
        'max_length':'密码不能超过16位'
    })
    password1 = forms.CharField(required=True,min_length=6,max_length=16,error_messages={
        'required':'密码必须填写',
        'min_length':'密码至少6位',
        'max_length':'密码不能超过16位'
    })

class UserChangeImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']

class UserChangeInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name','birthday','gender','address','phone']



class UserChangeEmailForm(forms.ModelForm):
    class Meta:
        model = EmailVerifyCode #用model =  UserProfile做验证也行，两张表对邮箱格式都是一样的限制
        fields = ['email']

class UserResetEmailForm(forms.ModelForm):
    class Meta:
        model = EmailVerifyCode
        fields = ['email','code']