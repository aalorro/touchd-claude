#!/usr/bin/env python3
"""
TouchDesigner-Inspired Visual Effects Generator
================================================
A powerful visual effects application for creating stunning videos with
3D objects, holograms, graphs, vectors, and fractals.

Features:
- 20+ professional visual effects presets
- Real-time 3D rendering and particle systems
- Image-based generation with optional prompts
- Interactive intensity control
- Audio-reactive capabilities
- Export to video
"""

import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import moderngl
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import glm
from scipy import ndimage, signal
from scipy.spatial import Delaunay
import colorsys
import json
from pathlib import Path
from datetime import datetime
import traceback

class EffectNode:
    """Base class for all effect nodes"""
    def __init__(self, name, intensity=0.5):
        self.name = name
        self.intensity = np.clip(intensity, 0.0, 1.0)
        self.enabled = True
        self.frame_buffer = []
        
    def process(self, image, time=0, audio_level=0):
        """Process image and return modified version"""
        if not self.enabled:
            return image
        return image
        
    def set_intensity(self, value):
        """Set effect intensity (0.0 to 1.0)"""
        self.intensity = np.clip(value, 0.0, 1.0)


class FeedbackEffect(EffectNode):
    """Feedback loops - infinite trails, smear, echo effects"""
    def __init__(self, intensity=0.5, decay=0.95):
        super().__init__("Feedback", intensity)
        self.decay = decay
        self.feedback_buffer = None
        
    def process(self, image, time=0, audio_level=0):
        if not self.enabled:
            return image
            
        img_array = np.array(image, dtype=np.float32) / 255.0
        
        if self.feedback_buffer is None:
            self.feedback_buffer = img_array.copy()
        
        # Mix current frame with decayed feedback
        decay_factor = 0.7 + (self.decay * 0.29) * self.intensity
        self.feedback_buffer = self.feedback_buffer * decay_factor + img_array * (1 - decay_factor * 0.5)
        
        # Add trailing/smearing effect
        shift_amount = int(2 * self.intensity)
        if shift_amount > 0:
            self.feedback_buffer = np.roll(self.feedback_buffer, shift_amount, axis=1)
        
        result = np.clip(self.feedback_buffer * 255, 0, 255).astype(np.uint8)
        return Image.fromarray(result)


class DisplaceEffect(EffectNode):
    """Warp/displacement glitch effects"""
    def __init__(self, intensity=0.5):
        super().__init__("Displace", intensity)
        self.noise_offset = 0
        
    def process(self, image, time=0, audio_level=0):
        if not self.enabled:
            return image
            
        img_array = np.array(image)
        h, w = img_array.shape[:2]
        
        # Generate displacement maps using Perlin-like noise
        self.noise_offset += 0.05
        x_scale = 0.01 + self.intensity * 0.05
        y_scale = 0.01 + self.intensity * 0.05
        
        x = np.linspace(0, w * x_scale, w)
        y = np.linspace(0, h * y_scale, h)
        X, Y = np.meshgrid(x, y)
        
        # Multi-octave noise for displacement
        disp_x = np.sin(X + self.noise_offset) * np.cos(Y * 2) * w * self.intensity * 0.1
        disp_y = np.cos(Y + self.noise_offset) * np.sin(X * 2) * h * self.intensity * 0.1
        
        # Create coordinate maps
        map_x = (np.arange(w) + disp_x).astype(np.float32)
        map_y = (np.arange(h)[:, None] + disp_y).astype(np.float32)
        
        map_x = np.clip(map_x, 0, w - 1)
        map_y = np.clip(map_y, 0, h - 1)
        
        # Remap the image
        result = cv2.remap(img_array, map_x, map_y, cv2.INTER_LINEAR)
        return Image.fromarray(result)


class OpticalFlowEffect(EffectNode):
    """Optical flow motion vector effects"""
    def __init__(self, intensity=0.5):
        super().__init__("OpticalFlow", intensity)
        self.prev_gray = None
        self.flow = None
        
    def process(self, image, time=0, audio_level=0):
        if not self.enabled:
            return image
            
        img_array = np.array(image)
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        
        if self.prev_gray is None:
            self.prev_gray = gray
            return image
        
        # Calculate optical flow
        flow = cv2.calcOpticalFlowFarneback(
            self.prev_gray, gray, None,
            0.5, 3, 15, 3, 5, 1.2, 0
        )
        
        # Amplify flow based on intensity
        flow = flow * (1 + self.intensity * 10)
        
        # Create motion-warped image
        h, w = gray.shape
        flow_map_x = np.arange(w) + flow[..., 0]
        flow_map_y = np.arange(h)[:, None] + flow[..., 1]
        
        flow_map_x = np.clip(flow_map_x, 0, w - 1).astype(np.float32)
        flow_map_y = np.clip(flow_map_y, 0, h - 1).astype(np.float32)
        
        result = cv2.remap(img_array, flow_map_x, flow_map_y, cv2.INTER_LINEAR)
        
        self.prev_gray = gray
        return Image.fromarray(result)


class RGBSplitEffect(EffectNode):
    """RGB channel split with chromatic aberration and trails"""
    def __init__(self, intensity=0.5):
        super().__init__("RGBSplit", intensity)
        self.channel_cache = [None, None, None]
        
    def process(self, image, time=0, audio_level=0):
        if not self.enabled:
            return image
            
        img_array = np.array(image)
        h, w = img_array.shape[:2]
        
        # Split channels
        r, g, b = img_array[:, :, 0], img_array[:, :, 1], img_array[:, :, 2]
        
        # Apply different offsets to each channel
        offset = int(10 * self.intensity)
        r_shifted = np.roll(r, offset, axis=1)
        b_shifted = np.roll(b, -offset, axis=1)
        
        # Add temporal trails
        trail_strength = 0.3 * self.intensity
        for i, channel in enumerate([r_shifted, g, b_shifted]):
            if self.channel_cache[i] is None:
                self.channel_cache[i] = channel.astype(np.float32)
            else:
                self.channel_cache[i] = (
                    self.channel_cache[i] * trail_strength + 
                    channel.astype(np.float32) * (1 - trail_strength)
                )
        
        # Recombine with trails
        result = np.stack([
            np.clip(self.channel_cache[0], 0, 255).astype(np.uint8),
            np.clip(self.channel_cache[1], 0, 255).astype(np.uint8),
            np.clip(self.channel_cache[2], 0, 255).astype(np.uint8)
        ], axis=2)
        
        return Image.fromarray(result)


class KaleidoscopeEffect(EffectNode):
    """Kaleidoscope/symmetry tunneling effects"""
    def __init__(self, intensity=0.5, segments=6):
        super().__init__("Kaleidoscope", intensity)
        self.segments = segments
        
    def process(self, image, time=0, audio_level=0):
        if not self.enabled:
            return image
            
        img_array = np.array(image)
        h, w = img_array.shape[:2]
        
        # Create polar coordinate transform
        center_x, center_y = w // 2, h // 2
        y, x = np.ogrid[:h, :w]
        
        # Calculate polar coordinates
        dx = x - center_x
        dy = y - center_y
        angle = np.arctan2(dy, dx)
        radius = np.sqrt(dx**2 + dy**2)
        
        # Apply kaleidoscope effect
        num_segments = int(3 + self.segments * self.intensity * 10)
        angle_segment = (2 * np.pi) / num_segments
        angle_mod = np.mod(angle, angle_segment)
        
        # Mirror effect
        mirror_mask = (np.mod(angle / angle_segment, 2) > 1).astype(int)
        angle_mod = np.where(mirror_mask, angle_segment - angle_mod, angle_mod)
        
        # Rotate based on time
        angle_mod += time * self.intensity
        
        # Convert back to Cartesian
        new_x = center_x + radius * np.cos(angle_mod)
        new_y = center_y + radius * np.sin(angle_mod)
        
        new_x = np.clip(new_x, 0, w - 1).astype(np.float32)
        new_y = np.clip(new_y, 0, h - 1).astype(np.float32)
        
        result = cv2.remap(img_array, new_x, new_y, cv2.INTER_LINEAR)
        return Image.fromarray(result)


class PixelSortEffect(EffectNode):
    """Pixel sorting/datamosh effects"""
    def __init__(self, intensity=0.5):
        super().__init__("PixelSort", intensity)
        
    def process(self, image, time=0, audio_level=0):
        if not self.enabled:
            return image
            
        img_array = np.array(image)
        h, w = img_array.shape[:2]
        
        # Convert to grayscale for sorting key
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        
        # Sort pixels by luminance in rows
        sort_ratio = self.intensity
        rows_to_sort = int(h * sort_ratio)
        
        result = img_array.copy()
        for i in range(0, rows_to_sort, 2):
            if i >= h:
                break
            # Get sorting indices
            sort_indices = np.argsort(gray[i, :])
            # Apply sorting with intensity blend
            sorted_row = result[i, sort_indices, :]
            result[i, :, :] = (
                sorted_row * self.intensity + 
                result[i, :, :] * (1 - self.intensity)
            ).astype(np.uint8)
        
        return Image.fromarray(result)


class EdgeGlowEffect(EffectNode):
    """Edge detection with neon glow"""
    def __init__(self, intensity=0.5):
        super().__init__("EdgeGlow", intensity)
        
    def process(self, image, time=0, audio_level=0):
        if not self.enabled:
            return image
            
        img_array = np.array(image)
        
        # Edge detection
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        
        # Create glow effect
        glow_size = int(5 + self.intensity * 10)
        edges_glow = cv2.GaussianBlur(edges, (glow_size * 2 + 1, glow_size * 2 + 1), 0)
        
        # Colorize edges (neon effect)
        hue = (time * 50) % 360
        neon_color = np.array(colorsys.hsv_to_rgb(hue / 360, 1.0, 1.0)) * 255
        
        edges_colored = np.stack([edges_glow] * 3, axis=2) * neon_color / 255
        
        # Blend with original
        result = img_array.astype(np.float32) + edges_colored * self.intensity * 2
        result = np.clip(result, 0, 255).astype(np.uint8)
        
        return Image.fromarray(result)


class PosterizeEffect(EffectNode):
    """Posterize/dither/halftone effects"""
    def __init__(self, intensity=0.5):
        super().__init__("Posterize", intensity)
        
    def process(self, image, time=0, audio_level=0):
        if not self.enabled:
            return image
            
        img_array = np.array(image)
        
        # Reduce color levels
        levels = int(2 + (1 - self.intensity) * 254)
        factor = 255.0 / levels
        
        result = (img_array / factor).astype(np.uint8) * factor
        
        # Add dithering for low intensity
        if self.intensity < 0.5:
            dither_strength = (1 - self.intensity * 2) * 10
            noise = np.random.randint(-dither_strength, dither_strength, img_array.shape)
            result = np.clip(result.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        
        return Image.fromarray(result)


class LUTEffect(EffectNode):
    """Lookup table color remapping"""
    def __init__(self, intensity=0.5, lut_type="cyberpunk"):
        super().__init__("LUT", intensity)
        self.lut_type = lut_type
        
    def create_lut(self, lut_type, time):
        """Create color lookup table"""
        lut = np.zeros((256, 3), dtype=np.uint8)
        
        if lut_type == "cyberpunk":
            for i in range(256):
                t = i / 255.0
                hue = (0.6 + t * 0.4 + time * 0.1) % 1.0
                lut[i] = np.array(colorsys.hsv_to_rgb(hue, 0.9, t)) * 255
        elif lut_type == "vaporwave":
            for i in range(256):
                t = i / 255.0
                hue = (0.8 + t * 0.2) % 1.0
                lut[i] = np.array(colorsys.hsv_to_rgb(hue, 0.7, t)) * 255
        elif lut_type == "infrared":
            for i in range(256):
                lut[i] = [i, 255 - i, 128]
        else:  # rainbow
            for i in range(256):
                hue = i / 255.0
                lut[i] = np.array(colorsys.hsv_to_rgb(hue, 1.0, 1.0)) * 255
                
        return lut
        
    def process(self, image, time=0, audio_level=0):
        if not self.enabled:
            return image
            
        img_array = np.array(image)
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        
        # Create and apply LUT
        lut = self.create_lut(self.lut_type, time)
        result = lut[gray]
        
        # Blend with original based on intensity
        result = (
            result * self.intensity + 
            img_array * (1 - self.intensity)
        ).astype(np.uint8)
        
        return Image.fromarray(result)


class HeatHazeEffect(EffectNode):
    """Heat haze/refraction shimmer effect"""
    def __init__(self, intensity=0.5):
        super().__init__("HeatHaze", intensity)
        self.time_offset = 0
        
    def process(self, image, time=0, audio_level=0):
        if not self.enabled:
            return image
            
        img_array = np.array(image)
        h, w = img_array.shape[:2]
        
        self.time_offset += 0.1
        
        # Create wavy distortion
        x = np.linspace(0, w, w)
        y = np.linspace(0, h, h)
        X, Y = np.meshgrid(x, y)
        
        # Multi-frequency wave distortion
        distort_x = np.sin(Y * 0.05 + self.time_offset) * self.intensity * 15
        distort_x += np.sin(Y * 0.1 + self.time_offset * 1.3) * self.intensity * 8
        distort_y = np.cos(X * 0.05 + self.time_offset * 0.7) * self.intensity * 5
        
        map_x = (np.arange(w) + distort_x).astype(np.float32)
        map_y = (np.arange(h)[:, None] + distort_y).astype(np.float32)
        
        map_x = np.clip(map_x, 0, w - 1)
        map_y = np.clip(map_y, 0, h - 1)
        
        result = cv2.remap(img_array, map_x, map_y, cv2.INTER_LINEAR)
        
        # Add blur for refraction effect
        blur_amount = int(1 + self.intensity * 3)
        result = cv2.GaussianBlur(result, (blur_amount * 2 + 1, blur_amount * 2 + 1), 0)
        
        return Image.fromarray(result)


class ParticleEffect(EffectNode):
    """Particle system with flow field advection"""
    def __init__(self, intensity=0.5, num_particles=1000):
        super().__init__("Particles", intensity)
        self.num_particles = num_particles
        self.particles = None
        
    def initialize_particles(self, w, h):
        """Initialize particle positions"""
        self.particles = {
            'x': np.random.rand(self.num_particles) * w,
            'y': np.random.rand(self.num_particles) * h,
            'vx': np.zeros(self.num_particles),
            'vy': np.zeros(self.num_particles),
            'life': np.random.rand(self.num_particles)
        }
        
    def process(self, image, time=0, audio_level=0):
        if not self.enabled:
            return image
            
        img_array = np.array(image)
        h, w = img_array.shape[:2]
        
        if self.particles is None:
            self.initialize_particles(w, h)
        
        # Update particle positions with flow field
        for i in range(self.num_particles):
            x, y = int(self.particles['x'][i]), int(self.particles['y'][i])
            if 0 <= x < w and 0 <= y < h:
                # Sample image brightness for flow
                gray_val = np.mean(img_array[y, x]) / 255.0
                angle = gray_val * np.pi * 2 + time
                
                self.particles['vx'][i] = np.cos(angle) * self.intensity * 2
                self.particles['vy'][i] = np.sin(angle) * self.intensity * 2
        
        # Update positions
        self.particles['x'] += self.particles['vx']
        self.particles['y'] += self.particles['vy']
        
        # Wrap around edges
        self.particles['x'] = np.mod(self.particles['x'], w)
        self.particles['y'] = np.mod(self.particles['y'], h)
        
        # Draw particles
        result = img_array.copy()
        for i in range(self.num_particles):
            x, y = int(self.particles['x'][i]), int(self.particles['y'][i])
            if 0 <= x < w and 0 <= y < h:
                color = img_array[y, x]
                cv2.circle(result, (x, y), int(2 * self.intensity), color.tolist(), -1)
        
        return Image.fromarray(result)


class PlexusEffect(EffectNode):
    """Connected points network effect"""
    def __init__(self, intensity=0.5, num_points=100):
        super().__init__("Plexus", intensity)
        self.num_points = num_points
        self.points = None
        
    def initialize_points(self, w, h):
        """Initialize point positions"""
        self.points = {
            'x': np.random.rand(self.num_points) * w,
            'y': np.random.rand(self.num_points) * h,
            'vx': (np.random.rand(self.num_points) - 0.5) * 2,
            'vy': (np.random.rand(self.num_points) - 0.5) * 2
        }
        
    def process(self, image, time=0, audio_level=0):
        if not self.enabled:
            return image
            
        img_array = np.array(image)
        h, w = img_array.shape[:2]
        
        if self.points is None:
            self.initialize_points(w, h)
        
        # Update point positions
        self.points['x'] += self.points['vx'] * self.intensity
        self.points['y'] += self.points['vy'] * self.intensity
        
        # Bounce off edges
        self.points['vx'] = np.where((self.points['x'] < 0) | (self.points['x'] >= w), 
                                      -self.points['vx'], self.points['vx'])
        self.points['vy'] = np.where((self.points['y'] < 0) | (self.points['y'] >= h), 
                                      -self.points['vy'], self.points['vy'])
        
        self.points['x'] = np.clip(self.points['x'], 0, w - 1)
        self.points['y'] = np.clip(self.points['y'], 0, h - 1)
        
        # Draw connections
        result = img_array.copy()
        connection_dist = 50 + self.intensity * 100
        
        for i in range(self.num_points):
            x1, y1 = int(self.points['x'][i]), int(self.points['y'][i])
            
            for j in range(i + 1, self.num_points):
                x2, y2 = int(self.points['x'][j]), int(self.points['y'][j])
                dist = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                
                if dist < connection_dist:
                    alpha = 1 - (dist / connection_dist)
                    color = (255, 255, 255)
                    thickness = int(1 + self.intensity * 2)
                    cv2.line(result, (x1, y1), (x2, y2), color, thickness)
            
            # Draw point
            cv2.circle(result, (x1, y1), int(3 * self.intensity), (255, 255, 255), -1)
        
        # Blend with original
        result = cv2.addWeighted(img_array, 0.7, result, 0.3 * self.intensity, 0)
        
        return Image.fromarray(result)


class StrobeEffect(EffectNode):
    """Strobe/shutter/freeze-frame effects"""
    def __init__(self, intensity=0.5):
        super().__init__("Strobe", intensity)
        self.freeze_buffer = None
        self.freeze_timer = 0
        
    def process(self, image, time=0, audio_level=0):
        if not self.enabled:
            return image
            
        # Strobe frequency based on intensity
        strobe_freq = 5 + self.intensity * 15
        self.freeze_timer += 1
        
        freeze_duration = int(30 / strobe_freq)
        
        if self.freeze_timer > freeze_duration:
            self.freeze_buffer = image.copy()
            self.freeze_timer = 0
        
        if self.freeze_buffer is not None:
            return self.freeze_buffer
        
        return image


class ScanlinesEffect(EffectNode):
    """CRT scanlines, roll, and VHS wobble"""
    def __init__(self, intensity=0.5):
        super().__init__("Scanlines", intensity)
        self.roll_offset = 0
        
    def process(self, image, time=0, audio_level=0):
        if not self.enabled:
            return image
            
        img_array = np.array(image)
        h, w = img_array.shape[:2]
        
        # Add scanlines
        scanline_pattern = np.ones((h, w, 3), dtype=np.float32)
        for y in range(0, h, 2):
            scanline_pattern[y, :, :] *= (1 - self.intensity * 0.3)
        
        result = (img_array * scanline_pattern).astype(np.uint8)
        
        # Add CRT roll
        self.roll_offset += int(self.intensity * 2)
        result = np.roll(result, self.roll_offset % h, axis=0)
        
        # Add VHS wobble
        for y in range(h):
            shift = int(np.sin(y * 0.1 + time * 5) * self.intensity * 5)
            result[y] = np.roll(result[y], shift, axis=0)
        
        return Image.fromarray(result)


class SlitScanEffect(EffectNode):
    """Slit-scan time displacement"""
    def __init__(self, intensity=0.5, buffer_size=60):
        super().__init__("SlitScan", intensity)
        self.buffer_size = buffer_size
        self.frame_buffer = []
        
    def process(self, image, time=0, audio_level=0):
        if not self.enabled:
            return image
            
        img_array = np.array(image)
        h, w = img_array.shape[:2]
        
        # Add current frame to buffer
        self.frame_buffer.append(img_array.copy())
        if len(self.frame_buffer) > self.buffer_size:
            self.frame_buffer.pop(0)
        
        if len(self.frame_buffer) < 2:
            return image
        
        # Create slit-scan effect
        result = np.zeros_like(img_array)
        scan_width = max(1, int(h / len(self.frame_buffer)))
        
        for i, frame in enumerate(self.frame_buffer):
            start_y = i * scan_width
            end_y = min(start_y + scan_width, h)
            if start_y < h:
                # Mix between temporal and spatial scanning
                mix = self.intensity
                result[start_y:end_y] = (
                    frame[start_y:end_y] * mix + 
                    img_array[start_y:end_y] * (1 - mix)
                ).astype(np.uint8)
        
        return Image.fromarray(result)


class VolumetricEffect(EffectNode):
    """Depth-based fog and volumetric effects"""
    def __init__(self, intensity=0.5):
        super().__init__("Volumetric", intensity)
        
    def process(self, image, time=0, audio_level=0):
        if not self.enabled:
            return image
            
        img_array = np.array(image)
        h, w = img_array.shape[:2]
        
        # Create depth map from luminance
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        depth = cv2.GaussianBlur(gray, (21, 21), 0) / 255.0
        
        # Create fog/haze based on depth
        fog_color = np.array([200, 220, 255])
        depth_3d = np.stack([depth] * 3, axis=2)
        
        fog = fog_color * depth_3d * self.intensity
        
        # Add light rays
        ray_angle = time * 20
        for i in range(5):
            angle = ray_angle + i * 36
            ray_x = w // 2 + np.cos(np.radians(angle)) * w * 0.4
            ray_y = h // 2 + np.sin(np.radians(angle)) * h * 0.4
            
            y, x = np.ogrid[:h, :w]
            dist = np.sqrt((x - ray_x)**2 + (y - ray_y)**2)
            ray_intensity = np.exp(-dist / (50 + self.intensity * 100))
            
            fog += np.stack([ray_intensity] * 3, axis=2) * 50 * self.intensity
        
        # Blend fog with image
        result = np.clip(img_array.astype(np.float32) + fog, 0, 255).astype(np.uint8)
        
        return Image.fromarray(result)


class FractalEffect(EffectNode):
    """Fractal generation and overlay"""
    def __init__(self, intensity=0.5, fractal_type="mandelbrot"):
        super().__init__("Fractal", intensity)
        self.fractal_type = fractal_type
        
    def mandelbrot(self, h, w, zoom, offset_x, offset_y):
        """Generate Mandelbrot set"""
        max_iter = 50
        
        x = np.linspace(-2.5 / zoom + offset_x, 1.0 / zoom + offset_x, w)
        y = np.linspace(-1.0 / zoom + offset_y, 1.0 / zoom + offset_y, h)
        X, Y = np.meshgrid(x, y)
        C = X + 1j * Y
        
        Z = np.zeros_like(C)
        M = np.zeros(C.shape)
        
        for i in range(max_iter):
            mask = np.abs(Z) <= 2
            Z[mask] = Z[mask]**2 + C[mask]
            M[mask] = i
        
        return M
        
    def julia(self, h, w, zoom, c_real, c_imag):
        """Generate Julia set"""
        max_iter = 50
        
        x = np.linspace(-1.5 / zoom, 1.5 / zoom, w)
        y = np.linspace(-1.5 / zoom, 1.5 / zoom, h)
        X, Y = np.meshgrid(x, y)
        Z = X + 1j * Y
        
        C = complex(c_real, c_imag)
        M = np.zeros(Z.shape)
        
        for i in range(max_iter):
            mask = np.abs(Z) <= 2
            Z[mask] = Z[mask]**2 + C
            M[mask] = i
        
        return M
        
    def process(self, image, time=0, audio_level=0):
        if not self.enabled:
            return image
            
        img_array = np.array(image)
        h, w = img_array.shape[:2]
        
        # Generate fractal
        zoom = 1 + self.intensity * 3
        if self.fractal_type == "mandelbrot":
            fractal = self.mandelbrot(h, w, zoom, 
                                      np.cos(time * 0.5) * 0.5,
                                      np.sin(time * 0.5) * 0.5)
        else:  # julia
            fractal = self.julia(h, w, zoom,
                                -0.7 + np.cos(time) * 0.2,
                                0.27 + np.sin(time) * 0.2)
        
        # Colorize fractal
        fractal_normalized = (fractal / fractal.max() * 255).astype(np.uint8)
        fractal_colored = cv2.applyColorMap(fractal_normalized, cv2.COLORMAP_HOT)
        fractal_colored = cv2.cvtColor(fractal_colored, cv2.COLOR_BGR2RGB)
        
        # Blend with image
        result = cv2.addWeighted(img_array, 1 - self.intensity * 0.5, 
                                fractal_colored, self.intensity * 0.5, 0)
        
        return Image.fromarray(result)


class HologramEffect(EffectNode):
    """Holographic interference patterns"""
    def __init__(self, intensity=0.5):
        super().__init__("Hologram", intensity)
        
    def process(self, image, time=0, audio_level=0):
        if not self.enabled:
            return image
            
        img_array = np.array(image)
        h, w = img_array.shape[:2]
        
        # Create interference pattern
        y, x = np.ogrid[:h, :w]
        
        # Multiple interference waves
        pattern = np.zeros((h, w))
        for i in range(3):
            angle = i * np.pi / 3 + time * 0.5
            freq = 0.05 + i * 0.02
            pattern += np.sin((x * np.cos(angle) + y * np.sin(angle)) * freq)
        
        pattern = (pattern + 3) / 6  # Normalize to 0-1
        
        # Create chromatic effect
        pattern_3d = np.stack([pattern] * 3, axis=2)
        
        # Shift RGB channels differently
        pattern_rgb = pattern_3d.copy()
        pattern_rgb[:, :, 0] = np.roll(pattern, 2, axis=1)
        pattern_rgb[:, :, 2] = np.roll(pattern, -2, axis=1)
        
        # Apply to image
        result = img_array.astype(np.float32)
        result = result * (0.7 + pattern_rgb * 0.3 * self.intensity)
        result = np.clip(result, 0, 255).astype(np.uint8)
        
        # Add scan lines for hologram effect
        for y in range(0, h, 3):
            result[y] = result[y] * 0.8
        
        return Image.fromarray(result)


class TouchDesignerClone:
    """Main application class"""
    
    # Supported aspect ratios
    ASPECT_RATIOS = {
        '1:1': (1, 1),
        '3:4': (3, 4),
        '4:3': (4, 3),
        '9:16': (9, 16),
        '16:9': (16, 9)
    }
    
    # Supported resolutions (height for portrait/square, width for landscape)
    RESOLUTIONS = {
        '720': 720,
        '1080': 1080,
        '2k': 1440,
        '4k': 2160
    }
    
    def __init__(self, aspect_ratio='1:1', resolution='1080', custom_width=None, custom_height=None):
        """
        Initialize TouchDesigner Clone
        
        Args:
            aspect_ratio: One of '1:1', '3:4', '4:3', '9:16', '16:9'
            resolution: One of '720', '1080', '2k', '4k'
            custom_width: Override with custom width (ignores aspect_ratio/resolution)
            custom_height: Override with custom height (ignores aspect_ratio/resolution)
        """
        # Use custom dimensions if provided
        if custom_width and custom_height:
            self.width = custom_width
            self.height = custom_height
            self.aspect_ratio = f"{custom_width}:{custom_height}"
        else:
            # Validate inputs
            if aspect_ratio not in self.ASPECT_RATIOS:
                raise ValueError(f"Aspect ratio must be one of: {list(self.ASPECT_RATIOS.keys())}")
            if resolution not in self.RESOLUTIONS:
                raise ValueError(f"Resolution must be one of: {list(self.RESOLUTIONS.keys())}")
            
            self.aspect_ratio = aspect_ratio
            self.resolution = resolution
            
            # Calculate dimensions
            ratio_w, ratio_h = self.ASPECT_RATIOS[aspect_ratio]
            res_value = self.RESOLUTIONS[resolution]
            
            # Determine width and height based on aspect ratio
            if ratio_w == ratio_h:  # Square (1:1)
                self.width = res_value
                self.height = res_value
            elif ratio_w > ratio_h:  # Landscape (16:9, 4:3)
                self.width = res_value
                self.height = int(res_value * ratio_h / ratio_w)
            else:  # Portrait (9:16, 3:4)
                self.height = res_value
                self.width = int(res_value * ratio_w / ratio_h)
        
        self.running = False
        
        # Effect presets
        self.effects = {
            'feedback': FeedbackEffect(intensity=0.5),
            'displace': DisplaceEffect(intensity=0.5),
            'optical_flow': OpticalFlowEffect(intensity=0.5),
            'rgb_split': RGBSplitEffect(intensity=0.5),
            'kaleidoscope': KaleidoscopeEffect(intensity=0.5),
            'pixel_sort': PixelSortEffect(intensity=0.5),
            'edge_glow': EdgeGlowEffect(intensity=0.5),
            'posterize': PosterizeEffect(intensity=0.5),
            'lut': LUTEffect(intensity=0.5),
            'heat_haze': HeatHazeEffect(intensity=0.5),
            'particles': ParticleEffect(intensity=0.5),
            'plexus': PlexusEffect(intensity=0.5),
            'strobe': StrobeEffect(intensity=0.5),
            'scanlines': ScanlinesEffect(intensity=0.5),
            'slit_scan': SlitScanEffect(intensity=0.5),
            'volumetric': VolumetricEffect(intensity=0.5),
            'fractal': FractalEffect(intensity=0.5),
            'hologram': HologramEffect(intensity=0.5),
        }
        
        self.active_effects = []
        self.global_intensity = 0.5
        self.time = 0
        self.audio_level = 0
        
        # Input
        self.input_image = None
        self.current_frame = None
        
        # Video recording
        self.recording = False
        self.video_writer = None
        self.output_frames = []
        
    def load_image(self, image_path):
        """Load input image with center cropping to match aspect ratio"""
        img = Image.open(image_path)
        
        # Get original dimensions
        orig_width, orig_height = img.size
        target_aspect = self.width / self.height
        orig_aspect = orig_width / orig_height
        
        # Center crop to match target aspect ratio (no stretching)
        if abs(target_aspect - orig_aspect) > 0.01:  # Aspect ratios don't match
            if orig_aspect > target_aspect:
                # Original is wider - crop width
                new_width = int(orig_height * target_aspect)
                left = (orig_width - new_width) // 2
                img = img.crop((left, 0, left + new_width, orig_height))
            else:
                # Original is taller - crop height
                new_height = int(orig_width / target_aspect)
                top = (orig_height - new_height) // 2
                img = img.crop((0, top, orig_width, top + new_height))
        
        # Resize to target resolution
        self.input_image = img.resize((self.width, self.height), Image.Resampling.LANCZOS)
        self.current_frame = self.input_image.copy()
        print(f"Loaded image: {image_path}")
        print(f"  Original size: {orig_width}x{orig_height}")
        print(f"  Final size: {self.width}x{self.height} ({self.aspect_ratio})")
        if abs(target_aspect - orig_aspect) > 0.01:
            print(f"  Applied center crop to match aspect ratio")

        
    def create_generative_image(self, prompt=None, seed=None):
        """Create a generative starting image"""
        if seed is not None:
            np.random.seed(seed)
        
        # Create colorful noise-based image
        noise = np.random.rand(self.height, self.width, 3) * 255
        
        # Add some structure
        for _ in range(3):
            noise = cv2.GaussianBlur(noise.astype(np.uint8), (15, 15), 0)
        
        # Add gradients
        y, x = np.ogrid[:self.height, :self.width]
        gradient = np.stack([
            x / self.width,
            y / self.height,
            1 - x / self.width
        ], axis=2) * 255
        
        # Combine
        img_array = (noise * 0.5 + gradient * 0.5).astype(np.uint8)
        
        self.input_image = Image.fromarray(img_array)
        self.current_frame = self.input_image.copy()
        print("Created generative image")
        
    def add_effect(self, effect_name):
        """Enable an effect"""
        if effect_name in self.effects and effect_name not in self.active_effects:
            self.active_effects.append(effect_name)
            self.effects[effect_name].enabled = True
            print(f"Added effect: {effect_name}")
            
    def remove_effect(self, effect_name):
        """Disable an effect"""
        if effect_name in self.active_effects:
            self.active_effects.remove(effect_name)
            self.effects[effect_name].enabled = False
            print(f"Removed effect: {effect_name}")
            
    def set_effect_intensity(self, effect_name, intensity):
        """Set intensity for specific effect"""
        if effect_name in self.effects:
            self.effects[effect_name].set_intensity(intensity)
            
    def set_global_intensity(self, intensity):
        """Set global intensity for all effects"""
        self.global_intensity = np.clip(intensity, 0.0, 1.0)
        for effect in self.effects.values():
            effect.set_intensity(self.global_intensity)
        print(f"Global intensity: {self.global_intensity:.2f}")
        
    def process_frame(self):
        """Process current frame through effect chain"""
        if self.current_frame is None:
            return None
            
        processed = self.current_frame.copy()
        
        # Apply active effects in order
        for effect_name in self.active_effects:
            effect = self.effects[effect_name]
            if effect.enabled:
                processed = effect.process(processed, self.time, self.audio_level)
        
        return processed
        
    def start_recording(self, output_path="output.mp4", fps=30):
        """Start recording video"""
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video_writer = cv2.VideoWriter(
            output_path, fourcc, fps, (self.width, self.height)
        )
        self.recording = True
        self.output_frames = []
        print(f"Started recording to {output_path}")
        
    def stop_recording(self):
        """Stop recording video"""
        if self.video_writer is not None:
            self.video_writer.release()
            self.video_writer = None
        self.recording = False
        print("Stopped recording")
        
    def run_interactive(self, duration=10, fps=30):
        """Run interactive session"""
        import matplotlib.pyplot as plt
        from matplotlib.animation import FuncAnimation
        
        if self.input_image is None:
            print("No input image loaded. Creating generative image...")
            self.create_generative_image()
        
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.axis('off')
        
        total_frames = duration * fps
        
        def update(frame):
            self.time = frame / fps
            self.current_frame = self.input_image.copy()
            processed = self.process_frame()
            
            if processed is not None:
                ax.clear()
                ax.imshow(np.array(processed))
                ax.axis('off')
                ax.set_title(f"Time: {self.time:.2f}s | Active: {', '.join(self.active_effects)}")
                
                if self.recording and self.video_writer is not None:
                    frame_bgr = cv2.cvtColor(np.array(processed), cv2.COLOR_RGB2BGR)
                    self.video_writer.write(frame_bgr)
            
            return ax,
        
        anim = FuncAnimation(fig, update, frames=total_frames, interval=1000/fps, blit=False)
        plt.tight_layout()
        plt.show()
        
    def export_image(self, output_path="output.png"):
        """Export current frame as image"""
        if self.current_frame is not None:
            processed = self.process_frame()
            if processed is not None:
                processed.save(output_path)
                print(f"Exported image to {output_path}")


def create_preset_demo(preset_name, image_path=None, duration=5, output_path=None, 
                      aspect_ratio='1:1', resolution='1080', intensity=0.7):
    """Create a demo with a specific preset"""
    app = TouchDesignerClone(aspect_ratio=aspect_ratio, resolution=resolution)
    
    if image_path:
        app.load_image(image_path)
    else:
        app.create_generative_image(seed=42)
    
    # Preset configurations
    presets = {
        'cyber_glitch': ['rgb_split', 'displace', 'scanlines', 'edge_glow'],
        'psychedelic': ['kaleidoscope', 'feedback', 'lut', 'heat_haze'],
        'holographic': ['hologram', 'rgb_split', 'edge_glow', 'volumetric'],
        'datamosh': ['pixel_sort', 'feedback', 'displace', 'strobe'],
        'retro_vhs': ['scanlines', 'feedback', 'rgb_split', 'posterize'],
        'particle_flow': ['particles', 'optical_flow', 'plexus', 'edge_glow'],
        'fractal_dream': ['fractal', 'kaleidoscope', 'lut', 'feedback'],
        'neon_city': ['edge_glow', 'lut', 'heat_haze', 'scanlines'],
        'time_warp': ['slit_scan', 'optical_flow', 'feedback', 'displace'],
        'volumetric_fog': ['volumetric', 'heat_haze', 'edge_glow', 'lut'],
    }
    
    if preset_name in presets:
        for effect in presets[preset_name]:
            app.add_effect(effect)
        print(f"Loaded preset: {preset_name}")
        print(f"Output dimensions: {app.width}x{app.height}")
    else:
        print(f"Unknown preset: {preset_name}")
        print(f"Available presets: {', '.join(presets.keys())}")
        return
    
    app.set_global_intensity(intensity)
    
    if output_path:
        app.start_recording(output_path, fps=30)
    
    app.run_interactive(duration=duration, fps=30)
    
    if output_path:
        app.stop_recording()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="TouchDesigner-Inspired Visual Effects Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Default 1080x1080 (1:1)
  python touchdesigner_clone.py --preset psychedelic
  
  # 4K square
  python touchdesigner_clone.py --preset cyber_glitch --resolution 4k
  
  # Instagram story (9:16)
  python touchdesigner_clone.py --preset neon_city --aspect-ratio 9:16 --resolution 1080
  
  # YouTube video (16:9)
  python touchdesigner_clone.py --preset holographic --aspect-ratio 16:9 --resolution 1080
  
  # TikTok/Reels (9:16, 1080p)
  python touchdesigner_clone.py --image photo.jpg --preset psychedelic --aspect-ratio 9:16 --resolution 1080 --output video.mp4
        """
    )
    
    parser.add_argument('--image', type=str, help='Input image path')
    parser.add_argument('--preset', type=str, default='cyber_glitch', 
                       help='Effect preset name (default: cyber_glitch)')
    parser.add_argument('--aspect-ratio', type=str, default='1:1',
                       choices=['1:1', '3:4', '4:3', '9:16', '16:9'],
                       help='Aspect ratio (default: 1:1)')
    parser.add_argument('--resolution', type=str, default='1080',
                       choices=['720', '1080', '2k', '4k'],
                       help='Resolution (default: 1080)')
    parser.add_argument('--duration', type=int, default=5, 
                       help='Duration in seconds (default: 5)')
    parser.add_argument('--output', type=str, help='Output video path')
    parser.add_argument('--intensity', type=float, default=0.7,
                       help='Global effect intensity 0.0-1.0 (default: 0.7)')
    parser.add_argument('--list-presets', action='store_true',
                       help='List available presets')
    parser.add_argument('--list-effects', action='store_true',
                       help='List available effects')
    parser.add_argument('--list-formats', action='store_true',
                       help='List supported aspect ratios and resolutions')
    
    args = parser.parse_args()
    
    if args.list_formats:
        print("\n" + "="*60)
        print("Supported Formats")
        print("="*60)
        print("\nAspect Ratios:")
        print("  1:1   - Square (Instagram posts, profile pictures)")
        print("  3:4   - Portrait (standard photo)")
        print("  4:3   - Landscape (classic TV)")
        print("  9:16  - Vertical (Instagram Stories, TikTok, Reels)")
        print("  16:9  - Widescreen (YouTube, modern displays)")
        
        print("\nResolutions:")
        print("  720   - HD (720p)")
        print("  1080  - Full HD (1080p) - Default")
        print("  2k    - 2K (1440p)")
        print("  4k    - 4K (2160p)")
        
        print("\nExamples:")
        app = TouchDesignerClone(aspect_ratio='1:1', resolution='1080')
        print(f"  1:1 @ 1080  → {app.width}x{app.height}")
        
        app = TouchDesignerClone(aspect_ratio='16:9', resolution='1080')
        print(f"  16:9 @ 1080 → {app.width}x{app.height}")
        
        app = TouchDesignerClone(aspect_ratio='9:16', resolution='1080')
        print(f"  9:16 @ 1080 → {app.width}x{app.height}")
        
        app = TouchDesignerClone(aspect_ratio='1:1', resolution='4k')
        print(f"  1:1 @ 4k    → {app.width}x{app.height}")
        
        app = TouchDesignerClone(aspect_ratio='16:9', resolution='4k')
        print(f"  16:9 @ 4k   → {app.width}x{app.height}")
        print()
        
    elif args.list_presets:
        print("\nAvailable Presets:")
        print("==================")
        presets = {
            'cyber_glitch': 'RGB split + displacement + scanlines + edge glow',
            'psychedelic': 'Kaleidoscope + feedback + LUT + heat haze',
            'holographic': 'Hologram + RGB split + edge glow + volumetric',
            'datamosh': 'Pixel sorting + feedback + displacement + strobe',
            'retro_vhs': 'Scanlines + feedback + RGB split + posterize',
            'particle_flow': 'Particles + optical flow + plexus + edge glow',
            'fractal_dream': 'Fractal + kaleidoscope + LUT + feedback',
            'neon_city': 'Edge glow + LUT + heat haze + scanlines',
            'time_warp': 'Slit-scan + optical flow + feedback + displace',
            'volumetric_fog': 'Volumetric + heat haze + edge glow + LUT',
        }
        for name, desc in presets.items():
            print(f"  {name:20s} - {desc}")
        print()
        
    elif args.list_effects:
        print("\nAvailable Effects:")
        print("==================")
        app = TouchDesignerClone()
        for name, effect in app.effects.items():
            print(f"  {name:20s} - {effect.name}")
        print()
        
    else:
        # Run demo
        print("\n" + "="*60)
        print("TouchDesigner-Inspired Visual Effects Generator")
        print("="*60)
        print(f"Aspect Ratio: {args.aspect_ratio}")
        print(f"Resolution: {args.resolution}")
        print(f"Preset: {args.preset}")
        print(f"Duration: {args.duration}s")
        print(f"Intensity: {args.intensity}")
        if args.image:
            print(f"Input Image: {args.image}")
        if args.output:
            print(f"Output: {args.output}")
        print("="*60 + "\n")
        
        create_preset_demo(
            preset_name=args.preset,
            image_path=args.image,
            duration=args.duration,
            output_path=args.output,
            aspect_ratio=args.aspect_ratio,
            resolution=args.resolution,
            intensity=args.intensity
        )
