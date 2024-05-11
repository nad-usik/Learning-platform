from .models import Teachers, Subjects, Lessons
from django import forms


class AddLessonForm(forms.ModelForm):
    date = forms.DateTimeField(label='',
                               widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}))
    duration = forms.IntegerField(label='', widget=forms.TextInput(
        attrs={'type': 'number', 'class': 'form-control', 'placeholder': 'Продолжительность в минутах'}))

    class Meta:
        model = Lessons
        fields = ('subject', 'date', 'duration')

    def __init__(self, teacher_id, *args, **kwargs):
        super(AddLessonForm, self).__init__(*args, **kwargs)
        teacher = Teachers.objects.get(user_id=teacher_id)
        subjects = teacher.subject.all()
        subject_choices = [(subject.id, subject.name) for subject in subjects]

        self.fields['subject'] = forms.ModelChoiceField(label='', queryset=Subjects.objects.filter(
            id__in=[subject.id for subject in subjects]),
                                                        widget=forms.Select(
                                                            attrs={'class': 'form-control', 'placeholder': 'Предмет'}))
