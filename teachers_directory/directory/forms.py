from django import forms
from django.core.validators import FileExtensionValidator
from .models import Teacher

#File Upload Forms
class UploadFileForm(forms.Form):
    csv_file = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['csv'])])
    zip_file = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['zip'])])

    def clean(self):
    	pass

class TeacherForm(forms.ModelForm):
	class Meta:
		model = Teacher
		fields = '__all__'