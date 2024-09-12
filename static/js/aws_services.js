document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('uploadForm_Image').addEventListener('submit', function(event) {
        event.preventDefault();

        var formData = new FormData(this);

        fetch('http://127.0.0.1:5000/analyze-image', {
            method: 'POST',
            body: formData,
            headers: {
                'Accept': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('resultContent').innerHTML = '<div class="alert alert-success">Analysis Results: ' + data.message + '</div>';
        })
        .catch(error => {
            document.getElementById('resultContent').innerHTML = '<div class="alert alert-danger">Error: ' + error.message + '</div>';
        });
    });
});