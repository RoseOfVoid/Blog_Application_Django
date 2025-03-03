from django.forms import Form, CharField, EmailField, Textarea, ModelForm

from blog.models import Comment


class EmailPostForm(Form):
    name = CharField(max_length=25, label="Your name")
    email = EmailField(label="Your email")
    to = EmailField(label="Recipient's email")
    comments = CharField(required=False,widget=Textarea)


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']


class SearchForm(Form):
    query = CharField()