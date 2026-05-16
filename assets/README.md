# Watch Face Background Images

Place your watch face background images here.

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
    "image": "assets/watch_face.png",
    "scale": 1.0
  }
}
```

3. Restart the application

## Image requirements
- Best size: 512x512 pixels (or square)
- The image will be scaled to fit the watch face
- Use a watch face design with:
  - Dark grey metallic background
  - Hour markers (12, 3, 6, 9)
  - Minute markers
  - Clear center area for hands

## Example images
You can find example watch face images online or create one in:
- Photoshop
- GIMP
- Any image editor