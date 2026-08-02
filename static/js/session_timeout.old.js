let loggingOut = false;
console.log("SESSION TIMEOUT VERSION 2");

document.addEventListener("DOMContentLoaded", function () {

    const WARNING_TIME = 1000;      // 1 seconds
    const LOGOUT_TIME = 3000;      // 3 seconds

    let warningTimer;
    let logoutTimer;
    let countdownTimer;

    const modalElement = document.getElementById("sessionTimeoutModal");

    if (!modalElement) return;

    const modal = new bootstrap.Modal(modalElement);

    const countdown = document.getElementById("countdown");

    const stayLoggedIn = document.getElementById("stayLoggedIn");

    const logoutNow = document.getElementById("logoutNow");

    if (logoutNow) {
        logoutNow.addEventListener("click", function () {
            logout();
        });
    }

    function resetTimers() {

        console.log("Timers reset");

        clearTimeout(warningTimer);
        clearTimeout(logoutTimer);
        clearInterval(countdownTimer);

        warningShown = false;

        modal.hide();

        warningTimer = setTimeout(showWarning, WARNING_TIME);

        logoutTimer = setTimeout(logout, LOGOUT_TIME);
    }

    function showWarning() {

        if (warningShown) {
            return;
        }

        warningShown = true;

        modal.show();

        let remaining = 2;

        countdown.textContent = "00:02";

        countdownTimer = setInterval(function () {

            remaining--;

            const seconds = remaining.toString().padStart(2, "0");

            countdown.textContent = `00:${seconds}`;

        }, 1000);

    }

    function logout() {

        if (loggingOut) {
            return;
        }

        loggingOut = true;

        if (window.location.pathname.startsWith("/portal/")) {

            window.location.href = "/portal/logout/";

        } else {

            window.location.href = "/accounts/logout/";

        }

    }

    if (stayLoggedIn) {

        stayLoggedIn.addEventListener("click", function () {

            const keepAliveUrl = window.location.pathname.startsWith("/portal/")
                ? "/portal/keep-alive/"
                : "/accounts/keep-alive/";

            fetch(keepAliveUrl)
                .finally(() => {
                    resetTimers();
                });

        });

    }

    [
        "mousemove",
        "keydown",
        "click",
        "scroll",
        "touchstart",
    ].forEach(event => {
        document.addEventListener(
            event,
            resetTimers
        );
    });

    resetTimers();

    });