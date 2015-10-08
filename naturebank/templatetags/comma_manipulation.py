# -*- coding: utf-8 -*-
# UTF8 Encoded
from django.template import (Library, TemplateSyntaxError, Variable,
                             Node, VariableDoesNotExist)

register = Library()


class SpeciesListNode(Node):
    def __init__(self, species):
        self.species = Variable(species)
    def render(self, context):
        try:
            species = self.species.resolve(context)
            context['threats'] = [(species.threat_hunt, "Κυνήγι"),
                                 (species.threat_fish, "Αλιεία"),
                                 (species.threat_coll, "Συλλογή"),
                                 (species.threat_fore, "Υλοτομία"),
                                 (species.threat_graz, "Βοσκή"),
                                 (species.threat_poll, "Ρύπανση"),
                                 (species.threat_cult, "Καλλιέργεια"),
                                 (species.threat_tour, "Τουρισμός"),
                                 (species.threat_road, "Διάνοιξη δρόμων"),
                                 (species.threat_buil, "Δόμηση"),
                                 (species.threat_drai, "Αποξήρανση"),
                                 (species.threat_eutr, "Ευτροφισμό"),
                                 (species.threat_pest, "Φυτοφάρμακα"),
                                 (species.threat_other, "Άλλες απειλές")]
            return ''
        except VariableDoesNotExist:
            return ''

@register.tag(name="load_threats")
def create_species_list(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, species = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError, "%r tag requires exactly one argument" % token.contents.split()[0]
    return SpeciesListNode(species)


class CategoryListNode(Node):
    def __init__(self, species):
        self.species = Variable(species)
    def render(self, context):
        try:
            species = self.species.resolve(context)
            context['categories'] = [(species.category_ende, "Ενδημικό"),
                                     (species.category_migr, "Μεταναστευτικό"),
                                     (species.category_bree, "Αναπαραγόμενο"),
                                     (species.category_resi, "Μόνιμος Κάτοικος"),
                                     (species.category_intr, "Εισαχθέν")]
            return ''
        except VariableDoesNotExist:
            return ''

@register.tag(name="load_categories")
def create_category_list(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, species = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError, "%r tag requires exactly one argument" % token.contents.split()[0]
    return CategoryListNode(species)


@register.filter
def comma_sep(value):
    """It gets a list of 2-tuples and returns a comma separated string."""
    k = [i[1] for i in value if i[0]]
    return ", ".join(k)
