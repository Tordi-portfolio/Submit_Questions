from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from assessment.models import (
    Question,
    StudentAnswer
)
from .forms import RegisterForm


from django.contrib.auth.models import User
from .models import Profile
from .forms import RegisterForm

def register_view(request):

    form = RegisterForm()

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            password = form.cleaned_data["password"]
            confirm = form.cleaned_data["confirm_password"]

            if password != confirm:
                return render(request, "accounts/register.html", {
                    "form": form,
                    "error": "Passwords do not match"
                })

            full_name = form.cleaned_data["full_name"]
            username = form.cleaned_data["username"]
            phone = form.cleaned_data["phone_number"]
            country = form.cleaned_data["country"]
            age = form.cleaned_data["age"]

            user = User.objects.create_user(
                username=username,
                password=password
            )

            # split full name
            name_parts = full_name.split(" ", 1)
            user.first_name = name_parts[0]

            if len(name_parts) > 1:
                user.last_name = name_parts[1]

            user.save()

            # create profile
            Profile.objects.create(
                user=user,
                phone_number=phone,
                country=country,
                age=age
            )

            return redirect("login")

    return render(request, "accounts/register.html", {
        "form": form
    })

from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):

    total_questions = Question.objects.count()

    completed = StudentAnswer.objects.filter(
        student=request.user
    ).count()

    remaining = total_questions - completed

    context = {
        'total_questions': total_questions,
        'completed': completed,
        'remaining': remaining,
    }

    return render(
        request,
        'accounts/dashboard.html',
        context
    )



from django.shortcuts import render, redirect
from django.contrib.auth import (
    login,
    logout,
    authenticate
)

from django.contrib.auth.decorators import login_required
from .forms import RegisterForm

def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('dashboard')

        else:

            return render(
                request,
                'accounts/login.html',
                {
                    'error':
                    'Invalid username or password'
                }
            )

    return render(
        request,
        'accounts/login.html'
    )


def logout_view(request):

    logout(request)

    return redirect('login')