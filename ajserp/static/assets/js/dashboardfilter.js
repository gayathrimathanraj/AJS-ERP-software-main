document.addEventListener('DOMContentLoaded', function () {

    const bulkAssignBtn = document.getElementById('bulkAssignBtn');
    const bulkAssignedTo = document.getElementById('bulkAssignedTo');
    const bulkAssignForm = document.getElementById('bulkAssignForm');
    const bulkAssignedToHidden = document.getElementById('bulkAssignedToHidden');
    const selectAll = document.getElementById('selectAll');

    // Select All
    if (selectAll) {
        selectAll.addEventListener('change', function () {
            document.querySelectorAll('.tracker-checkbox')
                .forEach(cb => cb.checked = selectAll.checked);
        });
    }

    // Bulk Assign Button
    bulkAssignBtn.addEventListener('click', function () {

        const userId = bulkAssignedTo.value;

        if (!userId) {
            alert("Please select a user to assign.");
            return;
        }

        const selectedCheckboxes = document.querySelectorAll('.tracker-checkbox:checked');

        if (selectedCheckboxes.length === 0) {
            alert("Please select at least one tracker.");
            return;
        }

        // Set user ID
        bulkAssignedToHidden.value = userId;

        // Remove old tracker_ids
        bulkAssignForm.querySelectorAll('input[name="tracker_ids"]').forEach(el => el.remove());

        // Add selected trackers
        selectedCheckboxes.forEach(cb => {
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'tracker_ids';
            input.value = cb.value;
            bulkAssignForm.appendChild(input);
        });

        // Submit form
        bulkAssignForm.submit();
    });

});




// document.addEventListener('DOMContentLoaded', function () {

//     const checkboxes = document.querySelectorAll('.tracker-checkbox');
//     const bulkAssignBtn = document.getElementById('bulkAssignBtn');
//     const bulkAssignedTo = document.getElementById('bulkAssignedTo');
//     const bulkAssignForm = document.getElementById('bulkAssignForm');
//     const assignedToHidden = document.getElementById('bulkAssignedToHidden');

//     // Bulk Assign Logic
//     bulkAssignBtn.addEventListener('click', function () {

//         const userId = bulkAssignedTo.value;
//         if (!userId) {
//             alert('Please select a user.');
//             return;
//         }

//         const selectedIds = Array.from(checkboxes)
//             .filter(cb => cb.checked)
//             .map(cb => cb.value);

//         if (selectedIds.length === 0) {
//             alert('No trackers selected.');
//             return;
//         }

//         assignedToHidden.value = userId;

//         // remove old ids
//         bulkAssignForm.querySelectorAll('input[name="tracker_ids"]').forEach(el => el.remove());

//         // add new ids
//         selectedIds.forEach(id => {
//             const input = document.createElement('input');
//             input.type = 'hidden';
//             input.name = 'tracker_ids';
//             input.value = id;
//             bulkAssignForm.appendChild(input);
//         });

//         bulkAssignForm.submit();
//     });

// });
