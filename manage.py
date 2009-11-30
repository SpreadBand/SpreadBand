#!/usr/bin/python
import sys, os.path
try:
    import external.autodeps as deps
except ImportError:
    sys.stderr.write("Error: you should download django-autodeps and put the 'autodeps' module under the 'external/' directory.\n")
    sys.exit(1)

try:
    import settings # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)


# For django-dependencies
# remove '.' from the path (you should use the project package to reference 
# anything in here)
sys.path.pop(0)
sys.path.insert(0, os.path.dirname(settings.PROJECT_PATH))

if len(sys.argv) > 1 and sys.argv[1] == 'up':
    deps.add_all_to_path(settings, auto_update=True)
    sys.exit(0)
else:
    deps.add_all_to_path(settings, auto_update=False)
# End django-dependencies

from django.core.management import execute_manager

if __name__ == "__main__":
    execute_manager(settings)
