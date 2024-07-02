document.addEventListener("DOMContentLoaded", function() {
    const contactForm = document.getElementById("contact-form");
    if (contactForm) {
        contactForm.addEventListener("submit", function(event) {
            event.preventDefault(); // Prevent the default form submission

            // Validate the form
            const name = document.getElementById("name").value;
            const email = document.getElementById("email").value;
            const phone = document.getElementById("phone").value;
            const message = document.getElementById("message").value;

            // Simple validation
            if (!name || !email || !phone || !message) {
                alert("Please fill in all required fields.");
                return;
            }

            // Create a contact object
            const contactData = {
                name: name,
                email: email,
                phone: phone,
                message: message
            };

            // Send the contact data to the server
            fetch(contactForm.action, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(contactData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert("Message sent successfully!");
                    contactForm.reset();
                } else {
                    alert("An error occurred while sending your message. Please try again later.");
                }
            })
            .catch(error => {
                console.error("Error:", error);
                alert("An error occurred while sending your message. Please try again later.");
            });
        });
    }
});
