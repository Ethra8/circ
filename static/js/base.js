// Ensure alert disappears fully once -close is clicked
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.alert .close').forEach(closeButton => {
        closeButton.addEventListener('click', () => {
            const alert = closeButton.closest('.alert');
            if (alert) {
                alert.classList.add('fade');
                setTimeout(() => alert.remove(), 300);
            }
        });
    });
});