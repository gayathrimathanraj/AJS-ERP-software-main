// =====================================================
// GLOBAL VARIABLES
// =====================================================
let currentGlobalWarehouseSuggestions = [];
let selectedGlobalWarehouseSuggestionIndex = -1;



// =====================================================
// GLOBAL WAREHOUSE SEARCH
// =====================================================
function showGlobalWarehouseSuggestions(query) {
    console.log('🔍 Global warehouse search query:', query);

    if (query.length < 2) {
        hideGlobalWarehouseSuggestions();
        return;
    }

    // FIXED FETCH URL
    fetch(`/ajserp/api/warehouse-global-suggestions/?q=${encodeURIComponent(query)}`)
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(suggestions => {
            console.log('✅ Warehouse suggestions received:', suggestions);
            showGlobalWarehouseDropdown(suggestions);
        })
        .catch(error => {
            console.error('❌ Error fetching warehouse suggestions:', error);
            hideGlobalWarehouseSuggestions();
        });
}



// =====================================================
// SHOW WAREHOUSE DROPDOWN
// =====================================================
function showGlobalWarehouseDropdown(suggestions) {
    const dropdown = document.getElementById('globalSearchSuggestions');
    const input = document.getElementById('globalSearchInput');

    if (!dropdown || !input) {
        console.error('❌ Global dropdown or input not found');
        return;
    }

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

    let dropdownHTML = '';

    suggestions.forEach((s, index) => {
        dropdownHTML += `
            <button 
                type="button" 
                class="dropdown-item" 
                data-index="${index}"
                onmousedown="selectGlobalWarehouseSuggestion('${s.value.replace(/'/g, "\\'")}')"
            >
                <strong>${s.text}</strong> 
                <small class="text-muted">(${s.type})</small>
            </button>
        `;
    });

    dropdown.innerHTML = dropdownHTML;
    dropdown.classList.add('show');

    console.log('✅ Warehouse dropdown shown with', suggestions.length, 'items');
}



// =====================================================
// HIDE WAREHOUSE DROPDOWN
// =====================================================
function hideGlobalWarehouseSuggestions() {
    const dropdown = document.getElementById('globalSearchSuggestions');

    if (dropdown) {
        dropdown.classList.remove('show');
        dropdown.innerHTML = '';
    }
}



// =====================================================
// SELECT A WAREHOUSE SUGGESTION
// =====================================================
function selectGlobalWarehouseSuggestion(value) {
    console.log('✅ Selected warehouse suggestion:', value);

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
        selectedGlobalWarehouseSuggestionIndex = Math.min(
            selectedGlobalWarehouseSuggestionIndex + 1,
            currentGlobalWarehouseSuggestions.length - 1
        );
        updateGlobalWarehouseSelection();

    } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        selectedGlobalWarehouseSuggestionIndex = Math.max(
            selectedGlobalWarehouseSuggestionIndex - 1,
            -1
        );
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
    const dropdown = document.getElementById('globalSearchSuggestions');
    const items = dropdown.getElementsByClassName('dropdown-item');

    for (let item of items) item.classList.remove('active');

    if (selectedGlobalWarehouseSuggestionIndex >= 0) {
        items[selectedGlobalWarehouseSuggestionIndex].classList.add('active');
        items[selectedGlobalWarehouseSuggestionIndex].scrollIntoView({ block: 'nearest' });
    }
}



// =====================================================
// CLEAR BUTTON
// =====================================================
function toggleSearchButtons(value) {
    const clearButton = document.getElementById('clearButton');

    if (clearButton) {
        if (value && value.trim() !== '') {
            clearButton.classList.remove('clear-hidden');
            clearButton.classList.add('clear-visible');
        } else {
            clearButton.classList.remove('clear-visible');
            clearButton.classList.add('clear-hidden');
        }
    }
}



// =====================================================
// PAGE INITIALIZATION
// =====================================================
document.addEventListener('DOMContentLoaded', function () {
    console.log('🏭 Warehouse search initialized');

    const globalInput = document.getElementById('globalSearchInput');
    const clearButton = document.getElementById('clearButton');

    if (globalInput) {
        // Replace input node to clear material listeners
        const newInput = globalInput.cloneNode(true);
        globalInput.parentNode.replaceChild(newInput, globalInput);

        const cleanInput = document.getElementById('globalSearchInput');

        cleanInput.addEventListener('input', function (e) {
            e.stopPropagation();
            showGlobalWarehouseSuggestions(e.target.value);
            toggleSearchButtons(e.target.value);
        }, true);

        cleanInput.addEventListener('keydown', function (e) {
            e.stopPropagation();
            handleGlobalWarehouseKeyNavigation(e);
        }, true);

        cleanInput.addEventListener('blur', function () {
            setTimeout(hideGlobalWarehouseSuggestions, 200);
        }, true);

        cleanInput.addEventListener('focus', function () {
            if (this.value.length >= 2) {
                showGlobalWarehouseSuggestions(this.value);
            }
        }, true);

        cleanInput.removeAttribute('oninput');
        cleanInput.removeAttribute('onkeydown');
        cleanInput.removeAttribute('onfocus');
        cleanInput.removeAttribute('onblur');
    }

    document.addEventListener('click', function (e) {
        const searchContainer = document.querySelector('.input-group.position-relative');
        if (!searchContainer || !searchContainer.contains(e.target)) {
            hideGlobalWarehouseSuggestions();
        }
    });

    if (globalInput && globalInput.value) {
        toggleSearchButtons(globalInput.value);
    }

    if (clearButton) {
        clearButton.addEventListener('click', function (e) {
            e.preventDefault();
            const input = document.getElementById('globalSearchInput');
            if (input) {
                input.value = '';
                toggleSearchButtons('');
            }
            hideGlobalWarehouseSuggestions();
            window.location.href = "/ajserp/warehouse/";
        });
    }
});



// =====================================================
// BLOCK MATERIAL SEARCH (PREVENT INTERFERENCE)
// =====================================================
function preventMaterialSearchInterference() {
    if (window.materialSearchTimeout) {
        clearTimeout(window.materialSearchTimeout);
        window.materialSearchTimeout = null;
    }

    if (typeof showMaterialSuggestions === 'function') {
        window.showMaterialSuggestions = function () {
            console.log('🚫 Material suggestions blocked on warehouse page');
            return false;
        };
    }

    if (typeof handleMaterialKeyNavigation === 'function') {
        window.handleMaterialKeyNavigation = function (e) {
            console.log('🚫 Material key navigation blocked on warehouse page');
            e.stopPropagation();
            return false;
        };
    }
}

setTimeout(preventMaterialSearchInterference, 100);
