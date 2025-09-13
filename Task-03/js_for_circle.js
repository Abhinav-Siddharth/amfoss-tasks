const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const scoreDisplay = document.getElementById('score-display');
const bestScoreDisplay = document.getElementById('best-score');
const errorMsg = document.getElementById('error-msg');
const resetBtn = document.getElementById('reset-btn');
const modeSelect = document.getElementById('mode-select');
const themeToggle = document.getElementById('theme-toggle');
const drawSound = document.getElementById('draw-sound');

let isDrawing = false;
let points = [];
let startTime;
let centerX = canvas.width / 2;
let centerY = canvas.height / 2;
let bestScore = sessionStorage.getItem('bestScore') || 0;
bestScoreDisplay.textContent = `Best Score: ${bestScore}%`;

let currentMode = 'medium';
let dotSize = 10;
let tolerance = 0.2;

function drawCenterDot() {
    ctx.beginPath();
    ctx.arc(centerX, centerY, dotSize, 0, 2 * Math.PI);
    ctx.fillStyle = 'red';
    ctx.fill();
}
drawCenterDot();

modeSelect.addEventListener('change', (e) => {
    currentMode = e.target.value;
    if (currentMode === 'easy') {
        dotSize = 20;
        tolerance = 0.3; 
    } else if (currentMode === 'medium') {
        dotSize = 10;
        tolerance = 0.2; 
    } else if (currentMode === 'hardcore') {
        dotSize = 5;
        tolerance = 0.12; 
    }
    resetCanvas();
});

themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    document.body.classList.toggle('light-mode');
    themeToggle.textContent = document.body.classList.contains('dark-mode') ? 'Toggle Light Mode' : 'Toggle Dark Mode';
});

canvas.addEventListener('mousedown', (e) => {
    isDrawing = true;
    points = [];
    errorMsg.textContent = '';
    startTime = Date.now();
    drawSound.play();
    
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    points.push({ x, y });
    
    ctx.beginPath();
    ctx.moveTo(x, y);
});

canvas.addEventListener('mousemove', (e) => {
    if (!isDrawing) return;
    
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    points.push({ x, y });
    
    ctx.lineTo(x, y);
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 2;
    ctx.stroke();
});

canvas.addEventListener('mouseup', () => {
    if (!isDrawing) return;
    isDrawing = false;
    drawSound.pause();
    drawSound.currentTime = 0;
    
    const endTime = Date.now();
    const drawTime = (endTime - startTime) / 1000;
    
    ctx.beginPath();
    ctx.moveTo(points[0].x, points[0].y);
    for (let i = 1; i < points.length; i++) {
        ctx.lineTo(points[i].x, points[i].y);
    }
    ctx.closePath();
    if (!ctx.isPointInPath(centerX, centerY)) {
        errorMsg.textContent = 'The red dot is not inside your circle!';
        return;
    }
    
    if (points.length < 20) {
        errorMsg.textContent = 'Draw a full circle!';
        return;
    }
  
    let distances = [];
    for (let point of points) {
        const dx = point.x - centerX;
        const dy = point.y - centerY;
        distances.push(Math.sqrt(dx * dx + dy * dy));
    }
    
    const avgRadius = distances.reduce((a, b) => a + b, 0) / distances.length;
    const avgDeviation = distances.reduce((sum, dist) => sum + Math.abs(dist - avgRadius), 0) / distances.length;
   
    let score = Math.max(0, 100 - (avgDeviation / avgRadius) * 150 / tolerance);
    
   
    const timeBonus = Math.max(0, 20 - drawTime * 4);
    score = Math.min(100, score + timeBonus);
    score = Math.round(score);
    
    scoreDisplay.textContent = `Score: ${score}%`;
    
    if (score > bestScore) {
        bestScore = score;
        sessionStorage.setItem('bestScore', bestScore);
        bestScoreDisplay.textContent = `Best Score: ${bestScore}%`;
    }
});

resetBtn.addEventListener('click', resetCanvas);

function resetCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawCenterDot();
    scoreDisplay.textContent = 'Score: --';
    errorMsg.textContent = '';
    points = [];
}
