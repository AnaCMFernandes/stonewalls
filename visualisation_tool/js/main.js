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
        color: "orange",
    
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
    style: {
           color: 'red',

           weight: 1,
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
                weight: 1,
                color: 'blue',
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

const filtered_found_500 = new L.GeoJSON(filtered_found_500_4326_geojson, {
    style: {
        color: "blue",
    
        weight: 1,
    },

}).addTo(map)

// filtered_found_500_4326_geojson.on('click', function(e) {
//     if (e.layer) {
//         console.log(e.layer.feature.properties);
//     }
// })

icon_new = L.divIcon({
	className: 'custom-div-icon',
        html: "<div style='background-color:#4281f5';' class='marker-pin'></div>",
        iconSize: [30, 42],
        iconAnchor: [15, 42]
    });

icon_rem = L.divIcon({
    className: 'custom-div-icon',
        html: "<div style='background-color:#f54242;' class='marker-pin'></div>",
        iconSize: [30, 42],
        iconAnchor: [15, 42]
    });


var wall_1 = L.marker([54.955368721939244, 10.2249294934193], {icon: icon_new}).bindPopup('Example of predicted new stone wall. Click on the wall for image.'),
    wall_2 = L.marker([54.955228862870165, 10.225110581380115], {icon: icon_new}).bindPopup('Example of predicted new stone wall. Click on the wall for image.'),
    wall_3 = L.marker([54.956377206754915, 10.224057661956104,], {icon: icon_new}).bindPopup('Example of predicted new stone wall. Click on the wall for image.'),
    wall_4 = L.marker([54.878147488748269, 10.331451047378346], {icon: icon_new}).bindPopup('Example of predicted new stone wall. Click on the wall for image.'),
    wall_5 = L.marker([54.845065977693395, 10.367429529185452], {icon: icon_new}).bindPopup('Example of predicted new stone wall. Click on the wall for image.'),
    wall_6 = L.marker([54.84613593682873, 10.373866918335558], {icon: icon_new}).bindPopup('Example of predicted new stone wall. Click on the wall for image.'),
    wall_7 = L.marker([54.844889538244431, 10.375909761579445], {icon: icon_new}).bindPopup('Example of predicted new stone wall. Click on the wall for image.'),
    wall_8 = L.marker([54.840167385414958, 10.423951215274126], {icon: icon_new}).bindPopup('Example of predicted new stone wall. Click on the wall for image.'),
    wall_9 = L.marker([54.845909076513507, 10.501657828576663], {icon: icon_new}).bindPopup('Example of predicted new stone wall. Click on the wall for image.'),
    wall_10 = L.marker([54.84238767935274, 10.500415483858058], {icon: icon_new}).bindPopup('Example of predicted new stone wall. Click on the wall for image.');

    
var Found_Examples = L.layerGroup([wall_1, wall_2, wall_3, wall_4, wall_5, wall_6, wall_7, wall_8, wall_9, wall_10]);

var nowall_1 = L.marker([54.959369099467729, 10.219892502308168], {icon: icon_rem}).bindPopup('Example of a removed/damaged stone wall. Click on the wall for image.'),
    nowall_2 = L.marker([54.857966485995043, 10.472710506255192], {icon: icon_rem}).bindPopup('Example of a removed/damaged stone wall. Click on the wall for image.'),
    nowall_3 = L.marker([54.860737969367065, 10.472740591692114], {icon: icon_rem}).bindPopup('Example of a removed/damaged stone wall. Click on the wall for image.'),
    nowall_4 = L.marker([54.946770698741744, 10.236846664197476], {icon: icon_rem}).bindPopup('Example of a removed/damaged stone wall. Click on the wall for image.'),
    nowall_5 = L.marker([54.946721314538742, 10.236772405757392], {icon: icon_rem}).bindPopup('Example of a removed/damaged stone wall. Click on the wall for image.');

var Removed_Examples = L.layerGroup([nowall_1, nowall_2, nowall_3, nowall_4, nowall_5]);


const baseMaps = {
    "OSM Background": background,
}

const features = {
    "Original Dataset": stonewall_original, 
    "Removed stone walls": removed_walls, Removed_Examples,
    "Visited found walls": found_walls, Found_Examples,
    "Found stone walls": filtered_found_500,
    "Final Prediction": prediction,
    "Initial Validation": stonewalls_antialiased,
}
    
L.control.layers(baseMaps, features, {collapsed: false}).addTo(map);



