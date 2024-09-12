$(document).ready(function() {
    // Handle SMS form submission
    $('#smsForm').submit(function(event) {
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/send_sms',
            contentType: 'application/json',
            data: JSON.stringify({
                number: $('#smsNumber').val(),
                message: $('#smsMessage').val()
            }),
            success: function(response) {
                if (response.status === 'success') {
                    alert('SMS sent successfully!');
                } else {
                    alert('Error sending SMS: ' + response.message);
                }
            },
            error: function(error) {
                alert('An error occurred.');
            }
        });
    });

    // Handle WhatsApp form submission
    $('#whatsappForm').submit(function(event) {
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/send_whatsapp',
            data: $(this).serialize(),
            success: function(response) {
                alert('WhatsApp message sent successfully!');
            },
            error: function(error) {
                alert('An error occurred.');
            }
        });
    });

    // Handle Call form submission
    $('#callForm').submit(function(event) {
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/call',
            data: $(this).serialize(),
            success: function(response) {
                alert('Call initiated successfully!');
            },
            error: function(error) {
                alert('An error occurred.');
            }
        });
    });

    // Handle Google Search form submission
    $('#googleSearchForm').submit(function(event) {
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/search/google',
            data: $(this).serialize(),
            success: function(response) {
                window.location.href = response.redirect;
            },
            error: function(error) {
                alert('An error occurred.');
            }
        });
    });

    // Handle Bing Search form submission
    $('#bingSearchForm').submit(function(event) {
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/search/bing',
            data: $(this).serialize(),
            success: function(response) {
                window.location.href = response.redirect;
            },
            error: function(error) {
                alert('An error occurred.');
            }
        });
    });
});
