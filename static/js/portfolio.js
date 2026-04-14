        // ---- Navbar scroll ----
        const nav = document.getElementById('pNav');
        window.addEventListener('scroll', () => {
            nav.classList.toggle('scrolled', window.scrollY > 50);
        });

        // ---- Mobile menu ----
        const toggle = document.getElementById('pNavToggle');
        const links = document.getElementById('pNavLinks');

        toggle.addEventListener('click', () => links.classList.toggle('open'));
        links.querySelectorAll('a').forEach(a => a.addEventListener('click', () => links.classList.remove('open')));

        // ---- Scroll reveal ----
        const revealEls = document.querySelectorAll('.reveal');
        const revealObs = new IntersectionObserver((entries) => {
            entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
        }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });
        revealEls.forEach(el => revealObs.observe(el));

        // ---- Skill bar animation ----
        const skillBars = document.querySelectorAll('.p-skill-bar-fill');
        const skillObs = new IntersectionObserver((entries) => {
            entries.forEach(e => {
                if (e.isIntersecting) {
                    e.target.style.width = e.target.getAttribute('data-level') + '%';
                    skillObs.unobserve(e.target);
                }
            });
        }, { threshold: 0.5 });
        skillBars.forEach(el => skillObs.observe(el));

        // ---- Floating particles ----
        const particlesContainer = document.getElementById('pParticles');
        for (let i = 0; i < 18; i++) {
            const p = document.createElement('div');
            p.classList.add('p-particle');
            p.style.left = Math.random() * 100 + '%';
            p.style.top = 40 + Math.random() * 60 + '%';
            const size = (2 + Math.random() * 4) + 'px';
            p.style.width = size;
            p.style.height = size;
            p.style.animationDelay = Math.random() * 12 + 's';
            p.style.animationDuration = (8 + Math.random() * 8) + 's';
            particlesContainer.appendChild(p);
        }

        // ---- Smooth scroll ----
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) target.scrollIntoView({ behavior: 'smooth' });
            });
        });
