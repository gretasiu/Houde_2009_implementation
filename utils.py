import os
import numpy as np

from astropy.io.fits import getdata
from astropy import wcs
from astropy.io import fits
from astropy import units as u
from astropy import constants as con
from astropy.coordinates import SkyCoord

class FITSimage:
    def __init__(self, image_file, intensity_scale=1.0):
        self.image_file = image_file
        self.intensity_scale = intensity_scale
        self.if_success = False
        self.hdu = None
        self.header = None
        self.data = None
        self.naxis1 = None
        self.naxis2 = None
        self.crval1 = None
        self.crpix1 = None
        self.cdelt1 = None
        self.crval2 = None
        self.crpix2 = None
        self.cdelt2 = None
        self.hduwcs = None
        self.bmaj = None
        self.bmin = None
        self.bpa = None

    def FITSdata(self):
        try:
            self.hdu = fits.open(self.image_file)
            self.header = repr(self.hdu[0].header) 
            self.hdu[0].data = self.hdu[0].data * self.intensity_scale
            self.data = self.hdu[0].data
            self.if_success = True
        except:
            print('Unable to read the PA FITS image. Please double-check the image file.')
            print(self.image_file)

        if self.if_success:
            try:
                self.naxis1 = self.hdu[0].header['naxis1']
                self.naxis2 = self.hdu[0].header['naxis2']
                self.crval1 = self.hdu[0].header['crval1']
                self.crpix1 = self.hdu[0].header['crpix1']
                self.cdelt1 = self.hdu[0].header['cdelt1']
                self.crval2 = self.hdu[0].header['crval2']
                self.crpix2 = self.hdu[0].header['crpix2']
                self.cdelt2 = self.hdu[0].header['cdelt2']
                self.hduwcs = wcs.WCS(self.hdu[0].header)
            except:
                print('Warning. No coordinate headers')

            try:
                self.bmaj = self.hdu[0].header['bmaj']
                self.bmin = self.hdu[0].header['bmin']
                self.bpa = self.hdu[0].header['bpa']
                print("bmaj is", self.bmaj, "degree")
            except:
                print('Warning. No header for synthesized beam size')

    #def PlotFits(self)

# g31PA = FITSimage('G31p4_Qband_D.rob2.PA.image.tt0.miriad.dropdeg.fits')
# g31PA.FITSdata()
# print(g31PA.bmaj)

def janskyPerbeam_to_brightTemp(bmaj, bmin, freq, mjanky_beam):
    '''
    Without using astropy, I just use the function from NRAO
    https://science.nrao.edu/facilities/vla/proposing/TBconv
    Input:
    bmaj         [arcsec]
    bmin         [arcsec]
    freq         [GHz]
    mjanky_beam  [mJy/beam] 

    Output:
    Tb           [K]
    '''

    Tb = 1.222e3*(mjanky_beam/(freq**2*bmaj*bmin))
    print(Tb, 'K')

    return Tb

# This is to convert brightness temperature to mJy/beam
# Same as above but flipped


def brightTemp_to_janskyPerbeam(bmaj, bmin, freq, Tb):
    '''
    Input:
    bmaj         [arcsec]
    bmin         [arcsec]
    freq         [GHz]
    Tb           [K]    

    Output:
    mjanky_beam  [mJy/beam] 
    '''

    mjanky_beam = Tb*(freq**2*bmaj*bmin)/1.222e3
    print(mjanky_beam, 'mJy/beam')

    return mjanky_beam
