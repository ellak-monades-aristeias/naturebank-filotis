# -*- coding: utf-8 -*-
# UTF8 Encoded
from django import forms
from naturebank.models import (Biotope, DesignationOption, OwnerOption,
    SiteTypeOption, ClimateOption, EcologicalValueOption, SocialValueOption,
    CulturalValueOption, ThreatOption, HumanActivityOption, HabitationOption,
    Species)
from django.conf import settings


class BiotopeAdminForm(forms.ModelForm):

    species_multi = forms.ModelMultipleChoiceField(
        label="Είδη του τόπου",
        queryset=Species.objects.all(),
        required=False,help_text=("Χαρακτηριστικά είδη του τόπου. "
                                  "Για να επιλέξετε πολλά κρατήστε πατημέντο"
                                  " το κουμπί \"control\"!"))

    class Meta:
        model = Biotope
        fields = '__all__'

