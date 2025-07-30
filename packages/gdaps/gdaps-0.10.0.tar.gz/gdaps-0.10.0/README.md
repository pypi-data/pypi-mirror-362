
The GDAPS library allows Django to make real "pluggable" apps.

A standard Django "app" is *reusable* (if done correctly), but is not *pluggable*,
like being distributed and "plugged" into a Django main application without modifications. GDAPS is filling this gap.

The reason you want to use GDAPS is: **you want to create an application that should be extended via plugins**. GDAPS consists of a few bells and twistles where Django lacks "automagic":

* Apps are automatically found using setuptools' entry points
* Apps can provide their own URLs (they are included and merged into urlpatterns automatically)
* Apps can define ``Interfaces``, that other GDAPS apps then can implement
* Apps can provide template hooks that can be filled with plugins' content


## Limitations

* GDAPS interfaces cannot inherit classes that import models (like `PermissionRequiredMixin`), as the declaration is too early in the Django setup process, and apps aren't loaded at that time.


## Contribute

You can support me in various ways.

* Test the code and write bug reports.
* Write code
* Suggest ideas (as bug report)


## Credits

I was majorly influenced by other plugin systems when writing this code, big thanks to them:

* Marty Alchin's [Simple plugin framework](http://martyalchin.com/2008/jan/10/simple-plugin-framework/)
* The [PyUtilib](https://github.com/PyUtilib/pyutilib) library
* [The Pretix ecosystem](https://pretix.eu/)
* [Yapsy](http://yapsy.sourceforge.net/)
* [Django-Rest-Framework](https://www.django-rest-framework.org/)
* [Graphene-Django](http://docs.graphene-python.org/projects/django/en/latest/)

## License

GDAPS is licensed under the **BSD License**, see [License](LICENSE.md).

