// material-search.js - NO CSS VERSION

$(document).ready(function(){
    console.log('=== MATERIAL SEARCH DEBUG ===');
    console.log('1. Script loaded successfully');
    
    // Test if elements exist
    console.log('materialNameInput exists:', $('#materialNameInput').length > 0);
    console.log('materialNameSuggestions exists:', $('#materialNameSuggestions').length > 0);
    console.log('filterForm exists:', $('#filterForm').length > 0);
    
    // Test API manually
    console.log('Testing API...');
    $.get("/ajserp/api/material-name-suggestions/?q=test", function(data) {
        console.log('API test response:', data);
        console.log('API response length:', data.length);
    }).fail(function(err) {
        console.error('API test failed:', err);
    });

    console.log('=== END DEBUG ===');

    let typingTimer;
    const doneTypingInterval = 300;

    // Material Name Autocomplete
    $("#materialNameInput").on("input", function(){
        console.log('Material name input:', $(this).val()); 

        clearTimeout(typingTimer);
        let query = $(this).val();

        if (query.length === 0) {
            $("#materialNameSuggestions").empty().hide();
            return;
        }

        if (query.length < 2) {
            $("#materialNameSuggestions").empty().hide();
            return;
        }

        typingTimer = setTimeout(function(){
            $.ajax({
                url: "/ajserp/api/material-name-suggestions/",
                data: {q: query},
                dataType: "json",
                success: function(data){
                    console.log('API success - Raw data:', data);
                    
                    // TEMPORARY: If API returns empty, use mock data for testing
                    if (data.length === 0) {
                        console.log('API returned empty, using mock data');
                        const mockData = {
                            'in': ['Inventory Item', 'Industrial Material', 'Installation Service'],
                            'test': ['Test Material', 'Testing Equipment', 'Test Service'],
                            'a': ['Assembly Part', 'Adapter', 'Accessory'],
                            'material': ['Material One', 'Material Two', 'Raw Material']
                        };
                        data = mockData[query] || ['Sample Material 1', 'Sample Material 2'];
                    }
                    
                    let items = "";
                    
                    data.forEach(function(materialName){
                        console.log('Adding suggestion:', materialName);
                        items += `
                            <div class="border-bottom p-2 bg-white" style="cursor: pointer;" data-material-name="${materialName}">
                                <strong>${materialName}</strong>
                            </div>`;
                    });
                    
                    $("#materialNameSuggestions").html(items).show();
                    console.log('Suggestions should be visible now');
                },
                error: function(err) {
                    console.error("Material Name API Error:", err);
                    $("#materialNameSuggestions").html("<div class='p-2 text-danger'>Error loading materials</div>").show();
                }
            });
        }, doneTypingInterval);
    });

    // Global Search Autocomplete
    $("#globalSearchInput").on("input", function(){
        clearTimeout(typingTimer);
        let query = $(this).val();

        if (query.length === 0) {
            $("#globalSearchSuggestions").empty().hide();
            return;
        }

        if (query.length < 2) {
            $("#globalSearchSuggestions").empty().hide();
            return;
        }

        typingTimer = setTimeout(function(){
            $.ajax({
                url: "/ajserp/api/material-suggestions/",
                data: {q: query},
                dataType: "json",
                success: function(data){
                    // TEMPORARY: Mock data for testing
                    if (data.length === 0) {
                        data = [
                            {
                                material_name: "Test Material",
                                material_code: "TEST001",
                                category: "Material",
                                uom: "PCS"
                            },
                            {
                                material_name: "Sample Item",
                                material_code: "SMP002", 
                                category: "Service",
                                uom: "HRS"
                            }
                        ];
                    }
                    
                    let items = "";
                    
                    data.forEach(function(material){
                        items += `
                            <div class="border-bottom p-2 bg-white" style="cursor: pointer;" data-material='${JSON.stringify(material)}'>
                                <strong>${material.material_name}</strong><br>
                                <small class="text-muted">
                                    Code: ${material.material_code} | 
                                    Category: ${material.category || 'N/A'} | 
                                    UOM: ${material.uom || 'N/A'}
                                </small>
                            </div>`;
                    });
                    $("#globalSearchSuggestions").html(items).show();
                },
                error: function(err) {
                    console.error("Global Search API Error:", err);
                    $("#globalSearchSuggestions").html("<div class='p-2 text-danger'>Error loading materials</div>").show();
                }
            });
        }, doneTypingInterval);
    });

    // Handle material name selection
    $(document).on("click", "#materialNameSuggestions div", function(){
        const materialName = $(this).data('material-name');
        console.log('Suggestion clicked:', materialName);
        $("#materialNameInput").val(materialName);
        $("#materialNameSuggestions").empty().hide();
        // Auto-submit the form
        $("#filterForm").submit();
    });

    // Handle global search selection
    $(document).on("click", "#globalSearchSuggestions div", function(){
        const material = $(this).data('material');
        $("#globalSearchInput").val(material.material_name);
        $("#globalSearchSuggestions").empty().hide();
        // Perform global search
        performGlobalSearch();
    });

    // Global search button click
    $("#globalSearchBtn").on("click", function(){
        performGlobalSearch();
    });

    // Close suggestions when clicking outside
    $(document).click(function(e){
        if (!$(e.target).closest("#materialNameInput, #materialNameSuggestions").length) {
            $("#materialNameSuggestions").empty().hide();
        }
        if (!$(e.target).closest("#globalSearchInput, #globalSearchSuggestions").length) {
            $("#globalSearchSuggestions").empty().hide();
        }
    });

    // Select All functionality
    $("#selectAll").on("change", function(){
        const isChecked = $(this).is(":checked");
        $(".rowCheckbox").prop("checked", isChecked);
    });

    // Individual checkbox change
    $(document).on("change", ".rowCheckbox", function(){
        const allChecked = $(".rowCheckbox").length === $(".rowCheckbox:checked").length;
        $("#selectAll").prop("checked", allChecked);
    });

    // Auto-submit on select change
    $("#categorySelect, #brandSelect, #statusSelect").on("change", function(){
        $("#filterForm").submit();
    });

    // Export functionality
    $(".dropdown-menu.import_1 a").on("click", function(e){
        e.preventDefault();
        const format = $(this).text().toLowerCase();
        exportData(format);
    });
});

function performGlobalSearch() {
    const query = $("#globalSearchInput").val().trim();
    if (query) {
        window.location.href = `?q=${encodeURIComponent(query)}`;
    } else {
        window.location.href = '{% url "ajserp:material" %}';
    }
}

function exportData(format) {
    const currentParams = new URLSearchParams(window.location.search);
    currentParams.set('export', format);
    const exportUrl = `${window.location.pathname}?${currentParams.toString()}`;
    window.location.href = exportUrl;
}

// DataTable initialization
// $(document).ready(function(){
//     if ($.fn.DataTable && $('#basic-datatables').length) {
//         try {
//             $('#basic-datatables').DataTable({
//                 "pageLength": 25,
//                 "ordering": true,
//                 "searching": false,
//                 "info": true,
//                 "lengthChange": true,
//                 "language": {
//                     "paginate": {
//                         "previous": "‹",
//                         "next": "›"
//                     }
//                 }
//             });
//         } catch (error) {
//             console.error('DataTable error:', error);
//         }
//     }
// });