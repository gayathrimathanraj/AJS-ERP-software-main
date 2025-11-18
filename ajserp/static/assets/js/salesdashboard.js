document.addEventListener('DOMContentLoaded', function() {
    // Check-in/Check-out functionality
    document.querySelectorAll('.check-in-btn').forEach(button => {
        button.addEventListener('click', function() {
            const trackerId = this.getAttribute('data-tracker-id');
            const action = this.getAttribute('data-action');
            const workForm = document.getElementById(`workForm${trackerId}`);
            
            if (action === 'check_in') {
                // Perform check-in
                fetch(`/tracker/${trackerId}/check-in-out/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: `action=check_in`
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        this.textContent = 'Check-out';
                        this.classList.remove('btn-primary');
                        this.classList.add('btn-danger');
                        this.setAttribute('data-action', 'check_out');
                        workForm.style.display = 'block';
                        alert(data.message);
                    } else {
                        alert('Error: ' + data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Error performing check-in');
                });
            } else {
                // Check-out will be handled by the work completion form
                alert('Please fill the work completion form below and submit for check-out.');
            }
        });
    });

    // Work completion form submission
    document.querySelectorAll('.work-completion-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const trackerId = this.getAttribute('data-tracker-id');
            const formData = new FormData(this);
            formData.append('action', 'check_out');

            fetch(`/tracker/${trackerId}/check-in-out/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    const button = document.querySelector(`.check-in-btn[data-tracker-id="${trackerId}"]`);
                    button.textContent = 'Check-in';
                    button.classList.remove('btn-danger');
                    button.classList.add('btn-primary');
                    button.setAttribute('data-action', 'check_in');
                    this.style.display = 'none';
                    alert(data.message);
                } else {
                    alert('Error: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error performing check-out');
            });
        });
    });

    // CSRF token function
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});