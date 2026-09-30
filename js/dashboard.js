document.addEventListener("DOMContentLoaded", () => {
    // Mobile Sidebar Toggle
    const toggleBtn = document.getElementById('mobileToggle');
    const sidebar = document.getElementById('sidebar');
    
    if(toggleBtn && sidebar) {
        toggleBtn.addEventListener('click', () => {
            sidebar.classList.toggle('active');
        });
    }

    // Common GSAP Animations for Dashboard
    if (typeof gsap !== 'undefined') {
        // Sidebar entrance
        gsap.from(".sidebar", { x: -250, opacity: 0, duration: 0.8, ease: "power3.out" });
        
        // Header reveal
        gsap.from(".top-header", { y: -50, opacity: 0, duration: 0.8, delay: 0.2, ease: "power3.out" });
        
        // KPI stagger
        gsap.from(".kpi-card", { y: 30, opacity: 0, duration: 0.8, stagger: 0.1, delay: 0.4, ease: "power2.out" });
        
        // Panel stagger
        gsap.from(".panel", { y: 30, opacity: 0, duration: 0.8, stagger: 0.1, delay: 0.6, ease: "power2.out" });
        
        // Counter animation
        const counters = document.querySelectorAll('.kpi-value');
        counters.forEach(counter => {
            if(counter.innerText.includes('₹') || counter.innerText.includes('L') || counter.innerText.includes('%')) {
                // simple animation for formatted strings can be done differently, 
                // but for simple numbers:
                return;
            }
            const target = +counter.getAttribute('data-target') || parseInt(counter.innerText);
            if(target) {
                counter.innerText = '0';
                gsap.to(counter, {
                    innerHTML: target,
                    duration: 2,
                    snap: { innerHTML: 1 },
                    ease: "power2.out",
                    delay: 0.5
                });
            }
        });
    }
});
