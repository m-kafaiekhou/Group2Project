import tempfile
import datetime
from PIL import Image
from menus.models import CafeItem, Category
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile

class CafeItemTestClass(TestCase) :
    @classmethod
    def setUpTestData(cls) -> None:
        cls.category = Category.objects.create(name="Test Category")
        # return super().setUpTestData()
        cls.cafeitem = CafeItem.objects.create(
            name='Test', 
            description='Just testing...',
            is_available=True,
            price=50,
            category=cls.category,
        )
    
    def test_create_cafeitem(self) :
        self.assertEqual(self.cafeitem.name, "Test")
        self.assertEqual(self.cafeitem.description, 'Just testing...')
        self.assertEqual(self.cafeitem.is_available, True)
        self.assertEqual(self.cafeitem.price, 50)
        self.assertEqual(self.cafeitem.category, self.category)
        self.assertIsInstance(self.cafeitem.date_added, datetime.datetime)
    
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

    def test_str_method(self):
        expected_str = "Test"
        self.assertEqual(str(self.name), expected_str)

    def test_slug_method(self):
        expected_slug = "Test"
        self.assertEqual(slugify(self.name), expected_slug)


def get_temporary_image(temp_file):
    size = (200, 200)
    color = (255, 0, 0, 0)
    image = Image.new("RGBA", size, color)
    image.save(temp_file, 'jpeg')
    return temp_file
    

class CafeItemImageTestClass(TestCase):
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_image(self):
        temp_file = tempfile.NamedTemporaryFile()
        test_image = get_temporary_image(temp_file)
        #test_image.seek(0)
        CafeItem.image.objects.create(picture=test_image.name)
        self.assertEqual(len(CafeItem.image.objects.all()), 1)


    # def setUp(self) -> None:
    #     return super().setUp()

