# -*- coding: utf-8 -*-
# UTF8 Encoded
from naturebank.models import *
from django.contrib.gis import admin
#from django.contrib import admin
from naturebank.forms import BiotopeAdminForm

##########################################
class SpeciesBiotopeInline(admin.TabularInline):
    model = SpeciesBiotope
    extra = 3
    raw_id_fields = ("species",)

class BiotopeSupplInline(admin.StackedInline):
    model = Biotope
    #FIXME: patch for collapsing can be used here
    #classes = ['collapse', 'collapsed']
    extra = 1

class SpeciesBiotopeAdmin(admin.ModelAdmin):
    list_display = [f.name for f in SpeciesBiotope._meta.fields]
    fieldsets = (
        (None, {
            'fields': ('species', 'biotope', 'abundance'),
        }),
    )

admin.site.register(SpeciesBiotope, SpeciesBiotopeAdmin)

class BiotopeImageInline(admin.TabularInline):
    classes = ['collapse']
    extra = 1
    model = BiotopeImage

class BiotopeAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.display_srid=4326
        admin.ModelAdmin.__init__(self, model, admin_site)
    list_display = ('site_code', 
                    'site_name_gr', 
                    'geo_code',
                    'category',
                    'creation_date', 
                    'update_date')
    list_filter = ('category',
                   'update_date',
                   'knowledge',
                   'conservation',
                   'social_reaction',
                   'condition')
    search_fields = ('site_code',
                     'site_name_gr',
                     'geo_code__name',
                     'category__name')
    ordering = ('site_name_gr',)
    list_display_links = ('site_code', 'site_name_gr')
    # Uncomment to use the custom ModelForm
    #form = BiotopeAdminForm
    fieldsets = (
        (None, {
            'fields': ('site_code', ('site_name', 'site_name_gr'),'category',
            ('creation_date','update_date'),
            ('main_char_biotopos', 'main_char_natural', 'main_char_built'),
            'reg_wide', ('comp_code', 'comp_name'), 
            # Uncomment to enable these extra fields of the DB
            # 'restore', 'introduct', 'intro_text', 'develop',
            'respondent',),
        }),
        ('GIS', {
            'classes': ('collapse',),
            'fields': ('gis_sitecode', 'gis_area', 'gis_perimeter'),
        }),
        ('Γεωγραφική Τοποθέτηση', {
            'classes': ('collapse',),
            'fields': ('geo_code','dist_name', 'reg_mun',
                       'area', 'area_l', 'area_s',
                       'long_deg', 'long_min', 'long_sec',
                       'lat_deg', 'lat_min', 'lat_sec',
                       'length_max', 'width_max',
                       'alt_mean', 'alt_max', 'alt_min'),
        }),
        ('Γνώση', {
            'classes': ('collapse',),
            'fields': ('knowledge', 'designation'),
        }),
        ('Προστασία', {
            'classes': ('collapse',),
            'fields': ('protection',
                       ('measures_take','measures_need'),
                       'social_reaction',
                       'social_reaction_text',
                       'conservation',
                       'owner',
                       'ownership_text',
                      ),
        }),
        ('Χαρακτηριστικά', {
            'classes': ('collapse',),
            'fields': ('site_type',
                       'climate',
                       'condition',
                       'trend',
                       'trend_text',
                       'abandon',
                       'geology',
                       'characteristics',
                       'history',
                      ),
        }),
        ('Αξίες', {
            'classes': ('collapse',),
            'fields': ('ecological_value',
                       'social_value',
                       'cultural_value',
                       'quality',
                      ),
        }),
        ('Κίνδυνοι', {
            'classes': ('collapse',),
            'fields': ('threat',
                       'threat_text',
                       'vulnerability',
                       ),
        }),
        ('Ανθρώπινη Παρουσία', {
            'classes': ('collapse',),
            'fields': ('population',
                       'landvalue',
                       'trend_pop',
                       'human_activity',
                       'tourism',
                       'infrastructure',
                       'view',
                       'path',
                       ),
        }),
        ('Πανίδα και Χλωρίδα', {
            'classes': ('collapse',),
            'fields': ('habitation',
                       # Uncomment if custom ModelForm is used
                       #'species_multi',
                       'species_text',
                       ),
        }),
        ('Τεκμηρίωση', {
            'classes': ('collapse',),
            'fields': ('document',),
        }),
# Uncomment if u want to enable extra DB fields
#        ('Kωδικοί περιοχών', {
#            'classes': ('collapse',),
#            'fields': (('reg_code_1', 'reg_code_2', 'reg_code_3', 'reg_code_4')),
#        }),
#        ('Πυρκαγιές', {
#            'classes': ('collapse',),
#            'fields': (('fire_50', 'fire_3050', 'fire_1030', 'fire_10'),
#                        'fire_text'),
#        }),
    )
    filter_horizontal = ('designation',
                         'owner',
                         'site_type',
                         'climate',
                         'ecological_value',
                         'social_value',
                         'cultural_value',
                         'threat',
                         'human_activity',
                         'habitation',)

# Uncomment all the following lines if custom ModelForm is used!
#    def get_form(self, request, obj=None, **kwargs):
#        if obj:
#            self.form.base_fields['species_multi'].initial = list(obj.species.all())
#            
#        return super(BiotopeAdmin, self).get_form(request, obj) 

#    def save_model(self, request, obj, form, change):
#        # Clear first and then set
#        SpeciesBiotope.objects.filter(biotope=obj).delete()
#        for spec in form.cleaned_data['species_multi']:
#            sp = SpeciesBiotope(biotope=obj, species=spec)
#            sp.save()
#        obj.save() 
    inlines = (BiotopeImageInline,SpeciesBiotopeInline,)

admin.site.register(Biotope, BiotopeAdmin)

class DesignationOptionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in DesignationOption._meta.fields]
    
admin.site.register(DesignationOption, DesignationOptionAdmin)

class BiotopeCategoryOptionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in BiotopeCategoryOption._meta.fields]
    
admin.site.register(BiotopeCategoryOption, BiotopeCategoryOptionAdmin)

class GeoCodeOptionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in GeoCodeOption._meta.fields]
    
admin.site.register(GeoCodeOption, GeoCodeOptionAdmin)

class WideAreaAdmin(admin.ModelAdmin):
    list_display = [f.name for f in WideArea._meta.fields]
    
admin.site.register(WideArea, WideAreaAdmin)

class AbandonmentOptionAdmin(admin.ModelAdmin):
    list_dsiplay = [f.name for f in AbandonmentOption._meta.fields]
    
admin.site.register(AbandonmentOption, AbandonmentOptionAdmin)

class ConditionOptionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ConditionOption._meta.fields]
    # Uncomment if u want to use inlines
#    inlines = (BiotopeSupplInline,)
    
admin.site.register(ConditionOption, ConditionOptionAdmin)
    
class TrendOptionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in TrendOption._meta.fields]
    # Uncomment if u want to use inlines
#    inlines = (BiotopeSupplInline,)
    
admin.site.register(TrendOption, TrendOptionAdmin)

class KnowledgeOptionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in KnowledgeOption._meta.fields]
    # Uncomment if u want to use inlines
#    inlines = (BiotopeSupplInline,)
    
admin.site.register(KnowledgeOption, KnowledgeOptionAdmin)

class SocialReactionOptionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in SocialReactionOption._meta.fields]
    # Uncomment if u want to use inlines
#    inlines = (BiotopeSupplInline,)
    
admin.site.register(SocialReactionOption, SocialReactionOptionAdmin)

class ConservationOptionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ConservationOption._meta.fields]
    # Uncomment if u want to use inlines
#    inlines = (BiotopeSupplInline,)
    
admin.site.register(ConservationOption, ConservationOptionAdmin)

class SocialValueOptionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in SocialValueOption._meta.fields]
    
admin.site.register(SocialValueOption, SocialValueOptionAdmin)

class CulturalValueOptionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in CulturalValueOption._meta.fields]
    
admin.site.register(CulturalValueOption, CulturalValueOptionAdmin)

class EcologicalValueOptionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in EcologicalValueOption._meta.fields]
    
admin.site.register(EcologicalValueOption, EcologicalValueOptionAdmin)

class HabitationOptionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in HabitationOption._meta.fields]
    
admin.site.register(HabitationOption, HabitationOptionAdmin)

class SiteTypeOptionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in SiteTypeOption._meta.fields]
    
admin.site.register(SiteTypeOption, SiteTypeOptionAdmin)

class ClimateOptionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ClimateOption._meta.fields]
    
admin.site.register(ClimateOption, ClimateOptionAdmin)

class HumanActivityOptionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in HumanActivityOption._meta.fields]
    
admin.site.register(HumanActivityOption, HumanActivityOptionAdmin)

class TrendPopOptionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in TrendPopOption._meta.fields]
    
admin.site.register(TrendPopOption, TrendPopOptionAdmin)

class ThreatOptionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ThreatOption._meta.fields]
    
admin.site.register(ThreatOption, ThreatOptionAdmin)

###############################################################################


class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('species_code',
                    'species_name',
                    'sub_species',
                    'species_category',
                    'plant_kind',
                    'creation_date',
                    'update_date')
    list_filter = ('species_category',
                   'plant_kind',
                   'update_date')
    search_fields = ('species_code',
                     'species_name',
                     'sub_species',
                     'species_category__name',
                     'plant_kind__name')
    ordering = ('species_name',)
    list_display_links = ('species_code', 'species_name')
    fieldsets = (
        ('Γενικά Στοιχεία', {
            'fields': ('species_code', 'species_name', 'sub_species', 
            ('creation_date','update_date'),
            'species_category', 'other_names', 'species_name_gr', 'plant_kind',
            'knowledge', 'habitat', 'expansion', 'origin', 'respondent', 'photo'),
        }),
        ('Γνωρίσματα', {
            'classes': ('collapse',),
            'fields': ('category_ende', 'category_migr', 'category_bree', 'category_resi', 
            'category_intr', 'category'),
        }),
        ('Στοιχεία Προστασίας και Ανάπτυξης', {
            'classes': ('collapse',),
            'fields': ('protection', 'conservation_prio', 'trend', 'measures_take', 
            'measures_need'),
        }),
        ('Κατάσταση Διατήρησης', {
            'classes': ('collapse',),
            'fields': ('conservation_gr', 'conservation_eec', 'conservation_bio'),
        }),
        ('Σπανιότητα', {
            'classes': ('collapse',),
            'fields': ('rarity_gr', 'rarity_eec', 'rarity_bio'),
        }),
        ('Απειλές', {
            'classes': ('collapse',),
            'fields': ('threat_hunt', 'threat_fish', 'threat_coll', 'threat_fore',
            'threat_graz', 'threat_poll', 'threat_cult', 'threat_tour', 
            'threat_road', 'threat_buil', 'threat_drai', 'threat_eutr', 
            'threat_pest', 'threat_other', 'threat'),
        }),
        ('Εκμετάλλευση', {
            'classes': ('collapse',),
            'fields': ('exploit_hunt', 'exploit_fish', 'exploit_coll', 'exploit_logg',
            'exploit_graz'),
        }),
    )
    # Uncomment if u want to use inlines
#    inlines = (SpeciesBiotopeInline,)
    
admin.site.register(Species, SpeciesAdmin)


#### #### #### Species Secondary Tables #### #### ####

class SpeciesCategoryOptionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in SpeciesCategoryOption._meta.fields]
    
admin.site.register(SpeciesCategoryOption, SpeciesCategoryOptionAdmin)

class SpeciesPlantKindOptionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in SpeciesPlantKindOption._meta.fields]
    
admin.site.register(SpeciesPlantKindOption, SpeciesPlantKindOptionAdmin)

class SpeciesKnowledgeOptionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in SpeciesKnowledgeOption._meta.fields]
    
admin.site.register(SpeciesKnowledgeOption, SpeciesKnowledgeOptionAdmin)

class SpeciesProtectionOptionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in SpeciesProtectionOption._meta.fields]
    
admin.site.register(SpeciesProtectionOption, SpeciesProtectionOptionAdmin)

class SpeciesConservationPriorityOptionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in SpeciesConservationPriorityOption._meta.fields]
    
admin.site.register(SpeciesConservationPriorityOption, SpeciesConservationPriorityOptionAdmin)

class SpeciesTrendOptionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in SpeciesTrendOption._meta.fields]
    
admin.site.register(SpeciesTrendOption, SpeciesTrendOptionAdmin)

class SpeciesConservationOptionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in SpeciesConservationOption._meta.fields]
    
admin.site.register(SpeciesConservationOption, SpeciesConservationOptionAdmin)

class SpeciesRarityOptionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in SpeciesCategoryOption._meta.fields]
    
admin.site.register(SpeciesRarityOption, SpeciesRarityOptionAdmin)

#TODO Investigate the following models from Legacy DB
#admin.site.register(Hlpchangedsitecodes)
#admin.site.register(Hlpdeletedsites)
#admin.site.register(Hlpdigitized)
#admin.site.register(Hlpdigitizedtifk)
#admin.site.register(Hlpreportsites)
#admin.site.register(Geolevels)
#admin.site.register(HabCove)
#admin.site.register(Motive)
#admin.site.register(TagKnowledge)

