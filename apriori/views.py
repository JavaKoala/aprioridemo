from django.shortcuts import redirect, render

# Create your views here.
from django.http import HttpResponse
from .models import Document
from .forms import UploadFileForm

def index(request):
    message = ''

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            return redirect('index')
        else:
            message = 'The form is not valid. Fix the following error:'
    else:
        form = UploadFileForm()

    documents = Document.objects.all()

    context = {'documents': documents, 'form': form, 'message': message}
    return render(request, 'apriori/index.html', context)

def show(request, document_id):
    document = Document.objects.get(pk=document_id)
    context = {'document': document}
    return render(request, 'apriori/show.html', context)
