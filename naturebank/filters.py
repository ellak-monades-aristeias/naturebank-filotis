# -*- coding: utf-8 -*-
from string import ascii_letters
import django_filters
from models import Biotope, Species, GeoCodeOption,\
                   BiotopeCategoryOption
                   

ASCII_LETTERS = ascii_letters[26:]

class NomoiFilter(django_filters.ChoiceFilter):
    @property
    def field(self):
        ts = GeoCodeOption._default_manager.filter(code__regex=r'[1-9]\,0$')
        ts = ts.extra(order_by = ['code'])
        rs = GeoCodeOption._default_manager.filter(code__endswith=u',0,0')
        qs = GeoCodeOption._default_manager.filter(name__startswith=u'Νομός')
        self.extra['choices'] = [("", "Όλες")]
        self.extra['choices'].extend([(o.code, o) for o in rs])
        self.extra['choices'].extend([(o.code, o) for o in ts])
        self.extra['choices'].extend([(o.code, o) for o in qs])
        return super(NomoiFilter, self).field

class CategoryFilter(django_filters.ChoiceFilter):
    @property
    def field(self):
        qs = BiotopeCategoryOption._default_manager.all().exclude(id=5)
        self.extra['choices'] = [("", "Όλοι")]
        self.extra['choices'].extend([(o.id, o) for o in qs])
        return super(CategoryFilter, self).field

class BiotopeFilter(django_filters.FilterSet):
    geo_code = NomoiFilter(label=u'Γεωγραφική Περιοχή')
    category = CategoryFilter(label=u'Κατηγορία Τόπου')
    class Meta:
        model = Biotope
        fields = ['category', 'geo_code', ]

class AlphabeticalFilter(django_filters.ChoiceFilter):
    """A filter to show only entries starting with a specific letter."""
    @property
    def field(self):
        self.extra['choices'] = [("", "---------")]
        self.extra['choices'].extend([(l, l) for l in ASCII_LETTERS])
        return super(AlphabeticalFilter, self).field

class SpeciesFilter(django_filters.FilterSet):
    species_name = AlphabeticalFilter(label=u'Αλφαβητική Επιλογή',
                                      lookup_type='startswith',
                                      widget=django_filters.widgets.LinkWidget)
    class Meta:
        model = Species
        fields = ['species_category', 'plant_kind', 'species_name']
