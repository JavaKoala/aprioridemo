from django.test import TestCase, Client
from .models import DataSet

client = Client()

def create_data_set():
  with open('sample-datafiles/Market_Basket_Optimisation_min.csv') as fp:
    client.post('/apriori/', {'datafile': fp})

class ViewIndexTests(TestCase):
  def test_get_no_datafiles(self):
    response = client.get('/apriori/')
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "No documents.")
    self.assertQuerysetEqual(response.context['data_sets'], [])

  def test_get_datafiles(self):
    create_data_set()
    response = client.get('/apriori/')
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "Market_Basket_Optimisation_min")
    self.assertQuerysetEqual(response.context['data_sets'], ['<DataSet: DataSet object (1)>'])

  def test_post(self):
    with open('sample-datafiles/Market_Basket_Optimisation.csv') as fp:
      response = client.post('/apriori/', {'datafile': fp})
    self.assertEqual(response.status_code, 302)

class ViewShowTests(TestCase):
  def test_get_datafile(self):
    create_data_set()
    response = client.get('/apriori/1/')
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "Market_Basket_Optimisation_min")

