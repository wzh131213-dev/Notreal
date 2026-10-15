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
2. **AI 读取 Skill 规范**：AI 按照本 Skill 中的分层设计、缓动函数（Easing）、卡片质感（Glassmorphism）与 Audio Ducking 音频混音原则，规划视频时间轴。
3. **生成并执行 Python 代码**：AI 输出完整且可直接运行的 Python 脚本，使用 `moviepy`/`Pillow`/`gTTS` 等库合成 `.mp4` 视频文件。
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

## 🎨 Design Principles for "AI-Grade" Visual Appeal

To achieve visual quality that rivals direct video AI outputs:

1. **Easing Functions over Linear Motion**:
   Always apply easing curves (e.g., `ease_out_cubic`, `ease_in_out_sine`) to position, scale, opacity, and rotation transforms instead of linear interpolation.
2. **Layered Depth & Parallax**:
   Organize frames into distinct layers:
   - **Background**: Soft gradients, animated procedural patterns, Bokeh lights, ambient particles.
   - **Midground**: Hero assets, vector illustrations, glassmorphic cards, dynamic charts, main subjects.
   - **Foreground**: Vignette overlays, lighting leaks, kinetic typography, floating micro-elements.
3. **Typography & Styling**:
   - Use high-quality web/modern fonts (e.g., Inter, Montserrat, Roboto, Fira Code).
   - Apply subtle drop shadows, stroke outlines, glassmorphism (semi-transparent blurred cards), and gradient text fills.
4. **Cinematic Motion**:
   - Continuous gentle camera motion (e.g., "Ken Burns effect" - slow subtle zoom and drift).
   - Dynamic entrance/exit animations (slide in with bounce, fade scale in, typewriter text effect).
5. **Polished Audio Design**:
   - Synchronize voiceover with kinetic text subtitles.
   - Background music with automatic audio ducking (lower BGM volume when voiceover speaks).
   - Subtle sound effects (whoosh, pop, click) at visual keyframes.

---

## 📐 Reusable Code Patterns & Boilerplate

### 1. Easing Functions (Smooth Animations)

```python
import numpy as np

def ease_out_cubic(t: float) -> float:
    """t ranges from 0.0 to 1.0"""
    return 1 - pow(1 - t, 3)

def ease_in_out_sine(t: float) -> float:
    return -(np.cos(np.pi * t) - 1) / 2

def ease_out_back(t: float, c1=1.70158, c3=2.70158) -> float:
    return 1 + c3 * pow(t - 1, 3) + c1 * pow(t - 1, 2)
```

### 2. Ken Burns Effect (Subtle Zoom & Pan with MoviePy)

```python
from moviepy.editor import ImageClip

def make_ken_burns_clip(image_path: str, duration: float, scale_start=1.0, scale_end=1.15):
    """Creates a smooth Ken Burns pan-and-zoom effect on a static image."""
    clip = ImageClip(image_path).set_duration(duration)

    def transform(get_frame, t):
        progress = t / duration
        # Smooth easing
        s = scale_start + (scale_end - scale_start) * (1 - pow(1 - progress, 2))
        frame = get_frame(t)
        # Apply scaling via resize callback or PIL transformation
        return frame # Custom frame resize logic

    return clip
```

### 3. Glassmorphism Card Frame Generator (Pillow)

```python
from PIL import Image, ImageDraw, ImageFilter

def create_glass_card(width=800, height=500, radius=30, bg_blur=15, opacity=180):
    """Generates a modern glassmorphic rounded card overlay."""
    card = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(card)

    # Rounded rectangle with semi-transparent white fill and light border
    draw.rounded_rectangle(
        [(0, 0), (width - 1, height - 1)],
        radius=radius,
        fill=(255, 255, 255, opacity),
        outline=(255, 255, 255, 220),
        width=2
    )
    return card
```

### 4. Audio Synthesis and Ducking Workflow

```python
from gtts import gTTS
from moviepy.editor import AudioFileClip, CompositeAudioClip, afx

def generate_voiceover_and_bgm(text: str, bgm_path: str, output_audio_path: str):
    # 1. Generate Voiceover TTS
    tts = gTTS(text=text, lang='en')
    tts.save("temp_speech.mp3")

    voice_clip = AudioFileClip("temp_speech.mp3")

    # 2. Load BGM and apply ducking (volume reduction during speech)
    bgm_clip = AudioFileClip(bgm_path).subclip(0, voice_clip.duration + 2)
    bgm_clip = bgm_clip.volumex(0.15) # Ducked BGM volume
    voice_clip = voice_clip.volumex(1.0)

    # 3. Composite
    final_audio = CompositeAudioClip([bgm_clip, voice_clip.set_start(0.5)])
    return voice_clip.duration + 2, final_audio
```

---

## 🚀 Step-by-Step Workflow for AI Code Generation

When an AI model is tasked with creating a video using Python code, follow these steps:

1. **Scripting & Scene Breakdown**:
   - Divide prompt into timed scenes/segments (e.g., Intro 0-3s, Scene 1 3-8s, Outro 8-10s).
   - Write speech narration text for each scene.

2. **Asset Pre-generation / Procedural Setup**:
   - Generate TTS audio files for scene voiceovers.
   - Use `Pillow` or `OpenCV` to draw dynamic frames, textures, particle animations, gradient backgrounds.

3. **Motion Animation Construction**:
   - Define clips using `MoviePy` or `Manim`.
   - Apply custom motion functions (`position`, `resize`, `opacity` animations using easing mathematical formulas).

4. **Composition & Audio Sync**:
   - Composite layers (`CompositeVideoClip`) ordering Background -> Visual Elements -> Text Overlay -> Lower Thirds.
   - Sync scene video durations exact to audio clip durations.

5. **Final Render**:
   - Render with H.264 codec (`libx264`), AAC audio (`aac`), specified fps (e.g., 30 or 60 fps), preset `medium` or `fast` for optimal balance.

---

## 🌟 Quality Checklist for Video Outputs

- [ ] **Frame Rate & Resolution**: Target 1080p (1920x1080) or Vertical Shorts/Reels (1080x1920) at 30fps or 60fps.
- [ ] **Smooth Transitions**: No harsh static cuts unless intentional. Crossfades (`fadein`, `fadeout`) between scenes.
- [ ] **Visual Dynamics**: Every frame has subtle continuous motion (particle drift, slow zoom, pulsating gradient, typing text).
- [ ] **Color Harmony**: Use cohesive color palettes (e.g., Dark Mode Cyberpunk, Clean Swiss Pastel, Corporate Navy & Gold).
- [ ] **Audio Balance**: Narration voice is crisp and clear; background music sits under narration at 10-20% volume.
