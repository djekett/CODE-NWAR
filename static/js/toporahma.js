        // ---- Navbar scroll effect ----
        const navbar = document.getElementById('navbar');
        let lastScroll = 0;

        window.addEventListener('scroll', () => {
            const currentScroll = window.scrollY;
            if (currentScroll > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
            lastScroll = currentScroll;
        });

        // ---- Mobile menu toggle ----
        const navToggle = document.getElementById('navToggle');
        const navLinks = document.getElementById('navLinks');

        navToggle.addEventListener('click', () => {
            navLinks.classList.toggle('open');
        });

        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('open');
            });
        });

        // ---- Scroll reveal (Intersection Observer) ----
        const revealElements = document.querySelectorAll('.reveal');

        const revealObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        revealElements.forEach(el => revealObserver.observe(el));

        // ---- Animated counters ----
        const counters = document.querySelectorAll('.hero-stat-value[data-count]');

        const counterObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const target = entry.target;
                    const count = parseInt(target.getAttribute('data-count'));
                    let current = 0;
                    const increment = Math.ceil(count / 40);
                    const duration = 1500;
                    const stepTime = duration / (count / increment);

                    const timer = setInterval(() => {
                        current += increment;
                        if (current >= count) {
                            current = count;
                            clearInterval(timer);
                        }
                        target.textContent = current + '+';
                    }, stepTime);

                    counterObserver.unobserve(target);
                }
            });
        }, { threshold: 0.5 });

        counters.forEach(el => counterObserver.observe(el));

        // ---- Floating particles ----
        const particlesContainer = document.getElementById('particles');

        function createParticles() {
            for (let i = 0; i < 20; i++) {
                const particle = document.createElement('div');
                particle.classList.add('particle');
                particle.style.left = Math.random() * 100 + '%';
                particle.style.top = 40 + Math.random() * 60 + '%';
                particle.style.width = (2 + Math.random() * 4) + 'px';
                particle.style.height = particle.style.width;
                particle.style.animationDelay = Math.random() * 12 + 's';
                particle.style.animationDuration = (8 + Math.random() * 8) + 's';
                particlesContainer.appendChild(particle);
            }
        }

        createParticles();

        // ---- Smooth scroll for anchor links ----
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
