document.addEventListener("DOMContentLoaded", function () {

    const modalElement = document.getElementById("sessionTimeoutModal");

    if (!modalElement) {
        return;
    }

    const modal = new bootstrap.Modal(modalElement);

    const stayButton = document.getElementById("stayLoggedIn");
    const logoutButton = document.getElementById("logoutNow");
    const countdown = document.getElementById("countdown");

    const WARNING_TIME = window.sessionTimeout.warning;
    const LOGOUT_TIME = window.sessionTimeout.logout;

    let warningTimer = null;
    let logoutTimer = null;
    let countdownTimer = null;

    let warningVisible = false;
    let loggingOut = false;

    function logoutUser() {

        if (loggingOut) return;

        loggingOut = true;

        if (window.location.pathname.startsWith("/portal/")) {
            window.location.replace("/portal/logout/");
        } else {
            window.location.replace("/accounts/logout/");
        }
    }

    function showWarning() {

        if (warningVisible || loggingOut) return;

        warningVisible = true;

        modal.show();

        let seconds = 30;

        countdown.textContent = "00:30";

        countdownTimer = setInterval(function () {

            seconds--;

            countdown.textContent =
                "00:" + String(Math.max(seconds, 0)).padStart(2, "0");

        }, 1000);

    }

    function resetTimers() {

        if (loggingOut) return;

        clearTimeout(warningTimer);
        clearTimeout(logoutTimer);
        clearInterval(countdownTimer);

        warningVisible = false;

        modal.hide();

        warningTimer = setTimeout(showWarning, WARNING_TIME);

        logoutTimer = setTimeout(logoutUser, LOGOUT_TIME);

    }

    if (stayButton) {

        stayButton.addEventListener("click", function () {

            const keepAliveUrl =
                window.location.pathname.startsWith("/portal/")
                    ? "/portal/keep-alive/"
                    : "/accounts/keep-alive/";

            fetch(keepAliveUrl)
                .finally(resetTimers);

        });

    }

    if (logoutButton) {

        logoutButton.addEventListener("click", logoutUser);

    }

    // Only keyboard activity keeps the session alive
    document.addEventListener(
        "keydown",
        resetTimers,
        true
    );

    resetTimers();

});