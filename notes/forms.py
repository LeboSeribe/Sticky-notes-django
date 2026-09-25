# notes/forms.py
from django import forms
from .models import StickyNote


class StickyNoteForm(forms.ModelForm):
    """Form for creating and updating StickyNote objects.

    Fields:
    - title: CharField for the note title.
    - content: TextField for the note content.

    Meta class:
    - Defines the model to use (StickyNote) and the fields to include in the form.

    :param forms.ModelForm: Django's ModelForm class.
    """

    class Meta:
        model = StickyNote
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Note title"}),
            "content": forms.Textarea(attrs={"rows": 6, "placeholder": "Write your note..."}),
        }
