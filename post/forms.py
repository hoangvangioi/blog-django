from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from mptt.forms import TreeNodeChoiceField
from tinymce.widgets import TinyMCE

from .models import Comment, Post


class PostForm(forms.ModelForm):
    title = forms.CharField(
        error_messages={'invalid': "Phone number have 4-25 digits and may start with '+'."},
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                    'placeholder': 'Nhập tiêu đề bài viết'
            }
        )
    )
    body = forms.CharField(
        # widget= CKEditorWidget(

        # )
        required=False,


        widget=CKEditorUploadingWidget(
            attrs={
                'class': 'form-control'
            }
        )
    )
    # previous_post = forms.ModelChoiceField(
    #         queryset=Post.published.all(),
    #         label='Bài trước')

    # next_post = forms.ModelChoiceField(
    #         queryset=Post.published.all(),
    #         label='Bài sau')

    featured_image = forms.ImageField(required=True, 
        widget=forms.FileInput(attrs={
            'class': 'form-control'
            }))

    class Meta:
        model = Post
        fields = ('title', 
                'body', 
                'previous_post', 
                'next_post', 
                'featured_image',
                'category',
                'status',
                'tags',
                )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['previous_post'].widget.attrs['class'] = 'form-control'
        self.fields['next_post'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['class'] = 'form-control'
        self.fields['tags'].widget.attrs['class'] = 'form-control'



class CommentForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=Comment.objects.all())
    content = forms.CharField(
        widget=TinyMCE(
            attrs={'cols': 3, 'rows': 3}
            )
            )
    # content = forms.CharField(widget = CKEditorWidget())
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['parent'].widget.attrs.update(
            {'class': 'd-none'}
            )
        self.fields['parent'].label = ''
        self.fields['parent'].required = False

    class Meta:
        model = Comment
        fields = ('parent', 'content')

    def save(self, *args, **kwargs):
        Comment.objects.rebuild()
        return super(CommentForm, self).save(*args, **kwargs)









from django import forms
from django.core.validators import RegexValidator


class NameWidget(forms.MultiWidget):

    def __init__(self, attrs=None):
        super().__init__([
            forms.TextInput(),
            forms.TextInput()
        ], attrs)

    def decompress(self, value):
        if value:
            return value.split(' ')
        return ['', '']

class NameField(forms.MultiValueField):

    widget = NameWidget

    def __init__(self, *args, **kwargs):

        fields = (
            forms.CharField(validators=[
                RegexValidator(r'[a-zA-Z]+', 'Enter a valid first name (only letters)')
            ]),
            forms.CharField(validators=[
                RegexValidator(r'[a-zA-Z]+', 'Enter a valid second name (only letters)')
            ])
        )

        super().__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        return f'{data_list[0]} {data_list[1]}'




class ContactForm(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    message = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(),
        help_text='Write here your message!'
    )
    source = forms.CharField(
        max_length=50,
        widget=forms.HiddenInput()
    )

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        message = cleaned_data.get('message')
        if not name and not email and not message:
            raise forms.ValidationError('You have to write something!')


class HTMLField(forms.Field):
    def __init__(self, attrs=None, *args, **kwargs):
        self.error_messages = {}
        self.label_suffix = None
        self.help_text = None
        self.label = ''
        self.initial = ''
        self.required = False
        self.attrs = {'id': False}
        self.show_hidden_initial = False
        self.localize = False
        self.disabled = False
        self.is_hidden = False



from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.core.exceptions import ValidationError
from django.forms import fields, forms, widgets
from django.utils.timezone import datetime


def validate_password(value):
    pwhasher = PBKDF2PasswordHasher()
    if not pwhasher.verify(value, 'pbkdf2_sha256$216000$salt$NBY9WN4TPwv2NZJE57BRxccYp0FpyOu82J7RmaYNgQM='):
        raise ValidationError("The password is wrong.")


class CompleteForm(forms.Form):
    """
    This form contains all standard widgets, Django provides out of the box.
    """
    CONTINENT_CHOICES = [
        ('', "––– please select –––"), ('am', "America"), ('eu', "Europe"), ('as', "Asia"),
        ('af', "Africa"), ('au', "Australia"), ('oc', "Oceania"), ('an', 'Antartica'),
    ]

    TRANSPORTATION_CHOICES = [
        ("Private Transport", [('foot', "Foot"), ('bike', "Bike"), ('mc', "Motorcycle"), ('car', "Car")]),
        ("Public Transport", [('taxi', "Taxi"), ('bus', "Bus"), ('train', "Train"), ('ship', "Ship"), ('air', "Airplane")]),
    ]

    NOTIFY_BY = [
        ('postal', "Letter"), ('email', "EMail"), ('phone', "Phone"), ('sms', "SMS"),
    ]

    last_name = fields.CharField(
        label="Last name",
        min_length=2,
        max_length=50,
        help_text="Please enter at least two characters",
    )

    first_name = fields.RegexField(
        r'^[A-Z][a-z -]*$',
        label="First name",
        error_messages={'invalid': "A first name must start in upper case."},
        help_text="Must start in upper case followed by one or more lowercase characters.",
    )

    gender = fields.ChoiceField(
        label="Gender",
        choices=[('m', "Male"), ('f', "Female")],
        widget=widgets.RadioSelect,
        error_messages={'invalid_choice': "Please select your gender."},
    )

    email = fields.EmailField(
        label="E-Mail",
        help_text="Please enter a valid email address",
    )

    subscribe = fields.BooleanField(
        label="Subscribe Newsletter",
        initial=False,
        required=False,
    )

    phone = fields.RegexField(
        r'^\+?[0-9 .-]{4,25}$',
        label="Phone number",
        error_messages={'invalid': "Phone number have 4-25 digits and may start with '+'."},
        widget=fields.TextInput(attrs={'hide-if': 'subscribe'})
    )

    birth_date = fields.DateField(
        label="Date of birth",
        widget=widgets.DateInput(attrs={'type': 'date', 'pattern': r'\d{4}-\d{2}-\d{2}'}),
        help_text="Allowed date format: yyyy-mm-dd",
    )

    continent = fields.ChoiceField(
        label="Living on continent",
        choices=CONTINENT_CHOICES,
        required=True,
        initial='',
        error_messages={'invalid_choice': "Please select your continent."},
    )

    weight = fields.IntegerField(
        label="Weight in kg",
        min_value=42,
        max_value=95,
        error_messages={'min_value': "You are too lightweight.", 'max_value': "You are too obese."},
    )

    height = fields.FloatField(
        label="Height in meters",
        min_value=1.45,
        max_value=1.95,
        widget=widgets.NumberInput(attrs={'step': 0.01}),
        error_messages={'max_value': "You are too tall."},
    )

    used_transportation = fields.MultipleChoiceField(
        label="Used Tranportation",
        choices=TRANSPORTATION_CHOICES,
        widget=widgets.CheckboxSelectMultiple,
        required=True,
        help_text="Used means of tranportation.",
    )

    preferred_transportation = fields.ChoiceField(
        label="Preferred Transportation",
        choices=TRANSPORTATION_CHOICES,
        widget=widgets.RadioSelect,
        help_text="Preferred mean of tranportation.",
    )

    available_transportation = fields.MultipleChoiceField(
        label="Available Tranportation",
        choices=TRANSPORTATION_CHOICES,
        help_text="Available means of tranportation.",
    )

    notifyme = fields.MultipleChoiceField(
        label="Notification",
        choices=NOTIFY_BY,
        widget=widgets.CheckboxSelectMultiple,
        required=True,
        help_text="Must choose at least one type of notification",
    )

    annotation = fields.CharField(
        label="Annotation",
        required=True,
        widget=widgets.Textarea(attrs={'cols': '80', 'rows': '3'}),
    )

    agree = fields.BooleanField(
        label="Agree with our terms and conditions",
        initial=False,
    )

    password = fields.CharField(
        label="Password",
        widget=widgets.PasswordInput,
        validators=[validate_password],
        help_text="The password is 'secret'",
    )

    confirmation_key = fields.CharField(
        max_length=40,
        required=True,
        widget=widgets.HiddenInput(),
        initial='hidden value',
    )


sample_complete_data = {
    'first_name': "John",
    'last_name': "Doe",
    'gender': 'm',
    'email': 'john.doe@example.org',
    'subscribe': True,
    'phone': '+1 234 567 8900',
    'birth_date': datetime(year=2000, month=5, day=18),
    'continent': 'eu',
    'available_transportation': ['foot', 'taxi'],
    'preferred_transportation': 'car',
    'used_transportation': ['foot', 'bike', 'car', 'train'],
    'height': 1.82,
    'weight': 81,
    'traveling': ['bike', 'train'],
    'notifyme': ['email', 'sms'],
    'annotation': "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    'password': 'secret',
}