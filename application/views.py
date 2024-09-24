from django.shortcuts import render
from .models import CustomUser


def registration(request):
    if request.method == 'POST' and len(request.POST) == 5:
        form_info = request.POST

        username = form_info.get('username')
        email = form_info.get('email')
        password = form_info.get('password')
        repeat_password = form_info.get('repeat_password')

        if password != repeat_password:
            return render(request, 'my_registration.html',
                          {'registration_response': 'passwords do not match', 'form_info': form_info})
        elif CustomUser.objects.filter(username=username).exists():
            return render(request, 'my_registration.html',
                          {'registration_response': 'username is already taken', 'form_info': form_info})
        elif CustomUser.objects.filter(email=email).exists():
            return render(request, 'my_registration.html',
                          {'registration_response': 'email is already taken', 'form_info': form_info})
        else:
            user = CustomUser.objects.create_user(username=username,
                                                  password=password,
                                                  email=email,
                                                  is_active=True)
            user.set_password(password)
            user.save()

            return render(request, 'my_registration.html', {'registration_response': 'success'})
    return render(request, 'my_registration.html')
