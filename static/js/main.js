// Modal functionality
const demoButton = document.getElementById('demo-button');
const demoModal = document.getElementById('demo-modal');
const modalClose = document.querySelector('.modal-close');
const demoVideo = document.getElementById('demo-video');
const flashCloses = document.querySelectorAll('.flash-close');

function closeModal() {
    demoModal.classList.remove('active');
    if (demoVideo) {
        const src = demoVideo.src;
        demoVideo.src = src;
    }
}

if (demoButton && demoModal) {
    demoButton.addEventListener('click', () => {
        demoModal.classList.add('active');
    });

    modalClose.addEventListener('click', closeModal);

    demoModal.addEventListener('click', (e) => {
        if (e.target === demoModal) {
            closeModal();
        }
    });
}

flashCloses.forEach((button) => {
    button.addEventListener('click', () => {
        const flash = button.closest('.flash');
        if (flash) {
            flash.remove();
        }
    });
});

// Auto-dismiss navbar toast after 2 seconds
const navbarToasts = document.querySelectorAll('.navbar-toast');
navbarToasts.forEach((toast) => {
    setTimeout(() => {
        toast.style.animation = 'slideDown 0.3s ease-out reverse';
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, 2000);
});

// Initialize Lucide icons
document.addEventListener('DOMContentLoaded', function () {
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
});
