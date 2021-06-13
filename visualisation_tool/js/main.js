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

const stonewalls_antialiased = L.tileLayer('http://127.0.0.1:5500/data/OUTPUT/{z}/{x}/{y}.png', {
    tms: true,
    minZoom: 12,
    maxZoom: 18,
    MaxNativeZoom: 20,
    // bounds: mybounds,
}).addTo(map)

const prediction = L.tileLayer('http://127.0.0.1:5500/data/prediction_tiles/{z}/{x}/{y}.png', {
    tms: true,
    minZoom: 12,
    maxZoom: 18,
    MaxNativeZoom: 20,
    // bounds: mybounds,
}).addTo(map)

const stonewall_original = new L.GeoJSON(stonewalls_geojson_4326, {
    style: {
        color: "blue",
    
        weight: 1,
    },
    onEachFeature: function (feature, layer) {
        popupOptions = {maxWidth: 250};
        layer.bindPopup("<b>Dige ID:</b> " + feature.properties.DigeID +
            "<br><b>Oprettet: </b>" + feature.properties.Oprettet.split(" ")[0] +
            "<br><br>Here is a text box that we can fill with some sort of text"
            ,popupOptions);
    }
}).addTo(map)


stonewall_original.on('click', function(e) {
    if (e.layer) {
        console.log(e.layer.feature.properties);
    }
})


const removed_walls = new L.GeoJSON(filtered_removed_walls_4326_img_geojson, {
    style: function(feature) {
        if (feature.properties.image) {
            return {        
                fillColor: 'red',
                weight: 2.5,
                color: 'yellow',
                smoothFactor: 2,
                }
        }
        else
            return {
                color: 'red',
                weight: 1,
                }
    },

    onEachFeature: function (feature, layer) {
        var popupImg = "<br><b>Eksempel : </b>" + feature.properties.validation + "<img class= 'img-in-popup' src='" + feature.properties.image + "'>";
        var popupText = "<b>Dige ID:</b> " + feature.properties.objectid +
        "<br><b>Oprettet: </b>" + feature.properties.oprettet.split(" ")[0] +
        "<br><b>Sidste opdateret: </b>" + feature.properties.systid_fra.split(" ")[0] +
        "<br><b>Længden af berørte digedele: </b>" + feature.properties.length_m.toFixed(2) + " meter</br>";
        
        if (feature.properties.image) 
        layer.bindPopup(popupText + popupImg, {maxWidth: "auto"});
        else 
        layer.bindPopup(popupText);

    }
}).addTo(map)

removed_walls.on('click', function(e) {
    if (e.layer) {
        console.log(e.layer.feature.properties);
    }
})

const found_walls = new L.GeoJSON(example_found_walls, {
    style: function(feature) {
        if (feature.properties.image) {
            return {        
                fillColor: 'purple',
                weight: 2.5,
                color: 'orange',
                smoothFactor: 2,
                }
        }
        else
            return {
                color: 'purple',
                weight: 1,
                }
    },

    onEachFeature: function (feature, layer) {
        var popupImg = "<br><b>Eksempel : </b>" + feature.properties.validation + "<img class= 'img-in-popup' src='" + feature.properties.image + "'>";
        
        if (feature.properties.image) 
        layer.bindPopup(popupImg, {maxWidth: "auto"});
        else 
        layer.bindPopup("<b>Eksemple:</b> " + feature.properties.validation);

    }
}).addTo(map)

found_walls.on('click', function(e) {
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
    "Removed stone walls": removed_walls,
    "Example of found walls": found_walls,
    }
    
L.control.layers(baseMaps, features, {collapsed: false}).addTo(map);



