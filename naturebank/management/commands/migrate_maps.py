# -*- coding: utf-8 -*-
# UTF8 Encoded
from django.core.management.base import BaseCommand
from django.conf import settings
import os
from django.utils.encoding import DjangoUnicodeDecodeError
from naturebank.models import GeoCodeOption, BiotopeCategoryOption, CategoryGeoMap


class Command(BaseCommand):
    help = "Migration of maps"

    def handle(self, *args, **options):

        # Maps Handling
        for filename in os.listdir("%s/Maps" % settings.MEDIA_ROOT ):
            print filename
            category = filename[0:-7]
            code = filename[-7]+","+filename[-6]+","+filename[-5]
            try:
                a = GeoCodeOption.objects.get(code=code)
                if category=="AB":
                    b = BiotopeCategoryOption.objects.get(name=u"Άλλοι Βιότοποι")
                    CategoryGeoMap(geocode_map="Maps/" + filename,
                                   geo_code=a,
                                   category=b).save()
                elif category=="A0":
                    b = BiotopeCategoryOption.objects.get(name=u"CORINE(Αγγλικά)")
                    CategoryGeoMap(geocode_map="Maps/" + filename,
                                   geo_code=a,
                                   category=b).save()
                    b = BiotopeCategoryOption.objects.get(name=u"CORINE(Ελληνικά)")
                    CategoryGeoMap(geocode_map="Maps/" + filename,
                                   geo_code=a,
                                   category=b).save()
                elif category=="AT":
                    b = BiotopeCategoryOption.objects.get(name=u"ΤΙΦΚ")
                    CategoryGeoMap(geocode_map="Maps/" + filename,
                                   geo_code=a,
                                   category=b).save()
                elif category=="GR":
                    b = BiotopeCategoryOption.objects.get(name=u"NATURA")
                    CategoryGeoMap(geocode_map="Maps/" + filename,
                                   geo_code=a,
                                   category=b).save()
                elif category=="ALL":
                    CategoryGeoMap(geocode_map="Maps/" + filename,
                                   geo_code=a).save()
            except GeoCodeOption.DoesNotExist, BiotopeCategoryOption.DoesNotExist:
                print "Entry does not exist"
            except DjangoUnicodeDecodeError:
                continue
