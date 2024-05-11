from django import forms
from .models import Assignment
from Teachers.models import Teachers, Subjects


class AssignmentCreationForm(forms.ModelForm):

    deadline = forms.DateTimeField(label='',
                               widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}))
    attached_file = forms.FileField(label='', widget=forms.FileInput(attrs={'class': 'form-control', 'id': 'inputGroupFile01'}), required=False)  # Добавляем поле для прикрепления файла
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control', 'type': 'image', 'style': 'width: 100%; box-sizing: border-box; padding: 10px', 'rows': 2, 'placeholder': "Комментарий к заданию..."}))
    attached_image = forms.ImageField(label='Выберите изображение',
                                     widget=forms.FileInput(attrs={'class': 'form-control', 'id': 'inputGroupFile01'}),
                                     required=False)
    title = forms.CharField(label='', max_length=50,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название'}))

    class Meta:
        model = Assignment
        fields = ('subject', 'title', 'deadline', 'content', 'attached_file', 'attached_image')

    def __init__(self, user, *args, **kwargs):
        super(AssignmentCreationForm, self).__init__(*args, **kwargs)
        
        teacher = Teachers.objects.get(user_id=user)
      
        subjects = teacher.subject.all()
        
        self.fields['subject'] = forms.ModelChoiceField(label='', queryset=Subjects.objects.filter(
            id__in=[subject.id for subject in subjects]),
                                                        widget=forms.Select(
                                                            attrs={'class': 'form-control', 'placeholder': 'Предмет'}))


class ResponseForm(forms.ModelForm):

    response_file = forms.FileField(label='', widget=forms.FileInput(attrs={'class': 'form-control', 'id': 'inputGroupFile01'}), required=False) 
    response_content = forms.CharField(label='', widget=forms.Textarea(attrs={'style': 'width: 100%; box-sizing: border-box; border: none; padding: 10px', 'rows': 2, 'placeholder': "Комментарий к ответу..."}))

   
    class Meta:
        model = Assignment
        fields = ('response_content', 'response_file')

