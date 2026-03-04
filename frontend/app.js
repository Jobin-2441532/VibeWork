// Enable scroll animations (progressive enhancement — CSS keeps sections visible if this fails)
document.body.classList.add('js-animations');

document.addEventListener('DOMContentLoaded', () => {
    // Scroll Animations
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.fade-in-up').forEach((el) => {
        observer.observe(el);
    });

    // Navbar scroll effect
    const navbar = document.getElementById('navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.classList.add('bg-white', 'shadow-sm');
                navbar.querySelectorAll('a, span').forEach(el => {
                    if (!el.classList.contains('bg-primary')) {
                        el.classList.replace('text-white', 'text-gray-800');
                    }
                });
            } else {
                navbar.classList.remove('bg-white', 'shadow-sm');
                navbar.querySelectorAll('a, span').forEach(el => {
                    if (!el.classList.contains('bg-primary')) {
                        el.classList.replace('text-gray-800', 'text-white');
                    }
                });
            }
        });
    }
});

