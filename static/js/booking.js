document.getElementById('booking-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission

    // Collect form data
    let formData = new FormData(document.getElementById('booking-form'));

    // Validate form fields
    let name = formData.get('name').trim();
    let email = formData.get('email').trim();
    let phone = formData.get('phone').trim();
    let service = formData.get('service').trim();
    let date = formData.get('date').trim();

    if (!name || !email || !phone || !service || !date) {
        showAlert('Please fill in all required fields.', 'danger');
        return;
    }

    // Submit data asynchronously using Fetch API
    fetch('/submit_booking', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('Booking submitted successfully!', 'success');
            document.getElementById('booking-form').reset(); // Reset form
        } else {
            showAlert('An error occurred: ' + data.message, 'danger');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('An error occurred. Please try again later.', 'danger');
    });
});

// Function to display alert messages
function showAlert(message, category) {
    let alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${category} mt-3`;
    alertDiv.textContent = message;

    // Add the alert to the alert container
    let alertContainer = document.getElementById('alert');
    alertContainer.innerHTML = ''; // Clear previous alerts
    alertContainer.appendChild(alertDiv);

    setTimeout(() => alertDiv.remove(), 5000); // Remove alert after 5 seconds
}
