from django import forms
from submissions.models import SubmissionCache

class SubmissionForm(forms.ModelForm):
    Source_Code = forms.CharField(widget=forms.Textarea(attrs={'data-editor':'text', 'rows':15, 'cols':80, 'maxlength':50000}))
# Change Maxlength to be dynamic as the max_src_code sz.
    class Meta():
        model = SubmissionCache
        fields = ('language',)
