// ==================== DROPDOWN SUGGESTIONS FOR CLAIM APPROVAL ====================

let currentSuggestions = [];
let activeSuggestionIndex = -1;
let activeInputId = null;

// Debounce Utility
function debounce(func, wait) {
    let timeout;
    return function (...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

// URL Configuration
const APPROVAL_URLS = {
    claimDocumentNumbers: null,
    claimRequestedBy: null
};

function initializeApprovalURLs() {
    const urlsData = document.getElementById('urls-data');
    if (urlsData) {
        APPROVAL_URLS.claimDocumentNumbers = urlsData.dataset.claimDocumentNumbers;
        APPROVAL_URLS.claimRequestedBy = urlsData.dataset.claimRequestedBy;
        console.log("✅ Approval URLs loaded:", APPROVAL_URLS);
    } else {
        console.error("❌ URLs data container missing!");
    }
}

// Init Autocomplete
function initializeApprovalAutocomplete() {
    initializeApprovalURLs();

    const docInput = document.getElementById('documentNoFilter');
    const reqInput = document.getElementById('requestedByFilter');

    if (docInput) {
        docInput.addEventListener("input", debounce(e => {
            const q = e.target.value.trim();
            if (q.length >= 2) handleDocumentNoSearch(q, "documentNoFilter");
            else hideSuggestions();
        }, 300));

        docInput.addEventListener("keydown", e => handleSuggestionNavigation(e, "documentNoFilter"));
    }

    if (reqInput) {
        reqInput.addEventListener("input", debounce(e => {
            const q = e.target.value.trim();
            if (q.length >= 2) handleRequestedBySearch(q, "requestedByFilter");
            else hideSuggestions();
        }, 300));

        reqInput.addEventListener("keydown", e => handleSuggestionNavigation(e, "requestedByFilter"));
    }

    // Hide when clicking outside
    document.addEventListener("click", e => {
        if (!e.target.closest(".dropdown-menu") && !e.target.closest("input")) {
            hideSuggestions();
        }
    });
}

// ==================== FETCH HANDLERS ====================

function handleDocumentNoSearch(query, inputId) {
    if (!APPROVAL_URLS.claimDocumentNumbers) return;

    const url = `${APPROVAL_URLS.claimDocumentNumbers}?q=${encodeURIComponent(query)}`;
    console.log("📡 Document search:", url);

    fetch(url)
        .then(res => res.json())
        .then(data => showApprovalSuggestions(inputId, data.document_numbers || []))
        .catch(err => console.error("❌ Document search error:", err));
}

function handleRequestedBySearch(query, inputId) {
    if (!APPROVAL_URLS.claimRequestedBy) return;

    const url = `${APPROVAL_URLS.claimRequestedBy}?q=${encodeURIComponent(query)}`;
    console.log("📡 Requested By search:", url);

    fetch(url)
        .then(res => res.json())
        .then(data => showApprovalSuggestions(inputId, data.usernames || []))
        .catch(err => console.error("❌ RequestedBy search error:", err));
}

// ==================== DISPLAY SUGGESTIONS ====================

function showApprovalSuggestions(inputId, suggestions) {
    hideSuggestions();
    if (!suggestions.length) return;

    currentSuggestions = suggestions;
    activeInputId = inputId;

    const input = document.getElementById(inputId);
    const dropdown = document.getElementById(`${inputId}Suggestions`);

    if (!dropdown) {
        console.error(`❌ Dropdown container #${inputId}Suggestions missing!`);
        return;
    }

    dropdown.innerHTML = "";
    dropdown.classList.add("show");

    suggestions.forEach((text, index) => {
        const item = document.createElement("a");
        item.className = "dropdown-item";
        item.href = "#";
        item.innerText = text;
        item.dataset.index = index;

        item.onclick = e => {
            e.preventDefault();
            input.value = text;
            hideSuggestions();
        };

        item.onmouseenter = () => setActiveSuggestion(index);

        dropdown.appendChild(item);
    });
}

// ==================== HIDE SUGGESTIONS ====================

function hideSuggestions() {
    document.querySelectorAll(".dropdown-menu").forEach(el => {
        el.classList.remove("show");
        el.innerHTML = "";
    });

    currentSuggestions = [];
    activeSuggestionIndex = -1;
    activeInputId = null;
}

// ==================== KEYBOARD NAVIGATION ====================

function handleSuggestionNavigation(e, inputId) {
    const dropdown = document.getElementById(`${inputId}Suggestions`);
    if (!dropdown || !dropdown.classList.contains("show")) return;

    const items = dropdown.querySelectorAll(".dropdown-item");

    switch (e.key) {
        case "ArrowDown":
            e.preventDefault();
            activeSuggestionIndex = Math.min(activeSuggestionIndex + 1, items.length - 1);
            setActiveSuggestion(activeSuggestionIndex);
            break;

        case "ArrowUp":
            e.preventDefault();
            activeSuggestionIndex = Math.max(activeSuggestionIndex - 1, 0);
            setActiveSuggestion(activeSuggestionIndex);
            break;

        case "Enter":
            e.preventDefault();
            if (items[activeSuggestionIndex]) items[activeSuggestionIndex].click();
            break;

        case "Escape":
            hideSuggestions();
            break;
    }
}

function setActiveSuggestion(index) {
    const dropdown = document.getElementById(`${activeInputId}Suggestions`);
    if (!dropdown) return;

    dropdown.querySelectorAll(".dropdown-item").forEach(i => i.classList.remove("active"));
    if (dropdown.children[index]) {
        dropdown.children[index].classList.add("active");
        dropdown.children[index].scrollIntoView({ block: "nearest" });
    }
}

// ==================== INIT ====================

document.addEventListener("DOMContentLoaded", () => {
    console.log("🚀 Claim Approval Autocomplete Initialized");
    initializeApprovalAutocomplete();
});
