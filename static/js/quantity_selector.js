// Disable +/- buttons outside 0-99 range for Adult Tickets
function handleEnableDisableAdult(itemId) {
    var currentValue = parseInt($(`#id_qty_adult_${itemId}`).val());
    var minusDisabled = currentValue <= 0; // Disable minus button if value is 0
    var plusDisabled = currentValue >= 99; // Disable plus button if value is 99
    $(`#decrement-qty-adult_${itemId}`).prop('disabled', minusDisabled);
    $(`#increment-qty-adult_${itemId}`).prop('disabled', plusDisabled);
}

// Disable +/- buttons outside 0-99 range for Reduced Tickets
function handleEnableDisableReduced(itemId) {
    var currentValue = parseInt($(`#id_qty_reduced_${itemId}`).val());
    var minusDisabled = currentValue <= 0; // Disable minus button if value is 0
    var plusDisabled = currentValue >= 99; // Disable plus button if value is 99
    $(`#decrement-qty-reduced_${itemId}`).prop('disabled', minusDisabled);
    $(`#increment-qty-reduced_${itemId}`).prop('disabled', plusDisabled);
}

// Ensure proper enabling/disabling of all inputs on page load
$('.qty_input').each(function() {
    var itemId = $(this).data('item_id');
    if ($(this).attr('id').includes('adult')) {
        handleEnableDisableAdult(itemId);
    } else if ($(this).attr('id').includes('reduced')) {
        handleEnableDisableReduced(itemId);
    }
});

// Check enable/disable every time the input is changed
$('.qty_input').change(function() {
    var itemId = $(this).data('item_id');
    if ($(this).attr('id').includes('adult')) {
        handleEnableDisableAdult(itemId);
    } else if ($(this).attr('id').includes('reduced')) {
        handleEnableDisableReduced(itemId);
    }
});

// Increment quantity
$('.increment-qty').click(function(e) {
    e.preventDefault();
    var closestInput = $(this).closest('.input-group').find('.qty_input')[0];
    var currentValue = parseInt($(closestInput).val());
    $(closestInput).val(currentValue + 1);
    var itemId = $(this).data('item_id');
    if ($(closestInput).attr('id').includes('adult')) {
        handleEnableDisableAdult(itemId);
    } else if ($(closestInput).attr('id').includes('reduced')) {
        handleEnableDisableReduced(itemId);
    }
});

// Decrement quantity
$('.decrement-qty').click(function(e) {
    e.preventDefault();
    var closestInput = $(this).closest('.input-group').find('.qty_input')[0];
    var currentValue = parseInt($(closestInput).val());
    if (currentValue > 0) {
        $(closestInput).val(currentValue - 1);
    }
    var itemId = $(this).data('item_id');
    if ($(closestInput).attr('id').includes('adult')) {
        handleEnableDisableAdult(itemId);
    } else if ($(closestInput).attr('id').includes('reduced')) {
        handleEnableDisableReduced(itemId);
    }
});
