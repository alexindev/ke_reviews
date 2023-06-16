from django import forms
from users.models import Users


class UserPicForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'custom-file-input'}),
        }
