// =====================================================
// GLOBAL VARIABLES
// =====================================================
let currentGlobalWarehouseSuggestions = [];
let selectedGlobalWarehouseSuggestionIndex = -1;


// =====================================================
// GLOBAL WAREHOUSE SEARCH
// =====================================================
function showGlobalWarehouseSuggestions(query) {
    if (query.length < 2) {
        hideGlobalWarehouseSuggestions();
        return;
    }

    fetch(`/ajserp/api/warehouse-global-suggestions/?q=${encodeURIComponent(query)}`)
        .then(response => {
            if (!response.ok) throw new Error('Failed API');
            return response.json();
        })
        .then(suggestions => {
            showGlobalWarehouseDropdown(suggestions);
        })
        .catch(() => {
            hideGlobalWarehouseSuggestions();
        });
}


// =====================================================
// SHOW WAREHOUSE DROPDOWN
// =====================================================
function showGlobalWarehouseDropdown(suggestions) {
    const dropdown = document.getElementById('globalSearchSuggestions');
    const input = document.getElementById('globalSearchInput');

    if (!dropdown || !input) return;

    dropdown.innerHTML = '';

    if (suggestions.length === 0) {
        dropdown.innerHTML = `
            <div class="dropdown-item text-muted">
                No warehouses found matching "${input.value}"
            </div>
        `;
        dropdown.classList.add('show');
        return;
    }

    currentGlobalWarehouseSuggestions = suggestions;
    selectedGlobalWarehouseSuggestionIndex = -1;

    dropdown.innerHTML = suggestions.map((s, index) => `
        <button 
            type="button"
            class="dropdown-item"
            data-index="${index}"
            onmousedown="selectGlobalWarehouseSuggestion('${s.value.replace(/'/g, "\\'")}')"
        >
            <strong>${s.text}</strong>
            <small class="text-muted">(${s.type})</small>
        </button>
    `).join('');

    dropdown.classList.add('show');
}


// =====================================================
// HIDE SUGGESTIONS
// =====================================================
function hideGlobalWarehouseSuggestions() {
    const dropdown = document.getElementById('globalSearchSuggestions');
    if (!dropdown) return;

    dropdown.classList.remove('show');
    dropdown.innerHTML = '';
}


// =====================================================
// SELECT A SUGGESTION
// =====================================================
function selectGlobalWarehouseSuggestion(value) {
    const input = document.getElementById('globalSearchInput');
    if (input) {
        input.value = value;
        hideGlobalWarehouseSuggestions();
        input.focus();
    }
}


// =====================================================
// KEYBOARD NAVIGATION
// =====================================================
function handleGlobalWarehouseKeyNavigation(e) {
    const dropdown = document.getElementById('globalSearchSuggestions');
    if (!dropdown || !dropdown.classList.contains('show')) return;

    if (e.key === 'ArrowDown') {
        e.preventDefault();
        selectedGlobalWarehouseSuggestionIndex =
            Math.min(selectedGlobalWarehouseSuggestionIndex + 1, currentGlobalWarehouseSuggestions.length - 1);
        updateGlobalWarehouseSelection();

    } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        selectedGlobalWarehouseSuggestionIndex =
            Math.max(selectedGlobalWarehouseSuggestionIndex - 1, -1);
        updateGlobalWarehouseSelection();

    } else if (e.key === 'Enter' && selectedGlobalWarehouseSuggestionIndex >= 0) {
        e.preventDefault();
        selectGlobalWarehouseSuggestion(
            currentGlobalWarehouseSuggestions[selectedGlobalWarehouseSuggestionIndex].value
        );

    } else if (e.key === 'Escape') {
        hideGlobalWarehouseSuggestions();
    }
}

function updateGlobalWarehouseSelection() {
    const items = document.querySelectorAll('#globalSearchSuggestions .dropdown-item');
    items.forEach(item => item.classList.remove('active'));

    if (selectedGlobalWarehouseSuggestionIndex >= 0) {
        const item = items[selectedGlobalWarehouseSuggestionIndex];
        if (item) {
            item.classList.add('active');
            item.scrollIntoView({ block: 'nearest' });
        }
    }
}


// =====================================================
// CLEAR BUTTON
// =====================================================
function toggleSearchButtons(value) {
    const clearButton = document.getElementById('clearButton');
    if (!clearButton) return;

    if (value.trim() !== '') {
        clearButton.classList.remove('clear-hidden');
        clearButton.classList.add('clear-visible');
    } else {
        clearButton.classList.add('clear-hidden');
        clearButton.classList.remove('clear-visible');
    }
}


// =====================================================
// INITIALIZATION ON PAGE LOAD
// =====================================================
document.addEventListener('DOMContentLoaded', function () {
    const globalInput = document.getElementById('globalSearchInput');
    const clearButton = document.getElementById('clearButton');

    if (globalInput) {
        // Reset existing listeners (prevents conflicts)
        const newInput = globalInput.cloneNode(true);
        globalInput.parentNode.replaceChild(newInput, globalInput);
        const cleanInput = document.getElementById('globalSearchInput');

        cleanInput.addEventListener('input', function (e) {
            showGlobalWarehouseSuggestions(e.target.value);
            toggleSearchButtons(e.target.value);
        });

        cleanInput.addEventListener('keydown', function (e) {
            handleGlobalWarehouseKeyNavigation(e);
        });

        cleanInput.addEventListener('blur', function () {
            setTimeout(hideGlobalWarehouseSuggestions, 200);
        });

        cleanInput.addEventListener('focus', function () {
            if (this.value.length >= 2) {
                showGlobalWarehouseSuggestions(this.value);
            }
        });
    }

    // Close on outside click
    document.addEventListener('click', function (e) {
        const container = document.querySelector('.input-group.position-relative');
        if (!container || !container.contains(e.target)) {
            hideGlobalWarehouseSuggestions();
        }
    });

    // Clear button logic
    if (clearButton) {
        clearButton.addEventListener('click', function () {
            const input = document.getElementById('globalSearchInput');
            if (input) input.value = '';

            hideGlobalWarehouseSuggestions();
            toggleSearchButtons('');
            window.location.href = "/ajserp/warehouse/";  // FINAL FIX
        });
    }
});


// =====================================================
// BLOCK MATERIAL SEARCH INTERFERENCE
// =====================================================
function preventMaterialSearchInterference() {
    window.showMaterialSuggestions = () => false;
    window.handleMaterialKeyNavigation = () => false;
}

setTimeout(preventMaterialSearchInterference, 100);
