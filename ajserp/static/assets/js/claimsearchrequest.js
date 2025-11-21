// ==================== URL CONFIGURATION ====================

const URLS = {
    claimDocumentNumbers: null,
    claimRequestedBy: null,
    searchClaims: null,
    claimApprovalPage: null,
    claimRequest: null
};

function initializeURLs() {
    const urlsData = document.getElementById('urls-data');

    if (!urlsData) {
        console.error("URLs data container (#urls-data) not found!");
        return;
    }

    URLS.claimDocumentNumbers = urlsData.dataset.claimDocumentNumbers;
    URLS.claimRequestedBy = urlsData.dataset.claimRequestedBy;
    URLS.searchClaims = urlsData.dataset.searchClaims;
    URLS.claimApprovalPage = urlsData.dataset.claimApprovalPage;
    URLS.claimRequest = urlsData.dataset.claimrequest;

    console.log("URLs Initialized:", URLS);
}



// ==================== AUTOCOMPLETE & SUGGESTIONS ====================

let currentSuggestions = [];
let activeSuggestionIndex = -1;
let currentSuggestionsDiv = null;

function initializeAutocomplete() {
    const documentNoFilter = document.getElementById('documentNoFilter');
    const requestedByFilter = document.getElementById('requestedByFilter');
    const globalSearch = document.getElementById('globalSearch');

    // Document No Autocomplete
    if (documentNoFilter) {
        documentNoFilter.addEventListener('input', debounce(e => {
            const query = e.target.value.trim();
            query.length >= 2
                ? handleDocumentNoSearch(query, documentNoFilter)
                : hideSuggestions();
        }, 300));

        documentNoFilter.addEventListener('keydown', e =>
            handleSuggestionNavigation(e, 'documentNoFilter')
        );
    }

    // Requested By Autocomplete
    if (requestedByFilter) {
        requestedByFilter.addEventListener('input', debounce(e => {
            const query = e.target.value.trim();
            query.length >= 2
                ? handleRequestedBySearch(query, requestedByFilter)
                : hideSuggestions();
        }, 300));

        requestedByFilter.addEventListener('keydown', e =>
            handleSuggestionNavigation(e, 'requestedByFilter')
        );
    }

    // Global Search Autocomplete
    if (globalSearch) {
        globalSearch.addEventListener('input', debounce(e => {
            const query = e.target.value.trim();
            query.length >= 2
                ? handleGlobalSearchSuggestions(query, globalSearch)
                : hideSuggestions();
        }, 300));

        globalSearch.addEventListener('keydown', e =>
            handleSuggestionNavigation(e, 'globalSearch')
        );
    }

    // Hide suggestions when clicking outside
    document.addEventListener('click', e => {
        if (!e.target.classList.contains('suggestion-item-bootstrap') &&
            !e.target.matches('#documentNoFilter, #requestedByFilter, #globalSearch')) {
            hideSuggestions();
        }
    });

    window.addEventListener('scroll', updateSuggestionsPosition, true);
    window.addEventListener('resize', updateSuggestionsPosition);
}



// ==================== FETCH HANDLERS ====================

function handleDocumentNoSearch(query, inputElement) {
    if (!URLS.claimDocumentNumbers) return;

    fetch(`${URLS.claimDocumentNumbers}?q=${encodeURIComponent(query)}`)
        .then(r => r.json())
        .then(d => showSuggestions('documentNoFilter', d.document_numbers || [], inputElement))
        .catch(hideSuggestions);
}

function handleRequestedBySearch(query, inputElement) {
    if (!URLS.claimRequestedBy) return;

    fetch(`${URLS.claimRequestedBy}?q=${encodeURIComponent(query)}`)
        .then(r => r.json())
        .then(d => showSuggestions('requestedByFilter', d.usernames || [], inputElement))
        .catch(hideSuggestions);
}

function handleGlobalSearchSuggestions(query, inputElement) {
    const suggestions = [];

    fetch(`${URLS.claimDocumentNumbers}?q=${encodeURIComponent(query)}`)
        .then(r => r.json())
        .then(d => {
            suggestions.push(...(d.document_numbers || []));
            return fetch(`${URLS.claimRequestedBy}?q=${encodeURIComponent(query)}`);
        })
        .then(r => r.json())
        .then(d => {
            suggestions.push(...(d.usernames || []));
            const unique = [...new Set(suggestions)];
            showSuggestions('globalSearch', unique.slice(0, 10), inputElement);
        })
        .catch(hideSuggestions);
}



// ==================== SUGGESTION DROPDOWN ====================

function showSuggestions(inputId, suggestions, inputElement) {
    hideSuggestions();
    if (!suggestions.length) return;

    currentSuggestions = suggestions;
    activeSuggestionIndex = -1;

    const input = inputElement || document.getElementById(inputId);

    currentSuggestionsDiv = document.createElement('div');
    currentSuggestionsDiv.id = `${inputId}Suggestions`;
    currentSuggestionsDiv.dataset.inputId = inputId;
    currentSuggestionsDiv.className = "position-absolute bg-white border border-secondary rounded shadow mt-1 overflow-auto";
    currentSuggestionsDiv.style.maxHeight = "200px";
    currentSuggestionsDiv.style.zIndex = "1060";

    suggestions.forEach((text, index) => {
        const div = document.createElement('div');
        div.className = "p-2 border-bottom border-light suggestion-item-bootstrap text-dark";
        div.textContent = text;
        div.style.cursor = "pointer";
        div.dataset.index = index;

        div.onclick = () => {
            input.value = text;
            hideSuggestions();
            if (inputId === "globalSearch") searchClaims();
        };

        div.onmouseenter = () => setActiveSuggestion(index);
        currentSuggestionsDiv.appendChild(div);
    });

    updateSuggestionsPositionForInput(input, currentSuggestionsDiv);
    document.body.appendChild(currentSuggestionsDiv);
}

function hideSuggestions() {
    document.querySelectorAll('.position-absolute.bg-white.border').forEach(el => el.remove());
    currentSuggestions = [];
    currentSuggestionsDiv = null;
    activeSuggestionIndex = -1;
}

function updateSuggestionsPosition() {
    if (!currentSuggestionsDiv) return;

    const inputId = currentSuggestionsDiv.dataset.inputId;
    const input = document.getElementById(inputId);

    if (!input) return;

    const rect = input.getBoundingClientRect();
    currentSuggestionsDiv.style.width = `${rect.width}px`;
    currentSuggestionsDiv.style.left = `${rect.left + window.pageXOffset}px`;
    currentSuggestionsDiv.style.top = `${rect.bottom + window.pageYOffset}px`;
}

function updateSuggestionsPositionForInput(input, div) {
    const rect = input.getBoundingClientRect();
    div.style.width = `${rect.width}px`;
    div.style.left = `${rect.left + window.pageXOffset}px`;
    div.style.top = `${rect.bottom + window.pageYOffset}px`;
}

function handleSuggestionNavigation(e, inputId) {
    const suggestionsDiv = document.getElementById(`${inputId}Suggestions`);
    if (!suggestionsDiv) return;

    const items = suggestionsDiv.querySelectorAll('.suggestion-item-bootstrap');

    switch (e.key) {
        case "ArrowDown":
            e.preventDefault();
            activeSuggestionIndex = (activeSuggestionIndex + 1) % items.length;
            setActiveSuggestion(activeSuggestionIndex);
            break;

        case "ArrowUp":
            e.preventDefault();
            activeSuggestionIndex = (activeSuggestionIndex - 1 + items.length) % items.length;
            setActiveSuggestion(activeSuggestionIndex);
            break;

        case "Enter":
            e.preventDefault();
            if (activeSuggestionIndex >= 0) items[activeSuggestionIndex].click();
            else inputId === "globalSearch" ? searchClaims() : filterClaims();
            break;

        case "Escape":
            hideSuggestions();
            break;
    }
}

function setActiveSuggestion(index) {
    if (!currentSuggestionsDiv) return;

    const items = currentSuggestionsDiv.querySelectorAll('.suggestion-item-bootstrap');
    items.forEach(item => item.classList.remove('bg-primary', 'text-white'));

    const active = items[index];
    if (active) {
        active.classList.add('bg-primary', 'text-white');
        active.scrollIntoView({ block: 'nearest' });
    }

    activeSuggestionIndex = index;
}



// ==================== SEARCH FUNCTIONS ====================

function filterClaims() {
    const params = new URLSearchParams({
        document_no: document.getElementById('documentNoFilter').value || "",
        requested_by: document.getElementById('requestedByFilter').value || "",
        status: document.getElementById('statusFilter').value || "",
        from_date: document.getElementById('fromDate').value || "",
        to_date: document.getElementById('toDate').value || ""
    });

    performSearch(params.toString());
}

function clearFilters() {
    ['documentNoFilter', 'requestedByFilter', 'statusFilter', 'fromDate', 'toDate', 'globalSearch']
        .forEach(id => document.getElementById(id).value = '');

    performSearch('');
}

function searchClaims() {
    const query = document.getElementById('globalSearch').value.trim();
    const params = new URLSearchParams();

    if (query) params.append('global_search', query);

    performSearch(params.toString());
}

function performSearch(queryString) {
    if (!URLS.searchClaims) {
        window.location.href = `${URLS.claimRequest}?${queryString}`;
        return;
    }

    const tbody = document.querySelector('#basic-datatables tbody');
    tbody.innerHTML = `<tr><td colspan="12" class="text-center"><div class="spinner-border spinner-border-sm"></div> Loading...</td></tr>`;

    fetch(`${URLS.searchClaims}?${queryString}`)
        .then(r => r.json())
        .then(d => updateTableWithResults(d.claims))
        .catch(() => window.location.href = `${URLS.claimRequest}?${queryString}`);
}



// ==================== UPDATE TABLE ====================

function updateTableWithResults(claims) {
    const tbody = document.querySelector('#basic-datatables tbody');
    if (!claims || claims.length === 0) {
        tbody.innerHTML = `<tr><td colspan="12" class="text-center">No claim requests found.</td></tr>`;
        return;
    }

    tbody.innerHTML = claims.map((claim, index) => {
        const first = claim.items?.[0] || {};
        const approvalUrl = URLS.claimApprovalPage.replace("0", claim.id);

        return `
        <tr>
            <td class="p-0"><input type="checkbox" class="rowCheckbox" data-id="${claim.id}"></td>
            <td>${index + 1}</td>
            <td><a href="${approvalUrl}" class="fw-bold text-decoration-none">${claim.document_number}</a></td>
            <td>${claim.requested_by || '-'}</td>
            <td>${first.type || '-'}</td>
            <td>${first.uom || '-'}</td>
            <td>${first.quantity || '-'}</td>
            <td>₹${first.amount || '0'}</td>
            <td>${claim.remarks || '-'}</td>
            <td><span class="badge ${getStatusBadgeClass(claim.status)}">${(claim.status || "Pending")}</span></td>
            <td class="small">
                <strong>Submitted:</strong><br>${claim.employee_submitted_at || "-"}<br>
                ${claim.manager_action_at ? `<strong>Latest:</strong><br>${claim.manager_action_type}: ${claim.manager_action_at}` : ""}
            </td>
            <td>
                <div class="btn-group btn-group-sm">
                    <button class="btn btn-link text-primary" onclick="editClaim('${claim.id}')"><i class="fa fa-edit"></i></button>
                    <button class="btn btn-link text-danger" onclick="confirmDelete('${claim.id}')"><i class="fa fa-times"></i></button>
                </div>
            </td>
        </tr>`;
    }).join('');
}

function getStatusBadgeClass(status) {
    switch ((status || "").toLowerCase()) {
        case "pending": return "bg-warning";
        case "approved": return "bg-success";
        case "rejected": return "bg-danger";
        case "query_raised": return "bg-info";
        case "paid": return "bg-primary";
        default: return "bg-secondary";
    }
}



// ==================== BUTTON OPERATIONS ====================

function editClaim(id) {
    window.location.href = `/ajserp/addclaimrequest/?edit=${id}`;
}

function confirmDelete(id) {
    document.getElementById("claimToDelete").value = id;
    new bootstrap.Modal(document.getElementById("deleteModal")).show();
}

function deleteClaim() {
    const id = document.getElementById("claimToDelete").value;

    fetch(`/ajserp/delete-claim/${id}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "X-Requested-With": "XMLHttpRequest"
        }
    })
        .then(r => r.ok ? location.reload() : alert("Error deleting claim"))
        .catch(() => alert("Error deleting claim"));
}



// ==================== UTILITIES ====================

function debounce(fn, delay) {
    let timeout;
    return (...args) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => fn.apply(this, args), delay);
    };
}

function getCookie(name) {
    const v = `; ${document.cookie}`;
    const parts = v.split(`; ${name}=`);
    return parts.length === 2 ? decodeURIComponent(parts.pop().split(";").shift()) : "";
}



// ==================== INIT ====================

document.addEventListener('DOMContentLoaded', () => {
    console.log("Claim Request JS Loaded");

    initializeURLs();
    initializeAutocomplete();
    initializeEventListeners();

    // ENTER key triggers search
    ['documentNoFilter', 'requestedByFilter', 'globalSearch'].forEach(id => {
        const element = document.getElementById(id);
        if (!element) return;

        element.addEventListener('keypress', e => {
            if (e.key === 'Enter') {
                e.preventDefault();
                id === "globalSearch" ? searchClaims() : filterClaims();
            }
        });
    });

    document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => new bootstrap.Tooltip(el));
});



// ==================== EVENT LISTENERS ====================

function initializeEventListeners() {
    document.getElementById('filterClaimsBtn')?.addEventListener('click', filterClaims);
    document.getElementById('clearFiltersBtn')?.addEventListener('click', clearFilters);
    document.getElementById('globalSearchBtn')?.addEventListener('click', searchClaims);
}



// ==================== MODAL FUNCTIONS ====================

function saveClaimApproval() { alert("Save functionality to be implemented."); }
function approveClaim() { alert("Approve functionality to be implemented."); }
function rejectClaim() { alert("Reject functionality to be implemented."); }
function raiseQuery() { alert("Raise query functionality to be implemented."); }

