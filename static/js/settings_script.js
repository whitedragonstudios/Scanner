// static/js/danger_zone.js

document.addEventListener('DOMContentLoaded', () => {
    function confirmWithPassword(message) {
        const password = prompt(message + "\n\nEnter admin password to continue:");
        if (password !== "stoic") {
            alert("Incorrect password. Action canceled.");
            return false;
        }
        return true;
    }

    const actions = [
        {
            id: "restoreBtn",
            confirmMsg: "Are you sure you want to restore default configuration settings?"
        },
        {
            id: "clearEmails",
            confirmMsg: "Delete all stored emails? You will need to add at least one email for reports to be sent to."
        },
        {
            id: "deleteBtn",
            confirmMsg: "This will permanently delete employee database and timesheets. Continue?"
        },
        {
            id: "reinstallBtn",
            confirmMsg: "WARNING: This will delete all data and reinstall the program. Are you absolutely sure?"
        }
    ];

    actions.forEach(({ id, confirmMsg }) => {
        const btn = document.getElementById(id);
        if (btn) {
            btn.addEventListener("click", (event) => {
                if (!confirmWithPassword(confirmMsg)) {
                    event.preventDefault();
                }
            });
        }
    });
});


document.addEventListener("DOMContentLoaded", () => {
    // Map input IDs to CSS variables
    const colorMap = {
        main_background_color: "--bg-color",
        main_text_color: "--text-color",
        content_color: "--content-color",
        content_text_color: "--content-text-color",
        sidebar_color: "--sidebar-color",
        sidebar_text_color: "--sidebar-text-color",
        button_color: "--button-color",
        button_text_color: "--button-text-color",
        button_hover_color: "--button-hover-color",
        border_color: "--border-color"
    };

    // For each color input, listen for changes
    Object.keys(colorMap).forEach(inputId => {
        const input = document.getElementById(inputId);
        if (!input) return;

        input.addEventListener("input", (e) => {
            const cssVar = colorMap[inputId];
            const value = e.target.value;
            document.documentElement.style.setProperty(cssVar, value);
        });
    });
});
