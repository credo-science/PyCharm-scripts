from typing import List, Tuple
from credo_cf.commons.utils import get_and_set
from credo_cf.commons.consts import BRIGHT_PIXELS,GOOD_BRIGHT, GRAY
import numpy as np


def bright_detections(detections: List[dict], bright_pixels=70, threshold=70,low_bright_pixels = 70,treshold_low = 30) -> Tuple[List[dict], List[dict],List[dict]]:
    """
        Analysis of the detection slice by checking the brightness of the pixels

        :param detections: list of detections
        :param bright_pixels (int) : maximum number of bright pixels on the slice (wycinek)
        :param threshold (int) – value of pixels for the bright_pixel (i.e bright pixel is when pixel have value >70)
        :param low_bright_pixels (int) : maximun number of pixels that are not bright pixels (value less than 70) but still visible
        :param treshold_low (int) – value of pixels for the low_bright_pixel (i.e low bright pixel is when pixel have value >30 and <70)

        Pobieramy kod obrazka w skali szarości w tablicy numpy. Wykorzystujemy wbudwane funkcje biblioteki numpy do sprawdzenia
        ile recordów (pojedyńczy element) tablicy jest większych niż próg - otrzymujemy wartość 0 - 1, więc sumując tablice
        dostaniemy na koniec ile przypadków spełniło dany przypadek.
        Następnie sprawdzamy w podobny sposób ile jest mało jasnych pikseli (wartość 30-70).

        Na koniec sprawdzamy czy liczba pikseli jest mniejsza od narzuconych progów ilości jeśli tak, uznajemy że to jest dobra detekcja.


        Required keys:
          * ``frame_content``: base64 image our detection

        Keys will be add:
          * ``BRIGHT_PIXELS``: number of bright pixels
          * ``GOOD_BRIGH``: True,or False.

        gray change used:
        https://pillow.readthedocs.io/en/stable/reference/Image.html

        Example::
          good,bad =  bright_detections(detections,70,70)
          good,bad =  bright_detections(detections,70,70,40,30)

        :return: tuple of (list of good detections, list of bad detections)
        Return type
        Tuple[List[dict], List[dict]]
    """
    good = []
    bad = []
    who_knows = []
    for image in detections:
        img =image[GRAY]
        count_bright_pixels= img > threshold
        suma = int(np.sum(count_bright_pixels))
        get_and_set(image, BRIGHT_PIXELS, suma)
        get_and_set(image, GOOD_BRIGHT, "False")

        dark_pixels= img < treshold_low# count when x<30
        sum_dark_pixels = int(np.sum(dark_pixels))

        low_than_bright_pixels = img < threshold # count when x<70
        sum_low_than_bright_pixels = int(np.sum(low_than_bright_pixels))

        suma_low = sum_low_than_bright_pixels - sum_dark_pixels

        if 0< suma < bright_pixels:
            if suma_low>low_bright_pixels:
                who_knows.append(image)
            else:
                image[GOOD_BRIGHT] = "True"
                good.append(image)
        else:
            bad.append(image)

    return good, bad, who_knows


