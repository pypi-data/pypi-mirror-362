from django.template.context import Context


class InterfaceNotFound(Exception):
    """Interface with this name was not found"""

    pass


class ITemplatePluginMixin:
    """A mixin that can be inherited from to build renderable plugins.

    Create an interface that inherits from ITemplatePluginMixin. Each
    implementation must either have a `template` (direct string HTML template,
    for short ones) or `template_name` (which points to the template to render).

    You can add fixed `context`, or override `get_plugin_context` which receives
    the context of the view the plugin is rendered in.

    In your template, use
    ```
    {% load gdaps %}
    <ul class="alerts">
    {% render_plugin IMyListItem %}
    </ul>
    ```
    in your template anywhere, and all of your implementations are rendered,
    one after each other, in a line. Each plugin can come from another app.
    You can change the order of the rendering using the `weight` attribute.
    """

    template: str = ""
    template_name: str = ""
    context: dict = {}
    weight = 0

    def get_plugin_context(self, context: Context) -> Context:
        """Override this method to add custom context to the plugin.

        :param context: the context where the plugin is rendered in.
            You can update it with own values, and return it.
            The return variable of this function will be the context
            of the rendered plugin. So if you don't update the passed
            context, but just return a new one, the plugin will not get
            access to the global context.

        Per default, it merges the plugin's ``context`` attribute into
        the given global context.
        """
        context.update(self.context)
        return context


# These hooks are highly experimental and likely to change in the future.
# don't take them as stable API.
class IFormExtensionMixin:
    """A mixin to create interfaces from, to extend Django forms."""

    class Media:
        js = ()
        css = {}

    field_names = []

    def alter_fields(self, fields: dict):
        """plugin hook for altering form fields.

        Attributes:
            fields: the form fields to alter. Can be changed in the method.
        """

    def alter_layout(self, layout):
        """plugin hook for altering a crispy form Layout() object.

        Call this method from your Form's  `__init__()` method.
        Attributes:
            layout: the crispy Layout object of the extended form.
                Modify it to your needs in this method.
        """

    def pre_save(self, instance, commit: bool) -> None:
        """Plugin hook to be called from a ModelForm's save() method before saving the instance."""

    def post_save(self, instance, commit: bool) -> None:
        """Plugin hook to be called from a ModelForm's save() method after saving the instance."""

    def clean(self, host_form) -> dict:
        """Plugin hook to be called from within the extended Form's `clean()` method.

        Call this method and return its result at the end of your form's clean() method.
        '''python
        for plugin in MyFormExtension:
            cleaned_data = plugin.clean(self)
        return cleaned_data
        ```
        You can then add some errors to the form via
        ```python
        form.add_error(field_name, ValidationError("Error message", code="invalid"))
        ```
        and the host form will display the error at the specified field.

        Attributes:
            form: the main form where this plugin hooks into.
                the cleaned_data of the form can be obtained via form.cleaned_data.

        Return:
            the (possibly modified) cleaned_data of the plugin form.
        """


class IViewExtensionMixin:
    """A mixin to create Interfaces from, which extend Django views."""

    def alter_context_data(self, **kwargs) -> dict:
        """hook to alter context data of a view.

        Call this hook from get_context_data().
        """
        return {}

    def alter_response(self, request, response, *args, **kwargs) -> None:
        """hook to alter a response during a post/get/delete etc. request.

        Call this hook from get/post/delete().

        Attributes:
            request: the current request
            response: the response, as the post method created it so far.
                Feel free to modify it.
        """

    def form_valid(self, form, response) -> None:
        """hook that should be called by form_valid() to add plugin functionality."""
