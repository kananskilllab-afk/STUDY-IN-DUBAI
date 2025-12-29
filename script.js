// Presentation Controller
let currentSlide = 1;
const totalSlides = 14;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    updateSlideCounter();
    updateProgressBar();
    setupEventListeners();
});

// Event Listeners
function setupEventListeners() {
    // Check if buttons exist before adding listeners
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');

    if (prevBtn) prevBtn.addEventListener('click', () => navigateSlide(-1));
    if (nextBtn) nextBtn.addEventListener('click', () => navigateSlide(1));

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft') navigateSlide(-1);
        if (e.key === 'ArrowRight') navigateSlide(1);
        if (e.key === ' ') {
            e.preventDefault();
            navigateSlide(1);
        }
    });
}

// Navigation
function navigateSlide(direction) {
    const newSlide = currentSlide + direction;
    if (newSlide >= 1 && newSlide <= totalSlides) {
        goToSlide(newSlide);
    }
}

function goToSlide(slideNumber) {
    document.querySelectorAll('.slide').forEach(slide => {
        slide.classList.remove('active');
    });

    const targetSlide = document.querySelector(`[data-slide="${slideNumber}"]`);
    if (targetSlide) {
        targetSlide.classList.add('active');
        currentSlide = slideNumber;
        updateSlideCounter();
        updateProgressBar();

        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

function updateSlideCounter() {
    const currentSlideEl = document.getElementById('currentSlide');
    const totalSlidesEl = document.getElementById('totalSlides');
    if (currentSlideEl) currentSlideEl.textContent = currentSlide;
    if (totalSlidesEl) totalSlidesEl.textContent = totalSlides;
}

function updateProgressBar() {
    const progressBar = document.getElementById('progressBar');
    if (progressBar) {
        const progress = (currentSlide / totalSlides) * 100;
        progressBar.style.width = `${progress}%`;
    }
}

// Touch support for mobile
let touchStartX = 0;
let touchEndX = 0;

document.addEventListener('touchstart', e => {
    touchStartX = e.changedTouches[0].screenX;
});

document.addEventListener('touchend', e => {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipe();
});

function handleSwipe() {
    if (touchEndX < touchStartX - 50) navigateSlide(1);
    if (touchEndX > touchStartX + 50) navigateSlide(-1);
}
