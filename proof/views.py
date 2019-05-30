from django.shortcuts import render
from django.forms import formset_factory
from django.contrib.admin.views.decorators import staff_member_required

from .forms import (
    ProofRowForm, ProofVerifyFormSet,
    PostulateRowForm, PostulateVerifyFormSet,
    NameForm
)   
from . import prover


def sandbox(request):
    my_template = "proof/sandbox.html"

    ProofForm = formset_factory(
        ProofRowForm, ProofVerifyFormSet, extra=1)

    context = {}
    context["reasons"] = prover.all_reason_names()
    if request.method == 'POST':
        formset = ProofForm(request.POST)
        if formset.is_valid():
            context["formset"] = formset
            context["valid"] = True
            return render(request, my_template, context)
    else:
        formset = ProofForm()

    context["formset"] = formset

    return render(request, my_template, context)

def theorize(request):
    my_template = "proof/theorize.html"

    ProofForm = formset_factory(
        ProofRowForm, ProofVerifyFormSet, extra=1)

    context = {}
    if request.method == 'POST':
        formset = ProofForm(request.POST)
        nameform = NameForm(request.POST)
        if formset.is_valid() and nameform.is_valid():
            new_theorem = prover.theorize(nameform.cleaned_data["name"], formset.plist)
            if new_theorem:
                prover.save_reason(new_theorem)
            context['valid'] = True
    else:
        formset = ProofForm()
        nameform = NameForm()
    
    context["formset"] = formset
    context["nameform"] = nameform

    return render(request, my_template, context)


@staff_member_required
def postulate(request):
    my_template = "proof/postulate.html"

    PostulateForm = formset_factory(
        PostulateRowForm, PostulateVerifyFormSet, extra=1)

    context = {}
    if request.method == 'POST':
        formset = PostulateForm(request.POST)
        nameform = NameForm(request.POST)
        if formset.is_valid() and nameform.is_valid():
            new_postulate = prover.postulate(nameform.cleaned_data["name"], formset.plist)
            if new_postulate:
                prover.save_reason(new_postulate)
            context["valid"] = True
    else:
        formset = PostulateForm()
        nameform = NameForm()

    context["formset"] = formset
    context["nameform"] = nameform

    return render(request, my_template, context)
