# MIT License
#
# Copyright (c) 2018 Tom Runia
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to conditions.
#
# Author: Tom Runia
# Date Created: 2018-12-04
#
# Modifed by CharlesShan from https://github.com/tomrunia/PyTorchSteerablePyramid
# Data Modified: 2025-2-12

# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function

import numpy as np
import torch
from math import factorial
import click

# import steerable.math_utils as math_utils
# pointOp = math_utils.pointOp

def prepare_grid(m, n):
    x = np.linspace(-(m // 2)/(m / 2), (m // 2)/(m / 2) - (1 - m % 2)*2/m, num=m)
    y = np.linspace(-(n // 2)/(n / 2), (n // 2)/(n / 2) - (1 - n % 2)*2/n, num=n)
    xv, yv = np.meshgrid(y, x)
    angle = np.arctan2(yv, xv)
    rad = np.sqrt(xv**2 + yv**2)
    rad[m//2][n//2] = rad[m//2][n//2 - 1]
    log_rad = np.log2(rad)
    return log_rad, angle

def rcosFn(width, position):
    N = 256  # abritrary
    X = np.pi * np.array(range(-N-1, 2))/2/N
    Y = np.cos(X)**2
    Y[0] = Y[1]
    Y[N+2] = Y[N+1]
    X = position + 2*width/np.pi*(X + np.pi/4)
    return X, Y

def pointOp(im, Y, X):
    out = np.interp(im.flatten(), X, Y)
    return np.reshape(out, im.shape)

################################################################################
################################################################################


class Steerable(object):
    '''
    This is a modified version of buildSFpyr, that constructs a
    complex-valued steerable pyramid  using Hilbert-transform pairs
    of filters. Note that the imaginary parts will *not* be steerable.

    Description of this transform appears in: Portilla & Simoncelli,
    International Journal of Computer Vision, 40(1):49-71, Oct 2000.
    Further information: http://www.cns.nyu.edu/~eero/STEERPYR/

    Modified code from the perceptual repository:
      https://github.com/andreydung/Steerable-filter

    This code looks very similar to the original Matlab code:
      https://github.com/LabForComputationalVision/matlabPyrTools/blob/master/buildSCFpyr.m

    Also looks very similar to the original Python code presented here:
      https://github.com/LabForComputationalVision/pyPyrTools/blob/master/pyPyrTools/SCFpyr.py

    '''

    def __init__(self, height=2, nbands=4, scale_factor=2, device=None):
        self.height = height  # including low-pass and high-pass
        self.nbands = nbands  # number of orientation bands
        self.scale_factor = scale_factor
        self.device = torch.device('cpu') if device is None else device

        # Cache constants
        self.lutsize = 1024
        self.Xcosn = np.pi * np.array(range(-(2*self.lutsize+1), (self.lutsize+2)))/self.lutsize
        self.alpha = (self.Xcosn + np.pi) % (2*np.pi) - np.pi
        self.complex_fact_construct   = np.power(complex(0, -1), self.nbands-1)
        self.complex_fact_reconstruct = np.power(complex(0, 1), self.nbands-1)
        # self.complex_fact_construct = torch.pow(torch.complex(torch.tensor(0.0), torch.tensor(-1.0)), self.nbands - 1)
        # self.complex_fact_reconstruct = torch.pow(torch.complex(torch.tensor(0.0), torch.tensor(1.0)), self.nbands - 1)
        
    ################################################################################
    # Construction of Steerable Pyramid

    def build(self, im_batch):
        ''' Decomposes a batch of images into a complex steerable pyramid. 
        The pyramid typically has ~4 levels and 4-8 orientations. 
        
        Args:
            im_batch (torch.Tensor): Batch of images of shape [N,C,H,W]
        
        Returns:
            pyramid: list containing torch.Tensor objects storing the pyramid
        '''
        
        assert im_batch.device == self.device, 'Devices invalid (pyr = {}, batch = {})'.format(self.device, im_batch.device)
        assert im_batch.dtype == torch.float32, 'Image batch must be torch.float32'
        assert im_batch.dim() == 4, 'Image batch must be of shape [N,C,H,W]'
        assert im_batch.shape[1] == 1, 'Second dimension must be 1 encoding grayscale image'

        im_batch = im_batch.squeeze(1)  # flatten channels dim
        height, width = im_batch.shape[2], im_batch.shape[1] 
        
        # Check whether image size is sufficient for number of levels
        if self.height > int(np.floor(np.log2(min(width, height))) - 2):
            raise RuntimeError('Cannot build {} levels, image too small.'.format(self.height))
        
        # Prepare a grid
        log_rad, angle = prepare_grid(height, width)

        # Radial transition function (a raised cosine in log-frequency):
        Xrcos, Yrcos = rcosFn(1, -0.5)
        Yrcos = np.sqrt(Yrcos)

        YIrcos = np.sqrt(1 - Yrcos**2)

        lo0mask = pointOp(log_rad, YIrcos, Xrcos)
        hi0mask = pointOp(log_rad, Yrcos, Xrcos)

        # Note that we expand dims to support broadcasting later
        lo0mask = torch.from_numpy(lo0mask).float()[None,:,:,None].to(self.device)
        hi0mask = torch.from_numpy(hi0mask).float()[None,:,:,None].to(self.device)

        # Fourier transform (2D) and shifting
        # batch_dft = torch.rfft(im_batch, signal_ndim=2, onesided=False) # old
        batch_dft = torch.fft.fft2(im_batch, dim=(1, 2))
        # batch_dft = math_utils.batch_fftshift2d(batch_dft)
        batch_dft = torch.fft.fftshift(batch_dft, dim=(1, 2))
        batch_dft = torch.stack((batch_dft.real, batch_dft.imag), -1)

        # tempa = torch.fft.fft2(im_batch, dim=(1, 2))
        # tempb = torch.fft.fftshift(tempa, dim=(1, 2))
        # tempc = torch.fft.ifftshift(tempb, dim=(1, 2))
        # tempd = torch.fft.ifft2(tempc, dim=(1,2))
        # glance([im_batch,tempd])

        # Low-pass
        lo0dft = batch_dft * lo0mask
        
        # Start recursively building the pyramids
        coeff = self._build_levels(lo0dft, log_rad, angle, Xrcos, Yrcos, self.height-1)

        # High-pass
        hi0dft = batch_dft * hi0mask
        # hi0 = math_utils.batch_ifftshift2d(hi0dft)
        temp = torch.complex(real=hi0dft[:,:,:,0],imag=hi0dft[:,:,:,1])
        hi0 = torch.fft.ifftshift(temp, dim=(1, 2))
        # hi0 = torch.ifft(hi0, signal_ndim=2) # old
        hi0 = torch.fft.ifft2(hi0, dim=(1, 2))
        # hi0_real = torch.unbind(hi0, -1)[0]
        coeff.insert(0, hi0.real)
        return coeff

    def _build_levels(self, lodft, log_rad, angle, Xrcos, Yrcos, height):

        if height <= 1:

            # Low-pass
            # lo0 = math_utils.batch_ifftshift2d(lodft)
            lodft = torch.complex(real=lodft[:,:,:,0],imag=lodft[:,:,:,1])
            lo0 = torch.fft.ifftshift(lodft, dim=(1, 2))
            # lo0 = torch.ifft(lo0, signal_ndim=2) # old
            lo0 = torch.fft.ifft2(lo0, dim=(1,2))
            # lo0_real = torch.unbind(lo0, -1)[0]
            coeff = [lo0.real]

        else:
            
            Xrcos = Xrcos - np.log2(self.scale_factor)

            ####################################################################
            ####################### Orientation bandpass #######################
            ####################################################################

            himask = pointOp(log_rad, Yrcos, Xrcos)
            himask = torch.from_numpy(himask[None,:,:,None]).float().to(self.device)

            order = self.nbands - 1
            const = np.power(2, 2*order) * np.square(factorial(order)) / (self.nbands * factorial(2*order))
            Ycosn = 2*np.sqrt(const) * np.power(np.cos(self.Xcosn), order) * (np.abs(self.alpha) < np.pi/2) # [n,]

            # Loop through all orientation bands
            orientations = []
            for b in range(self.nbands):

                anglemask = pointOp(angle, Ycosn, self.Xcosn + np.pi*b/self.nbands)
                anglemask = anglemask[None,:,:,None]  # for broadcasting
                anglemask = torch.from_numpy(anglemask).float().to(self.device)

                # Bandpass filtering                
                banddft = lodft * anglemask * himask

                # Now multiply with complex number
                # (x+yi)(u+vi) = (xu-yv) + (xv+yu)i
                banddft = torch.unbind(banddft, -1)
                banddft_real = self.complex_fact_construct.real*banddft[0] - self.complex_fact_construct.imag*banddft[1]
                banddft_imag = self.complex_fact_construct.real*banddft[1] + self.complex_fact_construct.imag*banddft[0]
                # banddft = torch.stack((banddft_real, banddft_imag), -1) # old
                banddft = torch.complex(banddft_real,banddft_imag)
                # band = math_utils.batch_ifftshift2d(banddft)
                band = torch.fft.ifftshift(banddft, dim=(-2, -1))
                # band = torch.ifft(band, signal_ndim=2) # old
                band = torch.fft.ifft2(band, dim=(-2,-1))
                band = torch.stack((band.real, band.imag), -1)

                orientations.append(band)

            ####################################################################
            ######################## Subsample lowpass #########################
            ####################################################################

            # Don't consider batch_size and imag/real dim
            dims = np.array(lodft.shape[1:3])  

            # Both are tuples of size 2
            low_ind_start = (np.ceil((dims+0.5)/2) - np.ceil((np.ceil((dims-0.5)/2)+0.5)/2)).astype(int)
            low_ind_end   = (low_ind_start + np.ceil((dims-0.5)/2)).astype(int)

            # Subsampling indices
            log_rad = log_rad[low_ind_start[0]:low_ind_end[0],low_ind_start[1]:low_ind_end[1]]
            angle = angle[low_ind_start[0]:low_ind_end[0],low_ind_start[1]:low_ind_end[1]]

            # Actual subsampling
            lodft = lodft[:,low_ind_start[0]:low_ind_end[0],low_ind_start[1]:low_ind_end[1],:]

            # Filtering
            YIrcos = np.abs(np.sqrt(1 - Yrcos**2))
            lomask = pointOp(log_rad, YIrcos, Xrcos)
            lomask = torch.from_numpy(lomask[None,:,:,None]).float().to(self.device)

            # Convolution in spatial domain
            lodft = lomask * lodft

            ####################################################################
            ####################### Recursion next level #######################
            ####################################################################

            coeff = self._build_levels(lodft, log_rad, angle, Xrcos, Yrcos, height-1)
            coeff.insert(0, orientations)

        return coeff

    ############################################################################
    ########################### RECONSTRUCTION #################################
    ############################################################################

    def reconstruct(self, coeff):
        # if self.nbands != len(coeff[1]):
        #     raise Exception("Unmatched number of orientations")
        
        height, width = coeff[0].shape[2], coeff[0].shape[1] 
        log_rad, angle = prepare_grid(height, width)

        Xrcos, Yrcos = rcosFn(1, -0.5)
        Yrcos  = np.sqrt(Yrcos)
        YIrcos = np.sqrt(np.abs(1 - Yrcos**2))

        lo0mask = pointOp(log_rad, YIrcos, Xrcos)
        hi0mask = pointOp(log_rad, Yrcos, Xrcos)

        # Note that we expand dims to support broadcasting later
        lo0mask = torch.from_numpy(lo0mask).float()[None,:,:,None].to(self.device)
        hi0mask = torch.from_numpy(hi0mask).float()[None,:,:,None].to(self.device)

        # Start recursive reconstruction
        tempdft = self._reconstruct_levels(coeff[1:], log_rad, Xrcos, Yrcos, angle)

        # hidft = torch.rfft(coeff[0], signal_ndim=2, onesided=False) # old
        hidft = torch.fft.fft2(coeff[0], dim=(1,2))
        # hidft = math_utils.batch_fftshift2d(hidft)
        hidft = torch.fft.fftshift(hidft, dim=(1,2))
        hidft = torch.stack((hidft.real, hidft.imag), -1)

        outdft = tempdft * lo0mask + hidft * hi0mask

        # reconstruction = math_utils.batch_ifftshift2d(outdft)
        temp = torch.complex(outdft[:,:,:,0],outdft[:,:,:,1])
        reconstruction = torch.fft.ifftshift(temp, dim=(1,2))
        # reconstruction = torch.ifft(reconstruction, signal_ndim=2) # old
        reconstruction = torch.fft.ifft2(reconstruction, dim=(1,2))
        # reconstruction = torch.unbind(reconstruction, -1)[0]  # real

        return reconstruction.real

    def _reconstruct_levels(self, coeff, log_rad, Xrcos, Yrcos, angle):
        if len(coeff) == 1:
            dft = torch.fft.fft2(coeff[0],dim=(1,2))
            dft = torch.fft.fftshift(dft, dim=(1,2))
            dft = torch.stack((dft.real, dft.imag), -1)
            return dft

        Xrcos = Xrcos - np.log2(self.scale_factor)

        ####################################################################
        ####################### Orientation Residue ########################
        ####################################################################

        himask = pointOp(log_rad, Yrcos, Xrcos)
        himask = torch.from_numpy(himask[None,:,:,None]).float().to(self.device)

        lutsize = 1024
        Xcosn = np.pi * np.array(range(-(2*lutsize+1), (lutsize+2)))/lutsize
        order = self.nbands - 1
        const = np.power(2, 2*order) * np.square(factorial(order)) / (self.nbands * factorial(2*order))
        Ycosn = np.sqrt(const) * np.power(np.cos(Xcosn), order)

        orientdft = torch.zeros_like(coeff[0][0])

        for b in range(self.nbands):
            anglemask = pointOp(angle, Ycosn, Xcosn + np.pi * b/self.nbands)
            anglemask = anglemask[None,:,:,None]  # for broadcasting
            anglemask = torch.from_numpy(anglemask).float().to(self.device)

            # banddft = torch.fft(coeff[0][b], signal_ndim=2) # old
            temp = torch.complex(coeff[0][b][:,:,:,0],coeff[0][b][:,:,:,1])
            banddft = torch.fft.fft2(temp, dim=(1,2))
            # banddft = torch.fft.fft2(coeff[0][b][:,:,:,0], dim=(1,2))
            # banddft = math_utils.batch_fftshift2d(banddft)
            banddft = torch.fft.fftshift(banddft, dim=(1,2))
            banddft = torch.stack((banddft.real, banddft.imag), -1)

            banddft = banddft * anglemask * himask
            banddft = torch.unbind(banddft, -1)

            banddft_real = self.complex_fact_reconstruct.real*banddft[0] - self.complex_fact_reconstruct.imag*banddft[1]
            banddft_imag = self.complex_fact_reconstruct.real*banddft[1] + self.complex_fact_reconstruct.imag*banddft[0]
            banddft = torch.stack((banddft_real, banddft_imag), -1)
            # banddft = torch.complex(banddft_real,banddft_imag)

            orientdft = orientdft + banddft
        
        ####################################################################
        ########## Lowpass component are upsampled and convoluted ##########
        ####################################################################
        
        dims = np.array(coeff[0][0].shape[1:3])
        
        lostart = (np.ceil((dims+0.5)/2) - np.ceil((np.ceil((dims-0.5)/2)+0.5)/2)).astype(np.int32)
        loend = lostart + np.ceil((dims-0.5)/2).astype(np.int32)

        nlog_rad = log_rad[lostart[0]:loend[0], lostart[1]:loend[1]]
        nangle = angle[lostart[0]:loend[0], lostart[1]:loend[1]]
        YIrcos = np.sqrt(np.abs(1 - Yrcos**2))
        lomask = pointOp(nlog_rad, YIrcos, Xrcos)

        # Filtering
        lomask = pointOp(nlog_rad, YIrcos, Xrcos)
        lomask = torch.from_numpy(lomask[None,:,:,None])
        lomask = lomask.float().to(self.device)

        ################################################################################

        # Recursive call for image reconstruction        
        nresdft = self._reconstruct_levels(coeff[1:], nlog_rad, Xrcos, Yrcos, nangle)
        resdft = torch.zeros_like(coeff[0][0]).to(self.device)
        resdft[:,lostart[0]:loend[0], lostart[1]:loend[1],:] = nresdft * lomask

        return resdft + orientdft
