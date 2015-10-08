from urllib import quote_plus

from django.test import Client, TestCase

from naturebank.models import Biotope, BiotopeCategoryOption, GeoCodeOption, \
    Species, SpeciesBiotope, SpeciesCategoryOption


class DataTestCase(TestCase):
    """
    A testing super class that has methods for creating data.
    """

    def create_test_categories(self):
        # We must not use id=5 for a category. See
        # BiotopeListView.get_queryset() for the reason. We therefore create
        # and delete five dummy categories to ensure we skip it.
        [BiotopeCategoryOption.objects.create(name=x) for x in '12345']
        BiotopeCategoryOption.objects.all().delete()

        # And now we go on to create our actual test categories
        self.categories = {
            'natura': BiotopeCategoryOption.objects.create(name='NATURA'),
            'corine': BiotopeCategoryOption.objects.create(name='CORINE'),
        }

    def create_test_data(self):

        # Categories
        self.create_test_categories()

        # Areas (aka GeoCodeOption)
        areas = {
            'central_greece': '2,0,0',
            'ionian_islands': '2,2,0',
            'kerkyra':        '2,2,3',
            'lefkada':        '2,2,4',
            'epirus':         '2,1,0',
            'arta':           '2,1,1',
            'thesprotia':     '2,1,2',
        }
        self.areas = {item: GeoCodeOption.objects.create(code=areas[item],
                                                         name=item)
                      for item in areas}

        # Biotopes
        biotopes = {
            'Corfu natural marshes':    ['GR01', 'natura', 'kerkyra'],
            'Corfu corinal forests':    ['GR02', 'corine', 'kerkyra'],
            'Lefkada natural lowlands': ['GR03', 'natura', 'lefkada'],
            'Lefkada corinal woods':    ['GR04', 'corine', 'lefkada'],
            'Arta natural springs':     ['GR05', 'natura', 'arta'],
            'Arta corinal highlands':   ['GR06', 'corine', 'arta'],
            'Thesprotia natural lakes': ['GR07', 'natura', 'thesprotia'],
            'Thesprotia corinal seas':  ['GR08', 'corine', 'thesprotia'],
        }
        for bname in biotopes:
            site_code, category_name, area_name = biotopes[bname]
            category = self.categories[category_name]
            area = self.areas[area_name]
            Biotope.objects.create(site_name=bname, site_name_gr=bname,
                                   site_code=site_code, category=category,
                                   geo_code=area)

        # Species types (aka SpeciesCategoryOption)
        self.species_types = {
            x: SpeciesCategoryOption.objects.create(name=x,
                                                    abbreviation=x.upper()[:4])
            for x in ('Amphibian', 'Bird', 'Fish', 'Flora', 'Invertebrate',
                      'Mammal', 'Reptile')
        }

        # Species
        species = {
            666: ['Freeway',  'Frog',         'Amphibian'],
            667: ['Highway',  'Toad',         'Amphibian'],
            999: ['Enhydris', 'Enhydris',     'Reptile'],
            998: ['Bitia',    'Hydroides',    'Reptile'],
            997: ['Erpeton',  'Tentaculatum', 'Reptile'],
        }
        for scode in species:
            species_name, sub_species_name, species_type_name = species[scode]
            species_type = self.species_types[species_type_name]
            Species.objects.create(species_code=scode,
                                   species_name=species_name,
                                   sub_species=sub_species_name,
                                   species_category=species_type)

        # Specify that Freeway Frog is found in Lefkada
        lefkada_biotopes = Biotope.objects.filter(
            geo_code=GeoCodeOption.objects.get(name='lefkada'))
        freeway_frog = Species.objects.get(species_code=666)
        for b in lefkada_biotopes:
            SpeciesBiotope.objects.create(species=freeway_frog, biotope=b)


class BiotopeListViewTest(DataTestCase):

    def setUp(self):
        self.create_test_data()

    def test_biotope_list(self):
        c = Client()
        response = c.get('/biotopes/?category={}&geo_code={}'.format(
            self.categories['natura'].id, quote_plus('2,2,0')))
        self.assertContains(response, 'GR01', status_code=200)
        self.assertContains(response, 'GR03', status_code=200)
        self.assertNotContains(response, 'GR02', status_code=200)
        self.assertNotContains(response, 'GR04', status_code=200)
        self.assertNotContains(response, 'GR05', status_code=200)
        self.assertNotContains(response, 'GR06', status_code=200)
        self.assertNotContains(response, 'GR07', status_code=200)
        self.assertNotContains(response, 'GR08', status_code=200)

    def test_biotope_list_2(self):
        """
        This is the same as test_biotope_list above, except that the url
        also contains an empty site_type= parameter; this is in order to guard
        against a bug where if an empty parameter were supplied a 404 was
        raised.
        """
        c = Client()
        response = c.get(
            '/biotopes/?site_type=&category={}&geo_code={}'
            .format(self.categories['natura'].id, quote_plus('2,2,0')))
        self.assertContains(response, 'GR01', status_code=200)
        self.assertContains(response, 'GR03', status_code=200)
        self.assertNotContains(response, 'GR02', status_code=200)
        self.assertNotContains(response, 'GR04', status_code=200)
        self.assertNotContains(response, 'GR05', status_code=200)
        self.assertNotContains(response, 'GR06', status_code=200)
        self.assertNotContains(response, 'GR07', status_code=200)
        self.assertNotContains(response, 'GR08', status_code=200)


class SpeciesListViewTestCase(DataTestCase):

    def setUp(self):
        self.create_test_data()

    def test_species_list(self):
        c = Client()
        response = c.get('/species/?species_category=' +
                         str(self.species_types['Amphibian'].id))
        self.assertContains(response, 'Freeway', status_code=200)
        self.assertContains(response, 'Highway', status_code=200)
        self.assertNotContains(response, 'Enhydris', status_code=200)
        self.assertNotContains(response, 'Bitia', status_code=200)
        self.assertNotContains(response, 'Erpeton', status_code=200)


class SpeciesDetailViewTestCase(DataTestCase):

    def setUp(self):
        self.create_test_data()

    def test_sort(self):
        c = Client()
        aid = Species.objects.get(species_code=666).id

        # Don't specify sort; should be sorted by category
        response = c.get(u'/species/d/{}/'.format(aid))
        self.assertEqual(response.status_code, 200)
        self.assertInHTML("""
                          <tr class="even">
                            <td><a href="/biotopes/c/GR03/">GR03</a></td>
                            <td><a href="/biotopes/c/GR03/">Lefkada natural
                              lowlands</a></td>
                            <td>NATURA</td>
                            <td>lefkada</td>
                          </tr>
                          """, response.content)

        # Sort by biotope code; this time GR03 should be in an odd row
        # (first)
        response = c.get(u'/species/d/{}/?sort=site_code'.format(aid))
        self.assertInHTML("""
                          <tr class="odd">
                            <td><a href="/biotopes/c/GR03/">GR03</a></td>
                            <td><a href="/biotopes/c/GR03/">Lefkada natural
                              lowlands</a></td>
                            <td>NATURA</td>
                            <td>lefkada</td>
                          </tr>
                          """, response.content)

        # Try to sort by a field that does not exist; should be the same as
        # no sort
        response = c.get(u'/species/d/{}/?sort=nonexistent'.format(aid))
        self.assertEqual(response.status_code, 200)
        self.assertInHTML("""
                          <tr class="even">
                            <td><a href="/biotopes/c/GR03/">GR03</a></td>
                            <td><a href="/biotopes/c/GR03/">Lefkada natural
                              lowlands</a></td>
                            <td>NATURA</td>
                            <td>lefkada</td>
                          </tr>
                          """, response.content)


class BiotopeDetailViewTest(DataTestCase):

    def setUp(self):
        self.create_test_data()

    def test_biotope_detail_by_code(self):
        c = Client()

        # We will test with GR04, let's find its id.
        gr04_id = Biotope.objects.get(site_code='GR04').id

        # Get it by site_code
        response = c.get('/biotopes/c/GR04/')
        self.assertContains(response, 'Lefkada corinal woods', status_code=200)

        # Get it by id
        response = c.get('/biotopes/d/{}/'.format(gr04_id))
        self.assertContains(response, 'Lefkada corinal woods', status_code=200)
