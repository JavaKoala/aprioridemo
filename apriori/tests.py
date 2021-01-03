import os
from django.test import TestCase, Client
from .models import DataSet
from os import remove

client = Client()

def create_data_set():
  with open('sample-datafiles/Market_Basket_Optimisation_min.csv') as fp:
    client.post('/apriori/', {'datafile': fp})

def remove_data_set(data_set_id):
  data_set = DataSet.objects.get(pk=data_set_id)

  if os.path.exists(data_set.datafile.name):
      os.remove(data_set.datafile.name)

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
    remove_data_set(1)

  def test_post(self):
    with open('sample-datafiles/Market_Basket_Optimisation.csv') as fp:
      response = client.post('/apriori/', {'datafile': fp})
    self.assertEqual(response.status_code, 302)
    remove_data_set(1)

class ViewShowTests(TestCase):
  def test_get_datafile(self):
    create_data_set()
    response = client.get('/apriori/1/')
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "Market_Basket_Optimisation_min")
    remove_data_set(1)

class ViewDeleteTests(TestCase):
  def test_delete_datafile(self):
    create_data_set()
    response = client.post('/apriori/delete/1/')
    self.assertEqual(response.status_code, 302)
    self.assertEqual(DataSet.objects.count(), 0)
