from django import forms
from MainSite.models import Student, Skill, CustomUser

from django.contrib.auth.forms import UserCreationForm
from django.core.validators import FileExtensionValidator
from django import forms


class StudentForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Иванов Иван Иванович'}), label="ФИО")
    gender = forms.ChoiceField(choices=[('Мужской', 'Мужской'), ('Женский', 'Женский')], label="Пол")

    date_of_birth = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label="Дата рождения")
    phone_number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': '88005553535'}),
                                   label="Номер телефона")
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'ivanov@mail.ru'}), label="Почта")
    photo = forms.ImageField(required=False, label="Фото")

    class Meta:
        model = Student
        fields = ['full_name', 'gender', 'date_of_birth', 'phone_number',
                  'email', 'photo', 'telegram', 'group', 'hide_contacts']


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)


    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name')

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


# Аргумент attrs в данном случае определяет HTML-атрибуты, которые будут добавлены к тегу select в HTML-коде формы. В данном случае мы добавляем атрибут class со значением form-control mr-2
class SortForm(forms.Form):
    sort_field = forms.ChoiceField(choices=[
        ('registration_date', 'Дата регистрации'),
        ('last_name', 'Фамилии'),
        ('first_name', 'Имени'),
        ('date_of_birth', 'Возрасту')
    ], required=False, widget=forms.Select(attrs={'class': 'form-control mr-2'}), initial='registration_date',
        label=False)


class StudentUploadForm(forms.Form):
    file = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['xls'])])
