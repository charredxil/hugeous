from django.shortcuts import render
from django.http import HttpResponse
from django.forms import formset_factory

from .forms import ProofRowForm

def sandbox(request):
    my_template = "proof/sandbox.html"

    ProofForm = formset_factory(ProofRowForm, extra=1)
    data = {
        'form-TOTAL_FORMS': '2',
        'form-INITIAL_FORMS': '0',
        'form-MAX_NUM_FORMS': '',
    }

    if request.method == 'POST':
        formset = ProofForm(request.POST)
        if formset.is_valid():
            context = {
                'formset' : formset,
                'valid' : True
            }
            return render(request, my_template, context)
    else:
        formset = ProofForm()

    return render(request, my_template, {'formset': formset})
