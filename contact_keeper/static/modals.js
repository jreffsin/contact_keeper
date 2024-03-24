// Handle modals depending on which page they're loaded to
    document.addEventListener("DOMContentLoaded", function() {
        var page = document.getElementById('page_id').getAttribute('data-page');
        if (page === 'view_contact') {
            var deleteButtons = document.querySelectorAll('[data-bs-target="#deleteAddressModal"]');
            deleteButtons.forEach(function(button) {
                button.addEventListener('click', function() {
                    var addressId = button.getAttribute('data-address-id');
                    var confirmButton = document.getElementById('confirmDelete');
                    confirmButton.setAttribute('data-address-id', addressId);
                    confirmButton.addEventListener('click', function() {
                        fetch(deleteUrlTemplate.replace('0', addressId), {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({address_id: addressId})
                        }).then(response => {
                            // Handle response
                            if (response.ok) {
                                window.location.reload(); // Reload the page to update the list
                            } else {
                                alert("Error deleting address");
                            }
                        });
                    });
                });
            });
        }
        else if (page === 'contacts') {
            var deleteContactButtons = document.querySelectorAll('[data-bs-target="#deleteModal"]');
            deleteContactButtons.forEach(function(button) {
                button.addEventListener('click', function() {
                    var contactId = button.getAttribute('data-contact-id');
                    var confirmButton = document.getElementById('confirmDelete');
                    confirmButton.setAttribute('data-contact-id', contactId);
                    confirmButton.addEventListener('click', function() {
                        fetch(deleteUrlTemplate.replace('0', contactId), {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({contact_id: contactId})
                        }).then(response => {
                            // Handle response
                            if (response.ok) {
                                window.location.reload(); // Reload the page to update the list
                            } else {
                                alert("Error deleting contact");
                            }
                        });
                    });
                });
            });
            
        }
    });
