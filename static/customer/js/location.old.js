console.log("========== LOCATION.JS LOADED ==========");

/******************************************************************************
 * Property Location Module
 * Customer Assessment - Step 2
 *
 * Responsibilities:
 * 1. State / LGA
 * 2. Google Places (coming next)
 * 3. Coordinates (coming next)
 * 4. Validation (coming next)
 ******************************************************************************/

/* ==========================================================================
   DOM Elements
   ========================================================================== */

const elements = {

    state: null,
    lga: null,
    city: null,
    address: null,

    latitude: null,
    longitude: null,

    map: null,

    coordinatePanel: null,
    latitudeDisplay: null,
    longitudeDisplay: null,

    currentLocationButton: null

};

/* ==========================================================================
   Google Maps Objects
   ========================================================================== */

let map = null;
let marker = null;
let geocoder = null;


/* ==========================================================================
   State / LGA
   ========================================================================== */

function populateStates() {

    Object.keys(STATE_LGAS)
        .sort()
        .forEach(stateName => {

            elements.state.add(
                new Option(stateName, stateName)
            );

        });

}

function populateLGAs(selectedState) {

    elements.lga.innerHTML = "";

    elements.lga.add(
        new Option("Select LGA", "")
    );

    if (!selectedState) {
        return;
    }

    STATE_LGAS[selectedState].forEach(lga => {

        elements.lga.add(
            new Option(lga, lga)
        );

    });

}

function initStateLGA() {

    populateStates();

    elements.state.addEventListener("change", function () {

        populateLGAs(this.value);

    });

}


/* ==========================================================================
   Google Places
   ========================================================================== */

async function initGooglePlaces() {
    if (!elements.address) return;

    try {
        const {
            AutocompleteSuggestion,
            AutocompleteSessionToken
        } = await google.maps.importLibrary("places");

        const input = elements.address;

        const suggestionsBox = document.createElement("div");
        suggestionsBox.className = "list-group shadow-sm";
        suggestionsBox.style.cssText =
            "position:relative;z-index:1000;width:100%;";

        input.insertAdjacentElement("afterend", suggestionsBox);

        let sessionToken = null;
        let debounceTimer = null;
        let requestId = 0;

        input.addEventListener("input", function () {
            clearTimeout(debounceTimer);
            const currentRequest = ++requestId;
            const query = input.value.trim();

            suggestionsBox.replaceChildren();

            // Prevent old coordinates from being saved
            // after the user manually changes an address.
            if (elements.latitude) elements.latitude.value = "";
            if (elements.longitude) elements.longitude.value = "";

            if (elements.coordinatePanel) {
                elements.coordinatePanel.style.display = "none";
            }

            if (elements.map) {
                elements.map.style.display = "none";
            }

            if (query.length < 3) return;

            if (!sessionToken) {
                sessionToken = new AutocompleteSessionToken();
            }

            debounceTimer = setTimeout(async () => {
                try {
                    const { suggestions } =
                        await AutocompleteSuggestion
                            .fetchAutocompleteSuggestions({
                                input: query,
                                includedRegionCodes: ["ng"],
                                language: "en",
                                sessionToken: sessionToken
                            });

                    // Discard responses from older searches.
                    if (currentRequest !== requestId) return;

                    suggestionsBox.replaceChildren();

                    for (const suggestion of suggestions) {
                        const prediction = suggestion.placePrediction;
                        if (!prediction) continue;

                        const button = document.createElement("button");
                        button.type = "button";
                        button.className =
                            "list-group-item list-group-item-action";

                        button.textContent = prediction.text.toString();

                        button.addEventListener("click", async () => {
                            ++requestId;
                            suggestionsBox.replaceChildren();

                            try {
                                const place = prediction.toPlace();

                                await place.fetchFields({
                                    fields: [
                                        "formattedAddress",
                                        "location",
                                        "addressComponents"
                                    ]
                                });

                                if (!place.location) return;

                                input.value =
                                    place.formattedAddress || "";

                                // Reuse the original coordinate logic.
                                const legacyShape = {
                                    geometry: {
                                        location: place.location
                                    }
                                };

                                updateCoordinates(legacyShape);

                                // Adapt the new address components
                                // to the existing State/LGA parser.
                                populateAddressFields(
                                    (place.addressComponents || []).map(
                                        component => ({
                                            types: component.types,
                                            long_name: component.longText
                                        })
                                    )
                                );

                                // Reuse the original map and marker.
                                showMap(legacyShape);

                                // Start a fresh billing session next time.
                                sessionToken = null;

                            } catch (error) {
                                console.error(
                                    "Address selection failed:",
                                    error
                                );
                            }
                        });

                        suggestionsBox.appendChild(button);
                    }

                } catch (error) {
                    console.error(
                        "Autocomplete suggestions failed:",
                        error
                    );
                }
            }, 350);
        });

        console.log("Single-field Google Autocomplete ready.");

    } catch (error) {
        console.error("Google Places failed to initialize:", error);
    }
}


//function initGooglePlaces() {
//
//    if (!elements.address) {
//        return;
//    }
//
//    if (
//        typeof google === "undefined" ||
//        !google.maps ||
//        !google.maps.places
//    ) {
//        console.error("Google Places API failed to load.");
//        return;
//    }
//
//    const autocomplete = new google.maps.places.Autocomplete(
//        elements.address,
//        {
//            types: ["address"],
//            componentRestrictions: {
//                country: "ng"
//            },
//            fields: [
//                "formatted_address",
//                "geometry",
//                "address_components"
//            ]
//        }
//    );
//
//    autocomplete.addListener("place_changed", () => {
//
//        const place = autocomplete.getPlace();
//
//        if (!place.geometry) {
//            console.warn("No geometry returned from Google.");
//            return;
//        }
//
//        /* ------------------------------------------
//           Update Address
//        ------------------------------------------- */
//
//        elements.address.value = place.formatted_address;
//
//        /* ------------------------------------------
//           Update Coordinates
//        ------------------------------------------- */
//
//        elements.latitude.value = place.geometry.location.lat();
//        elements.longitude.value = place.geometry.location.lng();
//
//        /* ------------------------------------------
//           Update City (Best Effort)
//        ------------------------------------------- */
//
//        if (elements.city && place.address_components) {
//
//            const cityComponent = place.address_components.find(component =>
//                component.types.includes("locality") ||
//                component.types.includes("administrative_area_level_2")
//            );
//
//            if (cityComponent) {
//                elements.city.value = cityComponent.long_name;
//            }
//        }
//
//        console.log("Address:", elements.address.value);
//        console.log("Latitude:", elements.latitude.value);
//        console.log("Longitude:", elements.longitude.value);
//
//        updateCoordinates(place);
//        populateAddressFields(place.address_components);
//        showMap(place);
//
//    });
//
//}

/* ==========================================================================
   Coordinates
   ========================================================================== */

function updateCoordinates(place) {

    if (!place.geometry) {
        return;
    }

    elements.latitude.value =
        place.geometry.location.lat();

    elements.longitude.value =
        place.geometry.location.lng();

    console.log("Coordinates updated successfully.");

    refreshCoordinateDisplay();

}


/* ==========================================================================
   Coordinate Display
   ========================================================================== */

function refreshCoordinateDisplay() {

    if (!elements.coordinatePanel) {
        return;
    }

    elements.coordinatePanel.style.display = "block";

    elements.latitudeDisplay.textContent =
        elements.latitude.value;

    elements.longitudeDisplay.textContent =
        elements.longitude.value;

}


/* ==========================================================================
   Google Map
   ========================================================================== */
function showMap(place) {

    if (!place.geometry) {
        return;
    }

    elements.map.style.display = "block";

    // Trigger fade-in animation
    requestAnimationFrame(() => {
        elements.map.classList.add("show");
    });

    if (!geocoder) {
        geocoder = new google.maps.Geocoder();
    }

    if (!map) {

        map = new google.maps.Map(elements.map, {

            center: place.geometry.location,

            zoom: 18,

            mapTypeControl: false,

            streetViewControl: false,

            fullscreenControl: true,

        });

    } else {

        map.panTo(place.geometry.location);

    }

    if (!marker) {

        marker = new google.maps.Marker({

            map: map,

            draggable: true,

            animation: google.maps.Animation.DROP,

        });

        marker.addListener("dragend", onMarkerDragged);

    }

    marker.setPosition(place.geometry.location);

    map.panTo(place.geometry.location);

    map.setZoom(18);

}


/* ==========================================================================
   Marker Drag
   ========================================================================== */

function onMarkerDragged() {

    const position = marker.getPosition();

    elements.latitude.value = position.lat();

    elements.longitude.value = position.lng();

    refreshCoordinateDisplay();

    reverseGeocode(position);

    console.log("Marker moved.");

    console.log("Latitude:", elements.latitude.value);

    console.log("Longitude:", elements.longitude.value);

}


/* ==========================================================================
   Reverse Geocoding
   ========================================================================== */

function reverseGeocode(position) {

    if (!geocoder) {
        return;
    }

    geocoder.geocode(
        {
            location: position
        },
        function (results, status) {

            if (
                status !== "OK" ||
                !results ||
                !results.length
            ) {
                console.warn("Reverse geocoding failed.");
                return;
            }

            const result = results[0];

            elements.address.value = result.formatted_address;

            populateAddressFields(result.address_components);

        }
    );

}


/* ==========================================================================
   Current Location
   ========================================================================== */

function useCurrentLocation() {

    if (!navigator.geolocation) {

        alert("Geolocation is not supported by this browser.");

        return;

    }

    navigator.geolocation.getCurrentPosition(

        onCurrentLocationSuccess,

        onCurrentLocationError,

        {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0
        }

    );

}

/*==========================================================================
Success Callback
 ===========================================================================*/

 function onCurrentLocationSuccess(position) {

    const latitude = position.coords.latitude;

    const longitude = position.coords.longitude;

    elements.latitude.value = latitude;
    elements.longitude.value = longitude;

    refreshCoordinateDisplay();

    const location = new google.maps.LatLng(
        latitude,
        longitude
    );

    showMap({

        geometry: {
            location: location
        }

    });

    reverseGeocode(location);

}

/*==========================================================================
Error Callback
 ===========================================================================*/


function onCurrentLocationError(error) {

    switch (error.code) {

        case error.PERMISSION_DENIED:

            alert("Location permission was denied.");

            break;

        case error.POSITION_UNAVAILABLE:

            alert("Unable to determine your location.");

            break;

        case error.TIMEOUT:

            alert("Location request timed out.");

            break;

        default:

            alert("Unable to retrieve your location.");

    }

}


/* ==========================================================================
   Address Components
   ========================================================================== */

function populateAddressFields(addressComponents) {

    if (!addressComponents) {
        return;
    }

    const state = addressComponents.find(component =>
        component.types.includes("administrative_area_level_1")
    );

    const lga = addressComponents.find(component =>
        component.types.includes("administrative_area_level_2")
    );

    const city = addressComponents.find(component =>
        component.types.includes("locality")
    );

    /* ------------------------------
       State
    ------------------------------ */

    if (state && elements.state) {

        elements.state.value = state.long_name;

        populateLGAs(state.long_name);

    }

    /* ------------------------------
       LGA
    ------------------------------ */

    if (lga && elements.lga) {

        const optionExists = [...elements.lga.options]
            .some(option => option.value === lga.long_name);

        if (optionExists) {
            elements.lga.value = lga.long_name;
        }

    }

    /* ------------------------------
       City
    ------------------------------ */

    if (city && elements.city) {
        elements.city.value = city.long_name;
    }

}

/* ==========================================================================
   Validation
   ========================================================================== */

function initValidation() {

    // Coming later

}


/* ==========================================================================
   Initialization
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {

    elements.state = document.getElementById("id_state");
    elements.lga = document.getElementById("id_lga");
    elements.address = document.getElementById("id_address");
    elements.latitude = document.getElementById("id_latitude");
    elements.longitude = document.getElementById("id_longitude");
    elements.city = document.getElementById("id_city");
    elements.map = document.getElementById("property-map");
    elements.coordinatePanel = document.getElementById("coordinate-panel");
    elements.latitudeDisplay = document.getElementById("latitude-display");
    elements.longitudeDisplay = document.getElementById("longitude-display");
    elements.currentLocationButton = document.getElementById("current-location-btn");


    if (elements.currentLocationButton) {

    elements.currentLocationButton.addEventListener(
        "click",
        useCurrentLocation
    );

}

    initStateLGA();
    initGooglePlaces();
    initValidation();

});