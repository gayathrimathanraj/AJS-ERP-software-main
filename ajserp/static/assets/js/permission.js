document.addEventListener("DOMContentLoaded", function () {

    // ✅ MODULE → toggle all View/Edit/Delete under that module
    document.querySelectorAll(".module-checkbox").forEach(function (moduleCheckbox) {
        moduleCheckbox.addEventListener("change", function () {
            var moduleKey = this.dataset.module;

            document.querySelectorAll(
                ".submenu-checkbox[data-module='" + moduleKey + "']"
            ).forEach(function (cb) {
                cb.checked = moduleCheckbox.checked;
            });
        });
    });

    // ✅ SUBMENU PERMISSION → auto-update module checkbox
    document.querySelectorAll(".submenu-checkbox").forEach(function (submenuCheckbox) {
        submenuCheckbox.addEventListener("change", function () {
            var moduleKey = this.dataset.module;

            var allSubmenus = document.querySelectorAll(
                ".submenu-checkbox[data-module='" + moduleKey + "']"
            );

            var moduleCheckbox = document.querySelector(
                ".module-checkbox[data-module='" + moduleKey + "']"
            );

            if (!moduleCheckbox) return;

            var allChecked = Array.from(allSubmenus).every(function (cb) {
                return cb.checked;
            });

            moduleCheckbox.checked = allChecked;
        });
    });

});

