# Watch Face Background Images

Place your watch face background images here.

## Current Files

- `watch_face.png` - Main watch face (no hands, black LCD areas)
- `watch_bezel_without_face.png` - Rotating bezel overlay
- `6x7seg.png` - Reference image for 7-segment display style
- `fonts/DSEG7Classic-Bold.ttf` - 7-segment LCD font

## Supported formats
- PNG (recommended)
- JPG/JPEG
- BMP

## How to use

1. Place your image in this folder (e.g., `assets/watch_face.png`)
2. Edit `config.json` and set the image path:
```json
{
  "background": {
    "image": "assets/your_image.png"
  }
}
```

3. Restart the application

## Image requirements
- Best size: Square aspect ratio (e.g., 512x512, 613x613)
- The image will be scaled to fit inside the bezel
- Use a watch face design with:
  - Dark grey metallic background
  - Black LCD areas for date/day and UTC time
  - Clear center area for analog hands

## Bezel Image
- The bezel image (`watch_bezel_without_face.png`) is drawn behind the watch face
- It rotates when you click and drag on the outer bezel area
- Rotation angle is saved between sessions

## LCD Areas
- Upper LCD: Date + Day (e.g., "16:05 sat")
- Lower LCD: UTC time (e.g., "14:32:45")
- LCD areas should be black rectangles in the image
- The DSEG7 font renders directly over these areas
