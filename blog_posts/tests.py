from django.test import TestCase
import requests

# Create your tests here.

url = 'https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=f2bdd9f8160b478b81946f6f3900e172'
data = requests.get(url)
print(data.json())