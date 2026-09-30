// Hamburger Menu Toggle
const hamburger = document.querySelector('.hamburger');
const navLinks = document.querySelector('.nav-links');
const navActions = document.querySelector('.nav-actions');

if (hamburger) {
    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        navLinks.classList.toggle('active');
        if(navActions) navActions.classList.toggle('active');
    });
}

// Global GSAP Page Transition / Preloader (if used)
document.addEventListener("DOMContentLoaded", () => {
    // Check if gsap is loaded
    if (typeof gsap !== 'undefined') {
        gsap.from("nav", { y: -100, opacity: 0, duration: 1, ease: "power4.out" });
        
        // General scroll animations for sections
        const sections = document.querySelectorAll('section');
        sections.forEach(sec => {
            gsap.from(sec, {
                scrollTrigger: {
                    trigger: sec,
                    start: "top 80%"
                },
                y: 50,
                opacity: 0,
                duration: 1,
                ease: "power3.out"
            });
        });
    }
});
