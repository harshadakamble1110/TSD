// Advanced animations and interactions
class AdvancedUI {
    constructor() {
        this.init();
        this.particles = [];
        this.notices = [];
    }

    init() {
        this.createParticles();
        this.createMovingNotices();
        this.addMicroInteractions();
        this.initScrollAnimations();
        this.initTypingEffect();
    }

    createParticles() {
        const particlesContainer = document.createElement('div');
        particlesContainer.className = 'particles';
        document.body.appendChild(particlesContainer);

        // Create 50 particles
        for (let i = 0; i < 50; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.animationDelay = Math.random() * 15 + 's';
            particle.style.animationDuration = (15 + Math.random() * 10) + 's';
            particlesContainer.appendChild(particle);
        }
    }

    createMovingNotices() {
        // Check if we're on admin panel - don't show notices there
        if (window.location.pathname.includes('/admin')) {
            return;
        }
        
        // Remove any existing notices to prevent duplicates
        const existingNotices = document.querySelector('.moving-notices');
        if (existingNotices) {
            existingNotices.remove();
        }
        
        const notices = [
            "🎯 New Course: Advanced Web Development - Enroll Now & Save 30%",
            "🚀 Limited Time: Premium Courses at Discounted Prices",
            "📚 Free Study Materials Available for All Students",
            "🏆 Certificate Programs Now Live - Get Certified Today",
            "💡 Daily Coding Challenges - Win Exciting Prizes"
        ];

        const noticeContainer = document.createElement('div');
        noticeContainer.className = 'moving-notices';
        noticeContainer.innerHTML = `
            <div class="notice-track">
                ${notices.map(notice => `<span class="notice-item">${notice}</span>`).join('')}
            </div>
        `;

        const header = document.querySelector('.main-header');
        if (header) {
            header.insertAdjacentElement('afterend', noticeContainer);
        }
    }

    addMicroInteractions() {
        // Enhanced hover effects for cards
        const cards = document.querySelectorAll('.course-card, .category-card, .stats-card');
        cards.forEach(card => {
            card.addEventListener('mouseenter', (e) => {
                e.target.style.transform = 'translateY(-10px) scale(1.02)';
                e.target.style.boxShadow = '0 30px 60px rgba(79, 70, 229, 0.3)';
            });

            card.addEventListener('mouseleave', (e) => {
                e.target.style.transform = 'translateY(0) scale(1)';
                e.target.style.boxShadow = '';
            });
        });

        // Button ripple effects
        const buttons = document.querySelectorAll('button, .btn');
        buttons.forEach(button => {
            button.addEventListener('click', function(e) {
                const ripple = document.createElement('span');
                ripple.className = 'ripple';
                this.appendChild(ripple);

                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;

                ripple.style.width = ripple.style.height = size + 'px';
                ripple.style.left = x + 'px';
                ripple.style.top = y + 'px';

                setTimeout(() => ripple.remove(), 600);
            });
        });
    }

    initScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, observerOptions);

        // Observe all sections
        document.querySelectorAll('section, .course-card, .category-card, .stats-card').forEach(el => {
            observer.observe(el);
        });
    }

    initTypingEffect() {
        const heroTitle = document.querySelector('.hero-title');
        if (heroTitle) {
            const text = heroTitle.textContent;
            heroTitle.textContent = '';
            let index = 0;

            const typeWriter = () => {
                if (index < text.length) {
                    heroTitle.textContent += text.charAt(index);
                    index++;
                    setTimeout(typeWriter, 50);
                }
            };

            setTimeout(typeWriter, 500);
        }
    }

    // Animated loading states
    showLoading(element) {
        element.classList.add('loading');
        const originalContent = element.innerHTML;
        element.innerHTML = '<div class="spinner"></div>';
        return originalContent;
    }

    hideLoading(element, originalContent) {
        element.classList.remove('loading');
        element.innerHTML = originalContent;
    }
}

// Theme Manager Class
class ThemeManager {
    constructor() {
        this.theme = this.getStoredTheme();
        this.init();
    }

    getStoredTheme() {
        // Default to light mode
        const stored = localStorage.getItem('tsd-theme');
        if (stored) {
            return stored;
        }
        // Default to light mode instead of system preference
        return 'light';
    }

    setStoredTheme(theme) {
        localStorage.setItem('tsd-theme', theme);
        this.theme = theme;
    }

    init() {
        // Apply theme immediately on page load
        this.applyTheme(this.theme);
        
        // Create floating buttons
        this.createFloatingButtons();
        
        // Listen for system theme changes
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            if (!localStorage.getItem('tsd-theme')) {
                this.theme = e.matches ? 'dark' : 'light';
                this.applyTheme(this.theme);
                this.updateToggleButton();
            }
        });
    }

    applyTheme(theme) {
        const root = document.documentElement;
        const body = document.body;
        
        if (theme === 'dark') {
            root.classList.add('dark-theme');
            body.classList.add('dark-theme');
            body.classList.remove('light-theme');
        } else {
            root.classList.remove('dark-theme');
            body.classList.remove('dark-theme');
            body.classList.add('light-theme');
        }
        
        // Update meta theme-color for mobile browsers
        const metaTheme = document.querySelector('meta[name="theme-color"]');
        if (metaTheme) {
            metaTheme.content = theme === 'dark' ? '#1a1a1a' : '#ffffff';
        }
    }

    toggleTheme() {
        const newTheme = this.theme === 'light' ? 'dark' : 'light';
        this.setStoredTheme(newTheme);
        this.applyTheme(newTheme);
        this.updateToggleButton();
        
        // Dispatch custom event for other components
        window.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme: newTheme } }));
    }

    updateToggleButton() {
        const toggle = document.querySelector('.theme-switch input');
        const iconLight = document.querySelector('.theme-icon-light');
        const iconDark = document.querySelector('.theme-icon-dark');
        
        if (toggle) {
            toggle.checked = this.theme === 'dark';
        }
        
        if (iconLight && iconDark) {
            if (this.theme === 'dark') {
                iconLight.style.opacity = '0.4';
                iconDark.style.opacity = '1';
            } else {
                iconLight.style.opacity = '1';
                iconDark.style.opacity = '0.4';
            }
        }
    }

    createFloatingButtons() {
        // Remove existing buttons if any
        const existingButtons = document.querySelector('.floating-buttons');
        if (existingButtons) {
            existingButtons.remove();
        }

        const container = document.createElement('div');
        container.className = 'floating-buttons';
        container.innerHTML = `
            <label class="theme-switch">
                <input type="checkbox" ${this.theme === 'dark' ? 'checked' : ''}>
                <span class="theme-slider">
                    <span class="theme-icon theme-icon-light">☀️</span>
                    <span class="theme-icon theme-icon-dark">🌙</span>
                </span>
            </label>
        `;

        document.body.appendChild(container);

        // Add event listener
        const toggle = container.querySelector('.theme-switch input');
        toggle.addEventListener('change', () => this.toggleTheme());
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Force light mode by default
    localStorage.setItem('tsd-theme', 'light');
    
    // Initialize theme manager
    const themeManager = new ThemeManager();
    
    // Initialize advanced UI
    const advancedUI = new AdvancedUI();
    
    // Add smooth scroll behavior
    document.documentElement.style.scrollBehavior = 'smooth';
    
    // Performance optimization: Defer non-critical animations
    setTimeout(() => {
        advancedUI.createParticles();
        advancedUI.createMovingNotices();
        advancedUI.addMicroInteractions();
        advancedUI.initScrollAnimations();
        advancedUI.initTypingEffect();
    }, 100);
    
    // Add page transition effects
    document.body.classList.add('page-loaded');
});

// Enhanced form interactions
document.addEventListener('DOMContentLoaded', () => {
    const inputs = document.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
        input.addEventListener('focus', (e) => {
            e.target.parentElement.classList.add('focused');
        });
        input.addEventListener('blur', (e) => {
            e.target.parentElement.classList.remove('focused');
        });
    });
});
