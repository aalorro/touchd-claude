# Visual Effects Reference Guide

## Complete Effect Catalog

This guide describes what each effect does and when to use it.

---

## 🔄 Feedback Loops
**Technical:** Blends previous frames with current frame using decay factor
**Visual Result:** Infinite trails, ghosting, temporal smearing
**Best For:** Motion graphics, ethereal effects, time-based art
**Intensity 0.3:** Subtle afterglow
**Intensity 0.7:** Long motion trails
**Intensity 1.0:** Persistent echo chamber

**Pro Tip:** Combine with movement-based effects (optical flow, displace) for dramatic motion trails

---

## 🌊 Warp/Displacement
**Technical:** Uses Perlin-like noise to create coordinate displacement maps
**Visual Result:** Organic warping, liquid distortion, wavy effects
**Best For:** Heat waves, water effects, dream sequences
**Intensity 0.3:** Gentle waves
**Intensity 0.7:** Dramatic warping
**Intensity 1.0:** Extreme distortion

**Pro Tip:** Great foundation effect - apply first, then layer other effects on top

---

## 🎯 Optical Flow
**Technical:** Calculates motion vectors between frames and amplifies movement
**Visual Result:** Motion-based warping, speed trails, dynamic distortion
**Best For:** Action sequences, sports videos, motion emphasis
**Intensity 0.3:** Subtle motion enhancement
**Intensity 0.7:** Dramatic speed effects
**Intensity 1.0:** Extreme motion blur

**Pro Tip:** Works best with video/changing content - less effective on static images

---

## 🌈 RGB Split
**Technical:** Separates color channels and applies spatial/temporal offsets
**Visual Result:** Chromatic aberration, glitch effect, channel trails
**Best For:** Glitch art, cyberpunk, VHS aesthetics
**Intensity 0.3:** Subtle chromatic aberration
**Intensity 0.7:** Strong RGB separation
**Intensity 1.0:** Extreme channel displacement

**Pro Tip:** Pair with scanlines and feedback for authentic VHS look

---

## 🔮 Kaleidoscope
**Technical:** Radial symmetry using polar coordinate transformation
**Visual Result:** Mirror patterns, mandala effects, geometric symmetry
**Best For:** Psychedelic visuals, pattern generation, meditation content
**Intensity 0.3:** 4-6 symmetry segments
**Intensity 0.7:** 8-12 segments (classic kaleidoscope)
**Intensity 1.0:** 16+ segments (intense patterns)

**Pro Tip:** Combine with feedback for evolving mandalas

---

## 📊 Pixel Sorting
**Technical:** Sorts pixels by luminance within rows/columns
**Visual Result:** Streaking, datamosh effect, organized chaos
**Best For:** Glitch art, experimental videos, abstract art
**Intensity 0.3:** Subtle sorting in select rows
**Intensity 0.7:** Heavy sorting across most of image
**Intensity 1.0:** Complete luminance-based reorganization

**Pro Tip:** Works best on high-contrast images with clear light/dark areas

---

## ✨ Edge Glow
**Technical:** Canny edge detection + gaussian blur + color overlay
**Visual Result:** Neon outlines, tron effect, comic book style
**Best For:** Neon aesthetics, wireframe looks, highlight emphasis
**Intensity 0.3:** Subtle edge highlight
**Intensity 0.7:** Strong neon glow
**Intensity 1.0:** Overwhelming wireframe

**Pro Tip:** Use with dark/black backgrounds for maximum neon impact

---

## 🎨 Posterize
**Technical:** Reduces color bit depth with optional dithering
**Visual Result:** Retro computer graphics, print look, reduced palette
**Best For:** 8-bit aesthetics, retro gaming, vintage printing
**Intensity 0.3:** Dithered reduction (16-bit look)
**Intensity 0.7:** Clear posterization (8-bit)
**Intensity 1.0:** Extreme reduction (2-4 colors)

**Pro Tip:** Lower intensity (0.2-0.4) gives nice dithered film look

---

## 🎭 LUT (Lookup Table)
**Technical:** Maps input colors to output palette using lookup table
**Visual Result:** Color grading, palette swaps, mood changes
**Best For:** Color grading, mood setting, stylization
**Types Available:**
- **cyberpunk**: Blue/purple/pink neon gradients
- **vaporwave**: Pink/cyan/purple pastels
- **infrared**: False-color heat map style
- **rainbow**: Full spectrum color mapping

**Pro Tip:** Combine with edge glow for neon city aesthetics

---

## 🌡️ Heat Haze
**Technical:** Wave-based displacement with multi-frequency distortion
**Visual Result:** Heat shimmer, water refraction, atmospheric distortion
**Best For:** Desert scenes, atmospheric effects, dreamy looks
**Intensity 0.3:** Gentle shimmer
**Intensity 0.7:** Noticeable heat waves
**Intensity 1.0:** Extreme refraction

**Pro Tip:** Add blur for enhanced refraction effect

---

## 💫 Particles
**Technical:** Flow-field particle system with image-based advection
**Visual Result:** Flowing particles, swarm behavior, organic movement
**Best For:** Abstract motion graphics, data visualization
**Intensity 0.3:** Slow, calm particle drift
**Intensity 0.7:** Active particle flow
**Intensity 1.0:** Chaotic particle storm

**Pro Tip:** Combine with optical flow for reactive particle systems

---

## 🕸️ Plexus
**Technical:** Connected network of moving points with distance-based links
**Visual Result:** Sci-fi networks, constellation maps, data connections
**Best For:** Tech presentations, data visualization, sci-fi aesthetics
**Intensity 0.3:** Sparse network
**Intensity 0.7:** Dense connections
**Intensity 1.0:** Maximum connectivity

**Pro Tip:** Works great with dark backgrounds and edge glow

---

## ⚡ Strobe
**Technical:** Temporal frame freezing at regular intervals
**Visual Result:** Freeze frames, stepped motion, rhythmic holds
**Best For:** Music videos, EDM visuals, dramatic emphasis
**Intensity 0.3:** Slow strobe (occasional freezes)
**Intensity 0.7:** Medium tempo strobe
**Intensity 1.0:** Fast strobe (seizure warning!)

**Pro Tip:** Sync with music BPM for audio-reactive effect

---

## 📺 Scanlines
**Technical:** CRT-style horizontal lines + vertical roll + wobble
**Visual Result:** Old TV, VHS tape, retro monitor look
**Best For:** 80s aesthetics, retro gaming, nostalgia
**Intensity 0.3:** Subtle CRT effect
**Intensity 0.7:** Clear scanlines with roll
**Intensity 1.0:** Heavy distortion + tracking errors

**Pro Tip:** Perfect companion for RGB split and posterize (VHS combo)

---

## ⏱️ Slit-Scan
**Technical:** Different image rows sampled from different time points
**Visual Result:** Time slicing, temporal displacement, stretched motion
**Best For:** Experimental film, time-based art, motion studies
**Intensity 0.3:** Subtle time offset
**Intensity 0.7:** Clear slit-scan effect
**Intensity 1.0:** Extreme temporal displacement

**Pro Tip:** Works best with moving subjects or camera motion

---

## 🌫️ Volumetric
**Technical:** Depth-based fog generation with light rays
**Visual Result:** Atmospheric haze, god rays, cinematic fog
**Best For:** Atmospheric scenes, mood pieces, cinematic looks
**Intensity 0.3:** Subtle atmospheric haze
**Intensity 0.7:** Strong fog with light beams
**Intensity 1.0:** Dense volumetric fog

**Pro Tip:** Use with edge glow for dramatic light ray effects

---

## 🌀 Fractal
**Technical:** Real-time Mandelbrot or Julia set generation
**Visual Result:** Mathematical patterns, infinite zoom, psychedelic forms
**Best For:** Mathematical art, psychedelic visuals, abstract backgrounds
**Types:**
- **mandelbrot**: Classic fractal zoom
- **julia**: Swirling organic patterns

**Intensity 0.3:** Subtle fractal overlay
**Intensity 0.7:** Clear fractal structure
**Intensity 1.0:** Dominant fractal patterns

**Pro Tip:** Animates over time - longer duration shows more evolution

---

## 👁️ Hologram
**Technical:** Interference pattern generation with chromatic shifts
**Visual Result:** Holographic shimmer, sci-fi displays, futuristic UI
**Best For:** Sci-fi effects, futuristic interfaces, tech demos
**Intensity 0.3:** Subtle interference
**Intensity 0.7:** Clear holographic effect
**Intensity 1.0:** Intense hologram distortion

**Pro Tip:** Combine with RGB split and volumetric for ultimate sci-fi look

---

## 🎬 Preset Combinations

### Maximum Glitch (Datamosh)
```
pixel_sort + feedback + displace + strobe
Intensity: 0.8
Duration: 5-10s for clips
```

### Psychedelic Journey
```
kaleidoscope + feedback + fractal + lut
Intensity: 0.9
Duration: 30-60s for full experience
```

### Cyberpunk City
```
edge_glow + rgb_split + scanlines + lut(cyberpunk)
Intensity: 0.7
Perfect for: Music videos, title sequences
```

### Holographic Display
```
hologram + rgb_split + edge_glow + volumetric
Intensity: 0.8
Perfect for: Sci-fi content, tech presentations
```

### Retro VHS
```
scanlines + feedback + rgb_split + posterize
Intensity: 0.6
Perfect for: 80s aesthetics, nostalgic content
```

### Ethereal Dream
```
volumetric + heat_haze + feedback + edge_glow
Intensity: 0.7
Perfect for: Atmospheric videos, mood pieces
```

### Motion Graphics Pro
```
particles + optical_flow + plexus + edge_glow
Intensity: 0.8
Perfect for: Abstract motion design
```

### Fractal Meditation
```
fractal + kaleidoscope + lut + feedback
Intensity: 1.0
Perfect for: Meditation videos, screensavers
```

---

## 📐 Effect Layering Strategy

### Layer 1: Foundation
Apply first for base transformation
- displace
- kaleidoscope
- fractal

### Layer 2: Motion
Add movement and flow
- optical_flow
- particles
- feedback

### Layer 3: Color
Establish color palette
- lut
- posterize

### Layer 4: Details
Add finishing touches
- edge_glow
- rgb_split
- scanlines
- hologram

### Layer 5: Atmosphere
Final ambience
- volumetric
- heat_haze

---

## 🎯 Effect Performance Guide

**Light (Fast Processing):**
- posterize
- lut
- edge_glow
- rgb_split

**Medium (Moderate Processing):**
- feedback
- kaleidoscope
- displace
- scanlines

**Heavy (Slower Processing):**
- optical_flow
- particles
- plexus
- fractal
- volumetric

**Recommendation:** Mix 2-3 light effects OR 1 heavy + 1-2 light effects for best performance

---

## 🌟 Pro Tips by Use Case

### For Social Media (Instagram/TikTok)
- Use high intensity (0.7-0.9) for eye-catching content
- Keep duration short (5-15 seconds)
- Stick to 2-3 effects maximum
- Recommended: cyber_glitch, psychedelic, neon_city presets

### For Music Videos
- Sync strobe effect to BPM
- Use feedback for motion trails during drops
- Layer kaleidoscope + lut for trippy sections
- Recommended: psychedelic, particle_flow presets

### For VJ/Live Performance
- Pre-render effect chains at different intensities
- Use lower resolution (720p) for real-time performance
- Recommended: All presets work great live

### For Digital Art/NFTs
- Use high resolution (2048x2048 or higher)
- Single frame processing
- Higher intensity (0.8-1.0) for unique results
- Recommended: fractal_dream, holographic presets

### For Film/Cinematics
- Subtle intensity (0.3-0.5) for professional look
- Focus on volumetric + heat_haze for atmosphere
- Recommended: volumetric_fog, time_warp presets

---

## ⚠️ Important Notes

**Seizure Warning:**
- Strobe effect at high intensity can trigger seizures
- Use responsibly in public content
- Add warnings to videos with intense strobing

**Performance:**
- More effects = slower processing
- Higher resolution = slower processing
- 60fps = 2x processing vs 30fps

**Export Quality:**
- 30fps for web/social media
- 60fps for smooth motion/professional use
- 1080p minimum for quality output
- 4K for maximum quality (requires powerful hardware)

---

Remember: The best effects come from experimentation! Don't be afraid to combine effects in unexpected ways. 🎨✨
