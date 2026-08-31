document.addEventListener('DOMContentLoaded', () => {
    const menuBtn = document.getElementById('menuBtn');
    const mainNav = document.getElementById('mainNav');
    const navUtils = document.getElementById('navUtils');
    menuBtn.addEventListener('click', () => {
        const isExpanded = menuBtn.getAttribute('aria-expanded') === 'true';
        menuBtn.setAttribute('aria-expanded', !isExpanded);
        mainNav.classList.toggle('show-mobile');
        navUtils.classList.toggle('show-mobile');
        menuBtn.innerHTML = !isExpanded ? '✕' : '☰';
    });
});