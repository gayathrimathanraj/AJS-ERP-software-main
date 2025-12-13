// STOP this JS file if not on material inward page
if (!window.location.pathname.includes("/ajserp/materialinward")) {
    console.log("Material Inward JS blocked on other pages");
    return;   // <-- this stops the script completely
}

// =====================================================
// GLOBAL VARIABLES
// =====================================================
let currentMaterialSuggestions = [];
let selectedMaterialSuggestionIndex = -1;

let currentGlobalSuggestions = [];
let selectedGlobalSuggestionIndex = -1;

let currentGrnSuggestions = [];
let selectedGrnSuggestionIndex = -1;

let currentBatchSuggestions = [];
let selectedBatchSuggestionIndex = -1;


// =====================================================
// MATERIAL NAME SUGGESTIONS
// =====================================================
function showMaterialNameSuggestions(query) {
    console.log('Material name query:', query);

    if (query.length < 2) {
        hideMaterialSuggestions();
        return;
    }

    fetch('/ajserp/api/material-name-suggestions/?q=' + encodeURIComponent(query))
        .then(response => response.json())
        .then(suggestions => {
            console.log('Material suggestions:', suggestions);

            const formatted = suggestions.map(name => ({
                value: name,
                text: name
            }));

            showMaterialDropdown(formatted);
        })
        .catch(error => {
            console.error('Error:', error);
            hideMaterialSuggestions();
        });
}


function showMaterialDropdown(suggestions) {
    const dropdown = document.getElementById('materialNameSuggestions');
    const input = document.getElementById('materialNameInput');

    if (!dropdown || !input) {
        console.error('Dropdown or input not found');
        return;
    }

    if (suggestions.length === 0) {
        dropdown.classList.remove('show');
        return;
    }

    currentMaterialSuggestions = suggestions;
    selectedMaterialSuggestionIndex = -1;

    let html = '';
    suggestions.forEach(s => {
        html += `
            <button type="button" class="dropdown-item"
                onclick="selectMaterialSuggestion('${s.value.replace(/'/g, "\\'")}')">
                ${s.text}
            </button>
        `;
    });

    dropdown.innerHTML = html;

    dropdown.style.position = 'absolute';
    dropdown.style.top = '100%';
    dropdown.style.left = '0';
    dropdown.style.width = '100%';
    dropdown.style.zIndex = '1060';

    dropdown.classList.add('show');
}

function hideMaterialSuggestions() {
    const dropdown = document.getElementById('materialNameSuggestions');
    if (dropdown) dropdown.classList.remove('show');
}

function selectMaterialSuggestion(value) {
    const input = document.getElementById('materialNameInput');
    if (input) {
        input.value = value;
        hideMaterialSuggestions();
    }
}

function handleMaterialKeyNavigation(e) {
    const dropdown = document.getElementById('materialNameSuggestions');
    if (!dropdown || !dropdown.classList.contains('show')) return;

    if (e.key === 'ArrowDown') {
        e.preventDefault();
        selectedMaterialSuggestionIndex = Math.min(
            selectedMaterialSuggestionIndex + 1,
            currentMaterialSuggestions.length - 1
        );
        updateMaterialSelection();
    } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        selectedMaterialSuggestionIndex = Math.max(
            selectedMaterialSuggestionIndex - 1,
            -1
        );
        updateMaterialSelection();
    } else if (e.key === 'Enter' && selectedMaterialSuggestionIndex >= 0) {
        e.preventDefault();
        selectMaterialSuggestion(
            currentMaterialSuggestions[selectedMaterialSuggestionIndex].value
        );
    } else if (e.key === 'Escape') {
        hideMaterialSuggestions();
    }
}

function updateMaterialSelection() {
    const dropdown = document.getElementById('materialNameSuggestions');
    const items = dropdown.getElementsByClassName('dropdown-item');

    for (let item of items) item.classList.remove('active');

    if (selectedMaterialSuggestionIndex >= 0) {
        items[selectedMaterialSuggestionIndex].classList.add('active');
    }
}


// =====================================================
// GLOBAL SEARCH SUGGESTIONS
// =====================================================
function showGlobalMaterialSuggestions(query) {
    if (query.length < 2) {
        hideGlobalSuggestions();
        return;
    }

    fetch('/ajserp/api/material-name-suggestions/?q=' + encodeURIComponent(query))
        .then(res => res.json())
        .then(suggestions => {
            const formatted = suggestions.map(name => ({
                value: name,
                text: name
            }));

            showGlobalDropdown(formatted);
        })
        .catch(error => {
            console.error('Error:', error);
            hideGlobalSuggestions();
        });
}

function showGlobalDropdown(suggestions) {
    const dropdown = document.getElementById('globalSearchSuggestions');
    const input = document.getElementById('globalSearchInput');

    if (!dropdown || !input) return;

    if (suggestions.length === 0) {
        dropdown.classList.remove('show');
        return;
    }

    currentGlobalSuggestions = suggestions;
    selectedGlobalSuggestionIndex = -1;

    let html = '';
    suggestions.forEach(s => {
        html += `
            <button type="button" class="dropdown-item"
                onclick="selectGlobalSuggestion('${s.value.replace(/'/g, "\\'")}')">
                ${s.text}
            </button>
        `;
    });

    dropdown.innerHTML = html;

    dropdown.style.position = 'absolute';
    dropdown.style.top = '100%';
    dropdown.style.left = '0';
    dropdown.style.width = '100%';
    dropdown.style.zIndex = '1060';

    dropdown.classList.add('show');
}

function hideGlobalSuggestions() {
    const dropdown = document.getElementById('globalSearchSuggestions');
    if (dropdown) dropdown.classList.remove('show');
}

function selectGlobalSuggestion(value) {
    const input = document.getElementById('globalSearchInput');
    if (input) {
        input.value = value;
        hideGlobalSuggestions();
        document.querySelector('form[method="GET"]').submit();
    }
}

function handleGlobalKeyNavigation(e) {
    const dropdown = document.getElementById('globalSearchSuggestions');
    if (!dropdown || !dropdown.classList.contains('show')) return;

    if (e.key === 'ArrowDown') {
        selectedGlobalSuggestionIndex = Math.min(
            selectedGlobalSuggestionIndex + 1,
            currentGlobalSuggestions.length - 1
        );
        updateGlobalSelection();

    } else if (e.key === 'ArrowUp') {
        selectedGlobalSuggestionIndex = Math.max(selectedGlobalSuggestionIndex - 1, -1);
        updateGlobalSelection();

    } else if (e.key === 'Enter' && selectedGlobalSuggestionIndex >= 0) {
        selectGlobalSuggestion(
            currentGlobalSuggestions[selectedGlobalSuggestionIndex].value
        );
    }
}

function updateGlobalSelection() {
    const dropdown = document.getElementById('globalSearchSuggestions');
    const items = dropdown.getElementsByClassName('dropdown-item');

    for (let item of items) item.classList.remove('active');

    if (selectedGlobalSuggestionIndex >= 0) {
        items[selectedGlobalSuggestionIndex].classList.add('active');
    }
}


// =====================================================
// GRN NUMBER SUGGESTIONS
// =====================================================
function showGrnSuggestions(query) {
    if (query.length < 2) {
        hideGrnSuggestions();
        return;
    }

    fetch('/ajserp/grn-number-suggestions/?q=' + encodeURIComponent(query))
        .then(res => res.json())
        .then(suggestions => {
            const formatted = suggestions.map(grn => ({
                value: grn,
                text: grn
            }));
            showGrnDropdown(formatted);
        })
        .catch(error => {
            console.error(error);
            hideGrnSuggestions();
        });
}

function showGrnDropdown(suggestions) {
    const dropdown = document.getElementById('grnNumberSuggestions');

    if (!dropdown) return;

    let html = '';
    suggestions.forEach(s => {
        html += `
            <button type="button" class="dropdown-item"
                onmousedown="event.preventDefault(); selectGrnSuggestion('${s.value.replace(/'/g, "\\'")}')">
                ${s.text}
            </button>
        `;
    });

    dropdown.innerHTML = html;
    dropdown.classList.add('show');
}

function hideGrnSuggestions() {
    const dropdown = document.getElementById('grnNumberSuggestions');
    if (dropdown) dropdown.classList.remove('show');
}

function selectGrnSuggestion(value) {
    const input = document.getElementById('grnNumberInput');
    if (input) {
        input.value = value;
        hideGrnSuggestions();
    }
}

function handleGrnKeyNavigation(e) {
    const dropdown = document.getElementById('grnNumberSuggestions');
    if (!dropdown || !dropdown.classList.contains('show')) return;

    if (e.key === 'ArrowDown') {
        selectedGrnSuggestionIndex = Math.min(
            selectedGrnSuggestionIndex + 1,
            currentGrnSuggestions.length - 1
        );
        updateGrnSelection();
    } else if (e.key === 'ArrowUp') {
        selectedGrnSuggestionIndex = Math.max(selectedGrnSuggestionIndex - 1, -1);
        updateGrnSelection();
    } else if (e.key === 'Enter' && selectedGrnSuggestionIndex >= 0) {
        selectGrnSuggestion(currentGrnSuggestions[selectedGrnSuggestionIndex].value);
    }
}

function updateGrnSelection() {
    const dropdown = document.getElementById('grnNumberSuggestions');
    const items = dropdown.getElementsByClassName('dropdown-item');

    for (let i of items) i.classList.remove('active');

    if (selectedGrnSuggestionIndex >= 0) {
        items[selectedGrnSuggestionIndex].classList.add('active');
    }
}


// =====================================================
// BATCH SUGGESTIONS
// =====================================================
function showBatchSuggestions(query) {
    if (query.length < 2) {
        hideBatchSuggestions();
        return;
    }

    fetch('/ajserp/batch-suggestions/?q=' + encodeURIComponent(query))
        .then(res => res.json())
        .then(suggestions => {
            const formatted = suggestions.map(batch => ({
                value: batch,
                text: batch
            }));
            showBatchDropdown(formatted);
        })
        .catch(error => {
            console.error(error);
            hideBatchSuggestions();
        });
}

function showBatchDropdown(suggestions) {
    const dropdown = document.getElementById('batchSuggestions');

    let html = '';
    suggestions.forEach(s => {
        html += `
            <button type="button" class="dropdown-item"
                onmousedown="event.preventDefault(); selectBatchSuggestion('${s.value.replace(/'/g, "\\'")}')">
                ${s.text}
            </button>
        `;
    });

    dropdown.innerHTML = html;
    dropdown.classList.add('show');
}

function hideBatchSuggestions() {
    const dropdown = document.getElementById('batchSuggestions');
    if (dropdown) dropdown.classList.remove('show');
}

function selectBatchSuggestion(value) {
    const input = document.getElementById('batchInput');
    if (input) {
        input.value = value;
        hideBatchSuggestions();
    }
}

function handleBatchKeyNavigation(e) {
    const dropdown = document.getElementById('batchSuggestions');
    if (!dropdown || !dropdown.classList.contains('show')) return;

    if (e.key === 'ArrowDown') {
        selectedBatchSuggestionIndex = Math.min(
            selectedBatchSuggestionIndex + 1,
            currentBatchSuggestions.length - 1
        );
        updateBatchSelection();
    } else if (e.key === 'ArrowUp') {
        selectedBatchSuggestionIndex = Math.max(selectedBatchSuggestionIndex - 1, -1);
        updateBatchSelection();
    } else if (e.key === 'Enter' && selectedBatchSuggestionIndex >= 0) {
        selectBatchSuggestion(currentBatchSuggestions[selectedBatchSuggestionIndex].value);
    }
}

function updateBatchSelection() {
    const dropdown = document.getElementById('batchSuggestions');
    const items = dropdown.getElementsByClassName('dropdown-item');

    for (let i of items) i.classList.remove('active');

    if (selectedBatchSuggestionIndex >= 0) {
        items[selectedBatchSuggestionIndex].classList.add('active');
    }
}


// =====================================================
// CLEAR SEARCH BUTTON
// =====================================================
function toggleSearchButtons(value) {
    const clearBtn = document.getElementById('clearButton');

    if (!clearBtn) return;

    if (value && value.trim() !== '') {
        clearBtn.classList.remove('clear-hidden');
        clearBtn.classList.add('clear-visible');
    } else {
        clearBtn.classList.remove('clear-visible');
        clearBtn.classList.add('clear-hidden');
    }
}

function initializeSearchButtons() {
    const input = document.getElementById('globalSearchInput');
    const clearBtn = document.getElementById('clearButton');

    if (!input || !clearBtn) return;

    if (input.value.trim() !== '') {
        clearBtn.classList.add('clear-visible');
    } else {
        clearBtn.classList.add('clear-hidden');
    }
}

function clearSearch() {
    const input = document.getElementById('globalSearchInput');
    const clearBtn = document.getElementById('clearButton');

    if (input) input.value = '';
    if (clearBtn) {
        clearBtn.classList.remove('clear-visible');
        clearBtn.classList.add('clear-hidden');
    }

    hideGlobalSuggestions();
    window.location.href = "/ajserp/material-inward/";
}


// =====================================================
// DOMContentLoaded
// =====================================================
document.addEventListener('DOMContentLoaded', () => {
    console.log("Material inward JS loaded");

    initializeSearchButtons();

    const clearBtn = document.getElementById('clearButton');
    if (clearBtn) {
        clearBtn.addEventListener('click', (e) => {
            e.preventDefault();
            clearSearch();
        });
    }

    document.addEventListener('click', (e) => {
        if (!e.target.closest('#grnNumberInput') && !e.target.closest('#grnNumberSuggestions')) {
            hideGrnSuggestions();
        }
        if (!e.target.closest('#batchInput') && !e.target.closest('#batchSuggestions')) {
            hideBatchSuggestions();
        }
    });
});
