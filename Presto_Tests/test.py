import numpy as np
import matplotlib.pylab as plt

array_size = 1024
width      = 4
# Create the time series of Gaussian noise
mu, sigma = 0, 1.0
time_data  = np.random.normal(mu, sigma, array_size)
# Add in a pulse to the data
for i in range(0,width):
  time_data[array_size//2+i] += 10.0

# Create the kernal
time_kern  = np.zeros(array_size)
for i in range(0,width):
  time_kern[i] = 1.0

# Convolve the time series and the kernel
freq_data = np.fft.rfft(time_data)
freq_kern = np.fft.rfft(time_kern)
freq_conv = freq_data*freq_kern
time_conv = np.fft.irfft(freq_conv)
print(np.max(time_conv))

# Look at the convolved time series
#plt.plot(time_conv.real)
#plt.plot(time_data)
#plt.plot(time_conv.imag)
#plt.show()
