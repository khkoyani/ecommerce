from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=160, label='Name: ',
                            widget=forms.TextInput(
                                attrs={'placeholder': 'Enter Your Name',
                                       'class': 'form-control',
                                       'id': 'form-full-name'}))
    email = forms.EmailField(required=True, label="Email Address:",
                             widget=forms.EmailInput(
                                 attrs={'placeholder': 'Enter your email address',
                                        'class': 'form-control'}))
    message = forms.CharField(label='Message',
                              widget=forms.Textarea(
                                  attrs={'placeholder': 'Enter Your Message',
                                         'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data.get("email")
        print(1)
        if '.com' not in email:
            print(2)
            raise forms.ValidationError('Email has to contain ".com"')
        return email