import numpy as np
from PIL import Image
from io import BytesIO
Image.LOAD_TRUNCATED_IMAGES = True
from astropy.stats import gaussian_fwhm_to_sigma
from astropy.convolution import Gaussian2DKernel
from photutils import detect_sources, source_properties
from skimage.measure import regionprops
from credo_cf.commons.consts import IMAGE
from credo_cf.io.io_utils import decode_base64

def astropy_analyze(detection):#after convert to Grayscale

    image_cod = detection["frame_content"]
    try:
        decode = decode_base64(image_cod)
        img = Image.open(BytesIO(decode)).convert('LA')

        gray, alpha = img.split()
        data = np.asarray(gray)  # convert to NumPy array
        brightest = data.max()
        darkest = brightest
        rows = data.shape[0]
        cols = data.shape[1]
        for x in range(0, cols):
            for y in range(0, rows):
                v = data[y, x]
                if v:  # skip pixels with 0 bright
                    darkest = min(darkest, v)
        threshold = np.ones(data.shape) * ((brightest - darkest) / 8 + darkest)

        sigma = 3.0 * gaussian_fwhm_to_sigma  # FWHM = 3.
        kernel = Gaussian2DKernel(sigma, x_size=3, y_size=3)
        kernel.normalize()
        segm = detect_sources(data, threshold, npixels=5, filter_kernel=kernel)
        cat = source_properties(data, segm)
        for obj in cat:
            detection['ellipticity'] = str(round(obj.ellipticity.value, 4))
            try:
                another_props = regionprops(obj.data_cutout)[0]
                detection['solidity'] = str(round(another_props.solidity, 4))
                detection['major_axis_length'] = str(round(another_props.major_axis_length, 4))
                detection['minor_axis_length'] = str(round(another_props.minor_axis_length, 4))

            except Exception as e:
                detection['solidity'] = 9999
                detection['major_axis_length'] = 9999
                detection['minor_axis_length'] = 9999
                continue
    except:
        detection['ellipticity'] = 9999
        detection['solidity'] = 9999
        detection['major_axis_length'] = 9999
        detection['minor_axis_length'] = 9999


    return detection
