document.addEventListener("DOMContentLoaded", function () {
    var tableEl = document.getElementById("basic-datatables");
    if (!tableEl) return; // Stop if table not on this page

    var isDataTable = typeof $.fn.DataTable !== 'undefined';
    
    if (isDataTable) {
        // Initialize DataTable
        var table = $('#basic-datatables').DataTable({
            paging: false,          // enable pagination
            searching: false,      // hide search box
            info: false,           // hide "Showing 1 to X of Y entries"
            lengthChange: false,   // hide "Show X entries" dropdown
            columnDefs: [
                { orderable: false, targets: 0 } // disable sorting on first column (checkbox)
            ]
        });

        // Master checkbox
        $('#selectAll').on('click', function() {
            var rows = table.rows({ 'search': 'applied' }).nodes();
            $('input.rowCheckbox', rows).prop('checked', this.checked);
        });

        // Row checkbox: update master checkbox
        $('#basic-datatables tbody').on('change', 'input.rowCheckbox', function() {
            var rows = table.rows({ 'search': 'applied' }).nodes();
            var allChecked = $('input.rowCheckbox:checked', rows).length === $('input.rowCheckbox', rows).length;
            $('#selectAll').prop('checked', allChecked);
        });

    } else {
        // Plain table
        const selectAll = document.getElementById("selectAll");
        const checkboxes = document.querySelectorAll("#basic-datatables .rowCheckbox");

        selectAll.addEventListener("change", function () {
            checkboxes.forEach(cb => cb.checked = this.checked);
        });

        checkboxes.forEach(cb => {
            cb.addEventListener("change", function () {
                const allChecked = document.querySelectorAll("#basic-datatables .rowCheckbox:checked").length === checkboxes.length;
                selectAll.checked = allChecked;
            });
        });
    }
});
