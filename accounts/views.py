from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from assessment.models import (
    Question,
    StudentAnswer
)
from .forms import RegisterForm


def register_view(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect('dashboard')

    else:          

        form = RegisterForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )


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