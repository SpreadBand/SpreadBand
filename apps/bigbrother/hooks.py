from django.db.models.signals import post_save

from .backends import OrmBackend

def collect_stats(aModelStats, backendType=OrmBackend):
    """
    To be used by end user. Tell the system we want to watch this
    particular model.
    """
    backend = backendType(aModelStats)

    post_save.connect(backend.on_save,
                      sender=aModelStats.Meta.model,
                      weak=False)

    print "Collecting stats for", aModelStats.Meta.model



