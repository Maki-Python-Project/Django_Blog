from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)

    def clean(self):
        cleaned_data = super().clean()
        comment_text = cleaned_data.get('text')

        if comment_text:
            if len(comment_text) < 3:
                raise forms.ValidationError(
                    'The comment must contain at least 3 characters'
                )
        return cleaned_data
