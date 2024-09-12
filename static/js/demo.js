// Function to reset button styles
function resetButtonStyles() {
    // List all button IDs
    const buttonIds = ['SendMessageBtn', 'otherTasksBtn', 'allBtn','OpenCv2'];
    
    buttonIds.forEach(id => {
        const button = document.getElementById(id);
        if (button) {
            button.style.backgroundColor = '';
            button.style.color = '';
        }
    });
}

// Event listener for 'Send Message' button
document.getElementById('SendMessageBtn').addEventListener('click', function() {
    resetButtonStyles(); // Reset styles for all buttons

    document.getElementById('SendMsg').style.display = 'block';
    document.getElementById('SendMail').style.display = 'block';
    document.getElementById('googlequery').style.display = 'block';
    document.getElementById('WhatMsg').style.display = 'block';
    document.getElementById('CallSomeone').style.display = 'block';
    document.getElementById('TextOnImage').style.display = 'block';
    this.style.backgroundColor = 'black';
    this.style.color = 'white';

    // Hide other projects
    document.getElementById('holiProject').style.display = 'none';
    document.getElementById('NewYearProject').style.display = 'none';
    document.getElementById('SearchGoogleBing').style.display = 'none';
    document.getElementById('PhotoCapture').style.display = 'none';

});

// Event listener for 'Other Tasks' button
document.getElementById('otherTasksBtn').addEventListener('click', function() {
    resetButtonStyles(); // Reset styles for all buttons

    document.getElementById('holiProject').style.display = 'block';
    document.getElementById('NewYearProject').style.display = 'block';
    this.style.backgroundColor = 'black';
    this.style.color = 'white';

    // Hide send message and send mail
    document.getElementById('SendMsg').style.display = 'none';
    document.getElementById('SendMail').style.display = 'none';
    document.getElementById('googlequery').style.display = 'none';
    document.getElementById('WhatMsg').style.display = 'none';
    document.getElementById('CallSomeone').style.display = 'none';
    document.getElementById('PhotoCapture').style.display = 'none';
    document.getElementById('TextOnImage').style.display = 'none';


});
 

// Event listener for 'OpenCv2' button
document.getElementById('OpenCv2').addEventListener('click', function() {
    resetButtonStyles(); // Reset styles for all buttons

    document.getElementById('OpenCv2').style.backgroundColor = 'black';
    document.getElementById('OpenCv2').style.color = 'white';

    // Hide other projects
    document.getElementById('SendMsg').style.display = 'none';
    document.getElementById('SendMail').style.display = 'none';
    document.getElementById('googlequery').style.display = 'none';
    document.getElementById('WhatMsg').style.display = 'none';
    document.getElementById('CallSomeone').style.display = 'none';
    document.getElementById('holiProject').style.display = 'none';
    document.getElementById('NewYearProject').style.display = 'none';
    document.getElementById('SearchGoogleBing').style.display = 'none';
    document.getElementById('PhotoCapture').style.display = 'none';
});
// Function to show all projects and set button styles
function showAllProjects() {
    document.getElementById('SendMsg').style.display = 'block';
    document.getElementById('SendMail').style.display = 'block';
    document.getElementById('googlequery').style.display = 'block';
    document.getElementById('WhatMsg').style.display = 'block';
    document.getElementById('CallSomeone').style.display = 'block';
    document.getElementById('SearchGoogleBing').style.display = 'block';
    document.getElementById('holiProject').style.display = 'block';
    document.getElementById('NewYearProject').style.display = 'block';
    document.getElementById('PhotoCapture').style.display = 'block';
    document.getElementById('TextOnImage').style.display = 'block';

    resetButtonStyles(); // Reset styles for all buttons
    document.getElementById('allBtn').style.backgroundColor = 'black';
    document.getElementById('allBtn').style.color = 'white';
}

// Event listener for 'All' button
document.getElementById('allBtn').addEventListener('click', function() {
    resetButtonStyles(); // Reset styles for all buttons

    document.getElementById('SendMsg').style.display = 'block';
    document.getElementById('SendMail').style.display = 'block';
    document.getElementById('googlequery').style.display = 'block';
    document.getElementById('WhatMsg').style.display = 'block';
    document.getElementById('CallSomeone').style.display = 'block';
    document.getElementById('SearchGoogleBing').style.display = 'block';
    document.getElementById('holiProject').style.display = 'block';
    document.getElementById('NewYearProject').style.display = 'block';
    document.getElementById('PhotoCapture').style.display = 'block';
    document.getElementById('TextOnImage').style.display = 'block';
    this.style.backgroundColor = 'black';
    this.style.color = 'white';
});

// Ensure all projects are shown when the page loads
document.addEventListener('DOMContentLoaded', (event) => {
    showAllProjects();
});
