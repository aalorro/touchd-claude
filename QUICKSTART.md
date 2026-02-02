# TouchDesigner Clone - Quick Start Guide

## Installation (60 seconds)

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Test the installation
python touchdesigner_clone.py --list-presets

# 3. See all supported formats
python touchdesigner_clone.py --list-formats
```

## Your First Effect (30 seconds)

```bash
# Run with default settings (1080x1080 square, cyber_glitch preset)
python touchdesigner_clone.py

# This will:
# - Create a 1080x1080 generative image
# - Apply RGB split + displacement + scanlines + edge glow
# - Show real-time preview for 5 seconds
```

## Create Your First Video (2 minutes)

```bash
# Create a 15-second holographic video (1080x1080 square)
python touchdesigner_clone.py \
    --preset holographic \
    --duration 15 \
    --output my_first_video.mp4 \
    --intensity 0.8
```

## Social Media Ready (1 minute each)

```bash
# Instagram Story (9:16 vertical, 1080p)
python touchdesigner_clone.py \
    --aspect-ratio 9:16 \
    --preset cyber_glitch \
    --output story.mp4

# YouTube Video (16:9 widescreen, 1080p)
python touchdesigner_clone.py \
    --aspect-ratio 16:9 \
    --preset holographic \
    --output youtube.mp4

# Instagram Post (1:1 square, 1080p) - This is the default!
python touchdesigner_clone.py \
    --preset psychedelic \
    --output post.mp4

# TikTok (9:16 vertical, 1080p)
python touchdesigner_clone.py \
    --aspect-ratio 9:16 \
    --preset neon_city \
    --output tiktok.mp4
```

## Use Your Own Image (1 minute)

```bash
# Apply effects to your photo (auto-crops to square)
python touchdesigner_clone.py \
    --image your_photo.jpg \
    --preset psychedelic \
    --duration 10

# Or create vertical story with your photo
python touchdesigner_clone.py \
    --image photo.jpg \
    --aspect-ratio 9:16 \
    --preset cyber_glitch \
    --output story.mp4
```

## Try All Presets (5 minutes)

```bash
# Cyber/Glitch Effects (default 1080x1080)
python touchdesigner_clone.py --preset cyber_glitch
python touchdesigner_clone.py --preset datamosh

# Psychedelic/Artistic
python touchdesigner_clone.py --preset psychedelic
python touchdesigner_clone.py --preset fractal_dream

# Sci-Fi/Futuristic
python touchdesigner_clone.py --preset holographic
python touchdesigner_clone.py --preset neon_city

# Retro/Vintage
python touchdesigner_clone.py --preset retro_vhs

# Abstract/Motion
python touchdesigner_clone.py --preset particle_flow
python touchdesigner_clone.py --preset time_warp

# Atmospheric
python touchdesigner_clone.py --preset volumetric_fog
```

## Different Aspect Ratios (2 minutes)

```bash
# Square (1:1) - Default, perfect for Instagram posts
python touchdesigner_clone.py --aspect-ratio 1:1 --preset psychedelic

# Vertical (9:16) - Instagram Stories, TikTok, Reels
python touchdesigner_clone.py --aspect-ratio 9:16 --preset cyber_glitch

# Widescreen (16:9) - YouTube, TV, presentations
python touchdesigner_clone.py --aspect-ratio 16:9 --preset holographic

# Classic TV (4:3) - Retro content
python touchdesigner_clone.py --aspect-ratio 4:3 --preset retro_vhs

# Portrait (3:4) - Vertical posters, portrait photos
python touchdesigner_clone.py --aspect-ratio 3:4 --preset neon_city
```

## Different Resolutions (3 minutes)

```bash
# 720p - Fast preview, smaller files
python touchdesigner_clone.py --resolution 720 --preset psychedelic

# 1080p - Default, perfect for social media
python touchdesigner_clone.py --resolution 1080 --preset cyber_glitch

# 2K - High quality for desktop
python touchdesigner_clone.py --resolution 2k --preset holographic

# 4K - Maximum quality for YouTube/archival
python touchdesigner_clone.py --resolution 4k --preset neon_city
```

## Python API - Quick Examples

### Minimal Example (3 lines)

```python
from touchdesigner_clone import create_preset_demo

create_preset_demo('cyber_glitch', duration=10)
```

### Basic Custom Effects (10 lines)

```python
from touchdesigner_clone import TouchDesignerClone

app = TouchDesignerClone()
app.create_generative_image()
app.add_effect('kaleidoscope')
app.add_effect('edge_glow')
app.set_global_intensity(0.7)
app.run_interactive(duration=5)
```

### Export Video (12 lines)

```python
from touchdesigner_clone import TouchDesignerClone

app = TouchDesignerClone(width=1920, height=1080)
app.create_generative_image(seed=42)
app.add_effect('hologram')
app.add_effect('volumetric')
app.set_global_intensity(0.8)

app.start_recording('output.mp4', fps=60)
app.run_interactive(duration=15, fps=60)
app.stop_recording()
```

## Common Use Cases

### For Music Videos
```bash
python touchdesigner_clone.py \
    --preset psychedelic \
    --intensity 0.9 \
    --duration 180 \
    --output music_video.mp4
```

### For Social Media
```bash
# Instagram-ready 15-second clip
python touchdesigner_clone.py \
    --preset cyber_glitch \
    --duration 15 \
    --intensity 0.7 \
    --output insta_clip.mp4
```

### For Digital Art
```python
from touchdesigner_clone import TouchDesignerClone

app = TouchDesignerClone(width=2048, height=2048)
app.create_generative_image(seed=12345)
app.add_effect('fractal')
app.add_effect('kaleidoscope')
app.set_global_intensity(1.0)

# Export single frame
app.current_frame = app.input_image.copy()
processed = app.process_frame()
processed.save('digital_art.png')
```

## Intensity Guide

- **0.0-0.3**: Subtle, professional enhancement
- **0.3-0.5**: Noticeable but tasteful effects
- **0.5-0.7**: Strong visual impact (default zone)
- **0.7-0.9**: Heavy, dramatic effects
- **0.9-1.0**: Maximum intensity, experimental

## Tips for Best Results

1. **Start Simple**: Begin with one or two effects
2. **Experiment with Intensity**: Try 0.3, 0.5, 0.7, 0.9
3. **Chain Effects**: Combine complementary effects
4. **Use Seeds**: For reproducible generative images
5. **Export at Higher FPS**: Use 60fps for smooth motion

## Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "Slow performance"
- Reduce resolution: `TouchDesignerClone(width=854, height=480)`
- Lower FPS: `run_interactive(fps=24)`
- Use fewer effects simultaneously

### "Can't see the preview"
- Close the preview window to stop playback
- Check that matplotlib is installed
- Try running examples.py for interactive demos

## Next Steps

1. **Explore Examples**: `python examples.py`
2. **Read Full Documentation**: See README.md
3. **Experiment**: Try different effect combinations
4. **Create**: Make something amazing!

## Effect Cheat Sheet

**Glitch/Digital:**
- rgb_split, pixel_sort, displace, scanlines

**Psychedelic:**
- kaleidoscope, feedback, fractal, lut

**Cyberpunk:**
- edge_glow, rgb_split, scanlines, hologram

**Atmospheric:**
- volumetric, heat_haze, feedback, edge_glow

**Motion:**
- optical_flow, particles, plexus, slit_scan

**Retro:**
- scanlines, posterize, rgb_split, feedback

Have fun creating! 🎨✨
