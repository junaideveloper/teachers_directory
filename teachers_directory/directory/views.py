from django.shortcuts import render
from .models import Subject,Teacher
import csv, io
from django.conf import settings
from .forms import UploadFileForm
from zipfile import ZipFile
from django.core.files import File
import os
from django.views.generic import ListView
from django.views.generic.base import TemplateResponseMixin, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic.detail import DetailView

class DirectoryHomeView(ListView):
    login_url = '/login/'
    template_name = 'directory/home.html'
    model = Teacher

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['last_name_filter'] = self.get_lastname_filter_char()
        context['subject_filter'] = self.get_subject_filter_chars()
        return context

    def get_lastname_filter_char(self):
        lname_char_list = []
        lastname_list = Teacher.objects.values_list('last_name', flat=True).filter(last_name__isnull=False).exclude(last_name='').order_by('last_name').distinct()
        for lname in lastname_list:
            char_ = lname.strip().upper()[0]
            if char_ in lname_char_list:pass
            else:lname_char_list.append(char_)
        return lname_char_list

    def get_subject_filter_chars(self):
        sub_char_list = []
        subject_list = Subject.objects.values_list('name', flat=True).filter(name__isnull=False).exclude(name='').order_by('name').distinct()
        for subject in subject_list:
            char_ = subject.strip().upper()[0]
            if char_ in sub_char_list: pass
            else:sub_char_list.append(char_)
        return sub_char_list

    def get_queryset(self):
        """
        Return the list of items for this view.
        """
        queryset = self.model.objects.all()
        if self.request.GET.get('filter'):
            val = self.request.GET.get('filter')
            if self.request.GET.get('type'):
                if self.request.GET.get('type') == 'lastname':
                    queryset = queryset.filter(last_name__istartswith=val)
                if self.request.GET.get('type') == 'subject':
                    queryset = queryset.filter(subjects__name__istartswith=val)
        return queryset


'''
LoginRequiredMixin : all requests by non-authenticated users will be redirected to the login page
'''
class BulkUploadView(LoginRequiredMixin,TemplateResponseMixin, View):
    # login_url = '/login/'
    template_name = "directory/upload.html"

    def get(self, request, *args, **kwargs):
        form = UploadFileForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            zip_file = request.FILES['zip_file']
            csv_file = request.FILES['csv_file']
            if (not csv_file.name.endswith('.csv')) or (not zip_file.name.endswith('.zip')):
                messages.error(request, 'Uploaded file is not either csv or zip')
            _uploaded,_message = self.handle_uploaded_file(zip_file,csv_file)
            if not _uploaded:
                messages.info(request, _message)
            else:messages.success(request, _message)
            return render(request, self.template_name, {'form': form})

    def handle_uploaded_file(self,zip_file,csv_file):
        global message
        is_upload = False
        zip_file_path = settings.MEDIA_ROOT.joinpath('temp').joinpath('teachers.zip') # Path to the uploaded zip file
        with open(zip_file_path, 'wb+') as zip:
            for chunk in zip_file.chunks():
                zip.write(chunk)
        archive = ZipFile(zip_file, 'r')
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        name_lista = archive.namelist()
        try:
            name_list = archive.namelist()
            print(f"Namelist : {name_list}")
            print(csv.reader(io_string, delimiter=',', quotechar="|"))
            for data in csv.reader(io_string, delimiter=',', quotechar="|"):
                teacher = Teacher()
                if len(data) >= 7:
                    if (data[0].strip() == '') or (data[3].strip() == ''):
                        pass
                        #raise Exception('first_name and email id should not be empty')
                    else:
                        teacher.first_name = data[0].strip()
                        teacher.last_name = data[1].strip()
                        teacher.email = data[3].strip()
                        teacher.phone = data[4].strip()
                        teacher.room_no =data[5].strip()
                        teacher.save()
                        subjects = data[6:]
                        for subject in subjects:
                            if subject != "":
                                subject = subject.replace('"', '')
                                subject, _ = Subject.objects.get_or_create(name=subject.strip().upper())
                                if teacher.subjects.count() < 5:
                                    teacher.subjects.add(subject)
                        if data[2] in name_list:
                            pic_name= data[2]
                            pic = archive.open(pic_name, 'r')
                            content = File(pic)
                            teacher.profile_picture.save(pic_name,content,save=True)
                        else:
                            print(f"{data[2]} is not match")
                        is_upload = True
                        message = "Data has been inserted successfully"
        except Exception as e:
            message = "Failed to upload bulk data.."
            pass
        finally:
            os.remove(zip_file_path)
        return is_upload,message

class TeacherProfileView(DetailView):
  model = Teacher





