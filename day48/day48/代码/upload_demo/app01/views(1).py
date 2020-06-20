from django.shortcuts import render, HttpResponse
from django.views import View


# Create your views here.
# from django.core.files.uploadedfile import InMemoryUploadedFile
class Upload(View):

    def get(self, request):
        return render(request, 'upload.html')

    def post(self, request):
        file = request.FILES.get('f1')

        with open(file.name, 'wb') as f:
            for i in file:
                f.write(i)

        return HttpResponse('ok')


def index(request):
    return render(request,'index.html')