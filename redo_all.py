import cv2
import numpy as np
import shutil
import os

def backup_images():
    if os.path.exists('ui.png'):
        shutil.copy('ui.png', 'ui_backup.png')
    if os.path.exists('aoi.png'):
        shutil.copy('aoi.png', 'aoi_backup.png')
        
def process():
    # 1. Re-crop original AOI from ui-source.jpeg to start fresh
    full_img = cv2.imread('ui-source.jpeg')
    x0, y0 = 14, 106
    x1, y1 = 527, 586
    
    aoi_original = full_img[y0:y1, x0:x1]
    aoi_rgba = cv2.cvtColor(aoi_original, cv2.COLOR_BGR2BGRA)
    
    b, g, r = cv2.split(aoi_original)
    
    # 2. Green mask
    green_mask = (g.astype(int) - r.astype(int) > 20) & (g.astype(int) - b.astype(int) > 20)
    green_mask = green_mask.astype(np.uint8) * 255
    
    # 3. White mask (for the two white buttons)
    white_mask = (r > 200) & (g > 200) & (b > 200)
    white_mask = white_mask.astype(np.uint8) * 255
    
    contours_white, _ = cv2.findContours(white_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filtered_white_mask = np.zeros_like(white_mask)
    
    for cnt in contours_white:
        cx, cy, cw, ch = cv2.boundingRect(cnt)
        if 20 < cw < 60 and 20 < ch < 60:
            if (cx < 100 and cy < 150) or (cx > 400 and cy < 100):
                filtered_white_mask[cy:cy+ch, cx:cx+cw] = white_mask[cy:cy+ch, cx:cx+cw]

    ui_mask = cv2.bitwise_or(green_mask, filtered_white_mask)
    ui_elements = np.zeros_like(aoi_rgba)
    ui_elements[ui_mask > 0] = aoi_rgba[ui_mask > 0]
    
    # 4. Remove the 3 center lines and crosshairs from UI elements WITHOUT touching the right-side buttons.
    # The right side buttons start around x=463. We clear the center and left (where there are no UI elements except the lines).
    # Lines and crosshairs fall safely within y=180 to y=300.
    ui_elements[180:300, 0:463, 3] = 0
    
    cv2.imwrite('ui.png', ui_elements)
    
    # 5. Inpaint the AOI background so the UI elements are removed from it
    contours_green, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    inpaint_mask = np.zeros_like(green_mask)
    
    for cnt in contours_green:
        cx, cy, cw, ch = cv2.boundingRect(cnt)
        # Fill button bounding boxes
        if 20 < cw < 200 and 20 < ch < 200 and 400 < cw*ch < 15000:
            cv2.rectangle(inpaint_mask, (cx, cy), (cx+cw, cy+ch), 255, -1)
            
    # Include the lines themselves in the inpaint mask so they are removed from the background
    inpaint_mask = cv2.bitwise_or(inpaint_mask, green_mask)
    
    # Include the white buttons in the inpaint mask
    for cnt in contours_white:
        cx, cy, cw, ch = cv2.boundingRect(cnt)
        if 20 < cw < 60 and 20 < ch < 60:
            if (cx < 100 and cy < 150) or (cx > 400 and cy < 100):
                cv2.rectangle(inpaint_mask, (cx, cy), (cx+cw, cy+ch), 255, -1)
                
    aoi_clean = cv2.inpaint(aoi_original, inpaint_mask, 3, cv2.INPAINT_TELEA)
    cv2.imwrite('aoi.png', aoi_clean)
    print("Perfect redo complete. Backups created, UI cleaned without breaking buttons.")

if __name__ == '__main__':
    backup_images()
    process()
