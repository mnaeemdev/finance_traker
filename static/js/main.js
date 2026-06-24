// Modal functionality
const demoButton = document.getElementById('demo-button');
const demoModal = document.getElementById('demo-modal');
const modalClose = document.querySelector('.modal-close');
const demoVideo = document.getElementById('demo-video');

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
