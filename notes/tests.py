# notes/tests.py
from django.test import TestCase
from django.urls import reverse
from .models import StickyNote
from .forms import StickyNoteForm


class StickyNoteModelTest(TestCase):
    """Tests that check the StickyNote model itself behaves correctly."""

    def setUp(self):
        StickyNote.objects.create(
            title="Test Note", content="This is a test note."
        )

    def test_note_has_title(self):
        note = StickyNote.objects.get(id=1)
        self.assertEqual(note.title, "Test Note")

    def test_note_has_content(self):
        note = StickyNote.objects.get(id=1)
        
        self.assertEqual(note.content, "This is a test note.")

    def test_note_string_representation(self):
        note = StickyNote.objects.get(id=1)
        self.assertEqual(str(note), "Test Note")

    def test_note_has_timestamps(self):
        note = StickyNote.objects.get(id=1)
        self.assertIsNotNone(note.created_at)
        self.assertIsNotNone(note.updated_at)


class StickyNoteViewTest(TestCase):
    """Tests that check each view (list, detail, create, update, delete)
    returns the correct response and performs the correct database action.
    """

    def setUp(self):
        self.note = StickyNote.objects.create(
            title="Test Note", content="This is a test note."
        )

    def test_note_list_view(self):
        response = self.client.get(reverse("note_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Note")

    def test_note_detail_view(self):
        response = self.client.get(
            reverse("note_detail", args=[str(self.note.id)])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Note")
        self.assertContains(response, "This is a test note.")

    def test_note_create_view_get(self):
        response = self.client.get(reverse("note_create"))
        self.assertEqual(response.status_code, 200)

    def test_note_create_view_post(self):
        response = self.client.post(
            reverse("note_create"),
            {"title": "New Note", "content": "New note content."},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(StickyNote.objects.filter(title="New Note").exists())

    def test_note_update_view_post(self):
        response = self.client.post(
            reverse("note_update", args=[str(self.note.id)]),
            {"title": "Updated Note", "content": "Updated content."},
        )
        self.assertEqual(response.status_code, 302)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, "Updated Note")
        self.assertEqual(self.note.content, "Updated content.")

    def test_note_delete_view_post(self):
        response = self.client.post(
            reverse("note_delete", args=[str(self.note.id)])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            StickyNote.objects.filter(id=self.note.id).exists()
        )

    def test_note_delete_view_get_shows_confirmation(self):
        response = self.client.get(
            reverse("note_delete", args=[str(self.note.id)])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            StickyNote.objects.filter(id=self.note.id).exists()
        )


class StickyNoteFormTest(TestCase):
    """Tests that check the form correctly validates data."""

    def test_form_valid_with_title_and_content(self):
        form = StickyNoteForm(
            data={"title": "Valid Note", "content": "Valid content."}
        )
        self.assertTrue(form.is_valid())

    def test_form_invalid_without_title(self):
        form = StickyNoteForm(data={"title": "", "content": "Some content."})
        self.assertFalse(form.is_valid())