from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Question, StudentAnswer, StudentProgress

from django.http import JsonResponse

@login_required
def assessment_view(request):

    questions = Question.objects.all()
    total_questions = questions.count()

    progress, created = StudentProgress.objects.get_or_create(
        student=request.user
    )

    # Completed
    if progress.completed or progress.current_index >= total_questions:
        progress.completed = True
        progress.save()
        return render(request, 'assessment/completed.html')

    question = questions[progress.current_index]

    if request.method == "POST":

        answer_text = request.POST.get("answer")

        StudentAnswer.objects.get_or_create(
            student=request.user,
            question=question,
            defaults={"answer": answer_text}
        )

        progress.current_index += 1

        if progress.current_index >= total_questions:
            progress.completed = True

        progress.save()

        # 🔥 return JSON for smooth frontend update
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({
                "next": True,
                "completed": progress.completed
            })

        return redirect("assessment")

    return render(
        request,
        "assessment/question.html",
        {
            "question": question,
            "current": progress.current_index + 1,
            "total": total_questions
        }
    )



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