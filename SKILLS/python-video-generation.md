---
name: python-video-generation
description: 指导 AI 大模型通过编写 Python 代码（使用 moviepy, Pillow, gTTS, OpenCV, numpy 等）生成媲美 Runway, Sora, Pika 等 AI 视频生成模型的精美、带声效缓动动画与专业排版的视频。
---

# Skill: Python Programmatic Video Generation (High-Quality AI-Grade Output)

This skill guide enables an AI agent or LLM assistant to write Python code (using libraries like `moviepy`, `manim`, `opencv-python`, `pillow`, `gTTS`, `vlc`/`ffmpeg`, `matplotlib`, `rembg`, `numpy`, `librosa`) that generates professional, visual-rich, high-production-value videos directly from prompt descriptions, rivaling direct AI video generation models (like Runway, Sora, Pika).

---

## 📖 使用说明 (Usage Instructions)

### 1. 适用场景 (When to Use)
- **AI Agent / 大模型 Prompt 注入**：将本 Skill 文件内容作为 System Prompt、Context 或 Tool 指引加载给 AI，使 AI 具备用 Python 编写高质感视频生成代码的能力。
- **开发者 / 自动化脚本**：开发者可参考本规范与代码模板，搭建基于 Python 代码的 AI 视频创作管线（Text-to-Video Engine）。

### 2. 使用流程 (How to Apply)
1. **输入 Prompt 需求**：例如“生成一段 10 秒的科技风 Product Launch 视频，带背景音乐、语音旁白与缓动文字动画”。
2. **AI 读取 Skill 规范**：AI 按照本 Skill 中的分层设计、缓动函数（Easing）、卡片质感（Glassmorphic Cards）、动态粒子（Particles）与 Audio Ducking 音频混音原则，规划视频时间轴。
3. **生成并执行 Python 代码**：AI 输出完整且可直接运行的 Python 脚本，使用 `moviepy`/`Pillow`/`gTTS`/`OpenCV` 等库合成 `.mp4` 视频文件。
4. **输出高质感视频**：运行生成的 Python 代码，即可直接渲染出媲美 AI 视频生成模型的精美视频。

---

## 💡 Core Philosophy & Paradigm

Direct video-generation AI models often suffer from temporal inconsistency, text rendering errors, lack of precise layout control, unpredictable motion, and inability to produce exact data/charts/animations.

By leveraging **Python-driven Programmatic Video Generation**, we combine:
1. **Algorithmic & Procedural Visuals**: Fluid motion graphics, mathematical animations, particle effects, vector art, smooth camera transforms.
2. **Dynamic Typography & Layouts**: Exact visual hierarchy, typography design, kinetic text, title cards, subtle animations, accurate multi-lingual subtitles.
3. **AI Asset Synthesis Integration**: Pre-generated diffusion images (via Pillow/OpenCV blending), AI voiceover (TTS/gTTS/elevenlabs API), multi-track audio mixing (BGM + Ducking + SFX).
4. **Cinematic Post-Processing**: Vignette, motion blur, color grading, film grain, smooth transitions (crossfade, slide, zoom-in/out), easing functions.

---

## 🛠️ Essential Tech Stack & Python Libraries

| Library | Purpose | Key Usage |
| :--- | :--- | :--- |
| `moviepy` (v1.x or v2.x) | Core video editing & timeline composition | Clips, compositions, transitions, audio mixing, rendering |
| `manim` | Mathematical / vector kinetic animations | High-grade explainer motion graphics, vector diagrams |
| `Pillow (PIL)` & `cairosvg` | High-precision graphic design & visual frame synthesis | Designing posters, overlays, vector shapes, badges, card layouts |
| `opencv-python (cv2)` | Procedural pixel-level rendering & video effects | Fast frame generation, optical flow, blur, color adjustment, filters |
| `numpy` | Mathematical curves, particle systems, noise generation | Easing functions (`sine`, `cubic`, `elastic`), Perlin noise backgrounds, matrix transforms |
| `gTTS` / `edge-tts` / `PyTTSx3` | Voiceover / Speech Synthesis | Generating timing-aligned audio narration |
| `librosa` / `pydub` | Audio processing & beat tracking | Audio waveform extraction, background music beat syncing, audio ducking |

---

## 🎨 Detailed Design Specifications & Visual Aesthetics

### 1. Color Palette Presets
To ensure high production value, avoid pure white (`#FFFFFF`) or pure black (`#000000`) stark solids. Use balanced, curated palettes:

| Palette Style | Background Primary | Secondary Accent | Text Color | Glow / Highlight |
| :--- | :--- | :--- | :--- | :--- |
| **Dark Cyberpunk / Tech** | `#0B0F19` (Deep Navy) | `#3B82F6` (Electric Blue) | `#F3F4F6` (Cool White) | `#8B5CF6` (Neon Purple) |
| **Swiss Clean Light** | `#F8FAFC` (Off-White) | `#0F172A` (Slate Dark) | `#1E293B` (Charcoal) | `#2563EB` (Royal Blue) |
| **Corporate Navy & Gold** | `#0F172A` (Midnight Navy) | `#D97706` (Warm Amber/Gold) | `#F1F5F9` (Soft White) | `#38BDF8` (Sky Blue) |
| **Pastel Creator Mood** | `#FAF5FF` (Soft Violet) | `#EC4899` (Vibrant Pink) | `#334155` (Slate) | `#A855F7` (Purple) |

### 2. Typography Hierarchy & Positioning
- **Title / Hero Text**: 64px - 96px bold font (e.g. `DejaVuSans-Bold.ttf`, `Inter-Bold.ttf`).
- **Subtitle / Secondary Text**: 32px - 48px regular/medium font.
- **Captions / Lower-Third Subtitles**: 24px - 36px medium font positioned at 80%-85% vertical height (`y = int(height * 0.8)`).
- **Text Shadow / Stroke**: Always render text with a subtle drop-shadow (offset `dx=2, dy=2`, color `#00000080`) or border outline (`width=2, color=#00000040`) for readability on dynamic backgrounds.

---

## 📐 Reusable Production-Ready Code Modules

### 1. Easing Functions (Smooth Motion Math)

```python
import numpy as np

def ease_out_cubic(t: float) -> float:
    """Fast start, smooth slowdown near arrival. t ranges from 0.0 to 1.0."""
    t = np.clip(t, 0.0, 1.0)
    return float(1.0 - pow(1.0 - t, 3))

def ease_in_out_sine(t: float) -> float:
    """Smooth sinusoidal acceleration and deceleration."""
    t = np.clip(t, 0.0, 1.0)
    return float(-(np.cos(np.pi * t) - 1.0) / 2.0)

def ease_out_back(t: float, c1: float = 1.70158, c3: float = 2.70158) -> float:
    """Over-shoots slightly and bounces back into place."""
    t = np.clip(t, 0.0, 1.0)
    return float(1.0 + c3 * pow(t - 1.0, 3) + c1 * pow(t - 1.0, 2))
```

### 2. Ken Burns Effect (Smooth Zoom and Pan on Static Images)

```python
import numpy as np
from PIL import Image
from moviepy.editor import VideoClip

def make_ken_burns_clip(image_path: str, duration: float, target_size=(1920, 1080), scale_start=1.0, scale_end=1.15):
    """Generates a VideoClip with a smooth Ken Burns pan-and-zoom motion using Pillow."""
    base_img = Image.open(image_path).convert("RGB")
    orig_w, orig_h = base_img.size
    target_w, target_h = target_size

    def make_frame(t: float) -> np.ndarray:
        progress = np.clip(t / duration, 0.0, 1.0)
        # Apply easing to scale factor
        eased_p = 1.0 - pow(1.0 - progress, 3) # ease_out_cubic
        scale = scale_start + (scale_end - scale_start) * eased_p

        # Crop box dimensions
        crop_w = int(orig_w / scale)
        crop_h = int(orig_h / scale)

        # Gentle pan from center to slightly right-bottom
        max_dx = max(0, orig_w - crop_w)
        max_dy = max(0, orig_h - crop_h)
        offset_x = int(max_dx * 0.5 * eased_p)
        offset_y = int(max_dy * 0.5 * eased_p)

        left = (orig_w - crop_w) // 2 + offset_x
        top = (orig_h - crop_h) // 2 + offset_y
        right = left + crop_w
        bottom = top + crop_h

        cropped = base_img.crop((left, top, right, bottom))
        resized = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)
        return np.array(resized)

    return VideoClip(make_frame, duration=duration)
```

### 3. Procedural Animated Particle Background (NumPy & OpenCV)

```python
import cv2
import numpy as np
from moviepy.editor import VideoClip

def make_particle_background(duration: float, width=1920, height=1080, num_particles=80):
    """Generates a dynamic particle background with animated ambient floating lights."""
    np.random.seed(42)
    particles = []
    for _ in range(num_particles):
        particles.append({
            "x": np.random.uniform(0, width),
            "y": np.random.uniform(0, height),
            "radius": np.random.uniform(2, 6),
            "speed_y": np.random.uniform(-30, -10),
            "speed_x": np.random.uniform(-10, 10),
            "alpha": np.random.uniform(0.2, 0.8)
        })

    def make_frame(t: float) -> np.ndarray:
        # Create dark gradient background
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        # Deep blue-violet gradient fill
        for y in range(height):
            r = int(11 + (20 - 11) * (y / height))
            g = int(15 + (30 - 15) * (y / height))
            b = int(25 + (50 - 25) * (y / height))
            frame[y, :] = (b, g, r) # OpenCV uses BGR

        # Draw floating particles
        overlay = frame.copy()
        for p in particles:
            px = int((p["x"] + p["speed_x"] * t) % width)
            py = int((p["y"] + p["speed_y"] * t) % height)
            radius = int(p["radius"])
            color = (255, 200, 150) # BGR glowing cyan-amber
            cv2.circle(overlay, (px, py), radius, color, -1)

        alpha = 0.5
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
        # Convert BGR to RGB for MoviePy
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    return VideoClip(make_frame, duration=duration)
```

### 4. Glassmorphism Card Frame Generator with Typography (Pillow)

```python
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

def draw_glass_card_frame(
    bg_image: Image.Image,
    card_rect: tuple,
    title_text: str,
    subtitle_text: str,
    blur_radius: int = 15,
    corner_radius: int = 24
) -> Image.Image:
    """Overlays a glassmorphic blurred card with title & subtitle on top of a background image."""
    x1, y1, x2, y2 = card_rect
    card_w, card_h = x2 - x1, y2 - y1

    # 1. Crop and blur card background region
    cropped_bg = bg_image.crop((x1, y1, x2, y2))
    blurred_bg = cropped_bg.filter(ImageFilter.GaussianBlur(blur_radius))

    # 2. Create semi-transparent overlay mask & white frame
    card_surface = Image.new("RGBA", (card_w, card_h), (255, 255, 255, 0))
    draw = ImageDraw.Draw(card_surface)

    # Semi-transparent white fill with subtle border
    draw.rounded_rectangle(
        [(0, 0), (card_w - 1, card_h - 1)],
        radius=corner_radius,
        fill=(255, 255, 255, 45), # 18% opacity fill
        outline=(255, 255, 255, 180), # Soft white edge
        width=2
    )

    # Composite blurred background with translucent card surface
    composite_card = Image.composite(card_surface, blurred_bg.convert("RGBA"), card_surface)

    # 3. Draw text on card
    draw_txt = ImageDraw.Draw(composite_card)
    try:
        font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 36)
        font_sub = ImageFont.truetype("DejaVuSans.ttf", 22)
    except IOError:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    draw_txt.text((30, 30), title_text, fill=(255, 255, 255, 255), font=font_title)
    draw_txt.text((30, 85), subtitle_text, fill=(220, 225, 240, 230), font=font_sub)

    # 4. Paste glass card back onto main image using rounded mask
    mask = Image.new("L", (card_w, card_h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([(0, 0), (card_w - 1, card_h - 1)], radius=corner_radius, fill=255)

    result = bg_image.copy().convert("RGBA")
    result.paste(composite_card, (x1, y1), mask)
    return result.convert("RGB")
```

### 5. Multi-Track Audio Pipeline with Ducking (Voiceover + BGM + SFX)

```python
import os
from gtts import gTTS
from moviepy.editor import AudioFileClip, CompositeAudioClip

def create_ducked_audio_track(
    script_text: str,
    bgm_path: str = None,
    speech_lang: str = "en"
) -> tuple[float, CompositeAudioClip]:
    """Synthesizes TTS speech and mixes it with ducked background music."""
    # Step 1: Generate Speech
    tts_file = "temp_voiceover.mp3"
    tts = gTTS(text=script_text, lang=speech_lang)
    tts.save(tts_file)

    voice_clip = AudioFileClip(tts_file)
    voice_duration = voice_clip.duration
    total_duration = voice_duration + 1.5 # Add padding at end

    audio_tracks = [voice_clip.set_start(0.5).volumex(1.0)]

    # Step 2: Mix BGM with Ducking if provided
    if bgm_path and os.path.exists(bgm_path):
        bgm_clip = AudioFileClip(bgm_path)
        # Loop or trim BGM to fit total duration
        if bgm_clip.duration < total_duration:
            bgm_clip = bgm_clip.loop(duration=total_duration)
        else:
            bgm_clip = bgm_clip.subclip(0, total_duration)

        # Duck BGM volume to 12% so voiceover remains crystal clear
        bgm_clip = bgm_clip.volumex(0.12).audio_fadeout(1.0)
        audio_tracks.append(bgm_clip)

    final_audio = CompositeAudioClip(audio_tracks)
    return total_duration, final_audio
```

---

## 🚀 Complete End-to-End Executable Script Example

Below is a complete, runnable Python script (`generate_product_launch.py`) demonstrating how to combine procedural backgrounds, Ken Burns images, kinetic text overlays, and audio synthesis into a polished 1080p MP4 video.

```python
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from gtts import gTTS
from moviepy.editor import (
    VideoClip, AudioFileClip, CompositeVideoClip, CompositeAudioClip
)

# 1. Helper: Easing curve
def ease_out_cubic(t: float) -> float:
    t = np.clip(t, 0.0, 1.0)
    return float(1.0 - pow(1.0 - t, 3))

# 2. Scene 1: Animated Procedural Particle Title Card
def make_title_scene(duration: float, title_text: str, subtitle_text: str):
    width, height = 1920, 1080

    def make_frame(t: float) -> np.ndarray:
        # Base gradient canvas
        img = Image.new("RGBA", (width, height), (15, 23, 42, 255))
        draw = ImageDraw.Draw(img)

        # Dynamic radial glow at center
        glow_alpha = int(120 + 30 * np.sin(t * 3))
        glow_radius = int(300 + 40 * ease_out_cubic(t / duration))
        draw.ellipse(
            [width//2 - glow_radius, height//2 - glow_radius,
             width//2 + glow_radius, height//2 + glow_radius],
            fill=(59, 130, 246, glow_alpha)
        )
        img = img.filter(ImageFilter.GaussianBlur(80))
        draw = ImageDraw.Draw(img)

        # Animated Glassmorphism Title Card
        card_w, card_h = 1100, 420
        cx, cy = width // 2, height // 2
        card_rect = [(cx - card_w//2, cy - card_h//2), (cx + card_w//2, cy + card_h//2)]

        # Glass surface
        draw.rounded_rectangle(card_rect, radius=32, fill=(255, 255, 255, 25), outline=(255, 255, 255, 120), width=2)

        # Animated Text Entrance (Scale & Opacity via t)
        progress = np.clip(t / 1.2, 0.0, 1.0)
        eased = ease_out_cubic(progress)

        try:
            font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 64)
            font_sub = ImageFont.truetype("DejaVuSans.ttf", 32)
        except IOError:
            font_title = ImageFont.load_default()
            font_sub = ImageFont.load_default()

        # Render Title Text
        draw.text((cx, cy - 50), title_text, fill=(255, 255, 255, int(255 * eased)), font=font_title, anchor="mm")
        draw.text((cx, cy + 60), subtitle_text, fill=(148, 163, 184, int(255 * eased)), font=font_sub, anchor="mm")

        return np.array(img.convert("RGB"))

    return VideoClip(make_frame, duration=duration)

# 3. Main Assembly Routine
def generate_product_launch_video(output_path="product_launch.mp4"):
    print("Synthesizing voiceover track...")
    narration = "Welcome to the future of AI. Experience lightning-fast programmatic video generation powered by Python."
    tts = gTTS(text=narration, lang="en")
    tts.save("temp_narration.mp3")

    speech_audio = AudioFileClip("temp_narration.mp3")
    total_duration = max(6.0, speech_audio.duration + 1.0)

    print("Building visual video timeline...")
    title_clip = make_title_scene(
        duration=total_duration,
        title_text="PYTHON VIDEO ENGINE",
        subtitle_text="Automated • High Quality • Code Driven"
    )

    # Attach speech audio track
    final_audio = CompositeAudioClip([speech_audio.set_start(0.5)])
    final_clip = title_clip.set_audio(final_audio)

    print(f"Rendering final MP4 to {output_path}...")
    final_clip.write_videofile(
        output_path,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        preset="medium"
    )

    # Cleanup temporary files
    if os.path.exists("temp_narration.mp3"):
        os.remove("temp_narration.mp3")
    print("Video generation complete!")

if __name__ == "__main__":
    generate_product_launch_video()
```

---

## ⚠️ Compatibility Notes & Common Error Fallbacks

1. **MoviePy v1.x vs v2.x Method Names**:
   - In MoviePy **v1.x**, clip transformation methods include `.set_duration()`, `.set_audio()`, `.set_start()`, `.volumex()`.
   - In MoviePy **v2.x**, method names were updated to snake_case (`.with_duration()`, `.with_audio()`, `.with_start()`).
   - *Best Practice*: Use fallback wrappers or stick to standard `VideoClip(make_frame, duration=...)` for maximum cross-version stability.

2. **Font Handling in Pillow**:
   - Systems may lack specific TTF fonts like `Inter` or `Montserrat`. Always use a `try...except IOError` fallback to standard system fonts (`DejaVuSans.ttf`, `Arial.ttf`, or `ImageFont.load_default()`).

3. **Audio Duration Sync**:
   - Always determine speech audio clip duration first before assembling visual clip timelines to ensure narration and visuals end cleanly together.

---

## 🌟 Quality Checklist for Video Outputs

- [ ] **Frame Rate & Resolution**: Target 1080p (1920x1080) or Vertical Shorts/Reels (1080x1920) at 30fps or 60fps.
- [ ] **Smooth Transitions**: No harsh static cuts unless intentional. Crossfades (`fadein`, `fadeout`) between scenes.
- [ ] **Visual Dynamics**: Every frame has subtle continuous motion (particle drift, slow zoom, pulsating gradient, typing text).
- [ ] **Color Harmony**: Use cohesive color palettes (e.g., Dark Mode Cyberpunk, Clean Swiss Pastel, Corporate Navy & Gold).
- [ ] **Audio Balance**: Narration voice is crisp and clear; background music sits under narration at 10-20% volume.
