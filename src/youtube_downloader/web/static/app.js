/**
 * YouTube Downloader - Main JavaScript
 * Day 4: 다크 모드 토글만 구현
 * Day 5: API 통신 및 WebSocket 로직 구현 예정
 */

// ========================================
// Dark Mode Toggle
// ========================================

const themeToggle = document.getElementById('theme-toggle');
const themeIcon = document.querySelector('.theme-icon');

// 저장된 테마 불러오기
const savedTheme = localStorage.getItem('theme') || 'light';
document.documentElement.setAttribute('data-theme', savedTheme);
updateThemeIcon(savedTheme);

// 테마 토글 이벤트
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
// Day 5에서 구현할 기능들
// ========================================

/*
TODO Day 5:
1. URL 입력 및 유효성 검사
2. 동영상 정보 조회 (GET /api/v1/video/info)
3. 미리보기 표시
4. 다운로드 시작 (POST /api/v1/download)
5. WebSocket 연결 및 실시간 진행률 업데이트
6. 파일 다운로드
7. 에러 처리
*/

console.log('YouTube Downloader - Day 4 UI Complete');
console.log('API Docs: http://localhost:8000/docs');
console.log('WebSocket Test: http://localhost:8000/static/test_ws.html');
