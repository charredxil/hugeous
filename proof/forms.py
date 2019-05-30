from django import forms
from django.forms import BaseFormSet, ValidationError, formset_factory

from .prover import verify, theorize, make_proof, load_base_reasons, all_reason_names
from .models import Reason

# PROOF


class ProofRowForm(forms.Form):
    statement = forms.CharField(label="", max_length=50, required=True)
    reason = forms.ChoiceField(label="", choices=all_reason_names, required=True)

    def clean_reason(self):
        reason = self.cleaned_data["reason"]
        if not Reason.objects.filter(name=reason).exists():
            raise ValidationError(
                "Reason \"{}\" does not exist".format(reason))
        return reason


class ProofVerifyFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(ProofVerifyFormSet, self).__init__(*args, **kwargs)
        self.proof = None
        self.result_system = None
        for form in self.forms:
            form.empty_permitted = False

    def clean(self):
        if any(self.errors):
            return
        proof = []
        for form in self.forms:
            reason = form.cleaned_data["reason"]
            statement = form.cleaned_data["statement"]
            proof.append((reason, statement))
        load_base_reasons()
        self.proof = make_proof(proof)
        self.result_system = verify(self.proof)
        if not self.result_system:
            raise ValidationError("Invalid proof")

# POSTULATE


class PostulateRowForm(forms.Form):
    statement = forms.CharField(label="", max_length=50, required=True)


class PostulateVerifyFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(PostulateVerifyFormSet, self).__init__(*args, **kwargs)
        self.plist = None
        for form in self.forms:
            form.empty_permitted = False

    def clean(self):
        if any(self.errors):
            return
        implication = False
        self.plist = []
        for form in self.forms:
            statement = form.cleaned_data["statement"]
            self.plist.append(statement)
            if "implies" in statement:
                implication = True
                break
        self.plist = [self.plist]
        if not implication:
            raise ValidationError(
                "Postulates require at least one implication")


class NameForm(forms.Form):
    name = forms.CharField(label="", max_length=50, required=True)
    def clean_name(self):
        name = self.cleaned_data["name"]
        if Reason.objects.filter(name=name).exists():
            raise ValidationError(
                "Reason with name \"{}\" already exists".format(name))
        return name
