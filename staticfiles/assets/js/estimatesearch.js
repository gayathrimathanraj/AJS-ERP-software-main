// Global variables
let currentSuggestions = [];
let selectedSuggestionIndex = -1;
let currentSuggestionType = '';

// ===== SUGGESTION FUNCTIONS =====
function showOrderNumberSuggestions(query) {
    console.log('Sales Order number query:', query);
    if (query.length < 1) {
        hideSuggestions('orderNumber');
        return;
    }
    
    fetch(`/ajserp/api/get-sales-order-suggestions/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(suggestions => {
            console.log('Sales Order suggestions:', suggestions);
            showDropdown('orderNumber', suggestions);
        })
        .catch(error => {
            console.error('Error:', error);
            hideSuggestions('orderNumber');
        });
}

function showCustomerNameSuggestions(query) {
    console.log('Customer name query:', query);
    if (query.length < 1) {
        hideSuggestions('customerName');
        return;
    }
    
    fetch(`/ajserp/api/get-customer-suggestions/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(suggestions => {
            console.log('Customer suggestions:', suggestions);
            showDropdown('customerName', suggestions);
        })
        .catch(error => {
            console.error('Error:', error);
            hideSuggestions('customerName');
        });
}

function showGlobalSuggestions(query) {
    console.log('Global query:', query);
    if (query.length < 2) {
        hideSuggestions('global');
        return;
    }
    
    fetch(`/ajserp/api/get-global-suggestions/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(suggestions => {
            console.log('Global suggestions:', suggestions);
            showDropdown('global', suggestions);
        })
        .catch(error => {
            console.error('Error:', error);
            hideSuggestions('global');
        });
}

// ===== DROPDOWN MANAGEMENT =====
function showDropdown(type, suggestions) {
    const dropdown = document.getElementById(type + 'Suggestions');
    console.log('Showing dropdown:', type, suggestions);
    
    if (!dropdown) {
        console.error('Dropdown not found:', type + 'Suggestions');
        return;
    }
    
    if (suggestions.length === 0) {
        dropdown.classList.remove('show');
        return;
    }
    
    currentSuggestions = suggestions;
    selectedSuggestionIndex = -1;
    currentSuggestionType = type;
    
    // Build dropdown items
    let dropdownHTML = '';
    suggestions.forEach((suggestion, index) => {
        dropdownHTML += `
            <button type="button" class="dropdown-item" onclick="selectSuggestion('${type}', '${suggestion.value.replace(/'/g, "\\'")}')">
                ${suggestion.text}
            </button>
        `;
    });
    
    dropdown.innerHTML = dropdownHTML;
    dropdown.classList.add('show');
    console.log('Dropdown shown with', suggestions.length, 'items');
}

function hideSuggestions(type) {
    const dropdown = document.getElementById(type + 'Suggestions');
    if (dropdown) {
        dropdown.classList.remove('show');
    }
}

function hideAllSuggestions() {
    hideSuggestions('global');
    hideSuggestions('orderNumber');
    hideSuggestions('customerName');
}

function selectSuggestion(type, value) {
    console.log('Selected suggestion:', type, value);
    let input;
    if (type === 'global') {
        input = document.getElementById('globalSearchInput');
    } else if (type === 'orderNumber') {
        input = document.getElementById('orderNumberInput');
    } else if (type === 'customerName') {
        input = document.getElementById('customerNameInput');
    }
    
    if (input) {
        input.value = value;
        hideSuggestions(type);
        
        if (type === 'global') {
            performGlobalSearch();
        } else {
            document.getElementById('filterForm').submit();
        }
    }
}

// ===== GLOBAL SEARCH =====
function performGlobalSearch() {
    const searchValue = document.getElementById('globalSearchInput').value;
    if (searchValue.trim() !== '') {
        window.location.href = `?q=${encodeURIComponent(searchValue)}`;
    }
}

// ===== EVENT LISTENERS =====
document.addEventListener('DOMContentLoaded', function() {
    console.log('Estimate search initialized');
    
    // Click outside to close
    document.addEventListener('click', function(e) {
        if (!e.target.matches('.form-control') && !e.target.closest('.dropdown-menu')) {
            hideAllSuggestions();
        }
    });
    
    // Enter key handlers
    const globalInput = document.getElementById('globalSearchInput');
    const estimateInput = document.getElementById('orderNumberInput');
    const customerInput = document.getElementById('customerNameInput');
    
    if (globalInput) {
        globalInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                performGlobalSearch();
            }
        });
    }
    
    if (estimateInput) {
        estimateInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                document.getElementById('filterForm').submit();
            }
        });
    }
    
    if (customerInput) {
        customerInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                document.getElementById('filterForm').submit();
            }
        });
    }
});