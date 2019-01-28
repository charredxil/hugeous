from django import forms
from django.forms import BaseFormSet, ValidationError

from .prover import verify, theorize, make_proof, load_base_reasons
from .models import Reason

class ProofRowForm(forms.Form):
    statement = forms.CharField(label="", max_length = 50, required=True)
    reason    = forms.CharField(label="", max_length = 100, required=True)
    def clean_reason(self):
        reason = self.cleaned_data["reason"]
        if not Reason.objects.filter(name=reason).exists():
            raise ValidationError("Reason \"{}\" does not exist".format(reason))
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
        self.proof  = make_proof(proof)
        self.result_system  = verify(self.proof)
        if not self.result_system:
            raise ValidationError("Invalid proof")
