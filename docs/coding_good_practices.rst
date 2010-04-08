Good practices
**************

Django
======

Forms
^^^^^

Use a :class:`ModelForm` if your form matches an existing model.

Try to minimize the usage of :attr:`exclude_fields` in the
:class:`Meta` inner-class which introduces some kind of
implicitness. Prefer to use :attr:`fields` attribute that makes
available fields explicit and so, upgrade-resistant.

Views
^^^^^

Never use a :class:`Model` directly in a view, use a form.

