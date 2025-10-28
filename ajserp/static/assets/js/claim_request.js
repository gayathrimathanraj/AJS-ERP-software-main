document.addEventListener("DOMContentLoaded", function () {
    const addLineBtn = document.getElementById("addLineBtn");
    const tableBody = document.querySelector("table tbody");

    function updateSerialNumbers() {
        const rows = tableBody.querySelectorAll("tr");
        rows.forEach((row, index) => {
            row.cells[0].textContent = index + 1;
        });
    }

    function addDeleteEvent(button) {
        button.addEventListener("click", function () {
            const rows = tableBody.querySelectorAll("tr");
            if (rows.length > 1) {
                const confirmed = confirm("Are you sure you want to delete this row?");
                if (confirmed) {
                    button.closest("tr").remove();
                    updateSerialNumbers();
                }
            } else {
                alert("At least one row must remain.");
            }
        });
    }

    // Attach delete to existing buttons
    document.querySelectorAll(".delete-row").forEach(addDeleteEvent);

    // ✅ FIX: Add null check before adding event listener
    if (addLineBtn && tableBody) {
        addLineBtn.addEventListener("click", function () {
            const lastRow = tableBody.lastElementChild;
            if (!lastRow) return;

            const newRow = lastRow.cloneNode(true);

            // Clear all inputs and selects
            const inputs = newRow.querySelectorAll("input, select");
            inputs.forEach(input => {
                if (input.tagName === "SELECT") {
                    input.selectedIndex = 0;
                } else if (input.type === "file") {
                    input.value = ""; // Clear file input (may not reset in all browsers)
                } else {
                    input.value = "";
                }
            });

            // Re-attach delete button
            const deleteBtn = newRow.querySelector(".delete-row");
            if (deleteBtn) {
                addDeleteEvent(deleteBtn);
            }

            tableBody.appendChild(newRow);
            updateSerialNumbers();
        });
    }
});


// document.addEventListener("DOMContentLoaded", function () {
//     const addLineBtn = document.getElementById("addLineBtn");
//     const tableBody = document.querySelector("table tbody");

//     function updateSerialNumbers() {
//         const rows = tableBody.querySelectorAll("tr");
//         rows.forEach((row, index) => {
//             row.cells[0].textContent = index + 1;
//         });
//     }

//     function addDeleteEvent(button) {
//         button.addEventListener("click", function () {
//             const rows = tableBody.querySelectorAll("tr");
//             if (rows.length > 1) {
//                 const confirmed = confirm("Are you sure you want to delete this row?");
//                 if (confirmed) {
//                     button.closest("tr").remove();
//                     updateSerialNumbers();
//                 }
//             } else {
//                 alert("At least one row must remain.");
//             }
//         });
//     }

//     // Attach delete to existing buttons
//     document.querySelectorAll(".delete-row").forEach(addDeleteEvent);

//     addLineBtn.addEventListener("click", function () {
//         const lastRow = tableBody.lastElementChild;
//         if (!lastRow) return;

//         const newRow = lastRow.cloneNode(true);

//         // Clear all inputs and selects
//         const inputs = newRow.querySelectorAll("input, select");
//         inputs.forEach(input => {
//             if (input.tagName === "SELECT") {
//                 input.selectedIndex = 0;
//             } else if (input.type === "file") {
//                 input.value = ""; // Clear file input (may not reset in all browsers)
//             } else {
//                 input.value = "";
//             }
//         });

//         // Re-attach delete button
//         const deleteBtn = newRow.querySelector(".delete-row");
//         if (deleteBtn) {
//             addDeleteEvent(deleteBtn);
//         }

//         tableBody.appendChild(newRow);
//         updateSerialNumbers();
//     });
// });
