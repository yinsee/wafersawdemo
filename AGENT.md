# SAW Demo - AOI Pan

## Project Overview
This project is an interactive HTML prototype simulating the UI of a machine vision system (e.g., a dicing saw). It features a static user interface overlay with a pannable camera feed ("AOI" - Area of Interest) underneath.

## Architecture & Components
- **`index.html`**: The main entry point. It constructs the interactive stage using HTML and CSS, and handles the panning logic via JavaScript.
- **`main-ui.png` (1024x768)**: The primary background interface image, featuring the full application layout with a solid blue placeholder box cut out for the camera feed.
- **`ui.png` (513x480)**: A transparent PNG containing the static UI overlays for the camera feed (such as the green crosshairs, buttons, and specific white text/squares).
- **`aoi.png` (513x480 native)**: The clean camera feed image (wafer structure) with all UI elements inpainted.

## Display Mechanics
1. The **`#stage`** is scaled dynamically to fit the browser viewport while maintaining the original 1024x768 aspect ratio.
2. The **`#placeholder`** acts as a fixed viewing window for the camera feed, located at:
   - **Left**: 14px
   - **Top**: 106px
   - **Width**: 513px
   - **Height**: 480px
3. **Layering**:
   - Bottom: `main-ui.png`
   - Middle (`#aoi`): The camera feed (`aoi.png`) is enlarged by **1.25x** inside the placeholder.
   - Top (`#ui-layer`): The static UI elements (`ui.png`) are pinned precisely over the placeholder, ensuring they remain stationary.

## Interactions
- **Panning**: Users can use the keyboard arrow keys (`Up`, `Down`, `Left`, `Right`) to pan the enlarged `aoi.png` image underneath the static `ui.png` overlay.
- **Boundaries**: The panning logic detects the edges of the scaled `aoi.png` image and clamps movement so the user cannot pan past the image boundaries.
- **Speed**: Movement is fixed at **2px** per key press.

- **Hairline Adjustment Mode**:
  - **F7 (Wafer Icon)**: Click the F7 button (wafer icon with arrows) to toggle the "Hairline ADJ" menu panel at the bottom of the screen. There is no keyboard hotkey for toggling this panel.
  - **F3 (Widen Hair)**: While in ADJ mode, click the "F3" button or press the `F3` key to move the top and bottom dashed green lines away from the center by 2px (up to a maximum offset of 240px).
  - **F8 (Narrow Hair)**: While in ADJ mode, click the "F8" button or press the `F8` key to move the dashed lines closer to the center by 2px (down to a minimum offset of 0px).
  - **Animation**: The interactive buttons overlay the original UI and feature a realistic "sink in" press animation using CSS pseudo-classes and background offsets. The background image of the buttons seamlessly switches to match the `adjust.jpeg` panel when toggled.