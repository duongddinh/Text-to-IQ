document.querySelector('form').addEventListener('submit', function(e) {
    e.preventDefault();

    // Clear previous output
    const outputElement = document.getElementById('output');
    outputElement.textContent = '';

    // Disable the button
    const button = this.querySelector('button[type="submit"]');
    button.disabled = true;
    button.textContent = 'Running...';

    // Access the form data to log it
    const formData = new FormData(this);
    const textInput = formData.get('textInput'); // Get the value of 'textInput'
    console.log('Sending textInput:', textInput); // Log the value to the console

    // Convert FormData to URL-encoded string
    const urlEncodedData = new URLSearchParams(formData).toString();

    // Send the request
    fetch('/predict', {
        method: 'post',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: urlEncodedData
    })
    .then(response => response.text())
    .then(text => {
        // Update the output element with the received text
        outputElement.textContent = text;
        // Re-enable the button
        button.disabled = false;
        button.textContent = 'Run';
    })
    .catch(error => {
        // Log and display errors, if any
        console.error('Error:', error);
        outputElement.textContent = `Error: ${error}`;
        // Re-enable the button even if there's an error
        button.disabled = false;
        button.textContent = 'Run';
    });
});
