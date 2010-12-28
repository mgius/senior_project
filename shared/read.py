import pygame
def load_image(filename, colorkey=None):
    ''' Loads an image, with some error checking. '''
    try:
        image = pygame.image.load(filename)
    except pygame.error, message:
        print 'Cannot load image:', filename
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

