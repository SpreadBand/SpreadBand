Syntax Aesthetics
*****************

General Python
==============

Imports
^^^^^^^

Order your imports like this, adding a blank line when changing to
another category:

 #. System wide imports
 #. Current framework core imports
 #. Current framework contrib imports
 #. Other modules imports
 #. Local modules imports

Usage of the '.' import is heavily recommended.
Never use the '..' relative import. 

Here's an example::

 from pil import Picture

 from django.shortcuts import redirect, render_to_response
 
 from django.contrib.auth.decorators import login_required
 
 from myapp.models import BobModel

 from .forms import FeedbackNewForm

.. _guidelines-python-functions:

Functions
^^^^^^^^^

Name your functions with underscores::

 def my_bob_method(...):
  ...

Classes
^^^^^^^

Class naming should follow the **UpperCamelCase** convention::

 class AwesomeBob(object):
   ...

Methods
"""""""

Use the **lowerCamelCase** convention::

 class AwesomeBob(object):
   def startEngine(self, ...):
     ...

Properties
^^^^^^^^^^

Use the new way of declaring properties and differenciate method names::

  @property
  def name(self, ...):
    ...

  @name.setter
  def setName(self, ...):
    ...

  @name.deleter
  def deleteName(self, ...):
    ...

Django
======

Models
^^^^^^

Forms
^^^^^

Forms are classes, Use the ModelForm as much as possible.

Views
^^^^^

Views are functions, so follow the python function syntax guidelines
(see :ref:`guidelines-python-functions`).

To name them, be explicit. Don't name your views like this::

 def add(request, ...):
  ...

 def remove(request, ...):
  ...

Instead, prefer to give a fully qualified name, related to what it
does::

 def band_add(request, ...):
  ...

 def band_remove(request, ...):
  ...
