import cv2
import numpy as np

def clean():
    img = cv2.imread('ui.png', cv2.IMREAD_UNCHANGED)
    
    # Rows for the lines: ~192, 238, 284. Let's define the bands.
    bands = [(189, 196), (235, 243), (281, 288)]
    
    alpha = img[:, :, 3]
    
    # Clean left side completely in these bands
    for (y0, y1) in bands:
        alpha[y0:y1, :100] = 0
        
    # Clean right side selectively.
    # We want to remove the horizontal lines but keep the vertical button borders and arrows.
    # The horizontal line is only a few pixels thick.
    for (y0, y1) in bands:
        for y in range(y0, y1):
            for x in range(450, img.shape[1]):
                if alpha[y, x] > 0:
                    # Check if it's part of a vertical structure
                    # If we look a few pixels above and below (outside the band), is there a pixel?
                    # Since the band is thin (e.g. y0 to y1 is ~7 pixels),
                    # if this pixel is part of a vertical line, there should be pixels above y0 and below y1 at this x.
                    has_above = np.any(alpha[y-6:y-2, x] > 0)
                    has_below = np.any(alpha[y+3:y+7, x] > 0)
                    
                    if not (has_above and has_below):
                        alpha[y, x] = 0
                        
    img[:, :, 3] = alpha
    cv2.imwrite('ui.png', img)
    print("Cleaned ui.png")

if __name__ == '__main__':
    clean()
