// ==================== AUTOCOMPLETE & DROPDOWN SUGGESTIONS ====================

let currentSuggestions = [];
let activeSuggestionIndex = -1;

function initializeAutocomplete() {
    const documentNoFilter = document.getElementById('documentNoFilter');
    const requestedByFilter = document.getElementById('requestedByFilter');
    const globalSearch = document.getElementById('globalSearch');

    // Document No autocomplete
    if (documentNoFilter) {
        documentNoFilter.addEventListener('input', debounce(function (e) {
            const query = e.target.value.trim();
            if (query.length >= 2) handleDocumentNoSearch(query);
            else hideSuggestions();
        }, 300));

        documentNoFilter.addEventListener('keydown', function (e) {
            handleSuggestionNavigation(e, 'documentNoFilter');
        });

        documentNoFilter.addEventListener('focus', function () {
            const query = this.value.trim();
            if (query.length >= 2) handleDocumentNoSearch(query);
        });
    }

    // Requested By autocomplete
    if (requestedByFilter) {
        requestedByFilter.addEventListener('input', debounce(function (e) {
            const query = e.target.value.trim();
            if (query.length >= 2) handleRequestedBySearch(query);
            else hideSuggestions();
        }, 300));

        requestedByFilter.addEventListener('keydown', function (e) {
            handleSuggestionNavigation(e, 'requestedByFilter');
        });

        requestedByFilter.addEventListener('focus', function () {
            const query = this.value.trim();
            if (query.length >= 2) handleRequestedBySearch(query);
        });
    }

    // Global search autocomplete
    if (globalSearch) {
        globalSearch.addEventListener('input', debounce(function (e) {
            const query = e.target.value.trim();
            if (query.length >= 2) handleGlobalSearchSuggestions(query);
            else hideSuggestions();
        }, 300));

        globalSearch.addEventListener('keydown', function (e) {
            handleSuggestionNavigation(e, 'globalSearch');
        });
    }

    // Close suggestions on outside click
    document.addEventListener('click', function (e) {
        if (!e.target.closest('.suggestions-dropdown') &&
            !e.target.closest('#documentNoFilter') &&
            !e.target.closest('#requestedByFilter') &&
            !e.target.closest('#globalSearch')) {
            hideSuggestions();
        }
    });
}

// ==================== FETCH FUNCTIONS ====================

function handleDocumentNoSearch(query) {
    fetch(`{% url 'ajserp:claim_document_numbers' %}?q=${encodeURIComponent(query)}`)
        .then(res => res.json())
        .then(data => showSuggestions('documentNoFilter', data.document_numbers || []))
        .catch(() => hideSuggestions());
}

function handleRequestedBySearch(query) {
    fetch(`{% url 'ajserp:claim_requested_by' %}?q=${encodeURIComponent(query)}`)
        .then(res => res.json())
        .then(data => showSuggestions('requestedByFilter', data.usernames || []))
        .catch(() => hideSuggestions());
}

function handleGlobalSearchSuggestions(query) {
    let suggestions = [];

    fetch(`{% url 'ajserp:claim_document_numbers' %}?q=${encodeURIComponent(query)}`)
        .then(res => res.json())
        .then(data => {
            suggestions.push(...(data.document_numbers || []));
            return fetch(`{% url 'ajserp:claim_requested_by' %}?q=${encodeURIComponent(query)}`);
        })
        .then(res => res.json())
        .then(data => {
            suggestions.push(...(data.usernames || []));
            const unique = [...new Set(suggestions)];
            showSuggestions('globalSearch', unique.slice(0, 10));
        })
        .catch(() => hideSuggestions());
}

// ==================== SHOW/HIDE SUGGESTIONS ====================

function showSuggestions(inputId, suggestions) {
    hideSuggestions();
    if (!suggestions.length) return;

    currentSuggestions = suggestions;
    activeSuggestionIndex = -1;

    const input = document.getElementById(inputId);
    const suggestionsDiv = document.createElement('div');

    suggestionsDiv.id = `${inputId}Suggestions`;
    suggestionsDiv.className = 'suggestions-dropdown';

    suggestions.forEach((suggestion, index) => {
        const item = document.createElement('div');
        item.className = 'suggestion-item';
        item.textContent = suggestion;
        item.dataset.index = index;

        item.addEventListener('click', () => {
            input.value = suggestion;
            hideSuggestions();
            if (inputId === 'globalSearch') searchClaims();
        });

        item.addEventListener('mouseenter', () => setActiveSuggestion(index));
        suggestionsDiv.appendChild(item);
    });

    document.body.appendChild(suggestionsDiv);
}

function hideSuggestions() {
    document.querySelectorAll('.suggestions-dropdown').forEach(el => el.remove());
    currentSuggestions = [];
    activeSuggestionIndex = -1;
}

// ==================== KEYBOARD NAVIGATION ====================

function handleSuggestionNavigation(e, inputId) {
    const box = document.getElementById(`${inputId}Suggestions`);
    if (!box) return;

    const items = box.querySelectorAll('.suggestion-item');

    switch (e.key) {
        case 'ArrowDown':
            e.preventDefault();
            activeSuggestionIndex = (activeSuggestionIndex + 1) % items.length;
            setActiveSuggestion(activeSuggestionIndex);
            break;

        case 'ArrowUp':
            e.preventDefault();
            activeSuggestionIndex = (activeSuggestionIndex - 1 + items.length) % items.length;
            setActiveSuggestion(activeSuggestionIndex);
            break;

        case 'Enter':
            e.preventDefault();
            if (activeSuggestionIndex >= 0) items[activeSuggestionIndex].click();
            else inputId === 'globalSearch' ? searchClaims() : filterClaims();
            break;

        case 'Escape':
        case 'Tab':
            hideSuggestions();
            break;
    }
}

function setActiveSuggestion(index) {
    const items = document.querySelectorAll('.suggestion-item');
    items.forEach(item => item.classList.remove('active'));
    if (items[index]) items[index].classList.add('active');
}

// ==================== FILTERING & SEARCH ====================

function filterClaims() {
    const params = new URLSearchParams();

    ["document_no", "requested_by", "status", "from_date", "to_date"].forEach((field, i) => {
        const ids = ["documentNoFilter", "requestedByFilter", "statusFilter", "fromDate", "toDate"];
        const value = document.getElementById(ids[i]).value;
        if (value) params.append(field, value);
    });

    performSearch(params.toString());
}

function searchClaims() {
    const params = new URLSearchParams();
    const value = document.getElementById('globalSearch').value.trim();
    if (value) params.append('global_search', value);
    performSearch(params.toString());
}

function performSearch(queryString) {
    fetch(`{% url 'ajserp:search_claims' %}?${queryString}`)
        .then(res => res.json())
        .then(data => updateTableWithResults(data.claims))
        .catch(() => {
            window.location.href = `{% url 'ajserp:claimrequest' %}?${queryString}`;
        });
}

function updateTableWithResults(claims) {
    const tbody = document.querySelector('#basic-datatables tbody');

    if (!claims.length) {
        tbody.innerHTML = `<tr><td colspan="12">No claim requests found.</td></tr>`;
        return;
    }

    let html = '';

    claims.forEach((claim, index) => {
        const item = claim.items?.[0] || {};

        html += `
        <tr>
            <td><input type="checkbox" class="rowCheckbox" data-id="${claim.id}"></td>
            <td>${index + 1}</td>
            <td><a href="{% url 'ajserp:claim_approval_page' claim_id=0 %}".replace('0', '${claim.id}')">${claim.document_number}</a></td>
            <td>${claim.requested_by || '-'}</td>
            <td>${item.type || '-'}</td>
            <td>${item.uom || '-'}</td>
            <td>${item.quantity || '-'}</td>
            <td>${item.amount || '-'}</td>
            <td>${claim.remarks || '-'}</td>
            <td>${claim.status}</td>
            <td>${claim.employee_submitted_at || '-'}</td>
            <td>
                <button onclick="editClaim('${claim.id}')">Edit</button>
                <button onclick="confirmDelete('${claim.id}')">Delete</button>
            </td>
        </tr>`;
    });

    tbody.innerHTML = html;
}

// ==================== BUTTON ACTIONS ====================

function editClaim(claimId) {
    window.location.href = `{% url 'ajserp:addclaimrequest' %}?edit=${claimId}`;
}

function confirmDelete(claimId) {
    document.getElementById('claimToDelete').value = claimId;
    new bootstrap.Modal(document.getElementById('deleteModal')).show();
}

function deleteClaim() {
    const id = document.getElementById('claimToDelete').value;

    fetch(`/ajserp/delete-claim/${id}/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken') }
    })
        .then(res => res.ok && location.reload());
}

// ==================== UTILITIES ====================

function debounce(func, wait) {
    let timeout;
    return function (...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func(...args), wait);
    };
}

function getCookie(name) {
    return document.cookie.split('; ').find(r => r.startsWith(name + '='))?.split('=')[1] || null;
}

// ==================== INIT ====================

document.addEventListener('DOMContentLoaded', function () {
    initializeAutocomplete();

    ['globalSearch', 'documentNoFilter', 'requestedByFilter'].forEach(id => {
        const input = document.getElementById(id);
        if (input) {
            input.addEventListener('keypress', function (e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    id === 'globalSearch' ? searchClaims() : filterClaims();
                }
            });
        }
    });
});
