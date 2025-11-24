
document.addEventListener("DOMContentLoaded", function () {

    // Attach autocomplete to all .customer-search fields
    document.querySelectorAll(".customer-search").forEach(function (input) {

        let suggestionBox;

        input.addEventListener("input", function () {
            let q = input.value.trim();

            // remove existing box
            if (suggestionBox) suggestionBox.remove();

            if (q.length < 1) return;

            fetch(`/ajserp/api/dashboard-customer-search/?q=` + q)
                .then(res => res.json())
                .then(data => {

                    suggestionBox = document.createElement("div");
                    suggestionBox.classList.add("suggest-box");
                    suggestionBox.style.position = "absolute";
                    suggestionBox.style.background = "#fff";
                    suggestionBox.style.border = "1px solid #ccc";
                    suggestionBox.style.zIndex = "9999";
                    suggestionBox.style.width = input.offsetWidth + "px";

                    data.results.forEach(item => {
                        let option = document.createElement("div");
                        option.classList.add("suggest-item");
                        option.style.padding = "6px";
                        option.style.cursor = "pointer";
                        option.innerText = `${item.name} (${item.city})`;

                        option.addEventListener("click", function () {
                            input.value = item.name;

                            // fill city automatically
                            let cityInput = input.closest("tr").querySelector(".customer-city");
                            if (cityInput) {
                                cityInput.value = item.city;
                            }

                            suggestionBox.remove();
                        });

                        suggestionBox.appendChild(option);
                    });

                    input.parentNode.appendChild(suggestionBox);
                });
        });

        // Click outside to close
        document.addEventListener("click", function (event) {
            if (suggestionBox && !input.contains(event.target)) {
                suggestionBox.remove();
            }
        });

    });

});

