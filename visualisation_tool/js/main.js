const aeroe_coords = [54.887, 10.345]

const map = L.map('mapid', {
    center: aeroe_coords,
    zoom: 12,
});

const background = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
 
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map)
    
const southWest = L.latLng(10.1997580729999999,54.8144306780000008);
const northEast = L.latLng(10.5523710469999994,54.9718533989999969);
const mybounds = L.latLngBounds(southWest, northEast);

const stonewalls_antialiased = L.tileLayer('http://127.0.0.1:8887/data/OUTPUT/{z}/{x}/{y}.png', {
    tms: true,
    minZoom: 12,
    maxZoom: 18,
    MaxNativeZoom: 20,
    // bounds: mybounds,
}).addTo(map)

const prediction = L.tileLayer('http://127.0.0.1:8887/data/prediction_tiles/{z}/{x}/{y}.png', {
    tms: true,
    minZoom: 12,
    maxZoom: 18,
    MaxNativeZoom: 20,
    // bounds: mybounds,
}).addTo(map)

const stonewall_original = new L.GeoJSON(stonewalls_geojson_4326, {
    style: {
        color: "blue",
    
        weight: 1.5,
    },
    onEachFeature: function (feature, layer) {
        popupOptions = {maxWidth: 200};
        layer.bindPopup("<b>Dige ID:</b> " + feature.properties.DigeID +
            "<br><b>Oprettet: </b>" + feature.properties.Oprettet.split(" ")[0] +
            "<br><br>Here is a text box that we can fill with some sort of text. Not sure if there's any information we actually want to put here."
            ,popupOptions);
    }
}).addTo(map)


stonewall_original.on('click', function(e) {
    if (e.layer) {
        console.log(e.layer.feature.properties);
    }
})

const baseMaps = {
    "OSM Background": background,
}

const features = {
    "Final Prediction": prediction,
    "Initial Validation": stonewalls_antialiased,
    "Original Dataset": stonewall_original,
    }
    
L.control.layers(baseMaps, features, {collapsed: false}).addTo(map);



