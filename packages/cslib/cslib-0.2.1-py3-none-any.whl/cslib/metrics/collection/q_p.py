from cslib.metrics.utils import fusion_preprocessing
from typing import Tuple
import torch

__all__ = [
    'q_p',
    'q_p_approach_loss',
    'q_p_metric'
]

def lowpassfilter(sze: Tuple[int, int], cutoff: float, n: int) -> torch.Tensor:
    """
    Creates a 2D lowpass filter for image processing.

    Args:
        sze (Tuple[int, int]): A tuple containing the number of rows and columns in the filter.
        cutoff (float): The cutoff frequency of the filter (0 to 0.5).
        n (int): The order of the filter (must be an integer >= 1).

    Returns:
        torch.Tensor: A 2D tensor representing the lowpass filter.
    """
    if cutoff < 0 or cutoff > 0.5:
        raise ValueError('cutoff frequency must be between 0 and 0.5')
    if not isinstance(n, int) or n < 1:
        raise ValueError('n must be an integer >= 1')

    rows, cols = sze
    x = (torch.matmul(torch.ones((rows,1)),torch.arange(1,cols+1).unsqueeze(0)*1.0) - (cols//2+1.0)) / cols
    y = (torch.matmul(torch.arange(1,rows+1).unsqueeze(-1)*1.0,torch.ones((1,cols))) - (rows//2+1.0)) / rows

    radius = torch.sqrt(x**2 + y**2)
    f = 1 / (1.0 + (radius / cutoff)**(2 * n))
    return torch.fft.fftshift(f)

def myphasecong3(im: torch.Tensor, nscale: int = 4, norient: int = 6,
                  minWaveLength: int = 3, mult: float = 2.1,
                  sigmaOnf: float = 0.55, dThetaOnSigma: float = 1.2,
                  k: float = 2.0, cutOff: float = 0.5,
                  g: int = 10, epsilon: float = 1e-10):
    """
    Computes phase congruency of an image using the phase congruency algorithm.

    Args:
        im (torch.Tensor): Input image tensor.
        nscale (int, optional): Number of wavelet scales. Defaults to 4.
        norient (int, optional): Number of filter orientations. Defaults to 6.
        minWaveLength (int, optional): Wavelength of smallest scale filter. Defaults to 3.
        mult (float, optional): Scaling factor between successive filters. Defaults to 2.1.
        sigmaOnf (float, optional): Ratio of the standard deviation of the Gaussian describing the log Gabor filter's
                                    transfer function in the frequency domain to the filter center frequency.
                                    Defaults to 0.55.
        dThetaOnSigma (float, optional): Ratio of angular interval between filter orientations and the standard deviation
                                        of the angular Gaussian function used to construct filters in the frequency plane.
                                        Defaults to 1.2.
        k (float, optional): Number of standard deviations of the noise energy beyond the mean at which we set the noise
                            threshold point. Defaults to 2.0.
        cutOff (float, optional): The fractional measure of frequency spread below which phase congruency values get
                                penalized. Defaults to 0.5.
        g (int, optional): Controls the sharpness of the transition in the sigmoid function used to weight phase congruency
                            for frequency spread. Defaults to 10.
        epsilon (float, optional): A small value used to prevent division by zero. Defaults to 1e-10.
    """
    # (thetaSigma) Calculate the standard deviation of the
    # angular Gaussian function used to
    # construct filters in the freq. plane.
    thetaSigma = torch.pi/norient/dThetaOnSigma
    _ , _, rows, cols = im.shape
    imagefft = torch.fft.fft2(im) # Fourier transform of image

    zero = torch.zeros(1,1,rows, cols, dtype=torch.float32)
    totalEnergy = zero.clone()  # Total weighted phase congruency values (energy).
    totalSumAn = zero.clone()   # Total filter response amplitude values.
    orientation = zero.clone()  # Matrix storing orientation with greatest

    EO = torch.empty(nscale, norient, rows, cols, dtype=torch.complex64) # Array of convolution results.
    covx2 = zero.clone()        # Matrices for covariance data
    covy2 = zero.clone()
    covxy = zero.clone()

    estMeanE2n = torch.empty(norient, dtype=torch.float32)

    ifftFilterArray = [] # Array of inverse FFTs of filters

    # Pre-compute some stuff to speed up filter construction

    # Set up X and Y matrices with ranges normalised to +/- 0.5
    # The following code adjusts things appropriately for odd and even values
    # of rows and columns.

    if cols//2 == 0:
        xrange = torch.arange(-(cols-1)/2, (cols-1)/2 + 1) / (cols - 1)
    else:
        xrange = torch.arange(-cols/2, cols/2) / cols
    if rows//2 == 0:
        yrange = torch.arange(-(rows-1)/2, (rows-1)/2 + 1) / (rows - 1)
    else:
        yrange = torch.arange(-rows/2, rows/2) / rows

    x, y = torch.meshgrid(xrange, yrange)

    radius = torch.sqrt(x**2 + y**2).T # Matrix values contain *normalised* radius from centre.
    radius[rows//2, cols//2] = 1 # so that taking the log of the radius will not cause trouble.
    theta = torch.atan2(-y, x) # % Matrix values contain polar angle. (note -ve y is used to give +ve anti-clockwise angles)
    radius = torch.fft.ifftshift(radius) # Quadrant shift radius and theta so that filters
    theta = torch.fft.ifftshift(theta)   # are constructed with 0 frequency at the corners.

    sintheta = torch.sin(theta)
    costheta = torch.cos(theta)

    # Filters are constructed in terms of two components.
    # 1) The radial component, which controls the frequency band that the filter
    #    responds to
    # 2) The angular component, which controls the orientation that the filter
    #    responds to.
    # The two components are multiplied together to construct the overall filter.

    # Construct the radial filter components...

    # First construct a low-pass filter that is as large as possible, yet falls
    # away to zero at the boundaries.  All log Gabor filters are multiplied by
    # this to ensure no extra frequencies at the 'corners' of the FFT are
    # incorporated as this seems to upset the normalisation process when
    # calculating phase congrunecy.

    lp = lowpassfilter((rows, cols), 0.45, 15)  # Radius 0.45, 'sharpness' 15

    logGabor = []
    for s in range(nscale):
        wavelength = minWaveLength * mult ** s
        fo = 1.0 / wavelength  # Centre frequency of filter.
        lg = torch.exp(-(torch.log(radius/fo)**2) / (2 * torch.log(torch.tensor(sigmaOnf))**2))
        temp = lg * lp         # Apply low-pass filter
        temp[0, 0] = 0         # Set the value at the 0 frequency point of the filter
        logGabor.append(temp)  # back to zero (undo the radius fudge).

    # Then construct the angular filter components...
    spread = []
    for o in range(norient):
        angl = torch.tensor(o * torch.pi / norient)
        # For each point in the filter matrix calculate the angular distance from
        # the specified filter orientation.  To overcome the angular wrap-around
        # problem sine difference and cosine difference values are first computed
        # and then the atan2 function is used to determine angular distance.
        ds = sintheta * torch.cos(angl) - costheta * torch.sin(angl) # Difference in sine.
        dc = costheta * torch.cos(angl) + sintheta * torch.sin(angl) # Difference in cosine.
        dtheta = torch.abs(torch.atan2(ds, dc))                      # Absolute angular distance.
        sp = torch.exp(-dtheta**2 / (2 * (torch.pi / norient / dThetaOnSigma)**2)) # % Calculate the angular filter component.
        spread.append(sp.T)

    # % The main loop...
    for o in range(norient): # For each orientation.
        # angl = o * torch.tensor(torch.pi / norient) # Filter angle.
        sumE_ThisOrient = zero.clone() # Initialize accumulator matrices.
        sumO_ThisOrient = zero.clone()
        sumAn_ThisOrient = zero.clone()
        Energy = zero.clone()

        maxAn = torch.tensor(0.0)              # 先声明变量
        for s in range(nscale):                # For each scale.
            filt = logGabor[s] * spread[o]     # Multiply radial and angular components to get the filter.
            filt = filt.unsqueeze(0).unsqueeze(0)
            ifftFilt = torch.fft.ifft2(filt).real * torch.sqrt(torch.tensor(rows * cols, dtype=torch.float32)) # Note rescaling to match power
            ifftFilterArray.append(ifftFilt)   # record ifft2 of filter
            # Convolve image with even and odd filters returning the result in EO
            EO = torch.fft.ifft2(imagefft * filt)#.unsqueeze(-1).unsqueeze(-1))
            print(torch.mean(filt))
            print(torch.mean(imagefft))
            print(torch.mean(EO))
            breakpoint()
            An = torch.abs(EO)                 # Amplitude of even & odd filter response.
            sumAn_ThisOrient += An             # Sum of amplitude responses.
            sumE_ThisOrient += torch.real(EO)  # Sum of even filter convolution results.
            sumO_ThisOrient += torch.imag(EO)  # Sum of odd filter convolution results.

            if s == 0:                         # Record mean squared filter value at smallest
                EM_n = torch.sum(filt**2)      # scale. This is used for noise estimation.
                maxAn = An                     # Record the maximum An over all scales.
            else:
                maxAn = torch.max(maxAn, An)
        continue

        # Get weighted mean filter response vector, this gives the weighted mean
        # phase angle.
        XEnergy = torch.sqrt(sumE_ThisOrient**2 + sumO_ThisOrient**2) + epsilon
        MeanE = sumE_ThisOrient / XEnergy
        MeanO = sumO_ThisOrient / XEnergy


        # Now calculate An(cos(phase_deviation) - | sin(phase_deviation)) | by
        # using dot and cross products between the weighted mean filter response
        # vector and the individual filter response vectors at each scale.  This
        # quantity is phase congruency multiplied by An, which we call energy.

        for s in range(nscale):
            E = torch.real(EO) # Extract even and odd
            O = torch.imag(EO) # convolution results.
            Energy += E * MeanE + O * MeanO - torch.abs(E * MeanO - O * MeanE)

        # Compensate for noise
        # We estimate the noise power from the energy squared response at the
        # smallest scale.  If the noise is Gaussian the energy squared will have a
        # Chi-squared 2DOF pdf.  We calculate the median energy squared response
        # as this is a robust statistic.  From this we estimate the mean.
        # The estimate of noise power is obtained by dividing the mean squared
        # energy value by the mean squared filter value

        medianE2n = torch.median(torch.reshape(torch.abs(EO)**2, (1, rows * cols)))
        meanE2n = -medianE2n / torch.log(torch.tensor(0.5))
        estMeanE2n[o] = meanE2n
        noisePower = meanE2n / EM_n # Estimate of noise power.

        # Now estimate the total energy^2 due to noise
        # Estimate for sum(An^2) + sum(Ai.*Aj.*(cphi.*cphj + sphi.*sphj))
        EstSumAn2 = zero.clone()
        for si in range(nscale):
            EstSumAn2 += ifftFilterArray[si]**2

        EstSumAiAj = zero.clone()
        for si in range(nscale - 1):
            for sj in range(si + 1, nscale):
                EstSumAiAj += ifftFilterArray[si] * ifftFilterArray[sj]

        sumEstSumAn2 = torch.sum(EstSumAn2)
        sumEstSumAiAj = torch.sum(EstSumAiAj)

        EstNoiseEnergy2 = 2 * noisePower * sumEstSumAn2 + 4 * noisePower * sumEstSumAiAj

        tau = torch.sqrt(EstNoiseEnergy2 / 2)                         # Rayleigh parameter
        EstNoiseEnergy = tau * torch.sqrt(torch.tensor(torch.pi / 2)) # Expected value of noise energy
        EstNoiseEnergySigma = torch.sqrt((2 - torch.pi / 2) * tau**2)
        T = EstNoiseEnergy + k * EstNoiseEnergySigma                  # Noise threshold

        # The estimated noise effect calculated above is only valid for the PC_1 measure.
        # The PC_2 measure does not lend itself readily to the same analysis.  However
        # empirically it seems that the noise effect is overestimated roughly by a factor
        # of 1.7 for the filter parameters used here.
        T = T / 1.7
        # Empirical rescaling of the estimated noise effect to
        # suit the PC_2 phase congruency measure
        Energy = torch.max(Energy - T, zero) # Apply noise threshold
        # Form weighting that penalizes frequency distributions that are
        # particularly narrow.  Calculate fractional 'width' of the frequencies
        # present by taking the sum of the filter response amplitudes and dividing
        # by the maximum amplitude at each point on the image.
        width = sumAn_ThisOrient / (torch.max(sumAn_ThisOrient) + epsilon) / nscale

        # Now calculate the sigmoidal weighting function for this orientation.
        weight = 1.0 / (1 + torch.exp((cutOff - width) * g))

        Energy_ThisOrient = weight * Energy
        totalSumAn += sumAn_ThisOrient
        totalEnergy += Energy_ThisOrient

        if o == 0:
            maxEnergy = Energy_ThisOrient
        else:
            change = Energy_ThisOrient > maxEnergy
            orientation = (o - 1) * change + orientation * (~change)
            maxEnergy = torch.max(maxEnergy, Energy_ThisOrient)


def q_p(A, B, F):
    '''
    Reference:
        J. Zhao, R. Laganiere, Z. Liu, Performance assessment of combinative 
        pixellevel image fusion based on an absolute feature measurement, 
        Int. J. Innovative Comput. Inf. Control 3 (6) (2007) 1433-1447.
    '''
    # 0) some global parameters
    fea_threshold=0.1 # threshold value for the feature

    # 1) first, calculate the PC
    myphasecong3(A)
    # myphasecong3(B)
    # myphasecong3(F)

def q_p_approach_loss(A, F):
    pass

@fusion_preprocessing
def q_p_metric(A, B, F):
    return q_p(A*255.0,B*255.0,F*255.0)

def main():
    from cslib.metrics.fusion import ir,vis,fused
    print(f'Q_p(vis,ir,fused):{q_p_metric(vis,ir,fused)}')

if __name__ == '__main__':
    main()
