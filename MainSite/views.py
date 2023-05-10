from django.contrib import messages
from django.shortcuts import render
from MainSite.forms import StudentForm, SortForm, StudentUploadForm
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from MainSite.models import Student, Skill, CustomUser
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.auth import logout
import xlrd
from datetime import date
from datetime import datetime
import random
import string
from transliterate import translit
import random
import xlwt
from django.db import IntegrityError


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
            student = Student(full_name=full_name, gender=gender, age=age, date_of_birth=date_of_birth,
                              phone_number=phone_number, email=email, photo=photo)
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
            print("данные верные, ты залогинился")
            return redirect('home')
        else:
            error_message = 'Invalid username or password'
    else:
        error_message = ''
    return render(request, 'login.html', {'error_message': error_message})


def logout_view(request):
    logout(request)
    return redirect('home')


def test(request):
    print("test")
    return render(request, "test.html", {'nodes': Skill.objects.all()})


def user_profile(request, id):
    user = CustomUser.objects.get(id=id)
    context = {"student": user.student,
               }
    return render(request, "user_profile.html", context)


def home(request):
    if request.method == "GET" and 'sort_form' in request.GET:
        form = SortForm(request.GET, initial={'sort_field': request.GET.get('sort_field')})
        if form.is_valid():
            print(request.GET.get('sort_field'))
            sort_options = {'registration_date': CustomUser.objects.order_by('date_joined').filter(is_superuser=False),
                            'last_name': CustomUser.objects.order_by('last_name').filter(is_superuser=False),
                            'first_name': CustomUser.objects.order_by('first_name').filter(is_superuser=False),
                            'date_of_birth': CustomUser.objects.filter(is_superuser=False).order_by(
                                '-student__date_of_birth')}

            context = {"users": sort_options[form.cleaned_data['sort_field']],
                       "sort_form": form}
            return render(request, "home.html", context=context)

    context = {"users": CustomUser.objects.order_by('date_joined').filter(is_superuser=False),
               "sort_form": SortForm()}
    return render(request, "home.html", context=context)


def upload_students(request):
    if request.method == 'POST':
        form = StudentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            workbook = xlrd.open_workbook(file_contents=file.read())
            sheet = workbook.sheet_by_index(0)
            content = []
            for row_idx in range(sheet.nrows):
                content.append(sheet.row_values(row_idx))
            new_workbook = xlwt.Workbook()
            new_sheet = new_workbook.add_sheet('Students')
            new_sheet.write(0, 0, "Имя")
            new_sheet.write(0, 1, "Фамилия")
            new_sheet.write(0, 2, "Логин")
            new_sheet.write(0, 3, "Пароль")
            for i, line in enumerate(content, 1):
                first_name = line[0]
                last_name = line[1]
                record_book = int(line[2])

                print(first_name, last_name)
                # Генерируем логин в формате имя_фамилия_число
                username = f"{record_book}"

                # Символы, из которых будет состоять пароль
                chars = string.ascii_letters + string.digits
                # Генерация пароля длиной length
                password = ''.join(random.choice(chars) for _ in range(6))
                user, created = CustomUser.objects.get_or_create(username=username, defaults={
                    'password': password,
                    'first_name': first_name,
                    'last_name': last_name
                })

                if created:
                    user.save()
                else:
                    # пользователь с таким именем уже существует
                    return HttpResponse(f"Вы пытаетесь добавить студента {first_name} {last_name}, но его номер зачетной книжки {record_book} уже используется")

                new_sheet.write(i, 0, first_name)
                new_sheet.write(i, 1, last_name)
                new_sheet.write(i, 2, username)
                new_sheet.write(i, 3, password)

            # Создаем HttpResponse с содержимым файла
            response = HttpResponse(content_type='application/ms-excel')

            # Устанавливаем заголовок Content-Disposition в attachment,
            # что заставляет браузер загрузить файл, а не показывать его в окне браузера.
            response['Content-Disposition'] = 'attachment; filename="students.xls"'

            # Записываем workbook в response
            new_workbook.save(response)

            return response
    else:
        form = StudentUploadForm()
    return render(request, 'upload.html', {'form': form})


def profile_edit(request, id):
    student = Student.objects.get(id=id)
    if student.user != request.user:
        return HttpResponse("Ай Ай Ай, у нас тут завелся hacker!")
    if request.method == "POST" and 'student_input' in request.POST:
        print("пришел пост запрос студент формы", id)
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if CustomUser.objects.filter(email=email).exclude(id=student.user.id).exists():
                return HttpResponse("Пользователь с такой почтой уже существует")

            # Check if phone number already exists
            phone_number = form.cleaned_data.get('phone_number')
            if CustomUser.objects.filter(phone_number=phone_number).exclude(id=student.user.id).exists():
                return HttpResponse("Пользователь с таким номером телефона уже существует")

            form.save()
            request.user.email = form.cleaned_data["email"]
            request.user.phone_number = form.cleaned_data["phone_number"]
            request.user.save()
            date_of_birth = form.cleaned_data["date_of_birth"]
            possible_age = date.today().year - date_of_birth.year - (
                    (date.today().month, date.today().day) < (date_of_birth.month, date_of_birth.day))
            age = max(0, possible_age)
            student = Student.objects.get(id=id)
            student.age = age
            student.save()
            return HttpResponseRedirect(f"/profile/{id}")
    elif request.method == "POST" and 'skills_input' in request.POST:
        print("пришел пост запрос скилл формы", id)
        selected_skills = request.POST.get('skills_input')
        print(selected_skills.split(","))

        skill_list = selected_skills.split(',')  # разбиваем строку на список
        student.skills.clear()
        for skill in filter(lambda item: len(item) > 0, skill_list):

            skill_obj = None
            try:
                skill_obj = Skill.objects.get(name=skill.strip())
            except Skill.DoesNotExist:
                return HttpResponse(f"Навыка {skill} нет в базе данных", status=400)

            if student.skills.filter(name=skill_obj.name).exists():
                print(f"{skill} уже был в навыках")
            else:
                student.skills.add(skill_obj)
        student.save()
        return HttpResponseRedirect(f"/profile/{id}")
    else:
        print("обычная страница", id)
        date_of_birth = None
        try:
            date_of_birth = student.date_of_birth.strftime('%Y-%m-%d')
        except:
            date_of_birth = ""
        data = {'full_name': student.full_name,
                'gender': student.gender,
                'date_of_birth': date_of_birth,
                'phone_number': student.phone_number,
                'email': student.email,
                'photo': student.photo,
                }
        context = {"form": StudentForm(initial=data, instance=student),
                   'id': id,
                   'nodes': Skill.objects.all(),
                   'selected_skills': student.skills.all()}
        print(context['selected_skills'])
        return render(request, "edit_profile.html", context=context)
