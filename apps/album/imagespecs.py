from imagekit.specs import ImageSpec 
from imagekit import processors 

# first we define our thumbnail resize processor 
class ResizeThumb(processors.Resize): 
    width = 150 
    height = 150 
    crop = True

class Thumbnail(ImageSpec): 
    access_as = 'thumbnail_image' 
    pre_cache = True 
    processors = [ResizeThumb]





