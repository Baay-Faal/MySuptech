// Initialize Feather Icons
document.addEventListener('DOMContentLoaded', function() {
    feather.replace();
    
    // Initialize Intersection Observer for scroll animations
    initScrollAnimations();
    
    // Initialize Mobile Menu Toggle
    initMobileMenu();
    
    // Initialize Live Demo Simulation
    initLiveDemoSimulation();
});

// Scroll Animations using Intersection Observer
function initScrollAnimations() {
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in-up');
                entry.target.style.opacity = '1';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe elements with animation classes
    document.querySelectorAll('.feature-card, .bg-white.rounded-xl').forEach((el) => {
        el.style.opacity = '0';
        observer.observe(el);
    });
}

// Mobile Menu Toggle
function initMobileMenu() {
    const menuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (menuButton && mobileMenu) {
        menuButton.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
            const icon = menuButton.querySelector('i');
            if (mobileMenu.classList.contains('hidden')) {
                icon.setAttribute('data-feather', 'menu');
            } else {
                icon.setAttribute('data-feather', 'x');
            }
            feather.replace();
        });
    }
}

// Live Demo Simulation - Updates status indicators randomly
function initLiveDemoSimulation() {
    const indicators = document.querySelectorAll('.demo-status-indicator');
    
    if (indicators.length === 0) return;
    
    setInterval(() => {
        const randomIndicator = indicators[Math.floor(Math.random() * indicators.length)];
        const statuses = ['emerald', 'rose', 'slate'];
        const currentStatus = randomIndicator.dataset.status;
        const newStatus = statuses[Math.floor(Math.random() * statuses.length)];
        
        if (currentStatus !== newStatus) {
            randomIndicator.className = `w-3 h-3 rounded-full bg-${newStatus}-500 transition-colors duration-500`;
            randomIndicator.dataset.status = newStatus;
        }
    }, 3000);
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add scroll effect to navbar
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('nav');
    if (window.scrollY > 50) {
        navbar?.classList.add('shadow-lg', 'bg-white/95', 'backdrop-blur-sm');
        navbar?.classList.remove('bg-transparent');
    } else {
        navbar?.classList.remove('shadow-lg', 'bg-white/95', 'backdrop-blur-sm');
        navbar?.classList.add('bg-transparent');
    }
});

// Counter Animation for Stats
function animateCounter(element, target, duration = 2000) {
    let start = 0;
    const increment = target / (duration / 16);
    
    const timer = setInterval(() => {
        start += increment;
        if (start >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(start);
        }
    }, 16);
}

// Trigger counters when visible
const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting && !entry.target.classList.contains('counted')) {
            const target = parseInt(entry.target.dataset.target);
            animateCounter(entry.target, target);
            entry.target.classList.add('counted');
        }
    });
});

document.querySelectorAll('.counter').forEach(counter => {
    counterObserver.observe(counter);
});