document.addEventListener('DOMContentLoaded', () => {
  const promptInput = document.getElementById('promptInput');
  const aspectRatioSelect = document.getElementById('aspectRatioSelect');
  const durationSelect = document.getElementById('durationSelect');
  const fpsSelect = document.getElementById('fpsSelect');
  const resolutionSelect = document.getElementById('resolutionSelect');
  const generateBtn = document.getElementById('generateBtn');
  const btnText = document.getElementById('btnText');
  const btnSpinner = document.getElementById('btnSpinner');

  const mainVideoPlayer = document.getElementById('mainVideoPlayer');
  const videoSource = document.getElementById('videoSource');
  const playerPlaceholder = document.getElementById('playerPlaceholder');
  const videoTitle = document.getElementById('videoTitle');
  const videoMetaSpecs = document.getElementById('videoMetaSpecs');

  const codeDisplay = document.getElementById('codeDisplay');
  const logsDisplay = document.getElementById('logsDisplay');
  const historyGrid = document.getElementById('historyGrid');

  const copyCodeBtn = document.getElementById('copyCodeBtn');
  const renderCustomBtn = document.getElementById('renderCustomBtn');

  let currentVideoData = null;

  // Preset prompt handler
  document.querySelectorAll('.tag-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const presetPrompt = btn.getAttribute('data-prompt');
      if (presetPrompt) {
        promptInput.value = presetPrompt;
      }
    });
  });

  // Tab switching
  document.querySelectorAll('.tab-btn').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.tab-btn').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

      tab.classList.add('active');
      const targetId = tab.getAttribute('data-tab');
      document.getElementById(targetId).classList.add('active');
    });
  });

  // Generate Video API call
  generateBtn.addEventListener('click', async () => {
    const prompt = promptInput.value.trim();
    if (!prompt) {
      alert('请填写视频 Prompt 描述！');
      return;
    }

    setLoading(true);
    clearLogs();
    addLog(`[System] Initializing AI API video generation call...`);
    addLog(`[Prompt] "${prompt}"`);

    try {
      const payload = {
        prompt: prompt,
        aspect_ratio: aspectRatioSelect.value,
        duration: parseFloat(durationSelect.value),
        fps: parseInt(fpsSelect.value, 10),
        resolution: resolutionSelect.value
      };

      addLog(`[API Request] Sending specs: ${payload.aspect_ratio}, ${payload.duration}s @ ${payload.fps}fps...`);

      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await response.json();

      if (data.status === 'completed') {
        currentVideoData = data;
        displayVideo(data);
        if (data.logs) {
          data.logs.forEach(msg => addLog(`[Engine] ${msg}`));
        }
        addLog(`[Success] Video rendering completed in ${data.elapsed_seconds}s!`);
        loadHistory();
      } else {
        addLog(`[Error] Generation failed: ${data.error || 'Unknown error'}`, true);
        alert(`视频生成失败: ${data.error || '请检查后端日志'}`);
      }
    } catch (err) {
      console.error(err);
      addLog(`[Network Error] API connection error: ${err.message}`, true);
      alert('无法连接后端 API，请确认服务器已启动。');
    } finally {
      setLoading(false);
    }
  });

  // Copy code
  copyCodeBtn.addEventListener('click', () => {
    if (!codeDisplay.textContent) return;
    navigator.clipboard.writeText(codeDisplay.textContent);
    alert('AI 生成的代码已复制到剪贴板！');
  });

  // Render Custom Code
  renderCustomBtn.addEventListener('click', async () => {
    const code = codeDisplay.textContent.trim();
    if (!code) return;

    setLoading(true);
    addLog(`[Custom Code] Re-executing updated code...`);

    try {
      const payload = {
        prompt: promptInput.value || "Custom Code Render",
        aspect_ratio: aspectRatioSelect.value,
        duration: parseFloat(durationSelect.value),
        fps: parseInt(fpsSelect.value, 10),
        resolution: resolutionSelect.value,
        custom_code: code
      };

      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await response.json();
      if (data.status === 'completed') {
        displayVideo(data);
        addLog(`[Success] Custom code executed successfully in ${data.elapsed_seconds}s!`);
        loadHistory();
      } else {
        addLog(`[Error] Custom code execution error: ${data.error}`, true);
      }
    } catch (err) {
      addLog(`[Error] Execution failed: ${err.message}`, true);
    } finally {
      setLoading(false);
    }
  });

  function displayVideo(item) {
    if (item.video_url) {
      videoSource.src = item.video_url;
      mainVideoPlayer.load();
      mainVideoPlayer.play().catch(() => {});

      mainVideoPlayer.style.display = 'block';
      playerPlaceholder.style.display = 'none';

      videoTitle.textContent = item.prompt;
      videoMetaSpecs.textContent = `${item.width}x${item.height} • ${item.duration}s • ${item.fps}fps • Render time: ${item.elapsed_seconds}s`;
    }

    codeDisplay.textContent = item.code || '# Code not available';
  }

  function setLoading(loading) {
    generateBtn.disabled = loading;
    if (loading) {
      btnText.textContent = 'AI 代码编译 & 视频渲染中...';
      btnSpinner.style.display = 'inline-block';
    } else {
      btnText.textContent = '✨ 调用 API 生成 AI 视频';
      btnSpinner.style.display = 'none';
    }
  }

  function addLog(msg, isError = false) {
    const time = new Date().toLocaleTimeString();
    const entry = document.createElement('div');
    entry.className = `log-entry ${isError ? 'error' : ''}`;
    entry.innerHTML = `<span style="color:#6b7280;">[${time}]</span> <span>${msg}</span>`;
    logsDisplay.appendChild(entry);
    logsDisplay.scrollTop = logsDisplay.scrollHeight;
  }

  function clearLogs() {
    logsDisplay.innerHTML = '';
  }

  // Load History Gallery
  async function loadHistory() {
    try {
      const res = await fetch('/api/history');
      const history = await res.json();

      historyGrid.innerHTML = '';
      if (!history || history.length === 0) {
        historyGrid.innerHTML = '<div style="color:var(--text-muted); padding:20px;">尚无历史生成视频。输入 Prompt 开始创建！</div>';
        return;
      }

      history.forEach(item => {
        const card = document.createElement('div');
        card.className = 'history-card';
        card.innerHTML = `
          <video class="card-video-preview" src="${item.video_url}" muted loop onmouseenter="this.play()" onmouseleave="this.pause()"></video>
          <div class="card-body">
            <div class="card-prompt">${escapeHtml(item.prompt)}</div>
            <div class="card-meta">
              <span>${item.aspect_ratio} • ${item.duration}s</span>
              <span>${item.created_at}</span>
            </div>
          </div>
        `;
        card.addEventListener('click', () => {
          promptInput.value = item.prompt;
          displayVideo(item);
          window.scrollTo({ top: 0, behavior: 'smooth' });
        });
        historyGrid.appendChild(card);
      });
    } catch (err) {
      console.error('Error loading history:', err);
    }
  }

  function escapeHtml(text) {
    return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  // Initial history load
  loadHistory();
});
