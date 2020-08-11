from datetime import datetime
from django.test import TestCase

from .models import Faculty


class FacultyModelTest(TestCase):

    def test_color_as_hex(self):
        """
        color_as_hex() returns valid hex-color
        """
        faculty = Faculty(
            name='Maschinenbau',
            slug='fmb',
            color='ABC123',
            deadline=datetime.now(),
        )
        self.assertEqual(faculty.color_as_hex(), '#ABC123')
