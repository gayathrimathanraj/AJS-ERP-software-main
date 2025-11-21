// ========================================================
// GLOBAL VARIABLES
// ========================================================
let activeDropdown = null;
let searchTimeout = null;

document.addEventListener("DOMContentLoaded", function () {
    initializeSearchFunctionality();
});

// ========================================================
// INITIALIZE
// ========================================================
function initializeSearchFunctionality() {
    console.log("🔍 Initializing receipt search...");

    // ----------------------------
    // Collection ID Search
    // ----------------------------
    const collectionIdSearch = document.getElementById("collectionIdSearch");

    if (collectionIdSearch) {
        collectionIdSearch.addEventListener("input", function () {
            if (searchTimeout) clearTimeout(searchTimeout);

            searchTimeout = setTimeout(() => {
                handleCollectionIdSearch(this.value);
            }, 300);
        });

        console.log("✅ Collection ID search initialized");
    }

    // ----------------------------
    // Customer Name Search
    // ----------------------------
    const customerNameSearch = document.getElementById("customerNameSearch");

    if (customerNameSearch) {
        customerNameSearch.addEventListener("input", function () {
            if (searchTimeout) clearTimeout(searchTimeout);

            searchTimeout = setTimeout(() => {
                handleCustomerNameSearch(this.value);
            }, 300);
        });

        console.log("✅ Customer Name search initialized");
    }

    // ----------------------------
    // Close dropdowns when clicking outside
    // ----------------------------
    document.addEventListener("click", function (e) {
        if (!e.target.closest("#collectionIdSearch") && !e.target.closest("#collectionIdSuggestions")) {
            hideSuggestions("collectionIdSuggestions");
        }
        if (!e.target.closest("#customerNameSearch") && !e.target.closest("#customerNameSuggestions")) {
            hideSuggestions("customerNameSuggestions");
        }
        activeDropdown = null;
    });

    // Hide on scroll
    document.addEventListener("scroll", hideAllSuggestions, true);
}

// ========================================================
// CUSTOMER NAME SEARCH
// ========================================================
function handleCustomerNameSearch(query) {
    if (query.length < 2) {
        hideSuggestions("customerNameSuggestions");
        return;
    }

    showLoadingState("customerNameSuggestions");

    fetch(`/ajserp/customer-receipt-global-suggestions/?q=${encodeURIComponent(query)}`)
        .then((response) => response.json())
        .then((data) => {
            console.log("🔍 CUSTOMER NAME suggestions:", data);
            displaySuggestions(data, "customerNameSuggestions", "customerNameSearch");
            activeDropdown = "customerNameSuggestions";
        })
        .catch((error) => {
            console.error("❌ Error fetching customer suggestions:", error);

            displaySuggestions(
                [{
                    value: "",
                    text: "Error loading suggestions. Try again.",
                    isMessage: true,
                }],
                "customerNameSuggestions",
                "customerNameSearch"
            );

            activeDropdown = "customerNameSuggestions";
        });
}

// ========================================================
// COLLECTION ID SEARCH
// ========================================================
function handleCollectionIdSearch(query) {
    if (query.length < 2) {
        hideSuggestions("collectionIdSuggestions");
        return;
    }

    showLoadingState("collectionIdSuggestions");

    fetch(`/ajserp/customer-receipt-global-suggestions/?q=${encodeURIComponent(query)}`)
        .then((response) => response.json())
        .then((data) => {
            console.log("🔍 COLLECTION ID suggestions:", data);

            // Filter for collection IDs specifically
            const filtered = data.filter((item) =>
                item.text?.toLowerCase().includes("receipt")
            );

            displaySuggestions(filtered, "collectionIdSuggestions", "collectionIdSearch");
            activeDropdown = "collectionIdSuggestions";
        })
        .catch((error) => {
            console.error("❌ Error fetching collection suggestions:", error);
            hideSuggestions("collectionIdSuggestions");
        });
}

// ========================================================
// LOADING STATE
// ========================================================
function showLoadingState(containerId) {
    const container = document.getElementById(containerId);
    const inputElement = document.getElementById(containerId.replace("Suggestions", "Search"));

    if (!container || !inputElement) return;

    container.innerHTML = `
        <div class="suggestion-item text-muted">
            <i class="fa fa-spinner fa-spin me-2"></i>Loading...
        </div>
    `;
    container.style.display = "block";

    positionDropdown(container, inputElement);
}

// ========================================================
// DISPLAY SUGGESTIONS
// ========================================================
function displaySuggestions(suggestions, containerId, inputId) {
    const container = document.getElementById(containerId);
    const inputElement = document.getElementById(inputId);

    if (!container || !inputElement) return;
    container.innerHTML = "";

    if (suggestions.length === 0) {
        container.innerHTML = `<div class="suggestion-item text-muted">No results found</div>`;
    } else {
        suggestions.slice(0, 8).forEach((suggestion) => {
            const div = document.createElement("div");
            div.className = "suggestion-item";
            div.innerHTML = `
                <i class="fa ${getSuggestionIcon(suggestion.text)} me-2"></i>
                ${suggestion.text}
            `;
            div.addEventListener("click", () => selectSuggestion(suggestion.value, inputId));
            container.appendChild(div);
        });
    }

    positionDropdown(container, inputElement);
    container.style.display = "block";
}

// ========================================================
// POSITION DROPDOWN
// ========================================================
function positionDropdown(container, inputElement) {
    container.style.position = "absolute";
    container.style.top = "100%";
    container.style.left = "0";
    container.style.width = "100%";
    container.style.zIndex = "1060";

    const rect = inputElement.getBoundingClientRect();
    const screenH = window.innerHeight;

    if (rect.bottom + 200 > screenH) {
        container.style.top = "auto";
        container.style.bottom = "100%";
    } else {
        container.style.bottom = "auto";
        container.style.top = "100%";
    }
}

// ========================================================
// ICON HELPER
// ========================================================
function getSuggestionIcon(text) {
    if (!text) return "fa-search";
    text = text.toLowerCase();

    if (text.includes("receipt")) return "fa-receipt";
    if (text.includes("customer")) return "fa-user";
    if (text.includes("code")) return "fa-hashtag";

    return "fa-search";
}

// ========================================================
// SELECT SUGGESTION
// ========================================================
function selectSuggestion(value, inputId) {
    document.getElementById(inputId).value = value;
    hideAllSuggestions();
}

// ========================================================
// HIDE FUNCTIONS
// ========================================================
function hideSuggestions(id) {
    const container = document.getElementById(id);
    if (container) container.style.display = "none";
}

function hideAllSuggestions() {
    hideSuggestions("collectionIdSuggestions");
    hideSuggestions("customerNameSuggestions");
    activeDropdown = null;
}

// ========================================================
// HANDLE RESIZE
// ========================================================
window.addEventListener("resize", () => {
    if (activeDropdown) {
        const container = document.getElementById(activeDropdown);
        const input = document.getElementById(activeDropdown.replace("Suggestions", "Search"));
        if (container && input && container.style.display === "block") {
            positionDropdown(container, input);
        }
    }
});

// Prevent form submission while selecting suggestions
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("form").forEach((form) => {
        form.addEventListener("submit", hideAllSuggestions);
    });
});
