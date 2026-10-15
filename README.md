# 🎬 代码驱动型 AI 视频生成平台 (AI CodeStudio)

本项目是一个在网页端通过调用 API 让 AI **用代码生成视频** 的 Web 系统。

AI 模型本身不直接输出二进制视频，而是通过生成高度优化的 **Python 动态渲染代码** (基于 OpenCV、PIL、NumPy)，在服务端沙箱中实时编译并渲染出逼真、富有影院光影特效与镜头运镜的 MP4 视频。

---

## ✨ 项目特性

- **代码合成视频引擎**：将 Prompt 语义转译为包含粒子系统、体积光照、3D 镜头拉近/运镜、色彩渐变与光影渲染的 Python 脚本。
- **现代化 Web UI 界面**：采用类 Sora / Runway / Gen-2 暗黑风格 UI 设计，包含快捷 Prompt 预设、画幅比例 (16:9/9:16/1:1)、时长、帧率与分辨率选择。
- **代码透明与可二次编辑**：提供“AI 生成的代码”查看标签页，支持一键复制代码或修改 Python 代码后重新编译渲染。
- **控制台实时日志**：展示 Prompt 解析、代码生成、帧渲染与 MP4 编码全过程日志。
- **作品画廊 (History)**：自动保存生成的历史视频，支持预览与快速载入。

---

## 🚀 快速开始与使用说明

### 1. 安装依赖

确保已安装 Python 3.10+ 及 `ffmpeg`：

```bash
# Ubuntu / Debian
sudo apt-get update && sudo apt-get install -y ffmpeg

# 安装 Python 依赖包
pip install -r requirements.txt
# 或者直接安装：
pip install fastapi uvicorn moviepy pillow numpy opencv-python-headless requests
```

### 2. 启动 Web 服务

在项目根目录运行以下命令启动 FastAPI 后端服务：

```bash
python3 -m uvicorn backend.server:app --host 0.0.0.0 --port 8000
```

启动成功后，在浏览器打开：
👉 **`http://localhost:8000`**

---

## 💡 使用步骤

1. **输入 Prompt 描述**：在网页左侧文本框输入想要生成的视频画面（例如：“赛博朋克霓虹城市”、“宇宙银河星云”、“日落海洋波浪”），也可以点击快捷标签预设。
2. **选择视频参数**：
   - 画幅比例：16:9 宽屏、9:16 竖屏、1:1 正方形
   - 时长：2秒、4秒、6秒、8秒
   - 帧率：15fps、30fps、60fps
   - 分辨率：720p / 1080p
3. **生成视频**：点击 **“✨ 调用 API 生成 AI 视频”** 按钮。
4. **播放与代码审查**：
   - **视频播放器** 标签页可实时播放生成的 MP4 视频。
   - **AI 生成的代码** 标签页可查看生成该视频的完整 Python 渲染源码。
   - **控制台日志** 标签页可查看实时编译渲染进度。

---

## 📡 API 接口说明

- `POST /api/generate`：发送 Prompt 生成视频代码并渲染 MP4 文件。
- `GET /api/history`：获取已生成的历史视频列表。
- `GET /api/videos/{id}`：获取指定视频元数据。
- `GET /api/code/{id}`：获取指定视频对应的 Python 源码。

---

## 🧪 运行单元测试

运行项目自动化测试：

```bash
python3 -m unittest discover -s tests
```
