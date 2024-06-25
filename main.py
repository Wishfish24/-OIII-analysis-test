import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.visualization import ImageNormalize, ZScaleInterval, LinearStretch
import matplotlib.widgets as widgets

# List of your FITS files
fits_files = ['1up.fits', '1down.fits', '2up.fits', '2down.fits', '3up.fits', '3down.fits', 'central.fits']

# Read the data from each FITS file
images = []
for file in fits_files:
    with fits.open(file) as hdul:
        images.append(hdul[0].data)

# Assume all images are the same shape and already aligned
combined_image = np.sum(images, axis=0)

# Create a figure and axis for the plot
fig, ax = plt.subplots(figsize=(10, 10))

# Define the colormap and normalization
cmap = plt.cm.gray  # Use gray colormap
norm = plt.Normalize(vmin=0, vmax=150)

# Initial display of the combined image
img = ax.imshow(combined_image, origin='lower', cmap=cmap, norm=norm)
plt.colorbar(img, ax=ax)
plt.title('Composite Image of Galaxy Showing All Nebulae')
plt.xlabel('X axis')
plt.ylabel('Y axis')

# Define a function to update the plot based on the slider value
def update(val):
    threshold = slider.val
    thresholded_image = np.where(combined_image > threshold, combined_image, 0)
    img.set_data(thresholded_image)
    ax.set_title(f'Composite Image with Threshold={threshold}')
    fig.canvas.draw_idle()

# Create a slider widget
slider_ax = fig.add_axes([0.15, 0.02, 0.7, 0.03])  # [left, bottom, width, height]
slider = widgets.Slider(slider_ax, 'Threshold', 0, np.max(combined_image), valinit=0)
slider.on_changed(update)

plt.show()
