from django import template
from django.conf import settings
from copy import copy
from crispy_forms.templatetags.crispy_forms_filters import flatatt_filter


register = template.Library()

@register.filter
def get_field_title(object, field_name):
    """Loads the practioner model based on its pk.
    
    Usage:
    
        {{ object|get_field_title:'my_field_name' }}
    """
    return object._meta.get_field(field_name).verbose_name


@register.filter
def get_field_value(object, field_name):
    """Outputs the value of an object's field.
    Equivalent to {{ object.field_name }}.
    
    Usage:
    
        {{ object|get_field_value:'my_field_name' }}
    """
    return getattr(object, field_name)


@register.filter
def instances_and_widgets(bound_field):
    """Returns a list of two-tuples of instances and widgets, designed to
    be used with ModelMultipleChoiceField and CheckboxSelectMultiple widgets.
    
    Allows templates to loop over a multiple checkbox field and display the
    related model instance, such as for a table with checkboxes.
      
    Usage:
        {% for instance, widget in form.my_field_name|instances_and_widgets %}
            <p>{{ instance }}: {{ widget }}</p> 
        {% endfor %}
    """
    instance_widgets = []
    index = 0
    for instance in bound_field.field.queryset.all():
         widget = copy(bound_field[index])
         # Hide the choice label so it just renders as a checkbox
         widget.choice_label = ''
         instance_widgets.append((instance, widget))
         index += 1
    return instance_widgets


@register.filter
def get_non_page_options(request):
    """Returns a urlencoded version of the GET options passed to the request,
    with the paginator page option removed.
    
    Used by templates/includes/paginator.html."""
    querydict = request.GET.copy()
    querydict.pop('page', None)
    return querydict.urlencode


@register.filter
def startswith(test_string, start_string):
    """Returns whether comparison string starts with the original string.
    Usage:
    
      {% if test_string|startswith:start_string %}
          <p>'{{ test_string }}' starts with '{{ start_string }}'!
      {% endif %}
    """
    return test_string.startswith(start_string)


@register.simple_tag
def base_url():
    """Returns the base url.
    
    Usage:
    
        {% base_url %}
    """
    return settings.BASE_URL


@register.filter
def flatatt_for_choice(widget, choice_value):
    """Outputs the attributes for the supplied widget and choice.  Designed to
    be used with apps.core.widgets.ChoiceAttrsRadioSelect.
    
    Usage:
        {% for choice in field.field.choices %}
            <input type="radio"
                {{ field.field.widget|flatatt_for_choice:choice.0 }}>
                {{ choice.1|unlocalize }}
        {% endfor %}
    """
    choice_attrs = copy(widget.attrs)
    try:
        choice_attrs.update(widget.choice_attrs[choice_value])
    except (AttributeError, KeyError):
        pass
    return flatatt_filter(choice_attrs)


@register.filter
def model_opts(instance):
    "Returns the _meta attribute from the supplied model."
    return instance._meta
