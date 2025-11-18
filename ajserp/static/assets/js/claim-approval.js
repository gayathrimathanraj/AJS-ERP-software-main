// static/js/claim-approval.js

class ClaimApprovalManager {
    constructor() {
        this.init();
    }

    init() {
        document.addEventListener('DOMContentLoaded', () => {
            this.hideAddLineButton();
            this.hideDeleteButtons();
        });
    }

    // Remove the "Add Line" button functionality since we're displaying existing data
    hideAddLineButton() {
        const addLineBtn = document.getElementById('addLineBtn');
        if (addLineBtn) {
            addLineBtn.style.display = 'none';
        }
    }

    // Remove delete buttons from table rows
    hideDeleteButtons() {
        const deleteButtons = document.querySelectorAll('.delete-row');
        deleteButtons.forEach(button => {
            button.style.display = 'none';
        });
    }
}

// Initialize the claim approval manager
window.claimApprovalManager = new ClaimApprovalManager();