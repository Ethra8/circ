// Ensure proper enabling/disabling of all inputs on page load
document.addEventListener('DOMContentLoaded', () => {
    const qtyInputs = document.querySelectorAll('.qty_input');

    if (qtyInputs.length === 0) {
        console.warn("No quantity inputs found on the page.");
        return;
    }

    // Handle enabling/disabling increment and decrement buttons for each item
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
            const currentValue = parseInt(closestInput.value) || 0;
            const maxValue = parseInt(closestInput.max) || 99; // Default max to 99 if not specified

            if (currentValue < maxValue) {
                closestInput.value = currentValue + 1;
            }

            if (closestInput.id.includes('adult')) {
                handleEnableDisableAdult(button.dataset.item_id);
            } else if (closestInput.id.includes('reduced')) {
                handleEnableDisableReduced(button.dataset.item_id);
            }
        });
    });

    document.querySelectorAll('.decrement-qty').forEach((button) => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const closestInput = button.closest('.input-group').querySelector('.qty_input');
            const currentValue = parseInt(closestInput.value) || 0;

            if (currentValue > 0) {
                closestInput.value = currentValue - 1;
            }

            if (closestInput.id.includes('adult')) {
                handleEnableDisableAdult(button.dataset.item_id);
            } else if (closestInput.id.includes('reduced')) {
                handleEnableDisableReduced(button.dataset.item_id);
            }
        });
    });
});

// Function to handle enabling/disabling increment and decrement buttons for "Adult" quantities
function handleEnableDisableAdult(itemId) {
    const input = document.querySelector(`#id_qty_adult_${itemId}`);
    const decrementButton = document.querySelector(`#decrement-qty-adult_${itemId}`);
    const incrementButton = document.querySelector(`#increment-qty-adult_${itemId}`);

    if (!input || !decrementButton || !incrementButton) {
        console.warn(`Missing elements for item ${itemId}.`);
        return;
    }

    const currentValue = parseInt(input.value) || 0;
    const maxValue = parseInt(input.max) || 99;

    decrementButton.disabled = currentValue <= 0;
    incrementButton.disabled = currentValue >= maxValue;
}

// Function to handle enabling/disabling increment and decrement buttons for "Reduced" quantities
function handleEnableDisableReduced(itemId) {
    const input = document.querySelector(`#id_qty_reduced_${itemId}`);
    const decrementButton = document.querySelector(`#decrement-qty-reduced_${itemId}`);
    const incrementButton = document.querySelector(`#increment-qty-reduced_${itemId}`);

    if (!input || !decrementButton || !incrementButton) {
        console.warn(`Missing elements for item ${itemId}.`);
        return;
    }

    const currentValue = parseInt(input.value) || 0;
    const maxValue = parseInt(input.max) || 99;

    decrementButton.disabled = currentValue <= 0;
    incrementButton.disabled = currentValue >= maxValue;
}
