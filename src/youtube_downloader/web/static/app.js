/**
 * YouTube Downloader - Main JavaScript
 * Day 5: 완전한 기능 구현
 */

// ========================================
// Global Variables
// ========================================

let currentTaskId = null;
let currentWebSocket = null;
let currentVideoInfo = null;

// ========================================
// DOM Elements
// ========================================

// Form elements
const downloadForm = document.getElementById('download-form');
const urlInput = document.getElementById('url-input');
const urlError = document.getElementById('url-error');
const qualitySelect = document.getElementById('quality-select');
const audioQualitySelect = document.getElementById('audio-quality-select');
const audioOnlyCheckbox = document.getElementById('audio-only');
const saveMetadataCheckbox = document.getElementById('save-metadata');
const saveThumbnailCheckbox = document.getElementById('save-thumbnail');
const downloadBtn = document.getElementById('download-btn');

// Preview elements
const videoPreviewSection = document.getElementById('video-preview-section');
const previewThumbnail = document.getElementById('preview-thumbnail');
const previewTitle = document.getElementById('preview-title');
const previewChannel = document.getElementById('preview-channel');
const previewDuration = document.getElementById('preview-duration');

// Progress elements
const progressSection = document.getElementById('progress-section');
const progressTitle = document.getElementById('progress-title');
const progressPercentage = document.getElementById('progress-percentage');
const progressFill = document.getElementById('progress-fill');
const progressSize = document.getElementById('progress-size');
const progressSpeed = document.getElementById('progress-speed');
const progressEta = document.getElementById('progress-eta');
const cancelBtn = document.getElementById('cancel-btn');

// Alert elements
const successSection = document.getElementById('success-section');
const successMessage = document.getElementById('success-message');
const downloadFileBtn = document.getElementById('download-file-btn');
const newDownloadBtn = document.getElementById('new-download-btn');

const errorSection = document.getElementById('error-section');
const errorMessage = document.getElementById('error-message');
const errorClose = document.getElementById('error-close');

// Theme toggle
const themeToggle = document.getElementById('theme-toggle');
const themeIcon = document.querySelector('.theme-icon');

// ========================================
// Dark Mode Toggle
// ========================================

const savedTheme = localStorage.getItem('theme') || 'light';
document.documentElement.setAttribute('data-theme', savedTheme);
updateThemeIcon(savedTheme);

themeToggle.addEventListener('click', () => {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
});

function updateThemeIcon(theme) {
    themeIcon.textContent = theme === 'dark' ? '☀️' : '🌙';
}

// ========================================
// URL Validation
// ========================================

let urlDebounceTimer;

urlInput.addEventListener('input', () => {
    clearTimeout(urlDebounceTimer);
    urlDebounceTimer = setTimeout(() => {
        const url = urlInput.value.trim();

        if (url) {
            if (isValidYouTubeUrl(url)) {
                urlInput.classList.remove('error');
                urlError.textContent = '';
                fetchVideoInfo(url);
            } else {
                urlInput.classList.add('error');
                urlError.textContent = '유효한 YouTube URL을 입력해주세요.';
                hideVideoPreview();
            }
        } else {
            urlInput.classList.remove('error');
            urlError.textContent = '';
            hideVideoPreview();
        }
    }, 500);
});

function isValidYouTubeUrl(url) {
    const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+$/;
    return youtubeRegex.test(url);
}

// ========================================
// Fetch Video Info
// ========================================

async function fetchVideoInfo(url) {
    try {
        downloadBtn.disabled = true;
        downloadBtn.querySelector('.btn-text').textContent = '정보 확인 중...';

        const response = await fetch(`/api/v1/video/info?url=${encodeURIComponent(url)}`);
        const data = await response.json();

        if (data.success && data.data) {
            currentVideoInfo = data.data;
            showVideoPreview(data.data);
            downloadBtn.disabled = false;
            downloadBtn.querySelector('.btn-text').textContent = '다운로드 시작';
        } else {
            throw new Error(data.error?.message || '동영상 정보를 가져올 수 없습니다.');
        }
    } catch (error) {
        console.error('Video info error:', error);
        showError(error.message || '동영상 정보를 가져오는 중 오류가 발생했습니다.');
        hideVideoPreview();
        downloadBtn.disabled = false;
        downloadBtn.querySelector('.btn-text').textContent = '다운로드 시작';
    }
}

function showVideoPreview(videoInfo) {
    previewThumbnail.src = videoInfo.thumbnail || '';
    previewTitle.textContent = videoInfo.title || 'Unknown';
    previewChannel.textContent = videoInfo.uploader || 'Unknown';
    previewDuration.textContent = formatDuration(videoInfo.duration || 0);

    videoPreviewSection.classList.remove('hidden');
}

function hideVideoPreview() {
    videoPreviewSection.classList.add('hidden');
    currentVideoInfo = null;
}

function formatDuration(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;

    if (hours > 0) {
        return `${hours}:${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    }
    return `${minutes}:${String(secs).padStart(2, '0')}`;
}

// ========================================
// Download Form Submit
// ========================================

downloadForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const url = urlInput.value.trim();

    if (!url || !isValidYouTubeUrl(url)) {
        showError('유효한 YouTube URL을 입력해주세요.');
        return;
    }

    // Prepare download options
    const options = {
        quality: qualitySelect.value,
        audio_quality: audioQualitySelect.value,
        audio_only: audioOnlyCheckbox.checked,
        save_metadata: saveMetadataCheckbox.checked,
        save_thumbnail: saveThumbnailCheckbox.checked
    };

    try {
        downloadBtn.disabled = true;
        downloadBtn.querySelector('.btn-text').textContent = '시작 중...';

        // Start download
        const response = await fetch('/api/v1/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url, options })
        });

        const data = await response.json();

        if (data.success && data.data) {
            currentTaskId = data.data.task_id;
            connectWebSocket(currentTaskId);
            showProgress();
            hideVideoPreview();
        } else {
            throw new Error(data.error?.message || '다운로드를 시작할 수 없습니다.');
        }
    } catch (error) {
        console.error('Download start error:', error);
        showError(error.message || '다운로드를 시작하는 중 오류가 발생했습니다.');
        downloadBtn.disabled = false;
        downloadBtn.querySelector('.btn-text').textContent = '다운로드 시작';
    }
});

// ========================================
// WebSocket Connection
// ========================================

function connectWebSocket(taskId) {
    const wsUrl = `ws://${window.location.host}/ws/download/${taskId}`;
    currentWebSocket = new WebSocket(wsUrl);

    currentWebSocket.onopen = () => {
        console.log('WebSocket connected');
    };

    currentWebSocket.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            handleWebSocketMessage(data);
        } catch (error) {
            console.error('WebSocket message parse error:', error);
        }
    };

    currentWebSocket.onerror = (error) => {
        console.error('WebSocket error:', error);
        showError('실시간 연결 오류가 발생했습니다.');
    };

    currentWebSocket.onclose = () => {
        console.log('WebSocket disconnected');
    };
}

function handleWebSocketMessage(data) {
    const { type, data: msgData } = data;

    switch (type) {
        case 'progress':
            updateProgress(msgData);
            break;
        case 'status':
            updateStatus(msgData);
            break;
        case 'complete':
            handleComplete(msgData);
            break;
        case 'error':
            handleError(msgData);
            break;
        default:
            console.log('Unknown message type:', type);
    }
}

// ========================================
// Progress Updates
// ========================================

function showProgress() {
    progressSection.classList.remove('hidden');
    successSection.classList.add('hidden');
    errorSection.classList.add('hidden');
}

function updateProgress(data) {
    const { percentage, downloaded_bytes, total_bytes, speed, eta } = data;

    progressPercentage.textContent = `${percentage}%`;
    progressFill.style.width = `${percentage}%`;

    progressSize.textContent = `${formatBytes(downloaded_bytes)} / ${formatBytes(total_bytes)}`;
    progressSpeed.textContent = speed || '0 MB/s';
    progressEta.textContent = `남은 시간: ${eta || '--:--'}`;
}

function updateStatus(data) {
    const { status, message } = data;
    progressTitle.textContent = message || `${status}...`;
}

function handleComplete(data) {
    const { filename, size, download_url } = data;

    // Close WebSocket
    if (currentWebSocket) {
        currentWebSocket.close();
        currentWebSocket = null;
    }

    // Hide progress
    progressSection.classList.add('hidden');

    // Show success
    successMessage.textContent = `${filename} (${formatBytes(size)})`;
    successSection.classList.remove('hidden');

    // Setup download button
    downloadFileBtn.onclick = () => {
        window.location.href = download_url;
    };

    // Reset form
    downloadBtn.disabled = false;
    downloadBtn.querySelector('.btn-text').textContent = '다운로드 시작';
}

function handleError(data) {
    const { code, message } = data;

    // Close WebSocket
    if (currentWebSocket) {
        currentWebSocket.close();
        currentWebSocket = null;
    }

    // Hide progress
    progressSection.classList.add('hidden');

    // Show error
    showError(`[${code}] ${message}`);

    // Reset form
    downloadBtn.disabled = false;
    downloadBtn.querySelector('.btn-text').textContent = '다운로드 시작';
}

// ========================================
// Cancel Download
// ========================================

cancelBtn.addEventListener('click', () => {
    if (currentWebSocket) {
        currentWebSocket.close();
        currentWebSocket = null;
    }

    progressSection.classList.add('hidden');
    downloadBtn.disabled = false;
    downloadBtn.querySelector('.btn-text').textContent = '다운로드 시작';

    showError('다운로드가 취소되었습니다.');
});

// ========================================
// New Download
// ========================================

newDownloadBtn.addEventListener('click', () => {
    successSection.classList.add('hidden');
    urlInput.value = '';
    urlInput.focus();
    hideVideoPreview();
});

// ========================================
// Error Handling
// ========================================

function showError(message) {
    errorMessage.textContent = message;
    errorSection.classList.remove('hidden');
}

errorClose.addEventListener('click', () => {
    errorSection.classList.add('hidden');
});

// ========================================
// Utility Functions
// ========================================

function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// ========================================
// Initialize
// ========================================

console.log('YouTube Downloader - Ready!');
console.log('API Docs: http://localhost:8000/docs');
