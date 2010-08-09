from imagekit.specs import ImageSpec 
from imagekit import processors 

class ResizeAvatar(processors.Resize): 
    width = 80
    height = 80
    crop = True

class ResizeSmallAvatar(processors.Resize):
    width = 48
    height = 48
    crop = True

class Avatar(ImageSpec):
    access_as = 'avatar_image'
    pre_cache = False
    processors = [ResizeAvatar]

class SmallAvatar(ImageSpec):
    access_as = 'small_avatar_image'
    pre_cache = False
    processors = [ResizeSmallAvatar]



