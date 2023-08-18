import tempfile
from PIL import Image
from menus.models import CafeItem, Category
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile

class CafeItemTestClass(TestCase) :
    @classmethod
    def setUpTestData(cls) -> None:
        # return super().setUpTestData()
        CafeItem.objects.create(name='Test', description='Just testing...')
    
    def test_name_label(self) :
        cafeitem = CafeItem.objects.get(id=1)
        field_label = cafeitem._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')
    
    def test_description_max_length(self):
        cafeitem = CafeItem.objects.get(id=1)
        max_length = cafeitem._meta.get_field('description').max_length
        self.assertEqual(max_length, 250)
    
    def test_name_max_length(self):
        cafeitem = CafeItem.objects.get(id=1)
        max_length = cafeitem._meta.get_field('name').max_length
        self.assertEqual(max_length, 50)


def get_temporary_image(temp_file):
    size = (200, 200)
    color = (255, 0, 0, 0)
    image = Image.new("RGBA", size, color)
    image.save(temp_file, 'jpeg')
    return temp_file
    



    # def setUp(self) -> None:
    #     return super().setUp()

