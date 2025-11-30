from django import forms
from .models import project

class projectInformForm(forms.ModelForm):
    class Meta:
        model = project
        fields = ['name', 'description', 'start_date', 'end_date', 'status']
        widgets = {'start_date': forms.DateInput(attrs={'type': 'date'}),
                   'end_date': forms.DateInput(attrs={'type': 'date'})}
        
    def clean_status(self):
        status = self.cleaned_data.get('status')
        valid_statuses = ['not started', 'in progress', 'completed']
        if status not in valid_statuses:
            raise forms.ValidationError(f"Status must be one of {valid_statuses}.")
        return status
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("End date must be after start date.")
        return cleaned_data
    
    def save(self, commit=True):
        project_instance = super().save(commit=False)
        # Additional processing can be done here
        if commit:
            project_instance.save()
        return project_instance
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'    
        self.fields['description'].widget.attrs['rows'] = 4
        self.fields['description'].widget.attrs['placeholder'] = 'Enter project description here...'
        self.fields['name'].widget.attrs['placeholder'] = 'Enter project name here...'
        self.fields['status'].widget.attrs['placeholder'] = 'Select project status...'
        self.fields['start_date'].widget.attrs['placeholder'] = 'Select start date...'
        self.fields['end_date'].widget.attrs['placeholder'] = 'Select end date...'  
        self.fields['status'].choices = [
            ('not started', 'Not Started'),
            ('in progress', 'In Progress'),
            ('completed', 'Completed')
        ]
        self.fields['status'].initial = 'not started'
        self.fields['name'].label = 'Project Name'
        self.fields['description'].label = 'Project Description'
        self.fields['start_date'].label = 'Start Date'
        self.fields['end_date'].label = 'End Date'
        self.fields['status'].label = 'Project Status'
        self.fields['name'].help_text = 'Enter the name of the project.'
        self.fields['description'].help_text = 'Provide a brief description of the project.'
        self.fields['start_date'].help_text = 'Select the project start date.'
        self.fields['end_date'].help_text = 'Select the project end date.'
        self.fields['status'].help_text = 'Choose the current status of the project.'
        self.fields['name'].required = True
        self.fields['description'].required = False
        self.fields['start_date'].required = True
        self.fields['end_date'].required = True
        self.fields['status'].required = True
        self.fields['description'].widget.attrs['maxlength'] = 500
        self.fields['name'].widget.attrs['maxlength'] = 100 
        self.fields['name'].widget.attrs['autofocus'] = True

        self.fields['description'].widget.attrs['style'] = 'resize:none;'