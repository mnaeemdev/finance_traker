// Modal functionality
const demoButton = document.getElementById('demo-button');
const demoModal = document.getElementById('demo-modal');
const modalClose = document.querySelector('.modal-close');

if (demoButton && demoModal) {
    demoButton.addEventListener('click', () => {
        demoModal.classList.add('active');
    });

    modalClose.addEventListener('click', () => {
        demoModal.classList.remove('active');
    });

    demoModal.addEventListener('click', (e) => {
        if (e.target === demoModal) {
            demoModal.classList.remove('active');
        }
    });
}
