from django.contrib.admin.utils import quote
from django.template import Library

from wagtail.contrib.modeladmin.templatetags.modeladmin_tags import (
    result_list,
    result_row_display,
)


register = Library()


@register.inclusion_tag("treemodeladmin/includes/tree_result_list.html",
                        takes_context=True)
def tree_result_list(context):
    """ Displays the headers and data list together with a link to children """
    context = result_list(context)
    return context


@register.inclusion_tag(
    "treemodeladmin/includes/tree_result_row.html", takes_context=True)
def tree_result_row_display(context, index):
    context = result_row_display(context, index)
    obj = context['object_list'][index]
    view = context['view']

    if view.has_child_admin:
        context.update({
            'children': view.get_children(obj),
            'child_index_url': view.child_url_helper.index_url,
            'child_filter': view.get_child_filter(quote(obj.pk)),
            'child_create_url': view.child_url_helper.create_url,
        })

    return context
