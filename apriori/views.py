import os
from django.shortcuts import redirect, render
from os import remove

# Create your views here.
from django.http import HttpResponse
from .models import DataSet
from .forms import UploadFileForm
from .ml import Apriori

def index(request):
    message = ''

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            new_data_set = DataSet(datafile=request.FILES['datafile'])
            new_data_set.save()

            return redirect('index')
        else:
            message = 'The form is not valid. Fix the following error:'
    else:
        form = UploadFileForm()

    data_sets = DataSet.objects.all()

    context = {'data_sets': data_sets, 'form': form, 'message': message}
    return render(request, 'apriori/index.html', context)

def show(request, data_set_id):
    data_set = DataSet.objects.get(pk=data_set_id)

    processor = Apriori(data_set.datafile)
    result = processor.process()

    context = {'data_set': data_set, 'result': result}
    return render(request, 'apriori/show.html', context)

def delete(request, data_set_id):
    data_set = DataSet.objects.get(pk=data_set_id)

    if os.path.exists(data_set.datafile.name):
        os.remove(data_set.datafile.name)

    data_set.delete()

    return redirect('index')