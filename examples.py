#!/usr/bin/env python3
"""
Example Usage Script for TouchDesigner Clone
=============================================

Demonstrates various ways to use the visual effects generator.
"""

from touchdesigner_clone import TouchDesignerClone, create_preset_demo
from PIL import Image, ImageDraw
import numpy as np


def example_1_basic_usage():
    """Example 1: Basic usage with generative image"""
    print("\n=== Example 1: Basic Usage ===")
    
    # Default is now 1080x1080 (1:1)
    app = TouchDesignerClone()
    
    # Create a generative starting image
    app.create_generative_image(seed=42)
    
    # Add some effects
    app.add_effect('feedback')
    app.add_effect('kaleidoscope')
    app.add_effect('edge_glow')
    
    # Set intensity
    app.set_global_intensity(0.7)
    
    # Run for 5 seconds
    print("Running basic demo...")
    app.run_interactive(duration=5, fps=30)


def example_2_custom_image():
    """Example 2: Using a custom image with different aspect ratios"""
    print("\n=== Example 2: Custom Image with Aspect Ratios ===")
    
    # Create a test image (landscape)
    test_img = Image.new('RGB', (1920, 1080), color=(50, 50, 100))
    draw = ImageDraw.Draw(test_img)
    
    # Draw some shapes
    for i in range(10):
        x = np.random.randint(0, 1920)
        y = np.random.randint(0, 1080)
        r = np.random.randint(20, 100)
        color = (
            np.random.randint(100, 255),
            np.random.randint(100, 255),
            np.random.randint(100, 255)
        )
        draw.ellipse([x-r, y-r, x+r, y+r], fill=color, outline=None)
    
    test_img.save('/tmp/test_image.png')
    
    # Create app with Instagram Story aspect ratio (9:16)
    print("\nCreating 9:16 vertical video (Instagram Story/TikTok format)...")
    app = TouchDesignerClone(aspect_ratio='9:16', resolution='1080')
    app.load_image('/tmp/test_image.png')
    
    # Add psychedelic effects
    app.add_effect('kaleidoscope')
    app.add_effect('lut')
    app.add_effect('heat_haze')
    
    app.set_global_intensity(0.8)
    
    print("Running custom image demo...")
    app.run_interactive(duration=5, fps=30)


def example_3_glitch_art():
    """Example 3: Create glitch art"""
    print("\n=== Example 3: Glitch Art ===")
    
    app = TouchDesignerClone()  # Default 1080x1080
    app.create_generative_image(seed=123)
    
    # Glitch art effect chain
    glitch_effects = [
        'rgb_split',
        'pixel_sort',
        'displace',
        'scanlines',
        'feedback'
    ]
    
    for effect in glitch_effects:
        app.add_effect(effect)
    
    # Different intensities for each effect
    app.set_effect_intensity('rgb_split', 0.7)
    app.set_effect_intensity('pixel_sort', 0.5)
    app.set_effect_intensity('displace', 0.6)
    app.set_effect_intensity('scanlines', 0.4)
    app.set_effect_intensity('feedback', 0.8)
    
    print("Creating glitch art...")
    app.run_interactive(duration=5, fps=30)


def example_4_export_video():
    """Example 4: Export to video in 4K 16:9"""
    print("\n=== Example 4: Export 4K Video (16:9 YouTube format) ===")
    
    # 4K widescreen for YouTube
    app = TouchDesignerClone(aspect_ratio='16:9', resolution='4k')
    app.create_generative_image(seed=999)
    
    print(f"Output resolution: {app.width}x{app.height}")
    
    # Create a beautiful effect combination
    app.add_effect('hologram')
    app.add_effect('volumetric')
    app.add_effect('edge_glow')
    app.add_effect('feedback')
    
    app.set_global_intensity(0.75)
    
    # Start recording
    output_path = '/tmp/hologram_4k_demo.mp4'
    app.start_recording(output_path, fps=30)
    
    print(f"Recording to {output_path}...")
    app.run_interactive(duration=10, fps=30)
    
    app.stop_recording()
    print(f"Video saved to {output_path}")


def example_5_fractal_animation():
    """Example 5: Fractal-based animation"""
    print("\n=== Example 5: Fractal Animation ===")
    
    app = TouchDesignerClone()  # Default 1080x1080
    app.create_generative_image(seed=777)
    
    # Fractal + psychedelic effects
    app.add_effect('fractal')
    app.add_effect('kaleidoscope')
    app.add_effect('lut')
    app.add_effect('feedback')
    
    # Higher intensity for trippy visuals
    app.set_global_intensity(0.9)
    
    print("Creating fractal animation...")
    app.run_interactive(duration=8, fps=30)


def example_6_single_frame_processing():
    """Example 6: Process a single frame"""
    print("\n=== Example 6: Single Frame Processing ===")
    
    app = TouchDesignerClone()  # Default 1080x1080
    app.create_generative_image(seed=555)
    
    # Add effects
    app.add_effect('edge_glow')
    app.add_effect('rgb_split')
    app.add_effect('posterize')
    
    app.set_global_intensity(0.6)
    
    # Process single frame
    app.current_frame = app.input_image.copy()
    processed = app.process_frame()
    
    # Save result
    output_path = '/tmp/processed_frame.png'
    processed.save(output_path)
    print(f"Processed frame saved to {output_path}")


def example_7_aspect_ratio_comparison():
    """Example 7: Compare different aspect ratios"""
    print("\n=== Example 7: Aspect Ratio Comparison ===")
    
    # Create base image (landscape 16:9)
    test_img = Image.new('RGB', (1920, 1080), color=(30, 30, 50))
    draw = ImageDraw.Draw(test_img)
    
    # Draw a gradient circle
    for r in range(300, 0, -10):
        brightness = int((300 - r) / 300 * 255)
        color = (brightness, brightness // 2, brightness)
        draw.ellipse([960-r, 540-r, 960+r, 540+r], fill=color)
    
    test_img.save('/tmp/gradient_circle.png')
    
    # Test different aspect ratios
    aspect_ratios = ['1:1', '9:16', '16:9', '4:3', '3:4']
    
    for aspect in aspect_ratios:
        print(f"\nTesting aspect ratio: {aspect}")
        
        app = TouchDesignerClone(aspect_ratio=aspect, resolution='1080')
        app.load_image('/tmp/gradient_circle.png')
        app.add_effect('kaleidoscope')
        app.set_global_intensity(0.7)
        
        # Process and save
        app.current_frame = app.input_image.copy()
        app.time = 1.0
        processed = app.process_frame()
        
        output_path = f'/tmp/aspect_{aspect.replace(":", "x")}.png'
        processed.save(output_path)
        print(f"  Dimensions: {app.width}x{app.height}")
        print(f"  Saved: {output_path}")


def example_8_social_media_formats():
    """Example 8: Export in different social media formats"""
    print("\n=== Example 8: Social Media Format Examples ===")
    
    formats = {
        'Instagram Post': ('1:1', '1080'),
        'Instagram Story': ('9:16', '1080'),
        'YouTube Video': ('16:9', '1080'),
        'TikTok': ('9:16', '1080'),
        'Twitter Video': ('16:9', '720')
    }
    
    for name, (aspect, res) in formats.items():
        print(f"\n{name} ({aspect}, {res})")
        app = TouchDesignerClone(aspect_ratio=aspect, resolution=res)
        print(f"  Dimensions: {app.width}x{app.height}")
        
        # Quick demo
        app.create_generative_image(seed=42)
        app.add_effect('edge_glow')
        app.set_global_intensity(0.7)
        
        app.current_frame = app.input_image.copy()
        processed = app.process_frame()
        
        filename = name.lower().replace(' ', '_')
        output_path = f'/tmp/{filename}_{app.width}x{app.height}.png'
        processed.save(output_path)
        print(f"  Saved: {output_path}")


def interactive_menu():
    """Interactive menu for running examples"""
    print("\n" + "="*60)
    print("TouchDesigner Clone - Example Menu")
    print("="*60)
    print("\nAvailable Examples:")
    print("  1. Basic Usage (1080x1080 square)")
    print("  2. Custom Image (9:16 vertical for Instagram/TikTok)")
    print("  3. Glitch Art (datamosh style)")
    print("  4. Export 4K Video (16:9 for YouTube)")
    print("  5. Fractal Animation (square format)")
    print("  6. Single Frame Processing")
    print("  7. Aspect Ratio Comparison (all formats)")
    print("  8. Social Media Format Examples")
    print("  9. Run All Examples")
    print("  0. Exit")
    print("="*60)
    
    choice = input("\nEnter your choice (0-9): ").strip()
    
    examples = {
        '1': example_1_basic_usage,
        '2': example_2_custom_image,
        '3': example_3_glitch_art,
        '4': example_4_export_video,
        '5': example_5_fractal_animation,
        '6': example_6_single_frame_processing,
        '7': example_7_aspect_ratio_comparison,
        '8': example_8_social_media_formats,
    }
    
    if choice == '9':
        # Run all examples
        for func in examples.values():
            try:
                func()
            except Exception as e:
                print(f"Error in example: {e}")
    elif choice in examples:
        examples[choice]()
    elif choice == '0':
        print("Exiting...")
        return
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Run specific example from command line
        example_num = sys.argv[1]
        examples = {
            '1': example_1_basic_usage,
            '2': example_2_custom_image,
            '3': example_3_glitch_art,
            '4': example_4_export_video,
            '5': example_5_fractal_animation,
            '6': example_6_single_frame_processing,
            '7': example_7_aspect_ratio_comparison,
            '8': example_8_social_media_formats,
        }
        
        if example_num in examples:
            examples[example_num]()
        else:
            print(f"Unknown example: {example_num}")
            print("Usage: python examples.py [1-8]")
    else:
        # Show interactive menu
        interactive_menu()
