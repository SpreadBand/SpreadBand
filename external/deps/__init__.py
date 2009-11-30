import os
import sys
import shutil
import logging
import urlparse


logger = logging.getLogger('deps')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


class MissingDependency(Exception):
    """
    This exception is raised when a software cannot be found and therefore need
    to be checkouted
    """
    def __init__(self, aName):
        Exception.__init__(self, '%s does not exist.  Run "./manage.py up" to retrieve this dependency' % aName)



class VersionControl(object):
    def __init__(self, url, root, app_name='', pathtomodule='', revision=''):
        self.url = url
        self.root = root
        self.revision = revision
        self.pathtomodule = pathtomodule

        # App_name is the name of the RCS module but also the name of the
        # directory where it will be downloaded
        if not app_name:
            self.app_name = os.path.basename((urlparse.urlparse(url)[2]).rstrip('/'))
        else:
            self.app_name = app_name

        # The dir where the software is going to be downloaded
        self.dl_path = os.path.join(root,
                                    self.app_name)

        # The RCS module dir
        self.checkout_path = os.path.join(self.dl_path,
                                          self.app_name)

        # The path to add the PYTHONPATH so that python will find it
        self.python_path = os.path.join(self.dl_path,
                                        self.pathtomodule)
    
    def __repr__(self):
        return "<VersionControl: %s>" % self.app_name
    
    def add_to_python_path(self, position):
        """
        Add this module to the PYTHONPATH
        """
        if not os.path.exists(self.checkout_path):
            raise MissingDependency(self.app_name)
        sys.path.insert(position, self.python_path)

class HG(VersionControl):
    """
    Backend for Mercurial (HG)
    """
    def checkout(self):
        old_dir = os.path.abspath(os.curdir)

        # Make the download dir
        os.mkdir(self.dl_path)
        os.chdir(self.dl_path)

        # Checkout
        logger.info('Checking out %s' % self.app_name)
        os.system('hg clone %s %s' % (self.url, self.app_name))

        # Switch to given revision (HG can't checkout a specific revision, we
        # have to do that in two steps
        if self.revision:
            os.chdir(self.checkout_path)
            logger.info('Switching to revision %s of %s' % (self.revision,
                                                            self.app_name)
                        )
            os.system('hg update -C %s' % (self.revision))

        os.chdir(old_dir)
    
    def up(self):
        logger.info('%s' % self)
        if not os.path.exists(self.checkout_path):
            self.checkout()
            return
            
        os.chdir(self.checkout_path)

        # Pull new changes
        logger.info("Pulling changes for %s" % self.app_name)
        os.system('hg pull')

        # Update to given revision or tip by default
        if self.revision:
            logger.info("Updating revision %s of %s" % (self.revision,
                                                        self.app_name))
            os.system('hg update -C %s' % (self.revision))
        else:
            logger.info("Updating tip of %s" % self.app_name)
            os.system('hg update')



class SVN(VersionControl):
    """
    Backend for Subversion (SVN)
    """
    def checkout(self):
        old_dir = os.path.abspath(os.curdir)

        # Make the download dir
        os.mkdir(self.dl_path)
        os.chdir(self.dl_path)

        # Checkout
        logger.info('Checking out %s' % self.app_name)
        os.system('svn co %s %s' % (self.url, self.app_name))

        os.chdir(old_dir)
    
    def up(self):
        logger.info('%s' % self)
        if not os.path.exists(self.checkout_path):
            self.checkout()
            return

        os.system('svn up %s' % self.path)

def add_all_to_path(settings, auto_update=False, position=1):
    for dependency in settings.DEPENDENCIES:
        if auto_update:
            dependency.up()

        try:
            dependency.add_to_python_path(position)
        except MissingDependency:
            dependency.up()
            dependency.add_to_python_path(position)
