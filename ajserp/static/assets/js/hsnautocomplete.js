document.addEventListener("DOMContentLoaded", function () {
    console.log("HSN Autocomplete loaded!"); // Debug
    
    document.querySelectorAll(".hsnSearch").forEach(function (input) {
        console.log("Found HSN input:", input); // Debug
        
        // ✅ FIXED: Get the NEXT element (suggestion box)
        const suggestionBox = input.nextElementSibling;
        console.log("Suggestion box:", suggestionBox); // Debug
        
        if (!suggestionBox || !suggestionBox.classList.contains('hsnSuggestions')) {
            console.error("Suggestion box not found!");
            return;
        }

        let debounceTimer;

        input.addEventListener("input", function () {
            console.log("Typing:", input.value); // Debug
            clearTimeout(debounceTimer);
            const query = input.value.trim();
            
            if (query.length < 2) {
                suggestionBox.innerHTML = "";
                return;
            }

            debounceTimer = setTimeout(() => {
                console.log("Calling API for:", query);
                
                // ✅ FIXED: Add leading slash to URL
                fetch(`/ajserp/get_hsn_suggestions/?q=${encodeURIComponent(query)}`)
                    .then((response) => {
                        console.log("API Status:", response.status);
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    })
                    .then((data) => {
                        console.log("API Data:", data);
                        suggestionBox.innerHTML = "";
                        
                        if (data.length === 0) {
                            const noResult = document.createElement("div");
                            noResult.classList.add("suggestion-item", "text-muted");
                            noResult.textContent = "No HSN codes found";
                            suggestionBox.appendChild(noResult);
                            return;
                        }
                        
                        data.forEach((item) => {
                            const div = document.createElement("div");
                            div.classList.add("suggestion-item");
                            div.textContent = item.hsn_code;
                            div.addEventListener("click", function () {
                                console.log("Selected:", item.hsn_code);
                                input.value = item.hsn_code;
                                suggestionBox.innerHTML = "";
                            });
                            suggestionBox.appendChild(div);
                        });
                    })
                    .catch((err) => {
                        console.error("Error:", err);
                        suggestionBox.innerHTML = "<div class='suggestion-item text-danger'>Error loading suggestions</div>";
                    });
            }, 300);
        });

        // Close suggestions when clicking outside
        document.addEventListener("click", function (e) {
            if (e.target !== input && !suggestionBox.contains(e.target)) {
                suggestionBox.innerHTML = "";
            }
        });
    });
});