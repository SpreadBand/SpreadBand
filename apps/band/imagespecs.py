from imagekit.specs import ImageSpec 
from imagekit import processors 

# first we define our thumbnail resize processor 
class ResizeThumb(processors.Resize): 
    width = 200
    height = 100 
    crop = True

class ResizeAvatar(processors.Resize): 
    width = 80
    height = 80

class ResizeSmallAvatar(processors.Resize):
    width = 48
    height = 48

class Thumbnail(ImageSpec): 
    access_as = 'thumbnail_image' 
    pre_cache = True 
    processors = [ResizeThumb]

class Avatar(ImageSpec):
    access_as = 'avatar_image'
    pre_cache = False
    processors = [ResizeAvatar]

class SmallAvatar(ImageSpec):
    access_as = 'small_avatar_image'
    pre_cache = False
    processors = [ResizeSmallAvatar]

