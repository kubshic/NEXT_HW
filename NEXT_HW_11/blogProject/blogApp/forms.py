from django import forms
from .models import Comment, User
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': '댓글을 입력해주세요'}),
        }

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'placeholder': '비밀번호를 입력해주세요'}))
    password2 = forms.CharField(
        label="Password Confirmation", widget=forms.PasswordInput(attrs={'placeholder': '비밀번호 확인'})
    )

    class Meta:
        model = User
        fields = ['username']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password1"] != cd["password2"]:
            raise forms.ValidationError("Passwords don't match.")
        return cd["password2"]
    

    def save(self, commit=True) -> User:
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            password=self.cleaned_data["password1"],
        )
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '아이디'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '비밀번호'}))