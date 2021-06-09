from django.http import Http404
from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required


def check_topic_owner(request, topic):
    if topic.owner != request.user:
        raise Http404


def index(request):
    """Домашняя страница приложения Learning Log."""
    return render(request, 'learning_logs/index.html')


@login_required()
def topics(request):
    """Выводит список тем."""
    # topics = Topic.objects.order_by('date_added')
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required()
def topic(request, topic_id):
    """Выводит одну тему и все ее записи"""
    topic = Topic.objects.get(id=topic_id)
    # Проверка того, что тема принадлежит текущему пользователю.
    # if topic.owner != request.user:
    #     raise Http404
    check_topic_owner(request, topic)

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required()
def new_topic(request):
    """Работа с новой темой."""
    if request.method != 'POST':
        # данные не отправлялись создается пустая форма
        form = TopicForm
    else:
        # Отправлены данные POST, обработка данных.(связь с шаблоном new_topic)
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)  # новая тема изменена перед сохранением в базе данных.
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')

    # Вывести пустую или недействительную форму
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required()
def new_entry(request, topic_id):
    """Добавляет новую запись по конкретной теме."""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        # Если данные не отправлялись, создается пустая форма
        form = EntryForm()
    else:
        # Данные отправлены POST, обрабатываем данные
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)  # сохраняем в new_entry, но не сохраняем в базе данных(commit=False)
            new_entry.topic = topic  # присваиваем атрибуту topic объекта new_entry тему, пр-ую из БД (через ForeignKey)
            new_entry.topic.owner = request.user
            new_entry.save()  # запись сохраняется в БД c правильно ассоциированной темой
            return redirect('learning_logs:topic', topic_id=topic_id)
            # new_topic = form.save(commit=False)  # новая тема изменена перед сохранением в базе данных.
            # new_topic.owner = request.user
            # new_topic.save()
            # return redirect('learning_logs:topics')



    # Вывести пустую или недействительную форму.
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required()
def edit_entry(request, entry_id):
    """Редактирование существующей записи"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic  # получаем тему, связанную с записью (через ForeignKey)
    # Проверка того, что тема принадлежит текущему пользователю.
    # if topic.owner != request.user:
    #     raise Http404
    check_topic_owner(request, topic)

    if request.method != 'POST':
        # исходный запрос, форма заполняется исходными данными
        form = EntryForm(instance=entry)
    else:
        # отправка данных POST
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
