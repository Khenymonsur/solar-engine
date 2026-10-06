document.addEventListener("DOMContentLoaded", function () {

    // -------------------------------------------------------
    // Elements
    // -------------------------------------------------------

    const stateSelect = document.getElementById("id_state");
    const lgaSelect = document.getElementById("id_lga");
    const addressInput = document.getElementById("id_address");
    const latitudeInput = document.getElementById("id_latitude");
    const longitudeInput = document.getElementById("id_longitude");

    // -------------------------------------------------------
    // State → LGA
    // -------------------------------------------------------

    if (stateSelect && lgaSelect) {

        // Populate State dropdown FIRST
        if (stateSelect.options.length <= 1) {

            Object.keys(STATE_LGAS)
                .sort()
                .forEach(function (state) {

                    const option = document.createElement("option");
                    option.value = state;
                    option.textContent = state;

                    stateSelect.appendChild(option);

                });

        }

        function populateLGAs(selected = "") {

            const state = stateSelect.value;

            lgaSelect.innerHTML = "";

            const defaultOption = document.createElement("option");
            defaultOption.value = "";
            defaultOption.textContent = "Select LGA";
            lgaSelect.appendChild(defaultOption);

            if (!STATE_LGAS[state]) {
                return;
            }

            STATE_LGAS[state].forEach(function (lga) {

                const option = document.createElement("option");
                option.value = lga;
                option.textContent = lga;

                if (lga === selected) {
                    option.selected = true;
                }

                lgaSelect.appendChild(option);

            });

        }

        const savedLGA = lgaSelect.dataset.selected || lgaSelect.value;

        populateLGAs(savedLGA);

        stateSelect.addEventListener("change", function () {
            populateLGAs();
        });

    }


    // -------------------------------------------------------
    // Google Places Autocomplete
    // -------------------------------------------------------

    if (
        addressInput &&
        latitudeInput &&
        longitudeInput &&
        window.google &&
        google.maps &&
        google.maps.places
    ) {

        const autocomplete = new google.maps.places.Autocomplete(addressInput, {

            componentRestrictions: {
                country: "ng"
            },

            fields: [
                "formatted_address",
                "geometry",
                "address_components"
            ]

        });

        autocomplete.addListener("place_changed", function () {

            const place = autocomplete.getPlace();

            if (!place.geometry) {

                alert("Please choose an address from the Google suggestions.");

                return;

            }

            // Fill address

            addressInput.value = place.formatted_address;

            // Store coordinates

            latitudeInput.value = place.geometry.location.lat();

            longitudeInput.value = place.geometry.location.lng();

            console.log("Address:", place.formatted_address);
            console.log("Latitude:", latitudeInput.value);
            console.log("Longitude:", longitudeInput.value);

        });

        console.log("✅ Google Places Autocomplete Initialized");

    } else {

        console.warn("Google Places API not available.");

    }

});