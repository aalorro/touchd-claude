# TouchDesigner-Inspired Visual Effects Generator

A powerful Python application that mimics TouchDesigner's visual effects capabilities for creating stunning videos with moving 3D objects, holograms, graphs, vectors, and fractals.

## 🌟 Features

### 20+ Professional Visual Effects

1. **Feedback Loops** - Infinite trails, smear, echo effects
2. **Warp/Displacement** - Bend images using noise and flow data
3. **Optical Flow** - Motion vector-driven particle warps
4. **RGB Split** - Chromatic aberration with channel delays
5. **Kaleidoscope** - Mirror and rotate for instant pattern magic
6. **Pixel Sorting** - Datamosh-style pixel smears
7. **Edge Glow** - Neon wireframe and outline effects
8. **Posterize** - Crunchy retro display vibes with dithering
9. **LUT Remapping** - Wild gradient color palettes
10. **Heat Haze** - Moving shimmer and watery distortions
11. **Particle System** - Flow-field particle advection
12. **Plexus Network** - Connected points visualization
13. **Strobe** - Rhythmic frame holds and stepped motion
14. **Scanlines** - CRT roll and VHS wobble effects
15. **Slit-Scan** - Time displacement effects
16. **Volumetric Fog** - Atmospheric beams and haze
17. **Fractal Generation** - Mandelbrot and Julia sets
18. **Hologram** - Interference patterns and chromatic shifts

### Control Features

- **Intensity Dial**: Fine-tune effect strength from 0.0 to 1.0
- **Effect Chaining**: Combine multiple effects for complex visuals
- **Real-time Preview**: Interactive matplotlib-based viewer
- **Video Export**: Record animations to MP4 format
- **Image Generation**: Create procedural starting images
- **Audio Reactivity**: Effects respond to audio levels (framework included)
- **Aspect Ratio Support**: 1:1 (default), 3:4, 4:3, 9:16, 16:9
- **Multiple Resolutions**: 720p, 1080p (default), 2K, 4K
- **Smart Cropping**: Center-crop images to match aspect ratio (no stretching)

## 📦 Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or install individually
pip install numpy opencv-python Pillow moderngl pygame PyOpenGL PyGLM scipy matplotlib
```

## 🚀 Quick Start

### Basic Usage

```bash
# List available presets
python touchdesigner_clone.py --list-presets

# List available effects
python touchdesigner_clone.py --list-effects

# List supported formats (aspect ratios & resolutions)
python touchdesigner_clone.py --list-formats

# Run with default preset (cyber_glitch, 1080x1080)
python touchdesigner_clone.py

# Run with specific preset
python touchdesigner_clone.py --preset psychedelic --duration 10

# Use your own image (auto-crops to 1:1 square)
python touchdesigner_clone.py --image my_photo.jpg --preset holographic

# Export to video
python touchdesigner_clone.py --preset neon_city --output output.mp4 --duration 15

# Adjust intensity
python touchdesigner_clone.py --preset fractal_dream --intensity 0.9

# Create Instagram Story (9:16 vertical)
python touchdesigner_clone.py --aspect-ratio 9:16 --preset cyber_glitch --output story.mp4

# Create YouTube video (16:9 widescreen, 4K)
python touchdesigner_clone.py --aspect-ratio 16:9 --resolution 4k --preset holographic --output youtube.mp4
```

## 🎨 Available Presets

### 1. **cyber_glitch**
RGB split + displacement + scanlines + edge glow
Perfect for: Cyberpunk aesthetics, glitch art, digital corruption

### 2. **psychedelic**
Kaleidoscope + feedback + LUT + heat haze
Perfect for: Music videos, trippy visuals, meditation content

### 3. **holographic**
Hologram + RGB split + edge glow + volumetric
Perfect for: Sci-fi effects, futuristic UI, tech demos

### 4. **datamosh**
Pixel sorting + feedback + displacement + strobe
Perfect for: Glitch art, experimental videos, compression artifacts

### 5. **retro_vhs**
Scanlines + feedback + RGB split + posterize
Perfect for: 80s aesthetics, retro gaming, nostalgia content

### 6. **particle_flow**
Particles + optical flow + plexus + edge glow
Perfect for: Abstract motion graphics, data visualization

### 7. **fractal_dream**
Fractal + kaleidoscope + LUT + feedback
Perfect for: Psychedelic art, mathematical visualization

### 8. **neon_city**
Edge glow + LUT + heat haze + scanlines
Perfect for: Synthwave, cyberpunk, neon aesthetics

### 9. **time_warp**
Slit-scan + optical flow + feedback + displace
Perfect for: Time-based art, motion studies, experimental film

### 10. **volumetric_fog**
Volumetric + heat haze + edge glow + LUT
Perfect for: Atmospheric effects, mood pieces, cinematic looks

## 💻 Python API Usage

### Basic Example

```python
from touchdesigner_clone import TouchDesignerClone

# Create application (default: 1080x1080 square)
app = TouchDesignerClone()

# Or specify aspect ratio and resolution
app = TouchDesignerClone(aspect_ratio='16:9', resolution='4k')

# Load an image (auto-crops to match aspect ratio)
app.load_image("input.jpg")

# Or create generative image
app.create_generative_image(seed=42)

# Add effects
app.add_effect('feedback')
app.add_effect('kaleidoscope')
app.add_effect('edge_glow')

# Set intensity
app.set_global_intensity(0.8)

# Run interactive preview
app.run_interactive(duration=10, fps=30)
```

### Social Media Formats

```python
# Instagram Story (9:16 vertical)
app = TouchDesignerClone(aspect_ratio='9:16', resolution='1080')
app.load_image("photo.jpg")
app.add_effect('cyber_glitch')
app.start_recording('story.mp4', fps=30)
app.run_interactive(duration=5, fps=30)
app.stop_recording()

# YouTube Video (16:9 widescreen, 4K)
app = TouchDesignerClone(aspect_ratio='16:9', resolution='4k')
app.create_generative_image()
app.add_effect('holographic')
app.start_recording('youtube.mp4', fps=60)
app.run_interactive(duration=30, fps=60)
app.stop_recording()

# Instagram Post (1:1 square)
app = TouchDesignerClone()  # Default is 1:1 @ 1080
app.load_image("artwork.jpg")
app.add_effect('fractal')
app.export_image('post.png')
```

### Custom Effect Chain

```python
from touchdesigner_clone import TouchDesignerClone

app = TouchDesignerClone()
app.load_image("photo.jpg")

# Build custom effect chain
effects_chain = [
    'feedback',
    'rgb_split',
    'kaleidoscope',
    'heat_haze',
    'edge_glow'
]

for effect in effects_chain:
    app.add_effect(effect)

# Fine-tune individual effects
app.set_effect_intensity('feedback', 0.6)
app.set_effect_intensity('kaleidoscope', 0.9)
app.set_effect_intensity('edge_glow', 0.5)

# Record to video
app.start_recording("custom_output.mp4", fps=30)
app.run_interactive(duration=15)
app.stop_recording()
```

### Process Single Frame

```python
from touchdesigner_clone import TouchDesignerClone
from PIL import Image

app = TouchDesignerClone()
app.load_image("input.jpg")

# Add effects
app.add_effect('hologram')
app.add_effect('volumetric')
app.set_global_intensity(0.7)

# Process and export single frame
app.current_frame = app.input_image.copy()
processed = app.process_frame()
processed.save("output_frame.png")
```

## 🎛️ Effect Parameters

### Intensity Control

All effects support intensity values from 0.0 to 1.0:

- **0.0** - No effect (disabled)
- **0.3** - Subtle, tasteful enhancement
- **0.5** - Moderate effect (default)
- **0.7** - Strong, noticeable effect
- **1.0** - Maximum intensity

```python
# Global intensity (affects all effects)
app.set_global_intensity(0.6)

# Per-effect intensity
app.set_effect_intensity('feedback', 0.8)
app.set_effect_intensity('displace', 0.4)
```

## 🎥 Video Recording

### Recording Options

```python
# Start recording with custom settings
app.start_recording(
    output_path="amazing_video.mp4",
    fps=60  # Higher FPS for smoother motion
)

# Run the animation
app.run_interactive(duration=20, fps=60)

# Stop recording
app.stop_recording()
```

### Export Settings

- **Format**: MP4 (H.264)
- **Resolution**: Matches application resolution (default 1280x720)
- **FPS**: Customizable (30 or 60 recommended)
- **Codec**: mp4v (compatible with most players)

## 🖼️ Image Generation

### Procedural Starting Images

```python
# Create random generative image
app.create_generative_image()

# Create with specific seed for reproducibility
app.create_generative_image(seed=12345)

# The seed ensures you can recreate the same starting image
```

## 🎨 Effect Details

### Feedback Loops
Creates infinite trails and temporal smearing by mixing previous frames with current frame. Decay parameter controls how long trails persist.

**Use cases**: Music videos, motion graphics, ethereal effects

### Displacement/Warp
Uses Perlin-like noise to create organic warping and distortion. Great for liquid, flowing effects.

**Use cases**: Water effects, heat distortion, dream sequences

### Optical Flow
Analyzes motion between frames and amplifies it, creating dramatic motion trails and warping.

**Use cases**: Action sequences, motion emphasis, sports videos

### RGB Split
Separates color channels and applies different offsets, creating chromatic aberration and glitch effects.

**Use cases**: Glitch art, cyberpunk, VHS aesthetics

### Kaleidoscope
Creates radial symmetry by mirroring and rotating image segments around a center point.

**Use cases**: Psychedelic visuals, pattern generation, meditation videos

### Pixel Sorting
Sorts pixels by luminance creating streaking datamosh effects popular in glitch art.

**Use cases**: Glitch art, experimental videos, abstract art

### Edge Glow
Detects edges and adds neon-colored glow for comic book or tron-like effects.

**Use cases**: Neon aesthetics, wireframe looks, comic book style

### Volumetric Effects
Creates depth-based fog and atmospheric light rays for cinematic looks.

**Use cases**: Atmospheric scenes, mood pieces, cinematic effects

### Fractal Generation
Generates Mandelbrot and Julia set fractals that can be overlaid on images.

**Use cases**: Mathematical art, psychedelic visuals, abstract backgrounds

## 🔧 Advanced Usage

### Effect Combination Tips

**For Glitch Art:**
```python
effects = ['pixel_sort', 'rgb_split', 'displace', 'scanlines']
```

**For Psychedelic:**
```python
effects = ['kaleidoscope', 'feedback', 'fractal', 'lut']
```

**For Cyberpunk:**
```python
effects = ['edge_glow', 'rgb_split', 'scanlines', 'lut']
```

**For Atmospheric:**
```python
effects = ['volumetric', 'heat_haze', 'feedback', 'edge_glow']
```

### Custom LUT Types

The LUT effect supports different color remapping styles:

```python
from touchdesigner_clone import LUTEffect

# Create custom LUT effect
lut = LUTEffect(intensity=0.7, lut_type="cyberpunk")
# Options: "cyberpunk", "vaporwave", "infrared", "rainbow"
```

### Custom Fractal Types

```python
from touchdesigner_clone import FractalEffect

# Mandelbrot set
fractal = FractalEffect(intensity=0.5, fractal_type="mandelbrot")

# Julia set
fractal = FractalEffect(intensity=0.5, fractal_type="julia")
```

## 📊 Performance Tips

1. **Lower Resolution**: Start with 720p for faster preview, export at 1080p or 4K
2. **Reduce Effects**: Fewer simultaneous effects = better performance
3. **Adjust FPS**: Use 30fps for preview, 60fps for final export
4. **Effect Order**: Place computationally expensive effects (optical flow, particles) last

```python
# Fast preview setup
app = TouchDesignerClone(width=854, height=480)  # 480p
app.run_interactive(duration=5, fps=24)

# High-quality export setup
app = TouchDesignerClone(width=1920, height=1080)  # 1080p
app.start_recording("final.mp4", fps=60)
app.run_interactive(duration=30, fps=60)
```

## 🎯 Use Cases

### Music Videos
Combine feedback, kaleidoscope, and LUT effects with audio reactivity

### Social Media Content
Quick glitch effects with RGB split and scanlines for eye-catching posts

### VJ Performances
Real-time effect chains with optical flow and particles

### Digital Art
Fractal generation combined with feedback loops for abstract pieces

### Experimental Film
Slit-scan and optical flow for avant-garde visual effects

### Game Assets
Particle systems and edge glow for UI elements and effects

### NFT Art
Unique generative pieces using fractal + kaleidoscope combos

## 🐛 Troubleshooting

### ModuleNotFoundError

```bash
# Make sure all dependencies are installed
pip install -r requirements.txt
```

### OpenGL Errors

```bash
# Install OpenGL utilities
# Ubuntu/Debian:
sudo apt-get install freeglut3-dev

# macOS:
brew install freeglut
```

### Slow Performance

- Reduce resolution
- Use fewer effects simultaneously
- Lower FPS for preview
- Close other applications

### Video Won't Export

- Check disk space
- Verify write permissions in output directory
- Try different output filename/path

## 📝 License

MIT License - Feel free to use in personal and commercial projects

## 🤝 Contributing

This is a demonstration project. Feel free to extend it with:

- Additional effects (fluid simulation, ray marching, etc.)
- Audio-reactive features
- Real-time webcam input
- MIDI controller support
- Custom shader support
- Machine learning integration

## 🔮 Future Enhancements

- [ ] Real-time webcam processing
- [ ] Audio analysis for reactive effects
- [ ] MIDI/OSC control support
- [ ] Custom GLSL shader support
- [ ] 3D geometry rendering
- [ ] Particle physics simulation
- [ ] Machine learning style transfer
- [ ] Multi-layer compositing
- [ ] Keyframe animation system
- [ ] Export to various formats (GIF, WebM, etc.)

## 📚 Resources

- TouchDesigner Official: https://derivative.ca/
- OpenGL Programming Guide
- Python Image Processing tutorials
- Visual effects theory and practice

---

**Created with ❤️ for creative coders and visual artists**

Enjoy creating stunning visual effects! 🎨✨
