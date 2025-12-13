// material-search.js (FINAL STABLE VERSION)

// =============================================================
//  SAFETY WRAPPER → Prevent JS errors on other pages
// =============================================================
(function () {

    console.log("materialsearch.js loaded");

    // Run only if Material page elements exist
    if (!document.getElementById("materialNameInput") &&
        !document.getElementById("globalSearchInput")) {

        console.log("materialsearch.js: Inputs not found → EXITING safely.");
        return; // SAFE because inside wrapper
    }

    // =============================================================
    // READY FUNCTION
    // =============================================================
    $(document).ready(function () {

        console.log("materialsearch.js ACTIVE");

        let typingTimer;
        const doneTypingInterval = 300;


        // =============================================================
        // MATERIAL NAME AUTOCOMPLETE
        // =============================================================
        $("#materialNameInput").on("input", function () {

            clearTimeout(typingTimer);
            let query = $(this).val().trim();

            if (query.length < 2) {
                $("#materialNameSuggestions").empty().hide();
                return;
            }

            typingTimer = setTimeout(function () {

                $.ajax({
                    url: "/ajserp/api/material-name-suggestions/",
                    data: { q: query },
                    dataType: "json",

                    success: function (data) {

                        if (!data || data.length === 0) {
                            $("#materialNameSuggestions")
                                .html("<div class='as-item no-results'>No results found</div>")
                                .show();
                            return;
                        }

                        let html = "";
                        data.forEach(function (name) {
                            html += `<div class="as-item" data-material-name="${name}">${name}</div>`;
                        });

                        $("#materialNameSuggestions").html(html).show();
                    },

                    error: function () {
                        $("#materialNameSuggestions")
                            .html("<div class='as-item error'>Error fetching data</div>")
                            .show();
                    }
                });

            }, doneTypingInterval);
        });



        // =============================================================
        // GLOBAL SEARCH AUTOCOMPLETE
        // =============================================================
        $("#globalSearchInput").on("input", function () {

            clearTimeout(typingTimer);
            let query = $(this).val().trim();

            if (query.length < 2) {
                $("#globalSearchSuggestions").empty().hide();
                return;
            }

            typingTimer = setTimeout(function () {

                $.ajax({
                    url: "/ajserp/api/material-suggestions/",
                    data: { q: query },
                    dataType: "json",

                    success: function (data) {

                        if (!data || data.length === 0) {
                            $("#globalSearchSuggestions")
                                .html("<div class='as-item no-results'>No results found</div>")
                                .show();
                            return;
                        }

                        let html = "";
                        data.forEach(function (material) {
                            html += `
                                <div class="as-item" data-material='${JSON.stringify(material)}'>
                                    <strong>${material.material_name}</strong><br>
                                    <small>
                                        Code: ${material.material_code} |
                                        Category: ${material.category || "N/A"} |
                                        UOM: ${material.uom || "N/A"}
                                    </small>
                                </div>`;
                        });

                        $("#globalSearchSuggestions").html(html).show();
                    },

                    error: function () {
                        $("#globalSearchSuggestions")
                            .html("<div class='as-item error'>Error fetching data</div>")
                            .show();
                    }
                });

            }, doneTypingInterval);
        });



        // =============================================================
        // CLICK HANDLERS
        // =============================================================
        $(document).on("click", "#materialNameSuggestions .as-item", function () {
            const name = $(this).data("material-name");
            $("#materialNameInput").val(name);
            $("#materialNameSuggestions").empty().hide();
            $("#filterForm").submit();
        });

        $(document).on("click", "#globalSearchSuggestions .as-item", function () {
            const item = $(this).data("material");
            $("#globalSearchInput").val(item.material_name);
            $("#globalSearchSuggestions").empty().hide();
            performGlobalSearch();
        });



        // =============================================================
        // CLOSE DROPDOWNS WHEN CLICK OUTSIDE
        // =============================================================
        $(document).click(function (e) {
            if (!$(e.target).closest("#materialNameInput, #materialNameSuggestions").length) {
                $("#materialNameSuggestions").hide();
            }
            if (!$(e.target).closest("#globalSearchInput, #globalSearchSuggestions").length) {
                $("#globalSearchSuggestions").hide();
            }
        });



        // =============================================================
        // FILTER AUTOSUBMIT
        // =============================================================
        $("#categorySelect, #brandSelect, #statusSelect").on("change", function () {
            $("#filterForm").submit();
        });



        // =============================================================
        // EXPORT HANDLER
        // =============================================================
        $(".dropdown-menu.import_1 a").on("click", function (e) {
            e.preventDefault();
            exportData($(this).text().toLowerCase());
        });

    }); // end document.ready



    // =============================================================
    // HELPER FUNCTIONS
    // =============================================================

    window.performGlobalSearch = function () {
        const query = $("#globalSearchInput").val().trim();
        window.location.href = query ? `?q=${encodeURIComponent(query)}` : "/ajserp/material/";
    };


    window.exportData = function (format) {
        const params = new URLSearchParams(window.location.search);
        params.set("export", format);
        window.location.href = `${window.location.pathname}?${params.toString()}`;
    };


})();   // END OF SAFE WRAPPER
