from django.test import TestCase
from product.serializers import ProductGetPostSerializer
from .models import Product

class AnimalTestCase(TestCase):
    # def setUp(self):
    #     Animal.objects.create(name="lion", sound="roar")
    #     Animal.objects.create(name="cat", sound="meow")

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        # Create your tests here.
        p = Product(name="test", price="10", category_id=1)
        serializer = ProductGetPostSerializer(p)
        print(serializer.data)

