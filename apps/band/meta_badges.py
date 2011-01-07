import badges

from .models import Band

class PressKitCompletion(badges.MetaBadge):
    id = "presskitcompletion"
    model = Band
    one_time_only = True
    
    title = "PressKit Completion"
    description = "Completed the PressKit"
    level = 'P'
    
    progress_start = 0
    progress_end = 6
    
    def get_user(self, instance):
        return instance

    def get_progress(self, candidate):
        has_biography = 1 if candidate.biography else 0
        has_localisation = 1 if candidate.place else 0
        has_tracks = 1 if len(candidate.presskit.tracks.all()) else 0
        has_pictures = 1 if len(candidate.pictures.all()) else 0
        has_techsheet = 1 if candidate.technical_sheet else 0
        has_socialnets = 1 if len(candidate.socialnetworks.all()) else 0

        return (has_biography + has_localisation + has_tracks + has_pictures + has_techsheet + has_socialnets)
    
    def check_biography(self, instance):
        return instance.biography
    
    def check_localisation(self, instance):
        return instance.place

    def check_techsheet(self, instance):
        return instance.technical_sheet

    def check_tracks(self, instance):
        return len(instance.presskit.tracks.all()) > 0

    def check_pictures(self, instance):
        return len(instance.pictures.all()) > 0

    def check_socialnets(self, instance):
        return len(instance.socialnetworks.all()) > 0


        
