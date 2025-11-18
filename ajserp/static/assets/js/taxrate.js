// taxrate.js - Auto-fetch HSN tax rates
function loadTaxRates() {
    // Check if we're on a page with HSN tax elements
    const taxCells = document.querySelectorAll('.tax-cell');
    if (taxCells.length === 0) {
        console.log('No tax cells found on this page, skipping tax rate loading');
        return; // Exit if no tax cells exist (like on estimate page)
    }

    // Show loading state only if elements exist
    taxCells.forEach(cell => {
        if (cell) {
            cell.innerHTML = '<span class="text-muted">Loading...</span>';
        }
    });

    fetch('/ajserp/api/get-hsn-codes-with-taxes/')
        .then(response => {
            if (!response.ok) throw new Error('Network error');
            return response.json();
        })
        .then(data => {
            // Update each row with tax rates
            data.forEach(item => {
                const cgstCell = document.getElementById(`cgst-${item.hsn_code}`);
                const sgstCell = document.getElementById(`sgst-${item.hsn_code}`);
                const igstCell = document.getElementById(`igst-${item.hsn_code}`);
                const cessCell = document.getElementById(`cess-${item.hsn_code}`);
                const row = document.getElementById(`hsn-row-${item.hsn_code}`);
                
                // Add null checks for all elements
                if (cgstCell && sgstCell && igstCell && cessCell && row) {
                    cgstCell.textContent = item.cgst + '%';
                    sgstCell.textContent = item.sgst + '%';
                    igstCell.textContent = item.igst + '%';
                    cessCell.textContent = item.cess + '%';
                    
                    // Color code based on tax existence
                    if (item.has_tax) {
                        row.classList.add('table-success');
                    } else {
                        row.classList.add('table-warning');
                        cgstCell.innerHTML = '<span class="text-muted">-</span>';
                        sgstCell.innerHTML = '<span class="text-muted">-</span>';
                        igstCell.innerHTML = '<span class="text-muted">-</span>';
                        cessCell.innerHTML = '<span class="text-muted">-</span>';
                    }
                }
            });
            
            // Show success message only if we're on the right page
            const cardHeader = document.querySelector('.card-header');
            if (cardHeader) {
                showTaxMessage('Tax rates loaded successfully!', 'success');
            }
        })
        .catch(error => {
            console.error('Failed to load tax rates:', error);
            // Only show error message if we're on the right page
            const cardHeader = document.querySelector('.card-header');
            if (cardHeader) {
                showTaxMessage('Failed to load tax rates. Please try again.', 'error');
            }
        });
}

function showTaxMessage(message, type) {
    // Remove existing messages
    const existingMsg = document.querySelector('.tax-message');
    if (existingMsg) existingMsg.remove();
    
    const alertClass = type === 'success' ? 'alert-success' : 'alert-danger';
    const messageHtml = `
        <div class="alert ${alertClass} tax-message mt-2">
            ${message}
        </div>
    `;
    
    const cardHeader = document.querySelector('.card-header');
    if (cardHeader) {
        cardHeader.insertAdjacentHTML('afterend', messageHtml);
        
        // Auto-remove after 3 seconds
        setTimeout(() => {
            const msg = document.querySelector('.tax-message');
            if (msg) msg.remove();
        }, 3000);
    }
}

// Auto-load tax rates when modal opens - with page detection
document.addEventListener("DOMContentLoaded", function() {
    const hsnModal = document.getElementById('hsnCodeModal');
    if (hsnModal) {
        hsnModal.addEventListener('show.bs.modal', function() {
            // Wait a bit for the modal to fully render, then load tax rates
            setTimeout(loadTaxRates, 500);
        });
    } else {
        console.log('HSN modal not found on this page, taxrate.js running in silent mode');
    }
});

// Make function globally available for the refresh button
window.refreshHsnTaxData = loadTaxRates;