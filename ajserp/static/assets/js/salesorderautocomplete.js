console.log("Sales Order Number Suggestion JS Loaded");

// ------------------------------
// ORDER NUMBER SUGGESTIONS
// ------------------------------
function showOrderNumberSuggestions(query) {
    const box = document.getElementById("orderNumberSuggestions");

    if (!query.trim()) {
        box.style.display = "none";
        box.innerHTML = "";
        return;
    }

    // ✅ Correct API for SALES ORDER (not estimate)
    fetch(`/ajserp/api/salesorder-suggestions/?q=${query}`)
        .then(response => response.json())
        .then(data => {
            box.innerHTML = "";

            if (!data || data.length === 0) {
                box.style.display = "none";
                return;
            }

            data.forEach(item => {
                const option = document.createElement("div");
                option.classList.add("dropdown-item");
                option.style.cursor = "pointer";
                option.innerHTML = item.text;

                option.onclick = () => {
                    document.getElementById("orderNumberInput").value = item.value;
                    box.style.display = "none";
                };

                box.appendChild(option);
            });

            box.style.display = "block";
        })
        .catch(err => {
            console.error("❌ Sales Order Suggestion Error:", err);
            box.style.display = "none";
        });
}

// Close dropdown when clicking outside
document.addEventListener("click", function (event) {
    const box = document.getElementById("orderNumberSuggestions");
    const input = document.getElementById("orderNumberInput");

    if (!box.contains(event.target) && event.target !== input) {
        box.style.display = "none";
    }
});
