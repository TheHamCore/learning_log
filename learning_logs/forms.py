from django import forms
from .models import Topic, Entry


class TopicForm(forms.ModelForm):
    """Форма для добавления тем."""

    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}  # не генерируем подпись для текстового поля


class EntryForm(forms.ModelForm):
    """Форма для добавления записей (к темам)."""
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': 'Entry:'}
        widget = {'text': forms.Textarea(attrs={'cols': 80})}
