Syntax Aesthetics
*****************

General Python
==============

Imports
-------

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

Blocks and blank spaces
-----------------------

Assignations have one blank space at each side of the equal sign::

  a = 2

Whenever you think your code can be splitted in logical blocks, just
add blank lines around these blocks. It helps people to split the
algorithms in their head and understand faster each little part::

  def do_that():
    a = 2
    c = 42*sin(x)
    
    do_megalaunch()
    wait_2_seconds()

    do_return()

Comments
--------

Don't forget to comment *classes*, *methods*, *functions* and
*modules* whenever it is not a trivial operation. Don't explain your
algorithm except if it is really complex, explain the purpose instead.

When commenting, always use the triple double-quotes for the docstrings
and starts your comment on the following line::

 def nice_function(...):
   """
   This function is very nice.
   """
   ...

When commenting a part of the code (to explain parts of an algorithm
for example), make sure to put a space after the # sign::

  # Now, upload to mars
  loader.run(target=Mars)

Strings
-------

Since Python doesn't make a difference between using single and double
quote, prefer to use the single ones, they take less space::

  say('hello')

Functions
---------

Name your functions with underscores::

 def my_bob_method(...):
  ...

A function name that involves multiple words should never be abbreviated.

Classes
-------

Class naming should follow the **UpperCamelCase** convention::

 class AwesomeBob(object):
   ...

Methods
^^^^^^^

Use the **lowerCamelCase** convention::

 class AwesomeBob(object):
   def startEngine(self, ...):
     ...

A method name that involves multiple words should never be abbreviated.

Properties
----------

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

Named arguments
---------------

When declaring a method or function signature, we make a distinction
between objects of type :class:`str`, :class:`int` and
:class:`object`. 

This choice is motivated by the fact that python is a dynamically
typed language. Indeed, one of its weakness appears when one has to
read a method/function signature: how to guess what kind of object to
pass ?

To solve that, we introduce a few naming convention that gives the
extra informations needed to understand how to use the function.

:class:`int` arguments
^^^^^^^^^^^^^^^^^^^^^^

When declaring a named argument for a :class:`int`, first write it in
lowercase and give its meaning (here, *article*).

Second, append the nature of your variable after an underscore::

 def buy(article_count):
   ...

 def choose(article_index):
   ...

Common suffixes include the followings:
 * **count**: how many things ;
 * **index**: the position inside a sequence (e.g. a list) ;
 * **id**: the identifier of an object.

:class:`str` arguments
^^^^^^^^^^^^^^^^^^^^^^

For strings, just follow the same convention as the :class:`int`
arguments, but consider the following suffixes:

* **name**: the name of something, not an instance of it ;
* **slug**: the slug of something, not an instance of it.

Example::

  def buy(article_name):
    ...

:class:`object` arguments
^^^^^^^^^^^^^^^^^^^^^^^^^

For any other object, you often only need one of each type for a
method call. It is therefore often very easy to guess what an argument
of a given type does in the corresponding method/function. We
therefore advocate the usage of the type as a naming convention and
let the developer explains the purpose in the docstrings.

In a nutshell, name your object with its type and prepend *"a"* or
*"an"* to indicate it is and instance and only one object. To name it,
follow the **lowerCamelCase**::

  def buy(aCaddy, anArticle):
    ...

If you want to make use of polymorphism, just use the most common type
for the naming.

In the case you really need more than one instance of a same type in
your method/functions, substitute the "a"/ "an" prefix with something
that has a stronger meaning::

  def buy(previousCaddy, currentCaddy, anArticle): ...

Set of entities
^^^^^^^^^^^^^^^

In the previous examples, we have only seen the naming convention for
a single object. If you have to deal with a set of objects, just
prepend the name of the entity with the nature of your set. It could
be a :class:`set`, a :class:`list` or anything else. Follow this
naming convention (and don't forget to make your class name plural !)::

  def buy(aCaddy, aListOfArticles): ...
  def buy(aCaddy, aSetOfArticles): ...


Calling functions and methods
-----------------------------

Always tries to make your calls explicit by using the named
arguments. This prevents swapping of arguments and makes it easier for
someone who doesn't know the API to understand what it does.

Here's an example::

 return render_to_response(template_name='backcap/feedback_new.html',
                           dictionary={'feedback_form': feedback_form},
                           )

When you pass named arguments, don't put spaces around the equal sign.

Also, feel free to split the line by putting each named argument on a
single line, it is much better than inlining everything when it is too
long.

On the other hand, when calling a function on a single line, put a
blank space only after the comma::

  call_me(3, a=2, next=None)

Django
======

Models
------

Forms
-----

Views
-----

Views are functions, so follow the python function syntax guidelines
(see :ref:`guidelines-python-functions`).

To name them, be explicit. Don't name your views like this::

 def add(request, ...): ...
 def remove(request, ...): ...

Instead, prefer to give a fully qualified name, related to what it
does::

 def band_add(request, ...): ...
 def band_remove(request, ...): ...

URLs
----

