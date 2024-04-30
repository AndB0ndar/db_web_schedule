from django.shortcuts import render, get_object_or_404, redirect

from schedule.forms import HomeworkForm
from schedule.models import Stats, TinyGroup, RichGroup, DaySchedule, Lesson, Homework


def home(request):
    return render(request, 'schedule/home.html')


def stats(request):
    stat = Stats.objects.all()[0]
    context = {
        'stat': stat
    }
    return render(request, 'schedule/stats.html', context)


def groups(request):
    search_query = request.GET.get('search_query', '')

    groups = TinyGroup.objects.all()

    if search_query:
        groups = groups.filter(groupName__icontains=search_query)

    context = {
        'groups': groups,
        'search_query': search_query,
    }
    return render(request, 'schedule/groups.html', context)


def group(request, pk: int):
    group = RichGroup.objects.get(group=pk)
    day_schedules = DaySchedule.objects.filter(group=group)

    week_lessons = []

    for day_schedule in day_schedules:
        even_week_lss = Lesson.objects.filter(day_schedule=day_schedule, is_even_week=True)
        odd_week_lss = Lesson.objects.filter(day_schedule=day_schedule, is_even_week=False)
        week_lessons.append((day_schedule, even_week_lss, odd_week_lss))

    context = {
        'title': group.group.groupName,
        'group': group,
        'week_lessons': week_lessons,
    }
    return render(request, 'schedule/group.html', context)


def homework(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            homework = form.save(commit=False)
            homework.save()

    homeworks = Homework.objects.all()
    form = HomeworkForm()
    context = {
        'homeworks': homeworks,
        'form': form,
    }
    return render(request, 'schedule/homework.html', context)


def delete_homework(request, pk: int):
    homework = get_object_or_404(Homework, id=pk)
    homework.delete()
    return redirect('homework')
