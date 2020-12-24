from django.shortcuts import redirect, render

# Create your views here.
from django.http import HttpResponse
from .models import DataSet
from .forms import UploadFileForm

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
    context = {'data_set': data_set}
    return render(request, 'apriori/show.html', context)
