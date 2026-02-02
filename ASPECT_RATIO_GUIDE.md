# Aspect Ratio & Resolution Guide

## 📐 Supported Aspect Ratios

### 1:1 - Square (Default)
**Best For:** Instagram posts, profile pictures, album art
**Resolutions:**
- 720p: 720x720
- 1080p: 1080x1080 ✨ Default
- 2K: 1440x1440
- 4K: 2160x2160

**Use Cases:**
- Instagram feed posts
- Twitter profile images
- Album covers
- Square canvas art

**Example:**
```bash
python touchdesigner_clone.py --aspect-ratio 1:1 --resolution 1080
python touchdesigner_clone.py --preset psychedelic
# 1:1 and 1080 are defaults, so both commands produce 1080x1080
```

---

### 9:16 - Vertical Portrait
**Best For:** Instagram Stories, TikTok, Reels, Snapchat
**Resolutions:**
- 720p: 405x720
- 1080p: 607x1080 ✨ Instagram/TikTok standard
- 2K: 810x1440
- 4K: 1215x2160

**Use Cases:**
- Instagram Stories
- TikTok videos
- Instagram Reels
- Snapchat content
- Mobile-first video

**Example:**
```bash
# Perfect for TikTok/Instagram Stories
python touchdesigner_clone.py \
  --aspect-ratio 9:16 \
  --resolution 1080 \
  --preset neon_city \
  --output story.mp4
```

---

### 16:9 - Widescreen Landscape
**Best For:** YouTube, TV, desktop displays, presentations
**Resolutions:**
- 720p: 1280x720 (HD)
- 1080p: 1920x1080 (Full HD)
- 2K: 2560x1440 (QHD)
- 4K: 3840x2160 (Ultra HD) ✨ YouTube standard

**Use Cases:**
- YouTube videos
- Vimeo content
- Desktop backgrounds
- Presentations
- TV/streaming content

**Example:**
```bash
# YouTube 4K upload
python touchdesigner_clone.py \
  --aspect-ratio 16:9 \
  --resolution 4k \
  --preset holographic \
  --duration 30 \
  --output youtube_4k.mp4
```

---

### 4:3 - Classic TV
**Best For:** Retro content, classic displays, art prints
**Resolutions:**
- 720p: 960x720
- 1080p: 1440x1080
- 2K: 1920x1440
- 4K: 2880x2160

**Use Cases:**
- Retro/vintage aesthetics
- Classic TV simulation
- Art prints
- Old-school gaming content

**Example:**
```bash
# Retro VHS look
python touchdesigner_clone.py \
  --aspect-ratio 4:3 \
  --resolution 720 \
  --preset retro_vhs
```

---

### 3:4 - Portrait Photo
**Best For:** Portrait photography, vertical posters
**Resolutions:**
- 720p: 540x720
- 1080p: 810x1080
- 2K: 1080x1440
- 4K: 1620x2160

**Use Cases:**
- Portrait photography
- Vertical posters
- Print media
- Vertical displays

**Example:**
```bash
python touchdesigner_clone.py \
  --image portrait.jpg \
  --aspect-ratio 3:4 \
  --resolution 1080 \
  --preset edge_glow
```

---

## 🎯 Resolution Guide

### 720p - HD
- **Speed:** Fastest ⚡⚡⚡
- **Quality:** Good for web/social
- **File Size:** Smallest
- **Best For:** Previews, fast iterations, web content
- **Export Time:** ~1x real-time

### 1080p - Full HD (Default)
- **Speed:** Fast ⚡⚡
- **Quality:** Excellent for most uses ✨
- **File Size:** Moderate
- **Best For:** Instagram, YouTube, general purpose
- **Export Time:** ~2x real-time

### 2K - Quad HD
- **Speed:** Moderate ⚡
- **Quality:** High-end web, small screens
- **File Size:** Large
- **Best For:** High-quality web, desktop backgrounds
- **Export Time:** ~4x real-time

### 4K - Ultra HD
- **Speed:** Slow 🐌
- **Quality:** Maximum quality
- **File Size:** Very large
- **Best For:** YouTube 4K, professional video, archival
- **Export Time:** ~8x real-time

---

## 🖼️ Center Crop Behavior

When you load an image with a different aspect ratio than your output settings, the image is **center-cropped** (NOT stretched) to match your target aspect ratio.

### Example: Loading 16:9 image for 1:1 output

**Input:** 1920x1080 (16:9) landscape photo
**Output Setting:** 1:1 @ 1080
**Result:** 
1. Center crop to 1080x1080 (crops left and right edges equally)
2. Image maintains quality - no stretching

### Example: Loading 1:1 image for 9:16 output

**Input:** 1080x1080 (1:1) square image
**Output Setting:** 9:16 @ 1080
**Result:**
1. Center crop to 607x1080 (crops top and bottom edges equally)
2. Maintains aspect ratio perfectly

### What Gets Cropped?

```
Original: 16:9 landscape
┌──────────────────────────┐
│    [  KEPT AREA   ]      │  ← Center portion kept
└──────────────────────────┘
 ^^^^                  ^^^^
 Cropped              Cropped

Output: 1:1 square
     ┌──────────┐
     │  KEPT    │
     │  AREA    │
     └──────────┘
```

---

## 📱 Social Media Cheat Sheet

### Instagram
```bash
# Feed Post (1:1)
--aspect-ratio 1:1 --resolution 1080

# Story/Reel (9:16)
--aspect-ratio 9:16 --resolution 1080

# IGTV (9:16 or 16:9)
--aspect-ratio 9:16 --resolution 1080
```

### TikTok
```bash
# Standard TikTok (9:16)
--aspect-ratio 9:16 --resolution 1080
```

### YouTube
```bash
# Standard YouTube (16:9)
--aspect-ratio 16:9 --resolution 1080

# 4K Upload (16:9)
--aspect-ratio 16:9 --resolution 4k
```

### Twitter/X
```bash
# Landscape Tweet (16:9)
--aspect-ratio 16:9 --resolution 720

# Portrait Tweet (9:16)
--aspect-ratio 9:16 --resolution 720
```

### LinkedIn
```bash
# Standard Post (1:1 or 16:9)
--aspect-ratio 1:1 --resolution 1080
```

### Pinterest
```bash
# Pin (3:4 or 2:3, use 3:4)
--aspect-ratio 3:4 --resolution 1080
```

---

## 💡 Best Practices

### For Maximum Quality
```bash
# Use 4K for archival/future-proofing
--aspect-ratio 16:9 --resolution 4k
```

### For Fast Iteration
```bash
# Use 720p for quick previews
--aspect-ratio 1:1 --resolution 720
```

### For Social Media
```bash
# Use 1080p - perfect balance
--aspect-ratio 9:16 --resolution 1080  # Stories
--aspect-ratio 1:1 --resolution 1080   # Posts
--aspect-ratio 16:9 --resolution 1080  # YouTube
```

### For NFTs/Digital Art
```bash
# Square 4K for maximum impact
--aspect-ratio 1:1 --resolution 4k
```

---

## 🎨 Python API Examples

### Create App with Specific Format

```python
from touchdesigner_clone import TouchDesignerClone

# Instagram Story
app = TouchDesignerClone(aspect_ratio='9:16', resolution='1080')
# Creates 607x1080 vertical video

# YouTube 4K
app = TouchDesignerClone(aspect_ratio='16:9', resolution='4k')
# Creates 3840x2160 widescreen video

# Square 1080p (default)
app = TouchDesignerClone()
# Creates 1080x1080 square video
```

### Custom Dimensions (Advanced)

```python
# Completely custom size
app = TouchDesignerClone(custom_width=1200, custom_height=1500)
# Creates 1200x1500 video (ignores aspect_ratio/resolution)
```

### Load Image with Auto-Crop

```python
app = TouchDesignerClone(aspect_ratio='1:1', resolution='1080')

# Load landscape photo - automatically center crops to square
app.load_image('landscape_photo.jpg')
# Original 4032x3024 → Cropped to 3024x3024 → Resized to 1080x1080

# Load portrait photo - automatically center crops to square
app.load_image('portrait_photo.jpg')
# Original 2268x4032 → Cropped to 2268x2268 → Resized to 1080x1080
```

---

## 🎬 Complete Workflow Examples

### Instagram Story Creation

```bash
# 1. Create with your photo
python touchdesigner_clone.py \
  --image my_photo.jpg \
  --aspect-ratio 9:16 \
  --resolution 1080 \
  --preset cyber_glitch \
  --intensity 0.8 \
  --duration 5 \
  --output story.mp4

# Output: 607x1080 vertical video, 5 seconds
```

### YouTube Intro (4K)

```bash
python touchdesigner_clone.py \
  --aspect-ratio 16:9 \
  --resolution 4k \
  --preset holographic \
  --intensity 0.9 \
  --duration 10 \
  --output intro_4k.mp4

# Output: 3840x2160 widescreen, 10 seconds
```

### Square NFT Art

```bash
python touchdesigner_clone.py \
  --aspect-ratio 1:1 \
  --resolution 4k \
  --preset fractal_dream \
  --intensity 1.0 \
  --duration 15 \
  --output nft_art.mp4

# Output: 2160x2160 square, 15 seconds
```

### TikTok Content

```bash
python touchdesigner_clone.py \
  --image dance_clip.jpg \
  --aspect-ratio 9:16 \
  --resolution 1080 \
  --preset particle_flow \
  --intensity 0.7 \
  --duration 15 \
  --output tiktok.mp4

# Output: 607x1080 vertical, 15 seconds
```

---

## ⚡ Performance Tips by Resolution

### 720p (Fast)
- Preview: Real-time on most hardware
- Export: ~5 minutes for 60s video
- Good for: Testing effects, quick iterations

### 1080p (Recommended)
- Preview: Near real-time on modern hardware
- Export: ~10 minutes for 60s video
- Good for: Final output for social media

### 2K (Slow)
- Preview: 50-70% real-time
- Export: ~20 minutes for 60s video
- Good for: High-quality web content

### 4K (Very Slow)
- Preview: 25-40% real-time
- Export: ~40 minutes for 60s video
- Good for: YouTube 4K, archival, professional

**Tip:** Use 720p for testing, export final at 1080p or 4K!

---

## 🔍 Quick Reference Table

| Aspect | Resolution | Dimensions | Common Use |
|--------|-----------|------------|------------|
| 1:1 | 720 | 720×720 | Quick preview |
| 1:1 | 1080 | 1080×1080 | Instagram post ⭐ |
| 1:1 | 4k | 2160×2160 | NFT art |
| 9:16 | 1080 | 607×1080 | Instagram Story ⭐ |
| 9:16 | 1080 | 607×1080 | TikTok ⭐ |
| 16:9 | 1080 | 1920×1080 | YouTube ⭐ |
| 16:9 | 4k | 3840×2160 | YouTube 4K |
| 4:3 | 720 | 960×720 | Retro content |
| 3:4 | 1080 | 810×1080 | Portrait art |

---

## 📊 File Size Estimates (30s video, 30fps)

| Resolution | File Size | Upload Time (10 Mbps) |
|-----------|-----------|---------------------|
| 720p | ~15 MB | 12 seconds |
| 1080p | ~35 MB | 28 seconds |
| 2K | ~60 MB | 48 seconds |
| 4K | ~140 MB | 112 seconds |

---

Remember: Always test with 720p first, then export your final version at the target resolution! 🚀
