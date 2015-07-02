__author__ = 'M1SRH'

class Formatter(object):

    def __init__(self, im):
        self.im = im

    def __call__(self, x, y):
        intensity = self.im.get_array()[int(y), int(x)]
        #return 'x={:.01f},  y={:.01f},  Int={:.01f}'.format(x, y, intensity)
        return 'X={:.0f}  Y={:.0f}  Int={:.0f}'.format(x, y, intensity)
