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
