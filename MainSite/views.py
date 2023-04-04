from django.shortcuts import render
from MainSite.forms import StudentForm, SortForm, StudentUploadForm
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from MainSite.models import Student
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth.models import User
from datetime import date
from datetime import datetime
import random
import string
from transliterate import translit
import random


def student_add(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            gender = form.cleaned_data['gender']
            date_of_birth = form.cleaned_data['date_of_birth']
            age = date.today().year - date_of_birth.year - ((date.today().month, date.today().day) < (
            date_of_birth.month, date_of_birth.day))
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            photo = form.cleaned_data['photo']
            skills = form.cleaned_data['skills']
            student = Student(full_name=full_name, gender=gender, age=age, date_of_birth=date_of_birth, phone_number=phone_number, email=email, photo=photo)
            student.save()
            student.skills.set(skills)
            return HttpResponse('Student added successfully!')
    else:
        form = StudentForm()
    return render(request, 'student_add.html', {'form': form, })


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid username or password'
    else:
        error_message = ''
    return render(request, 'login.html', {'error_message': error_message})


def logout_view(request):
    logout(request)
    return redirect('home')


def user_profile(request, id):
    user = User.objects.get(id=id)
    context = {"student": user.student,
               }
    return render(request, "user_profile.html", context)


def home(request):
    if request.method == "GET" and 'sort_form' in request.GET:
        form = SortForm(request.GET, initial={'sort_field': request.GET.get('sort_field')})
        if form.is_valid():

            print(request.GET.get('sort_field'))
            sort_options = {'registration_date': User.objects.order_by('date_joined').filter(is_superuser=False),
                            'last_name': User.objects.order_by('last_name').filter(is_superuser=False),
                            'first_name': User.objects.order_by('first_name').filter(is_superuser=False),
                            'date_of_birth': User.objects.filter(is_superuser=False).order_by('-student__date_of_birth')}

            context = {"users": sort_options[form.cleaned_data['sort_field']],
                       "sort_form": form}
            return render(request, "home.html", context=context)

    context = {"users": User.objects.order_by('date_joined').filter(is_superuser=False),
               "sort_form": SortForm()}
    return render(request, "home.html", context=context)


def upload_students(request):
    if request.method == 'POST':
        form = StudentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            content = list(map(lambda line: line.decode('utf-8').rstrip(), file.readlines()))
            print(type(file))
            new_file = ""
            for fullName in content:
                first_name = fullName.split()[1]
                last_name = fullName.split()[0]

                # Генерируем логин в формате имя_фамилия_число
                username = f"{translit(first_name.lower(), 'ru', reversed=True)}_{translit(last_name.lower(), 'ru', reversed=True)}_{User.objects.count() + 1}"

                # Символы, из которых будет состоять пароль
                chars = string.ascii_letters + string.digits
                # Генерация пароля длиной length
                password = ''.join(random.choice(chars) for _ in range(6))
                user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
                user.save()
                new_file +=f"{user.first_name} {user.last_name} login: {user.username} password: {password}\n"

            # Создаем HttpResponse с содержимым файла
            response = HttpResponse(new_file, content_type='text/plain')

            # Устанавливаем заголовок Content-Disposition в attachment,
            # что заставляет браузер загрузить файл, а не показывать его в окне браузера.
            response['Content-Disposition'] = 'attachment; filename="file.txt"'

            return response
    else:
        form = StudentUploadForm()
    return render(request, 'upload.html', {'form': form})


def profile_edit(request, id):
    student = Student.objects.get(id=id)
    if student.user != request.user:
        return HttpResponse("Ай Ай Ай, у нас тут завелся hacker!")
    if request.method == "POST":
        print("пришел пост запрос",id)
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            date_of_birth = form.cleaned_data["date_of_birth"]
            age = date.today().year - date_of_birth.year - ((date.today().month, date.today().day) < (date_of_birth.month, date_of_birth.day))
            student = Student.objects.get(id=id)
            student.age = age
            student.save()
            return HttpResponseRedirect(f"/profile/{id}")
    else:
        data = {'full_name': student.full_name,
                'gender': student.gender,
                'date_of_birth': student.date_of_birth.strftime('%Y-%m-%d'),
                'phone_number': student.phone_number,
                'email': student.email,
                'photo': student.photo,
                'skills': student.skills.all()}
        context = {"form": StudentForm(initial=data, instance=student),
                   'id': id}
        return render(request, "edit_profile.html", context=context)