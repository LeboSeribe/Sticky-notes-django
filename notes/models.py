# notes/models.py
from django.db import models


class StickyNote(models.Model):
    """Model representing a single sticky note.

    Fields:
    - title: CharField for the note's title, max length 255 characters.
    - content: TextField for the body of the note.
    - created_at: DateTimeField set automatically when the note is created.
    - updated_at: DateTimeField updated automatically every time the note is saved.

    Methods:
    - __str__: Returns a string representation of the note, showing the title.

    :param models.Model: Django's base model class.
    """

    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title
