from django import forms
from django.forms import ModelForm
from problems.models import Problem
class ProblemUploadForm(forms.ModelForm):
    class Meta:
        model = Problem
        widgets = {
            'problem_statement':forms.Textarea(attrs={'class':'editable'})
        }
        exclude = ('slug', 'setter',)
    def __init__(self, *args, **kwargs):
        super(ProblemUploadForm, self).__init__(*args, **kwargs)
        self.fields['problem_name'].label = 'Problem Name'
        self.fields['problem_statement'].label = 'Problem Statement'
        self.fields['time_limit'].label = 'Time Limit'
        self.fields['memory_limit'].label = 'Memory Limit'
        self.fields['src_code_size'].label = 'Source Code Size'
        self.fields['solution_file'].label = 'Solution File'
        self.fields['test_file'].label = 'Input Test File Zip'
        self.fields['score'].label = 'Score'
