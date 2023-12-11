from django.template import Library

from wagtail_modeladmin.templatetags.modeladmin_tags import (
    result_list,
    result_row_display,
)


register = Library()


@register.inclusion_tag(
    "treemodeladmin/includes/tree_result_list.html", takes_context=True
)
def tree_result_list(context):
    """Displays the headers and data list together with a link to children"""
    context = result_list(context)
    return context


@register.inclusion_tag(
    "treemodeladmin/includes/tree_result_row.html", takes_context=True
)
def tree_result_row_display(context, index):
    context = result_row_display(context, index)
    obj = context["object_list"][index]
    view = context["view"]
    child_url_helper = view.child_url_helper

    if view.has_child_admin:
        context.update(
            {
                "children": view.get_children(obj),
                "child_index_url": child_url_helper.get_index_url_with_parent(
                    view.child_model_admin.parent_field, obj.pk
                ),
                "child_create_url": child_url_helper.get_create_url_with_parent(  # noqa
                    view.child_model_admin.parent_field, obj.pk
                ),
            }
        )

    return context
