from django.forms import Form, CharField, EmailField, Textarea

class EmailPostForm(Form):
    name = CharField(max_length=25, label="Your name")
    email = EmailField(label="Your email")
    to = EmailField(label="Recipient's email")
    comments = CharField(required=False,widget=Textarea)
