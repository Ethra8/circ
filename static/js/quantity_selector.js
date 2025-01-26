// Ensure proper enabling/disabling of all inputs on page load
document.addEventListener('DOMContentLoaded', () => {
    const qtyInputs = document.querySelectorAll('.qty_input');

    if (qtyInput) {
        console.log(qtyInput.dataset);
    } else {
        console.warn('Element with class `.qty_input` not found.');
    }
    
    if (qtyInputs.length === 0) {
        console.log("No quantity inputs found on the page.");
        return;
    }

    qtyInputs.forEach((input) => {
        const itemId = input.dataset.item_id;
        if (itemId) {
            if (input.id.includes('adult')) {
                handleEnableDisableAdult(itemId);
            } else if (input.id.includes('reduced')) {
                handleEnableDisableReduced(itemId);
            }
        }
    });

    // Increment and decrement event listeners
    document.querySelectorAll('.increment-qty').forEach((button) => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const closestInput = button.closest('.input-group').querySelector('.qty_input');
            const currentValue = parseInt(closestInput.value);
            closestInput.value = currentValue + 1;
            handleEnableDisableAdult(button.dataset.item_id);
        });
    });

    document.querySelectorAll('.decrement-qty').forEach((button) => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const closestInput = button.closest('.input-group').querySelector('.qty_input');
            const currentValue = parseInt(closestInput.value);
            if (currentValue > 0) {
                closestInput.value = currentValue - 1;
            }
            handleEnableDisableAdult(button.dataset.item_id);
        });
    });
});
