function validateForm(event) {
    event.preventDefault(); // Prevent the form from being submitted by default
    var status = true;
    // Get form field values
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (username.length < 3) {
        Message('Username must be at least 3 characters long.', 'Error', 'error');

        status = false;
    }

    if (password.length < 4) {

        Message('Password must be at least 6 characters long.', 'Error', 'error');
        status = false;
    // Exit the function, form submission is prevented
    }
    if (status) {
        // If validation passes, allow the form to be submitted
            document.getElementById('Form').submit();
    }
}