---
name: python-video-generation
description: 指导 AI 大模型通过编写 Python 代码（使用 moviepy, Pillow, gTTS, OpenCV, numpy 等）生成媲美 Runway, Sora, Pika 等 AI 视频生成模型的精美、带声效缓动动画与专业排版的视频。
---

# Skill: Python Programmatic Video Generation (High-Quality AI-Grade Output)

This skill guide enables an AI agent or LLM assistant to write Python code (using `moviepy`, `Pillow`, `gTTS`, `opencv-python`, `numpy`, `librosa`, etc.) to programmatically generate professional, visually rich, dynamic videos with custom typography, smooth easing animations, and synchronized audio.

---

## 📖 使用说明 (Usage Instructions)

### 1. 适用场景 (When to Use)
- **AI Agent / 大模型 Prompt 注入**：将本 Skill 内容作为 Context 或 Tool 指引，使 AI 具备自动生成与渲染短视频 Python 脚本的能力。
- **自动化视频生成管线**：用于批量生成产品宣介、新闻简报、知识科普、数据可视化等精美视频。

### 2. 使用流程 (How to Apply)
1. **解析 Prompt**：分析主题、分镜（Scene Breakdown）、旁白文本、视觉风格与时长。
2. **构建视觉与动画**：使用 Pillow/OpenCV 绘制逐帧/卡片与图层，使用 Numpy 实现缓动函数（Easing Curves）。
3. **音频生成与 Ducking**：使用 gTTS 生成语音旁白，计算时长并叠加背景音乐（BGM Audio Ducking）。
4. **MoviePy 合成与渲染**：组合背景图层、主视觉卡片、缓动字幕与音频轨，导出 1080p 高清 MP4 视频。

---

## 🎨 视觉设计规范与参数定义 (Visual Design Specifications)

| 参数项 | 标准配置 / 推荐值 | 说明 |
| :--- | :--- | :--- |
| **分辨率 (Resolution)** | `1920x1080` (横屏 16:9) / `1080x1920` (竖屏 9:16) | 建议全局统一定义 `WIDTH` 和 `HEIGHT` 常量 |
| **帧率 (FPS)** | 30 FPS (标准) / 60 FPS (高流畅动画) | 兼顾渲染速度与流畅度 |
| **主配色方案 (Color Palette)** | **Dark Cyber**: Background `#0F172A`, Accent `#38BDF8`, Text `#F8FAFC`<br>**Clean Pastel**: Background `#F8FAFC`, Accent `#6366F1`, Text `#0F172A` | 采用高对比度、具备现代感调色 |
| **字体与排版 (Typography)** | 标题: 36-60pt Bold; 正文: 24-32pt Regular | 使用 Pillow 渲染时需配置备用字体（如 Arial / DejaVuSans / NotoSansSC） |
| **卡片与边框 (Glassmorphic)** | 填充色 `(255, 255, 255, 180)`, 描边 `(255, 255, 255, 220)`, 圆角 `30px` | 毛玻璃质感背景卡片，增加视觉层次 |

---

## 📐 缓动动画数学公式 (Easing Functions Implementation)

动画切忌线性平移（Linear Interpolation）。所有位置、缩放、透明度变化必须使用缓动函数。

```python
import numpy as np

def ease_out_cubic(t: float) -> float:
    """t 从 0.0 到 1.0；减速缓出，适用于元素进入画面"""
    t = np.clip(t, 0.0, 1.0)
    return float(1.0 - pow(1.0 - t, 3))

def ease_in_out_sine(t: float) -> float:
    """平滑 S 型过渡，适用于柔和呼吸或位移"""
    t = np.clip(t, 0.0, 1.0)
    return float(-(np.cos(np.pi * t) - 1.0) / 2.0)

def ease_out_back(t: float, c1: float = 1.70158, c3: float = 2.70158) -> float:
    """带轻微回弹效果的缓出，适用于标题与卡片弹入"""
    t = np.clip(t, 0.0, 1.0)
    return float(1.0 + c3 * pow(t - 1.0, 3) + c1 * pow(t - 1.0, 2))
```

---

## 🖼️ 动态图像与卡片渲染 (PIL / OpenCV Graphics)

为了规避 MoviePy 对 ImageMagick 的依赖，建议使用 Pillow 绘制带排版、圆角、阴影的图像作为 `ImageClip` 或 `VideoClip` 图层。

```python
from PIL import Image, ImageDraw, ImageFont
import textwrap

def draw_text_card(
    title: str,
    body: str,
    width: int = 1200,
    height: int = 600,
    bg_color=(15, 23, 42, 230),
    accent_color=(56, 189, 248, 255),
    text_color=(248, 250, 252, 255)
) -> Image.Image:
    """生成具备高质感与自动换行的标题内容卡片"""
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 绘制毛玻璃/圆角卡片背景
    draw.rounded_rectangle([(0, 0), (width - 1, height - 1)], radius=24, fill=bg_color, outline=accent_color, width=3)

    # 顶部装饰线
    draw.line([(40, 50), (120, 50)], fill=accent_color, width=6)

    # 绘制标题
    try:
        title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 48)
        body_font = ImageFont.truetype("DejaVuSans.ttf", 28)
    except IOError:
        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()

    draw.text((40, 80), title, font=title_font, fill=accent_color)

    # 自动换行正文
    wrapped_lines = textwrap.wrap(body, width=50)
    y_text = 170
    for line in wrapped_lines:
        draw.text((40, y_text), line, font=body_font, fill=text_color)
        y_text += 40

    return img
```

---

## 🎙️ 音频合成与 Audio Ducking 混音

处理旁白（TTS）与背景音乐（BGM）时，必须在语音播放期间对 BGM 进行自动降噪/降音（Audio Ducking）。

```python
from gtts import gTTS
import os
from moviepy.editor import AudioFileClip, CompositeAudioClip, afx

def build_audio_track(speech_text: str, bgm_path: str = None) -> tuple:
    """生成 TTS 音频并与背景音乐混音，返回 (总时长, CompositeAudioClip)"""
    tts_filename = "temp_voice.mp3"
    tts = gTTS(text=speech_text, lang="en")
    tts.save(tts_filename)

    voice_clip = AudioFileClip(tts_filename)
    duration = voice_clip.duration + 1.5 # 留出 1.5s 尾部余量

    tracks = [voice_clip.set_start(0.5).volumex(1.0)]

    if bgm_path and os.path.exists(bgm_path):
        bgm_clip = AudioFileClip(bgm_path).subclip(0, duration)
        # 语音期间降音至 15%
        bgm_clip = bgm_clip.volumex(0.15)
        tracks.insert(0, bgm_clip)

    final_audio = CompositeAudioClip(tracks)
    return duration, final_audio
```

---

## 🚀 完整可执行 Python 脚本示例 (End-to-End Pipeline)

以下为完整可运行的脚本模板，演示如何一步生成带渐变背景、缓动卡片进入、旁白语音与字幕合成的专业视频：

```python
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
from moviepy.editor import (
    ImageClip,
    CompositeVideoClip,
    AudioFileClip,
    CompositeAudioClip,
    ColorClip
)

# 1. 常量定义
WIDTH, HEIGHT = 1920, 1080
FPS = 30
OUTPUT_FILE = "output_presentation.mp4"

# 2. 缓动函数定义
def ease_out_back(t: float, c1=1.70158, c3=2.70158) -> float:
    t = np.clip(t, 0.0, 1.0)
    return float(1.0 + c3 * pow(t - 1.0, 3) + c1 * pow(t - 1.0, 2))

# 3. 动态绘制渐变背景帧
def create_gradient_background(w=WIDTH, h=HEIGHT) -> np.ndarray:
    base = Image.new("RGB", (w, h), "#0F172A")
    draw = ImageDraw.Draw(base)
    # 绘制柔和渐变圆圈
    draw.ellipse([w//2 - 400, h//2 - 400, w//2 + 400, h//2 + 400], fill="#1E1B4B")
    draw.ellipse([w - 600, -100, w + 200, 700], fill="#0284C7")
    return np.array(base)

# 4. 绘制前景文本卡片
def create_card_image(title_text: str, desc_text: str) -> np.ndarray:
    card = Image.new("RGBA", (1200, 500), (0, 0, 0, 0))
    draw = ImageDraw.Draw(card)
    # 绘制卡片底色与描边
    draw.rounded_rectangle([(0, 0), (1199, 499)], radius=30, fill=(15, 23, 42, 220), outline=(56, 189, 248, 255), width=3)

    try:
        title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 42)
        body_font = ImageFont.truetype("DejaVuSans.ttf", 26)
    except IOError:
        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()

    draw.text((60, 60), title_text, font=title_font, fill=(56, 189, 248, 255))
    draw.text((60, 150), desc_text, font=body_font, fill=(241, 245, 249, 255))
    return np.array(card)

def generate_video():
    speech_text = "Welcome to programmatic video generation using Python. This method delivers smooth animations, dynamic layouts, and exact timing."

    # A. 生成旁白音频
    tts_file = "temp_speech.mp3"
    gTTS(text=speech_text, lang="en").save(tts_file)
    voice_audio = AudioFileClip(tts_file)
    total_duration = voice_audio.duration + 2.0

    # B. 创建背景图层 (Ken Burns 微放大动效)
    bg_img = create_gradient_background()
    bg_clip = ImageClip(bg_img).set_duration(total_duration)

    def bg_transform(get_frame, t):
        # 0% - 5% 缓慢放大
        scale = 1.0 + 0.05 * (t / total_duration)
        frame = get_frame(t)
        # 返回基础帧
        return frame

    bg_clip = bg_clip.fl(bg_transform)

    # C. 创建卡片动效图层
    card_img = create_card_image(
        "Python Programmatic Video Engine",
        "• High-precision typography\n• Easing motion graphics\n• Multi-track audio ducking\n• No ImageMagick dependency required"
    )
    card_clip = ImageClip(card_img).set_duration(total_duration - 0.5).set_start(0.5)

    # 卡片弹出缓动动画：Y 轴上升位移 + 透明度淡入
    card_start_y = HEIGHT
    card_target_y = (HEIGHT - 500) // 2
    anim_duration = 1.0

    def card_pos(t):
        if t < 0.5:
            return ("center", HEIGHT)
        rel_t = (t - 0.5) / anim_duration
        if rel_t >= 1.0:
            return ("center", card_target_y)
        progress = ease_out_back(rel_t)
        current_y = card_start_y - (card_start_y - card_target_y) * progress
        return ("center", current_y)

    card_clip = card_clip.set_position(card_pos)

    # D. 合成视频轨与音频轨
    video = CompositeVideoClip([bg_clip, card_clip], size=(WIDTH, HEIGHT))
    audio = CompositeAudioClip([voice_audio.set_start(0.5)])
    video = video.set_audio(audio)

    # E. 导出渲染
    video.write_videofile(
        OUTPUT_FILE,
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        preset="medium"
    )

    # 清理临时音频
    voice_audio.close()
    if os.path.exists(tts_file):
        os.remove(tts_file)

if __name__ == "__main__":
    generate_video()
```

---

## 🛠️ 排错与性能优化指南 (Troubleshooting & Best Practices)

1. **避免 ImageMagick 依赖**：MoviePy 的 `TextClip` 依赖系统环境中的 ImageMagick。优先使用 `Pillow` 绘制文本与卡片，再转换为 `ImageClip`，可确保在任何 Linux/Docker 环境中无缝运行。
2. **MoviePy v1 vs v2 兼容性**：
   - MoviePy v1: `from moviepy.editor import ImageClip`, `clip.volumex(0.5)`
   - MoviePy v2: `from moviepy.video.io.VideoFileClip import VideoFileClip`, `clip.with_volume_scaled(0.5)`
3. **内存与渲染速度**：
   - 避免生成巨大尺寸的中间 Numpy 数组。
   - 使用 `preset="fast"` 或 `preset="medium"` 权衡渲染耗时与压缩率。
   - 设置合理的 `FPS`（30fps 足以提供流畅视觉体验）。
