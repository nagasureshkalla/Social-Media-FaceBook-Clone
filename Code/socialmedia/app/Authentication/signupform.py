from email import message
from django import forms
from django.core.validators import EmailValidator,MinValueValidator,RegexValidator
class UserForm(forms.Form):
    
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,18}$"

    # email=forms.EmailField(max_length = 254,required=True,validators=[EmailValidator(message="Please enter Valid Email")])
    # username=forms.CharField(min_length=6,max_length=20,validators=[MinValueValidator(limit_value=6,message="Username must be 6 to 20 characters")])
    # password = forms.CharField(required=True,validators=[RegexValidator(regex=reg,message="Password MustContain 1 Capital, 1 Number, 1 Special character and 8>=length<28")])
    # repassword = forms.CharField(required=True,validators=[RegexValidator(regex=reg,message="Password MustContain 1 Capital, 1 Number, 1 Special character and 8>=length<28")])


    email=forms.EmailField(max_length = 254,required=True)
    username=forms.CharField(min_length=6,max_length=20)
    password = forms.CharField(required=True,widget=forms.PasswordInput)
    repassword = forms.CharField(required=True,widget=forms.PasswordInput)




