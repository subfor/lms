from django import forms

from .models import Group, Lecturer, Student


class AddStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'email')


class AddLecturerForm(forms.ModelForm):
    class Meta:
        model = Lecturer
        fields = ('first_name', 'last_name', 'email')


class AddGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('course', 'group_name', 'course', 'students', 'teachers')


class ContactForm(forms.Form):
    name = forms.CharField(max_length=50, required=True, label='Your name')
    from_email = forms.EmailField(max_length=50,
                                  required=True,
                                  label='Email',
                                  error_messages={'invalid': 'Enter a valid e-mail address!!!!.'}
                                  )
    subject = forms.CharField(max_length=100, required=True)
    message = forms.CharField(widget=forms.Textarea)
