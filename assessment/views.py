from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

from .models import Question, StudentAnswer, StudentProgress, ExamSettings
from .decorators import admin_only
# =========================
# STUDENT ASSESSMENT VIEW
# =========================
@login_required
def assessment_view(request):

    questions = Question.objects.all()
    total_questions = questions.count()

    progress, created = StudentProgress.objects.get_or_create(
        student=request.user
    )

    # =========================
    # START TIMER
    # =========================
    if not progress.start_time:
        return redirect("dashboard") 
        progress.save()

    # =========================
    # GET EXAM DURATION
    # =========================
    settings = ExamSettings.objects.first()
    duration = settings.duration_minutes if settings else 30

    time_limit = progress.start_time + timedelta(minutes=duration)

    # =========================
    # RESET IF TIME EXPIRED
    # =========================
    if timezone.now() > time_limit:

        # RESET PROGRESS
        progress.current_index = 0
        progress.completed = False
        progress.start_time = None
        progress.save()

        # DELETE ALL ANSWERS FOR THIS STUDENT (RESET EXAM)
        StudentAnswer.objects.filter(student=request.user).delete()

        # SEND USER BACK TO DASHBOARD
        return redirect("dashboard")

    # =========================
    # COMPLETED CHECK
    # =========================
    if progress.completed or progress.current_index >= total_questions:
        progress.completed = True
        progress.save()
        return render(request, 'assessment/completed.html')

    question = questions[progress.current_index]

    # =========================
    # HANDLE ANSWER SUBMISSION
    # =========================
    if request.method == "POST":

        answer_text = request.POST.get("answer")

        StudentAnswer.objects.update_or_create(
            student=request.user,
            question=question,
            defaults={"answer": answer_text}
        )

        progress.current_index += 1

        if progress.current_index >= total_questions:
            progress.completed = True

        progress.save()

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({
                "next": True,
                "completed": progress.completed
            })

        return redirect("assessment")

    # =========================
    # END TIME FOR TIMER UI
    # =========================
    end_time = progress.start_time + timedelta(minutes=duration)

    return render(request, "assessment/question.html", {
        "question": question,
        "current": progress.current_index + 1,
        "total": total_questions,
        "end_time": end_time.isoformat()   # 🔥 FOR FRONTEND TIMER
    })


# =========================
# ADMIN: EXAM SETTINGS
# =========================
@admin_only
def exam_settings(request):

    settings, created = ExamSettings.objects.get_or_create(id=1)

    if request.method == "POST":

        settings.duration_minutes = request.POST.get("duration_minutes")
        settings.save()

        return redirect("exam_settings")

    return render(request, "admin/exam_settings.html", {
        "settings": settings
    })


from .models import Question, StudentAnswer
from .decorators import admin_only

@admin_only
def admin_questions(request):

    if request.method == "POST":

        text = request.POST.get("question_text")

        Question.objects.create(question_text=text)

        return redirect("admin_questions")

    questions = Question.objects.all().order_by("-id")

    return render(request, "admin/questions.html", {
        "questions": questions
    })


from django.shortcuts import get_object_or_404

@admin_only
def edit_question(request, pk):

    question = get_object_or_404(Question, id=pk)

    if request.method == "POST":

        question.question_text = request.POST.get("question_text")
        question.save()

        return redirect("admin_questions")

    return render(request, "admin/edit_question.html", {
        "question": question
    })


@admin_only
def delete_question(request, pk):

    question = get_object_or_404(Question, id=pk)

    question.delete()

    return redirect("admin_questions")


@admin_only
def admin_responses(request):

    answers = StudentAnswer.objects.select_related(
        "student", "question"
    ).order_by("-submitted_at")

    return render(request, "admin/responses.html", {
        "answers": answers
    })



from django.contrib.auth.models import User
from django.db.models import Q

@admin_only
def admin_users(request):

    query = request.GET.get("q")

    if query:
        users = User.objects.filter(
            Q(username__icontains=query)
        ).filter(is_staff=False)
    else:
        users = User.objects.filter(is_staff=False)

    return render(request, "admin/users.html", {
        "users": users,
        "query": query
    })



@admin_only
def user_responses(request, user_id):

    user = get_object_or_404(User, id=user_id)

    answers = StudentAnswer.objects.filter(
        student=user
    ).select_related("question").order_by("-submitted_at")

    return render(request, "admin/user_responses.html", {
        "user": user,
        "answers": answers
    })



from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import StudentProgress

@login_required
def start_assessment(request):

    progress, created = StudentProgress.objects.get_or_create(
        student=request.user
    )

    # ONLY START IF NOT ALREADY STARTED
    if not progress.start_time:
        progress.start_time = timezone.now()
        progress.current_index = 0
        progress.completed = False
        progress.save()

    return redirect("assessment")