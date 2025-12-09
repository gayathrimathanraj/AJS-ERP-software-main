// Email sending functionality
// Note: call this from your button like: onclick="sendReceiptEmail({{ receipt.id }}, event)"
async function sendReceiptEmail(receiptId, event) {
    // keep a reference to the button and original content
    const button = event ? event.target : null;
    const originalHTML = button ? button.innerHTML : null;

    try {
        // form id uses template literal; ensure your template uses the same id
        const form = document.getElementById(`emailForm${receiptId}`);
        if (!form) throw new Error('Email form not found');

        const formData = new FormData(form);

        // Show loading (if button present)
        if (button) {
            button.innerHTML = '<i class="fa fa-spinner fa-spin"></i> Sending...';
            button.disabled = true;
        }

        // Send request (do NOT include Content-Type header when sending FormData)
        const response = await fetch(`/ajserp/send-receipt-email/${receiptId}/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken') || getCSRFToken()
            }
        });

        const result = await response.json().catch(() => ({}));

        if (response.ok) {
            alert('✅ Receipt sent via email successfully!');
            // Close modal if present
            const modalEl = document.getElementById(`emailModal${receiptId}`);
            if (modalEl) {
                const modalInstance = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
                modalInstance.hide();
            }
        } else {
            alert('❌ Error: ' + (result.error || 'Failed to send email'));
        }
    } catch (error) {
        console.error('Email send error:', error);
        alert('❌ Failed to send email. Please try again.');
    } finally {
        // Restore button
        if (button && originalHTML !== null) {
            button.innerHTML = originalHTML;
            button.disabled = false;
        }
    }
}

// Bulk email sending
async function sendBulkEmails() {
    // collect selected receipt ids
    const selectedReceipts = Array.from(document.querySelectorAll('.rowCheckbox:checked'))
        .map(checkbox => checkbox.value);

    if (selectedReceipts.length === 0) {
        alert('Please select at least one receipt');
        return;
    }

    const email = prompt('Enter recipient email address:');
    if (!email) return;

    if (!confirm(`Send ${selectedReceipts.length} receipt(s) to ${email}?`)) return;

    try {
        // Using URLSearchParams (application/x-www-form-urlencoded)
        const formData = new URLSearchParams();
        formData.append('email', email);
        selectedReceipts.forEach(id => formData.append('receipt_ids[]', id));

        const csrf = getCSRFToken();
        if (!csrf) throw new Error('CSRF token not found');

        const response = await fetch('/ajserp/send-bulk-receipts-email/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrf,
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            },
            body: formData.toString()
        });

        const result = await response.json().catch(() => ({}));

        if (response.ok) {
            alert(`✅ ${result.message || 'Bulk emails sent successfully'}`);
        } else {
            alert('❌ Error: ' + (result.error || 'Failed to send bulk emails'));
        }
    } catch (error) {
        console.error('Bulk email error:', error);
        alert('❌ Failed to send bulk emails');
    }
}

// Row selection functions
function selectAllRows() {
    document.querySelectorAll('.rowCheckbox').forEach(checkbox => {
        checkbox.checked = true;
    });
}

function deselectAllRows() {
    document.querySelectorAll('.rowCheckbox').forEach(checkbox => {
        checkbox.checked = false;
    });
}

function getCSRFToken() {
    // Try form input, then cookie fallback
    const input = document.querySelector('[name=csrfmiddlewaretoken]');
    if (input && input.value) return input.value;

    // Cookie fallback (Django default name: csrftoken)
    const match = document.cookie.match(/(^|;)\s*csrftoken=([^;]+)/);
    return match ? match.pop() : null;
}

// Initialize select all checkbox
document.addEventListener('DOMContentLoaded', function() {
    const selectAll = document.getElementById('selectAll');
    if (selectAll) {
        selectAll.addEventListener('change', function() {
            document.querySelectorAll('.rowCheckbox').forEach(checkbox => {
                checkbox.checked = this.checked;
            });
        });
    }
});
