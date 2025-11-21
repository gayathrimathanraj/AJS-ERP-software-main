// static/js/claim-form.js

class ClaimFormManager {
    constructor() {
        this.init();
    }

    init() {
        document.addEventListener('DOMContentLoaded', () => {
            // Add line functionality
            const addLineBtn = document.getElementById('addLineBtn');
            if (addLineBtn) {
                addLineBtn.addEventListener('click', () => this.addItem());
            }
            
            // Form submission
            const claimForm = document.getElementById('claimForm');
            if (claimForm) {
                claimForm.addEventListener('submit', (event) => this.handleFormSubmit(event));
            }
            
            // Cancel button
            const cancelBtn = document.getElementById('cancelBtn');
            if (cancelBtn) {
                cancelBtn.addEventListener('click', () => {
                    window.location.href = document.querySelector('a[href*="claimrequest"]')?.href || '/ajserp/claimrequest/';
                });
            }
        });
    }

    // Update item indices when adding/removing items
    updateItemIndices() {
        const rows = document.querySelectorAll('#itemsTableBody tr');
        rows.forEach((row, index) => {
            const inputs = row.querySelectorAll('input, select');
            inputs.forEach(input => {
                const name = input.name;
                input.name = name.replace(/items\[\d+\]/, `items[${index}]`);
            });
            // Update row number
            row.cells[0].textContent = index + 1;
        });
    }

    // Add new item row
    addItem() {
        const tbody = document.getElementById('itemsTableBody');
        if (!tbody) return;
        
        const rowCount = tbody.children.length;
        
        const newRow = document.createElement('tr');
        newRow.innerHTML = `
            <td>${rowCount + 1}</td>
            <td style="padding: 8px 2px !important">
                <select class="form-select form-select-sm" name="items[${rowCount}][type]" required>
                    <option value="">Select Type</option>
                    <option value="petrol">Petrol</option>
                    <option value="diesel">Diesel</option>
                    <option value="oil">Oil</option>
                    <option value="other">Other</option>
                </select>
            </td>
            <td>
                <input type="text" class="form-control form-control-sm" name="items[${rowCount}][uom]" placeholder="UOM" required />
            </td>
            <td>
                <input type="number" class="form-control form-control-sm" name="items[${rowCount}][quantity]" step="0.01" min="0" placeholder="Quantity" required />
            </td>
            <td>
                <input type="number" class="form-control form-control-sm" name="items[${rowCount}][amount]" step="0.01" min="0" placeholder="Amount" required />
            </td>
            <td>
                <input type="text" class="form-control form-control-sm" name="items[${rowCount}][remarks]" placeholder="Remarks" />
            </td>
            <td>
                <input type="file" class="form-control form-control-sm" name="items[${rowCount}][document]" />
            </td>
            <td>
                <button type="button" class="btn btn-sm btn-danger delete-row" onclick="claimFormManager.removeItem(this)">X</button>
            </td>
        `;
        tbody.appendChild(newRow);
        this.updateItemIndices();
    }

    // Remove item row
    removeItem(button) {
        const row = button.closest('tr');
        const rows = document.querySelectorAll('#itemsTableBody tr');
        
        if (rows.length > 1) {
            row.remove();
            this.updateItemIndices();
        } else {
            alert('At least one item is required.');
        }
    }

    handleFormSubmit(event) {
        event.preventDefault();
        
        // Validate at least one complete item
        const rows = document.querySelectorAll('#itemsTableBody tr');
        let hasValidItem = false;
        
        for (let row of rows) {
            const type = row.querySelector('select[name*="type"]').value;
            const uom = row.querySelector('input[name*="uom"]').value;
            const quantity = row.querySelector('input[name*="quantity"]').value;
            const amount = row.querySelector('input[name*="amount"]').value;
            
            if (type && uom && quantity && amount) {
                hasValidItem = true;
                break;
            }
        }
        
        if (!hasValidItem) {
            alert('Please fill at least one complete claim item (Type, UOM, Quantity, and Amount are required).');
            return;
        }
        
        // Submit the form
        event.target.submit();
    }

    clearForm() {
        const claimForm = document.getElementById('claimForm');
        if (!claimForm) return;
        
        claimForm.reset();
        
        // Clear all rows except the first one
        const tbody = document.getElementById('itemsTableBody');
        if (!tbody) return;
        
        while (tbody.children.length > 1) {
            tbody.removeChild(tbody.lastChild);
        }
        
        // Clear the first row
        const firstRow = tbody.querySelector('tr');
        if (firstRow) {
            firstRow.querySelector('select[name*="type"]').value = '';
            firstRow.querySelector('input[name*="uom"]').value = '';
            firstRow.querySelector('input[name*="quantity"]').value = '';
            firstRow.querySelector('input[name*="amount"]').value = '';
            firstRow.querySelector('input[name*="remarks"]').value = '';
            const fileInput = firstRow.querySelector('input[name*="document"]');
            if (fileInput) fileInput.value = '';
        }
        
        this.updateItemIndices();
    }
}

// Initialize the claim form manager
window.claimFormManager = new ClaimFormManager();