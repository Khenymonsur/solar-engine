document.addEventListener("DOMContentLoaded", function () {

    // ======================================================
    // Elements
    // ======================================================

    const stateSelect =
        document.getElementById("id_state");

    const lgaSelect =
        document.getElementById("id_lga");

    const addressInput =
        document.getElementById("id_address");

    const latitudeInput =
        document.getElementById("id_latitude");

    const longitudeInput =
        document.getElementById("id_longitude");

    const suggestionsBox =
        document.getElementById("address-suggestions");

    const locationButton =
        document.getElementById("current-location-btn");

    const mapElement =
        document.getElementById("property-map");

    const coordinatePanel =
        document.getElementById("coordinate-panel");

    const latitudeDisplay =
        document.getElementById("latitude-display");

    const longitudeDisplay =
        document.getElementById("longitude-display");

    const API_KEY =
        window.GEOAPIFY_API_KEY || "";


    let map = null;
    let marker = null;
    let searchTimer = null;


    // ======================================================
    // State → LGA
    // ======================================================

    if (
        stateSelect &&
        lgaSelect &&
        typeof STATE_LGAS !== "undefined"
    ) {

        if (stateSelect.options.length <= 1) {

            Object.keys(STATE_LGAS)
                .sort()
                .forEach(function (state) {

                    const option =
                        document.createElement("option");

                    option.value = state;
                    option.textContent = state;

                    stateSelect.appendChild(option);

                });

        }


        function populateLGAs(selected = "") {

            const state =
                stateSelect.value;

            lgaSelect.innerHTML = "";


            const defaultOption =
                document.createElement("option");

            defaultOption.value = "";
            defaultOption.textContent =
                "Select LGA";

            lgaSelect.appendChild(
                defaultOption
            );


            if (!STATE_LGAS[state]) {
                return;
            }


            STATE_LGAS[state].forEach(
                function (lga) {

                    const option =
                        document.createElement(
                            "option"
                        );

                    option.value = lga;
                    option.textContent = lga;


                    if (lga === selected) {
                        option.selected = true;
                    }


                    lgaSelect.appendChild(
                        option
                    );

                }
            );

        }


        const savedLGA =
            lgaSelect.dataset.selected ||
            lgaSelect.value;


        populateLGAs(savedLGA);


        stateSelect.addEventListener(
            "change",
            function () {

                populateLGAs();

            }
        );

    }


    // ======================================================
    // Coordinate Display
    // ======================================================

    function displayCoordinates(
        latitude,
        longitude
    ) {

        if (latitudeDisplay) {

            latitudeDisplay.textContent =
                Number(latitude).toFixed(6);

        }

        if (longitudeDisplay) {

            longitudeDisplay.textContent =
                Number(longitude).toFixed(6);

        }

        if (coordinatePanel) {

            coordinatePanel.style.display =
                "block";

        }

    }


    // ======================================================
    // Leaflet Map
    // ======================================================

    function showMap(
        latitude,
        longitude
    ) {

        if (
            !mapElement ||
            typeof L === "undefined"
        ) {
            return;
        }


        const lat =
            Number(latitude);

        const lon =
            Number(longitude);


        mapElement.style.display =
            "block";

        const mapHelp =
            document.getElementById(
                "map-help"
            );

        if (mapHelp) {
            mapHelp.style.display =
                "flex";
        }


        if (!map) {

            map = L.map(
                mapElement
            ).setView(
                [lat, lon],
                17
            );

        // ---------------------------------------------
        // Click anywhere on map to select location
        // ---------------------------------------------

        map.on(
            "click",
            async function (event) {

                const latitude =
                    event.latlng.lat;

                const longitude =
                    event.latlng.lng;


                if (marker) {

                    marker.setLatLng([
                        latitude,
                        longitude
                    ]);

                }


                if (latitudeInput) {
                    latitudeInput.value =
                        latitude;
                }

                if (longitudeInput) {
                    longitudeInput.value =
                        longitude;
                }


                displayCoordinates(
                    latitude,
                    longitude
                );


                await reverseGeocode(
                    latitude,
                    longitude
                );

            }
        );


            const isRetina = L.Browser.retina;

            const baseUrl =
                "https://maps.geoapify.com/v1/tile/osm-bright/{z}/{x}/{y}.png?apiKey={apiKey}";

            const retinaUrl =
                "https://maps.geoapify.com/v1/tile/osm-bright/{z}/{x}/{y}@2x.png?apiKey={apiKey}";


            L.tileLayer(
                isRetina ? retinaUrl : baseUrl,
                {
                    apiKey: API_KEY,
                    maxZoom: 20,

                    attribution:
                        'Powered by <a href="https://www.geoapify.com/" target="_blank">Geoapify</a> | ' +
                        '<a href="https://www.openstreetmap.org/copyright" target="_blank">© OpenStreetMap</a> contributors'
                }
            ).addTo(map);

        } else {

            map.setView(
                [lat, lon],
                17
            );

        }


        if (marker) {

            marker.setLatLng(
                [lat, lon]
            );

        } else {

            marker = L.marker(
                [lat, lon],
                {
                    draggable: true
                }
            ).addTo(map);


            // ---------------------------------------------
            // User moves the map marker
            // ---------------------------------------------

            marker.on(
                "dragend",
                async function () {

                    const position =
                        marker.getLatLng();

                    const latitude =
                        position.lat;

                    const longitude =
                        position.lng;


                    // Update hidden form fields +
                    // coordinate display
                    if (latitudeInput) {
                        latitudeInput.value =
                            latitude;
                    }

                    if (longitudeInput) {
                        longitudeInput.value =
                            longitude;
                    }


                    displayCoordinates(
                        latitude,
                        longitude
                    );


                    // Get new address from Geoapify
                    await reverseGeocode(
                        latitude,
                        longitude
                    );

                }
            );

        }


        setTimeout(function () {

            map.invalidateSize();

        }, 100);

    }


    // ======================================================
    // Store Coordinates
    // ======================================================

    function setCoordinates(
        latitude,
        longitude
    ) {

        if (latitudeInput) {

            latitudeInput.value =
                latitude;

        }

        if (longitudeInput) {

            longitudeInput.value =
                longitude;

        }


        displayCoordinates(
            latitude,
            longitude
        );


        showMap(
            latitude,
            longitude
        );

    }


    // ======================================================
    // Geoapify Address Search
    // ======================================================

    async function searchAddress(query) {

        if (
            !query ||
            query.length < 3 ||
            !suggestionsBox
        ) {

            if (suggestionsBox) {

                suggestionsBox.style.display =
                    "none";

            }

            return;

        }


        if (!API_KEY) {

            console.error(
                "Geoapify API key is missing."
            );

            return;

        }


        const params =
            new URLSearchParams({

                text: query,

                format: "json",

                limit: "6",

                filter: "countrycode:ng",

                lang: "en",

                apiKey: API_KEY

            });


        const url =
            "https://api.geoapify.com/v1/geocode/autocomplete?"
            + params.toString();


        try {

            const response =
                await fetch(url);


            if (!response.ok) {

                throw new Error(
                    "Geoapify autocomplete failed: "
                    + response.status
                );

            }


            const data =
                await response.json();


            renderSuggestions(
                data.results || []
            );


        } catch (error) {

            console.error(
                "Geoapify autocomplete error:",
                error
            );


            if (suggestionsBox) {

                suggestionsBox.style.display =
                    "none";

            }

        }

    }





    // ======================================================
    // Render Suggestions
    // ======================================================

    function applyAddressDetails(result) {

    if (!result) {
        return;
    }

    // --------------------------------------------------
    // Address
    // --------------------------------------------------

    if (
        addressInput &&
        result.formatted
    ) {
        addressInput.value =
            result.formatted;
    }


    // --------------------------------------------------
    // State
    // --------------------------------------------------

    if (
        stateSelect &&
        result.state
    ) {

        const stateName =
            result.state.replace(
                /\s+State$/i,
                ""
            );

        for (
            let i = 0;
            i < stateSelect.options.length;
            i++
        ) {

            const option =
                stateSelect.options[i];

            if (
                option.value
                    .toLowerCase()
                ===
                stateName.toLowerCase()
            ) {

                stateSelect.value =
                    option.value;

                stateSelect.dispatchEvent(
                    new Event("change")
                );

                break;
            }
        }
    }


    // --------------------------------------------------
    // City / Town
    // --------------------------------------------------

    const cityInput =
        document.getElementById(
            "id_city"
        );

    const cityName =
        result.city ||
        result.town ||
        result.village ||
        result.suburb ||
        "";


    if (
        cityInput &&
        cityName
    ) {

        cityInput.value =
            cityName;

    }


    // --------------------------------------------------
    // LGA
    // --------------------------------------------------

    if (
        lgaSelect &&
        stateSelect
    ) {

        const possibleLGA =
            result.county ||
            result.district ||
            result.city_district ||
            result.suburb ||
            "";


        if (possibleLGA) {

            setTimeout(
                function () {

                    const normalizedTarget =
                        possibleLGA
                            .toLowerCase()
                            .replace(
                                /\blocal government area\b/g,
                                ""
                            )
                            .replace(
                                /\blga\b/g,
                                ""
                            )
                            .trim();


                    for (
                        let i = 0;
                        i < lgaSelect.options.length;
                        i++
                    ) {

                        const option =
                            lgaSelect.options[i];

                        const normalizedOption =
                            option.value
                                .toLowerCase()
                                .trim();


                        if (
                            normalizedOption &&
                            (
                                normalizedOption ===
                                    normalizedTarget
                                ||
                                normalizedTarget.includes(
                                    normalizedOption
                                )
                                ||
                                normalizedOption.includes(
                                    normalizedTarget
                                )
                            )
                        ) {

                            lgaSelect.value =
                                option.value;

                            break;
                        }

                    }

                },
                50
            );

        }

    }

}

    function renderSuggestions(results) {

        if (!suggestionsBox) {
            return;
        }


        suggestionsBox.innerHTML = "";


        if (!results.length) {

            suggestionsBox.style.display =
                "none";

            return;

        }


        results.forEach(
            function (result) {

                const item =
                    document.createElement(
                        "button"
                    );


                item.type = "button";

                item.className =
                    "list-group-item " +
                    "list-group-item-action " +
                    "text-start";


                item.textContent =
                    result.formatted;


                item.addEventListener(
                    "click",
                    function () {

                        applyAddressDetails(
                            result
                        );

                        setCoordinates(
                            result.lat,
                            result.lon
                        );


                        suggestionsBox.style.display =
                            "none";

                    }
                );


                suggestionsBox.appendChild(
                    item
                );

            }
        );


        suggestionsBox.style.display =
            "block";

    }


    // ======================================================
    // Address Input Listener
    // ======================================================

    if (addressInput) {

        addressInput.addEventListener(
            "input",
            function () {

                clearTimeout(
                    searchTimer
                );


                const query =
                    addressInput.value.trim();


                searchTimer =
                    setTimeout(
                        function () {

                            searchAddress(
                                query
                            );

                        },
                        350
                    );

            }
        );

    }


    // ======================================================
    // Reverse Geocoding
    // ======================================================

                async function reverseGeocode(
                    latitude,
                    longitude
                ) {

                    if (!API_KEY) {
                        return;
                    }

                    const params =
                        new URLSearchParams({

                            lat: latitude,
                            lon: longitude,
                            format: "json",
                            apiKey: API_KEY

                        });

                    const url =
                        "https://api.geoapify.com/v1/geocode/reverse?"
                        + params.toString();

                    try {

                        const response =
                            await fetch(url);

                        if (!response.ok) {

                            throw new Error(
                                "Reverse geocoding failed: "
                                + response.status
                            );

                        }

                        const data =
                            await response.json();

                        if (
                            data.results &&
                            data.results.length > 0
                        ) {

                            const result =
                                data.results[0];

                            applyAddressDetails(
                                result
                            );

                        }

                    } catch (error) {

                        console.error(
                            "Reverse geocoding error:",
                            error
                        );

                    }

                }


    // ======================================================
    // Use My Current Location
    // ======================================================

    if (locationButton) {

        locationButton.addEventListener(
            "click",
            function () {

                if (!navigator.geolocation) {

                    alert(
                        "Your browser does not support location services."
                    );

                    return;

                }


                const originalHTML =
                    locationButton.innerHTML;


                locationButton.disabled =
                    true;


                locationButton.innerHTML = `
                    <span
                        class="spinner-border
                               spinner-border-sm
                               me-2"
                        role="status">
                    </span>

                    Finding Location...
                `;


                navigator.geolocation
                    .getCurrentPosition(

                        async function (
                            position
                        ) {

                            const latitude =
                                position.coords
                                    .latitude;

                            const longitude =
                                position.coords
                                    .longitude;


                            setCoordinates(
                                latitude,
                                longitude
                            );


                            await reverseGeocode(
                                latitude,
                                longitude
                            );


                            locationButton.disabled =
                                false;


                            locationButton.innerHTML =
                                originalHTML;

                        },


                        function (error) {

                            locationButton.disabled =
                                false;


                            locationButton.innerHTML =
                                originalHTML;


                            let message =
                                "Unable to determine your current location.";


                            if (
                                error.code ===
                                error.PERMISSION_DENIED
                            ) {

                                message =
                                    "Location permission was denied. " +
                                    "Please allow location access " +
                                    "in your browser and try again.";

                            }


                            else if (
                                error.code ===
                                error.POSITION_UNAVAILABLE
                            ) {

                                message =
                                    "Your current location is unavailable.";

                            }


                            else if (
                                error.code ===
                                error.TIMEOUT
                            ) {

                                message =
                                    "Location request timed out. " +
                                    "Please try again.";

                            }


                            alert(message);


                            console.error(
                                "Geolocation error:",
                                error
                            );

                        },


                        {
                            enableHighAccuracy:
                                true,

                            timeout:
                                15000,

                            maximumAge:
                                0
                        }

                    );

            }
        );

    }


    // ======================================================
    // Close Suggestions When Clicking Outside
    // ======================================================

    document.addEventListener(
        "click",
        function (event) {

            if (
                suggestionsBox &&
                addressInput &&
                !suggestionsBox.contains(
                    event.target
                ) &&
                event.target !== addressInput
            ) {

                suggestionsBox.style.display =
                    "none";

            }

        }
    );


    console.log(
        "Geoapify location services initialized."
    );

});