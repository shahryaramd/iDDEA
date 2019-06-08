$(document).ready(function() {
    // the "href" attribute of the modal trigger must specify the modal ID that wants to be triggered
    $('.modal').modal();
});

L.Control.Layers.include({
	_addItem: function (obj) {
		var label = document.createElement('label'),
		    checked = this._map.hasLayer(obj.layer),
		    input;

		if (obj.overlay) {
			input = document.createElement('input');
			input.type = 'checkbox';
			input.className = 'leaflet-control-layers-selector';
			input.defaultChecked = checked;
		} else {
			input = this._createRadioElement('leaflet-base-layers', checked);
		}

		input.layerId = L.stamp(obj.layer);
    // Create an explicit ID so that we can associate a <label> to the <input>.
    var id = input.id = 'leaflet-layers-control-layer-' + input.layerId;

		L.DomEvent.on(input, 'click', this._onInputClick, this);

		// Use a <label> instead of a <span> and associate it to the <input>.
		var name = document.createElement('label');
		name.innerHTML = ' ' + obj.name;
    name.setAttribute('for', id);

		// Helps from preventing layer control flicker when checkboxes are disabled
		// https://github.com/Leaflet/Leaflet/issues/2771
		var holder = document.createElement('div');

		label.appendChild(holder);
		holder.appendChild(input);
		holder.appendChild(name);

		var container = obj.overlay ? this._overlaysList : this._baseLayersList;
		container.appendChild(label);

		this._checkDisabledLayers();
		return label;
}
});

$('.modal').modal({
    dismissible: true, // Modal can be dismissed by clicking outside of the modal
    opacity: .5, // Opacity of modal background
    inDuration: 300, // Transition in duration
    outDuration: 200, // Transition out duration
    startingTop: '4%', // Starting top style attribute
    endingTop: '10%', // Ending top style attribute
    ready: function(modal, trigger) { // Callback for Modal open. Modal and trigger parameters available.
        alert("Ready");
        console.log(modal, trigger);
    },
    complete: function() {
        alert('Closed');
    } // Callback for Modal close
});
// Initialize date

function initialize() {
    var monthNames = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];

    var date = new Date();
    date.setDate(date.getDate() - 1);
    var yyyy = date.getFullYear().toString();
    var mm = (date.getMonth() + 1).toString(); // getMonth() is zero-based
    var mmfull = (monthNames[date.getMonth()]).toString();
    var dd = date.getDate().toString();
    var reqDate = yyyy + (mm[1] ? mm : "0" + mm[0]) + (dd[1] ? dd : "0" + dd[0]);

    document.getElementById('forecastdate').value = (dd[1] ? dd : "0" + dd[0]) + " " + mmfull + ", " + yyyy;
    document.getElementById('visdate').value = (dd[1] ? dd : "0" + dd[0]) + " " + mmfull + ", " + yyyy;
    document.getElementById('optimdate').value = (dd[1] ? dd : "0" + dd[0]) + " " + mmfull + ", " + yyyy;
    document.getElementById('downloaddate').value = (dd[1] ? dd : "0" + dd[0]) + " " + mmfull + ", " + yyyy;
    document.getElementById('assessdate').value = (dd[1] ? dd : "0" + dd[0]) + " " + mmfull + ", " + yyyy;

    var date = new Date();
    date.setDate(date.getDate() - 9);
    var yyyy = date.getFullYear().toString();
    var mm = (date.getMonth() + 1).toString(); // getMonth() is zero-based
    var mmfull = (monthNames[date.getMonth()]).toString();
    var dd = date.getDate().toString();
    var reqDate_fc = yyyy + (mm[1] ? mm : "0" + mm[0]) + (dd[1] ? dd : "0" + dd[0]);
    document.getElementById('assessdate_fc').value = (dd[1] ? dd : "0" + dd[0]) + " " + mmfull + ", " + yyyy;

    // document.getElementById('selInfo').innerHTML = "Please select Basin.";
}

// Functions for incrementing/decrementing date

function decreaseForecastDate() {
    var monthNames = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];
    el = document.getElementById('forecastdate');
    var curdate = new Date(el.value);
    curdate.setDate(curdate.getDate() - 1);
    var yyyy = curdate.getFullYear().toString();
    var mm = (curdate.getMonth() + 1).toString(); // getMonth() is zero-based
    var mmfull = (monthNames[curdate.getMonth()]).toString();
    var dd = curdate.getDate().toString();
    el.value = (dd[1] ? dd : "0" + dd[0]) + " " + mmfull + ", " + yyyy;
    ev = document.createEvent('Event');
    ev.initEvent('change', true, false);
    el.dispatchEvent(ev);

}

function increaseForecastDate() {
    var monthNames = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];
    el = document.getElementById('forecastdate');

    var curdate = new Date(el.value);
    curdate.setDate(curdate.getDate() + 1);
    var yyyy = curdate.getFullYear().toString();
    var mm = (curdate.getMonth() + 1).toString(); // getMonth() is zero-based
    var mmfull = (monthNames[curdate.getMonth()]).toString();
    var dd = curdate.getDate().toString();
    el.value = (dd[1] ? dd : "0" + dd[0]) + " " + mmfull + ", " + yyyy;
    ev = document.createEvent('Event');
    ev.initEvent('change', true, false);
    el.dispatchEvent(ev);
}

function decreaseVisDate() {
    var monthNames = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];
    el = document.getElementById('visdate');
    var curdate = new Date(el.value);
    curdate.setDate(curdate.getDate() - 1);
    var yyyy = curdate.getFullYear().toString();
    var mm = (curdate.getMonth() + 1).toString(); // getMonth() is zero-based
    var mmfull = (monthNames[curdate.getMonth()]).toString();
    var dd = curdate.getDate().toString();
    el.value = (dd[1] ? dd : "0" + dd[0]) + " " + mmfull + ", " + yyyy;
    ev = document.createEvent('Event');
    ev.initEvent('change', true, false);
    el.dispatchEvent(ev);

}

function increaseVisDate() {
    var monthNames = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];
    el = document.getElementById('visdate');

    var curdate = new Date(el.value);
    curdate.setDate(curdate.getDate() + 1);
    var yyyy = curdate.getFullYear().toString();
    var mm = (curdate.getMonth() + 1).toString(); // getMonth() is zero-based
    var mmfull = (monthNames[curdate.getMonth()]).toString();
    var dd = curdate.getDate().toString();
    el.value = (dd[1] ? dd : "0" + dd[0]) + " " + mmfull + ", " + yyyy;
    ev = document.createEvent('Event');
    ev.initEvent('change', true, false);
    el.dispatchEvent(ev);
}


function decreaseOptimDate() {
    var monthNames = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];
    el = document.getElementById('optimdate');
    var curdate = new Date(el.value);
    curdate.setDate(curdate.getDate() - 1);
    var yyyy = curdate.getFullYear().toString();
    var mm = (curdate.getMonth() + 1).toString(); // getMonth() is zero-based
    var mmfull = (monthNames[curdate.getMonth()]).toString();
    var dd = curdate.getDate().toString();
    el.value = (dd[1] ? dd : "0" + dd[0]) + " " + mmfull + ", " + yyyy;
    ev = document.createEvent('Event');
    ev.initEvent('change', true, false);
    el.dispatchEvent(ev);

}

function increaseOptimDate() {
    var monthNames = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];
    el = document.getElementById('optimdate');

    var curdate = new Date(el.value);
    curdate.setDate(curdate.getDate() + 1);
    var yyyy = curdate.getFullYear().toString();
    var mm = (curdate.getMonth() + 1).toString(); // getMonth() is zero-based
    var mmfull = (monthNames[curdate.getMonth()]).toString();
    var dd = curdate.getDate().toString();
    el.value = (dd[1] ? dd : "0" + dd[0]) + " " + mmfull + ", " + yyyy;
    ev = document.createEvent('Event');
    ev.initEvent('change', true, false);
    el.dispatchEvent(ev);
}

function decreaseDownloadDate() {
    var monthNames = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];
    el = document.getElementById('downloaddate');
    var curdate = new Date(el.value);
    curdate.setDate(curdate.getDate() - 1);
    var yyyy = curdate.getFullYear().toString();
    var mm = (curdate.getMonth() + 1).toString(); // getMonth() is zero-based
    var mmfull = (monthNames[curdate.getMonth()]).toString();
    var dd = curdate.getDate().toString();
    el.value = (dd[1] ? dd : "0" + dd[0]) + " " + mmfull + ", " + yyyy;
    ev = document.createEvent('Event');
    ev.initEvent('change', true, false);
    el.dispatchEvent(ev);

}

function increaseDownloadDate() {
    var monthNames = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];
    el = document.getElementById('downloaddate');

    var curdate = new Date(el.value);
    curdate.setDate(curdate.getDate() + 1);
    var yyyy = curdate.getFullYear().toString();
    var mm = (curdate.getMonth() + 1).toString(); // getMonth() is zero-based
    var mmfull = (monthNames[curdate.getMonth()]).toString();
    var dd = curdate.getDate().toString();
    el.value = (dd[1] ? dd : "0" + dd[0]) + " " + mmfull + ", " + yyyy;
    ev = document.createEvent('Event');
    ev.initEvent('change', true, false);
    el.dispatchEvent(ev);
}

function decreaseAssessDate() {
    var monthNames = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];
    el = document.getElementById('assessdate');
    var curdate = new Date(el.value);
    curdate.setDate(curdate.getDate() - 1);
    var yyyy = curdate.getFullYear().toString();
    var mm = (curdate.getMonth() + 1).toString(); // getMonth() is zero-based
    var mmfull = (monthNames[curdate.getMonth()]).toString();
    var dd = curdate.getDate().toString();
    el.value = (dd[1] ? dd : "0" + dd[0]) + " " + mmfull + ", " + yyyy;
    ev = document.createEvent('Event');
    ev.initEvent('change', true, false);
    el.dispatchEvent(ev);

}

function increaseAssessDate() {
    var monthNames = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];
    el = document.getElementById('assessdate');

    var curdate = new Date(el.value);
    curdate.setDate(curdate.getDate() + 1);
    var yyyy = curdate.getFullYear().toString();
    var mm = (curdate.getMonth() + 1).toString(); // getMonth() is zero-based
    var mmfull = (monthNames[curdate.getMonth()]).toString();
    var dd = curdate.getDate().toString();
    el.value = (dd[1] ? dd : "0" + dd[0]) + " " + mmfull + ", " + yyyy;
    ev = document.createEvent('Event');
    ev.initEvent('change', true, false);
    el.dispatchEvent(ev);
}

// forecast assessment
function decreaseAssessDate_fc() {
    var monthNames = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];
    el = document.getElementById('assessdate_fc');
    var curdate = new Date(el.value);
    curdate.setDate(curdate.getDate() - 1);
    var yyyy = curdate.getFullYear().toString();
    var mm = (curdate.getMonth() + 1).toString(); // getMonth() is zero-based
    var mmfull = (monthNames[curdate.getMonth()]).toString();
    var dd = curdate.getDate().toString();
    el.value = (dd[1] ? dd : "0" + dd[0]) + " " + mmfull + ", " + yyyy;
    ev = document.createEvent('Event');
    ev.initEvent('change', true, false);
    el.dispatchEvent(ev);

}

function increaseAssessDate_fc() {
    var monthNames = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];
    el = document.getElementById('assessdate_fc');

    var curdate = new Date(el.value);
    curdate.setDate(curdate.getDate() + 1);
    var yyyy = curdate.getFullYear().toString();
    var mm = (curdate.getMonth() + 1).toString(); // getMonth() is zero-based
    var mmfull = (monthNames[curdate.getMonth()]).toString();
    var dd = curdate.getDate().toString();
    el.value = (dd[1] ? dd : "0" + dd[0]) + " " + mmfull + ", " + yyyy;
    ev = document.createEvent('Event');
    ev.initEvent('change', true, false);
    el.dispatchEvent(ev);
}

//Materialize options
$(document).ready(function() {
    $('select').material_select();
});

$('.datepicker').pickadate({
    selectMonths: true, // Creates a dropdown to control month
    selectYears: 15, // Creates a dropdown of 15 years to control year,
    today: 'Today',
    clear: 'Clear',
    // close: 'Ok',
    closeOnSelect: true // Close upon selecting a date,
});


function initActualChart() {

    var srcChart = ""
    if (document.getElementById('actualVar').value == "inflow") {
        srcChart = "charts/curr_inoutflow.html";
    } else if (document.getElementById('actualVar').value == "elev") {
        srcChart = "charts/curr_level.html";
    } else if (document.getElementById('actualVar').value == "hp") {
        srcChart = "charts/curr_hp.html";
    } else {
        srcChart = ""
    }

    if (srcChart == "") {
        document.getElementById('ifr_actual').innerHTML = "Please select a variable to start with!"
    } else {
        strIfr = '<iframe src=' + srcChart + ' height="430px" width="95%" frameborder="0"></iframe>'
        document.getElementById('ifr_actual').innerHTML = strIfr;
    }
}

function initForecastChart() {
    var date = new Date(document.getElementById('forecastdate').value);
    var yyyy = date.getFullYear().toString();
    var mm = (date.getMonth() + 1).toString(); // getMonth() is zero-based
    var dd = date.getDate().toString();
    var reqDate = yyyy + (mm[1] ? mm : "0" + mm[0]) + (dd[1] ? dd : "0" + dd[0]);
    if (document.getElementById('forecastVar').value == "gfs") {
        srcChart = "charts/forecast_inflow.html?date=" + reqDate;
    } else if (document.getElementById('forecastVar').value == "ann") {
        srcChart = "charts/forecast_inflowANN.html?date=" + reqDate;
    } else {
        srcChart = ""
    }

    if (srcChart == "") {
        document.getElementById('ifr_forecast').innerHTML = "GEFS will be implemented soon, stay tuned."
    } else {
        strIfr = '<iframe src=' + srcChart + ' height="430px" width="95%" frameborder="0"></iframe>'
        document.getElementById('ifr_forecast').innerHTML = strIfr;
    }

}

function initVisRaster() {
    // if ((layerControl._map)) {
    //     layerControl.remove(map);
    // }
    map.removeControl(legendVis)
    map.removeLayer(layerL1)
    map.removeLayer(layerL4)
    map.removeLayer(layerL7)
    map.removeLayer(layerL10)
    map.removeLayer(layerL15)
    var date = new Date(document.getElementById('visdate').value);
    var yyyy = date.getFullYear().toString();
    var mm = (date.getMonth() + 1).toString(); // getMonth() is zero-based
    var dd = date.getDate().toString();
    var reqDate = yyyy + (mm[1] ? mm : "0" + mm[0]) + (dd[1] ? dd : "0" + dd[0]);

    var visvar = document.getElementById('visVar').value;

    var fvar = './data/vis_data/'+reqDate + "." + visvar + ".tif"
    console.log(fvar);

    let vName = $("option:selected", visVar).text()
    if (visvar == 'precip') {
        colorRamp = 'YlGnBu'
        unit = 'mm'
    }
    else if (visvar == 'ts_max') {
        colorRamp = 'YlOrRd'
        unit = '˚C'
    }
    else if (visvar == 'ts_min') {
        colorRamp = 'YlOrRd'
        unit = '˚C'
    }
    else if (visvar == 'w_ave') {
        colorRamp = 'YlGn'
        unit = 'm/s'
    } else  {
        colorRamp = 'YlGnBu'
    }


    /* 16 lead times in GeoTIFF with multiple bands */

    d3.request(fvar).responseType('arraybuffer').get(
        function(error, tiffData) {
            //  (BAND 1)  (Lead 1)  (2nd in index)
            let lyr = L.ScalarField.fromGeoTIFF(tiffData.response, bandIndex = 1);

            layerL1 = L.canvasLayer.scalarField(lyr, {
                color: chroma.scale(colorRamp).domain(lyr.range),
                opacity: 0.65
            });
            layerL1.addTo(map);
            layerL1.on('click', function(e) {
                if (e.value !== null) {
                    let v = e.value.toFixed(0);
                    let html = (`<span class="popupText"> `+ vName +`: ${v} ` +unit+ `</span>`);
                    let popup = L.popup()
                        .setLatLng(e.latlng)
                        .setContent(html)
                        .openOn(map);
                }
            });

            //   (Lead 4)
            lyr = L.ScalarField.fromGeoTIFF(tiffData.response, bandIndex = 4);

            layerL4 = L.canvasLayer.scalarField(lyr, {
                color: chroma.scale(colorRamp).domain(lyr.range),
                opacity: 0.65
            });
            // layerL4.addTo(map);
            layerL4.on('click', function(e) {
                if (e.value !== null) {
                    let v = e.value.toFixed(0);
                    let html = (`<span class="popupText"> `+ vName +`:  ${v} ` +unit+ `</span>`);
                    let popup = L.popup()
                        .setLatLng(e.latlng)
                        .setContent(html)
                        .openOn(map);
                }
            });

            //   (Lead 7)
            lyr = L.ScalarField.fromGeoTIFF(tiffData.response, bandIndex = 7);

            layerL7 = L.canvasLayer.scalarField(lyr, {
                color: chroma.scale(colorRamp).domain(lyr.range),
                opacity: 0.65
            });
            // layerL7.addTo(map);
            layerL7.on('click', function(e) {
                if (e.value !== null) {
                    let v = e.value.toFixed(0);
                    let html = (`<span class="popupText"> `+ vName +`:  ${v} ` +unit+ `</span>`);
                    let popup = L.popup()
                        .setLatLng(e.latlng)
                        .setContent(html)
                        .openOn(map);
                }
            });

            //   (Lead 10)
             lyr = L.ScalarField.fromGeoTIFF(tiffData.response, bandIndex = 10);

            layerL10 = L.canvasLayer.scalarField(lyr, {
                color: chroma.scale(colorRamp).domain(lyr.range),
                opacity: 0.65
            });
            // layerL10.addTo(map);
            layerL10.on('click', function(e) {
                if (e.value !== null) {
                    let v = e.value.toFixed(0);
                    let html = (`<span class="popupText"> `+ vName +`:  ${v} ` +unit+ `</span>`);
                    let popup = L.popup()
                        .setLatLng(e.latlng)
                        .setContent(html)
                        .openOn(map);
                }
            });

            //   (Lead 15)
             lyr = L.ScalarField.fromGeoTIFF(tiffData.response, bandIndex = 15);

            layerL15 = L.canvasLayer.scalarField(lyr, {
                color: chroma.scale(colorRamp).domain(lyr.range),
                opacity: 0.65
            });
            // layerL15.addTo(map);
            layerL15.on('click', function(e) {
                if (e.value !== null) {
                    let v = e.value.toFixed(0);
                    let html = (`<span class="popupText"> `+ vName +`:  ${v} ` +unit+ `</span>`);
                    let popup = L.popup()
                        .setLatLng(e.latlng)
                        .setContent(html)
                        .openOn(map);
                }
            });

            // Min Temperature (BAND 1)
            // let t = L.ScalarField.fromGeoTIFF(tiffData.response, bandIndex = 1);
            // layerT = L.canvasLayer.scalarField(t, {
            //     color: chroma.scale('OrRd').domain(t.range),
            //     opacity: 0.65
            // });
            // layerT.on('click', function(e) {
            //     if (e.value !== null) {
            //         let v = e.value.toFixed(1);
            //         let html = (`<span class="popupText">Temperature ${v} ºC</span>`);
            //         let popup = L.popup()
            //             .setLatLng(e.latlng)
            //             .setContent(html)
            //             .openOn(map);
            //     }
            // });

            legendVis = L.control.layers({
                "Lead: 1 day": layerL1,
                "Lead: 4 days": layerL4,
                "Lead: 7 days": layerL7,
                "Lead: 10 days": layerL10,
                "Lead: 15 days": layerL15
            }, {}, {
                position: 'bottomleft',
                collapsed: false
            });

            legendVis.addTo(map);

            map.fitBounds(layerL1.getBounds());

        });
}
function initOptimChart() {
    var date = new Date(document.getElementById('optimdate').value);
    var yyyy = date.getFullYear().toString();
    var mm = (date.getMonth() + 1).toString(); // getMonth() is zero-based
    var dd = date.getDate().toString();
    var reqDate = yyyy + (mm[1] ? mm : "0" + mm[0]) + (dd[1] ? dd : "0" + dd[0]);
    if (document.getElementById('optimVar').value == "outflow") {
        srcChart = "charts/optim_outflow.html?date=" + reqDate;
    } else if (document.getElementById('optimVar').value == "elev") {
        srcChart = "charts/optim_elev.html?date=" + reqDate;
    } else if (document.getElementById('optimVar').value == "hp") {
        srcChart = "charts/optim_hp.html?date=" + reqDate;
    } else {
        srcChart = ""
    }

    if (srcChart == "") {
        document.getElementById('ifr_optim').innerHTML = "Please select a variable to start with!"
    } else {
        strIfr = '<iframe src=' + srcChart + ' height="430px" width="95%" frameborder="0"></iframe>'
        document.getElementById('ifr_optim').innerHTML = strIfr;
    }

}

function initAssessChart() {
    if (document.getElementById('assessType').value == "week") {
        $('#fc_elem').hide();
        var date = new Date(document.getElementById('assessdate').value);
        var yyyy = date.getFullYear().toString();
        var mm = (date.getMonth() + 1).toString(); // getMonth() is zero-based
        var dd = date.getDate().toString();
        var reqDate = yyyy + (mm[1] ? mm : "0" + mm[0]) + (dd[1] ? dd : "0" + dd[0]);

        var date = new Date(document.getElementById('assessdate_fc').value);
        var yyyy = date.getFullYear().toString();
        var mm = (date.getMonth() + 1).toString(); // getMonth() is zero-based
        var dd = date.getDate().toString();
        var reqDate_fc = yyyy + (mm[1] ? mm : "0" + mm[0]) + (dd[1] ? dd : "0" + dd[0]);

        srcChart = "charts/assess.html?date=" + reqDate + "&date_fc=" + reqDate_fc;

        if (srcChart == "") {
            document.getElementById('ifr_assess').innerHTML = "Please select a variable to start with!"
        } else {
            strIfr = '<iframe src=' + srcChart + ' height="430px" width="95%" frameborder="0"></iframe>'
            document.getElementById('ifr_assess').innerHTML = strIfr;
        }
    }
    else if (document.getElementById('assessType').value == "weekfc") {
        $('#fc_elem').show();

        var date = new Date(document.getElementById('assessdate').value);
        var yyyy = date.getFullYear().toString();
        var mm = (date.getMonth() + 1).toString(); // getMonth() is zero-based
        var dd = date.getDate().toString();
        var reqDate = yyyy + (mm[1] ? mm : "0" + mm[0]) + (dd[1] ? dd : "0" + dd[0]);

        var date = new Date(document.getElementById('assessdate_fc').value);
        var yyyy = date.getFullYear().toString();
        var mm = (date.getMonth() + 1).toString(); // getMonth() is zero-based
        var dd = date.getDate().toString();
        var reqDate_fc = yyyy + (mm[1] ? mm : "0" + mm[0]) + (dd[1] ? dd : "0" + dd[0]);
        srcChart = "charts/assess_fc.html?date=" + reqDate+"&date_fc=" + reqDate_fc;
        strIfr = '<iframe src=' + srcChart + ' height="430px" width="95%" frameborder="0"></iframe>'
        document.getElementById('ifr_assess').innerHTML = strIfr;
    }
}

function initDownload() {
    var date = new Date(document.getElementById('downloaddate').value);
    var yyyy = date.getFullYear().toString();
    var mm = (date.getMonth() + 1).toString(); // getMonth() is zero-based
    var dd = date.getDate().toString();
    var reqDate = yyyy + (mm[1] ? mm : "0" + mm[0]) + (dd[1] ? dd : "0" + dd[0]);
    if (document.getElementById('downloadData').value == "flowA") {
        document.getElementById('downloaddate').style.display = 'none';
        document.getElementById('quickdate').style.display = 'none';
        srcChart = "./data/usace_data/det_flow.txt";

    } else if (document.getElementById('downloadData').value == "elevA") {
        document.getElementById('downloaddate').style.display = 'none';
        document.getElementById('quickdate').style.display = 'none';
        srcChart = "./data/usace_data/det_elev.txt";
    } else if (document.getElementById('downloadData').value == "hpA") {
        document.getElementById('downloaddate').style.display = 'none';
        document.getElementById('quickdate').style.display = 'none';
        srcChart = "./data/usace_data/det_hp.txt";
    } else if (document.getElementById('downloadData').value == "inflowF") {
        document.getElementById('downloaddate').style.display = 'inline-block';
        document.getElementById('quickdate').style.display = 'inline-block';
        srcChart = "./data/optim_data/forecastFull_inflow_" + reqDate + ".txt";
    } else if (document.getElementById('downloadData').value == "inflowH") {
        document.getElementById('downloaddate').style.display = 'inline-block';
        document.getElementById('quickdate').style.display = 'inline-block';
        srcChart = "./data/optim_data/forecast_inflow_" + reqDate + ".txt";
    } else if (document.getElementById('downloadData').value == "inflowANN") {
        document.getElementById('downloaddate').style.display = 'inline-block';
        document.getElementById('quickdate').style.display = 'inline-block';
        srcChart = "./data/ann_data/forecast_inflow_" + reqDate + ".txt";
    } else if (document.getElementById('downloadData').value == "releaseO") {
        document.getElementById('downloaddate').style.display = 'inline-block';
        document.getElementById('quickdate').style.display = 'inline-block';
        srcChart = "./data/optim_data/release_optim_" + reqDate + ".txt";
    } else if (document.getElementById('downloadData').value == "elevO") {
        document.getElementById('downloaddate').style.display = 'inline-block';
        document.getElementById('quickdate').style.display = 'inline-block';
        srcChart = "./data/optim_data/elev_optim_" + reqDate + ".txt";
    } else if (document.getElementById('downloadData').value == "hpO") {
        document.getElementById('downloaddate').style.display = 'inline-block';
        document.getElementById('quickdate').style.display = 'inline-block';
        srcChart = "./data/optim_data/hp_optim_" + reqDate + ".txt";
    } else if (document.getElementById('downloadData').value == "releaseANN") {
        document.getElementById('downloaddate').style.display = 'inline-block';
        document.getElementById('quickdate').style.display = 'inline-block';
        srcChart = "./data/ann_data/release_optim_" + reqDate + ".txt";
    } else if (document.getElementById('downloadData').value == "elevANN") {
        document.getElementById('downloaddate').style.display = 'inline-block';
        document.getElementById('quickdate').style.display = 'inline-block';
        srcChart = "./data/ann_data/elev_optim_" + reqDate + ".txt";
    } else if (document.getElementById('downloadData').value == "hpANN") {
        document.getElementById('downloaddate').style.display = 'inline-block';
        document.getElementById('quickdate').style.display = 'inline-block';
        srcChart = "./data/ann_data/hp_optim_" + reqDate + ".txt";
    } else {
        srcChart = ""
    }

    if (srcChart == "") {
        document.getElementById('ifr_download').innerHTML = "Please select a variable to start with!"
    } else {
        strIfr = '<iframe src=' + srcChart + ' height="430px" width="95%" frameborder="0"></iframe>'
        document.getElementById('ifr_download').innerHTML = strIfr;
        document.getElementById('linkd').href = srcChart;
        document.getElementById('linkd').style = "color:#26a59a;";
    }

}

//Define Layers
var highlightLayer;

function highlightFeature(e) {
    highlightLayer = e.target;

    if (e.target.feature.geometry.type === 'LineString') {
        highlightLayer.setStyle({
            color: '#ffff00',
        });
    } else {
        highlightLayer.setStyle({
            fillColor: '#ffff00',
            fillOpacity: 1
        });
    }
}
L.ImageOverlay.include({
    getBounds: function() {
        return this._bounds;
    }
});
var map = L.map('map', {
    zoomControl: true,
    maxZoom: 28,
    minZoom: 1
});
map.setView(new L.LatLng(44.6354, -122.0794), 11);
var hash = new L.Hash(map);
var measureControl = new L.Control.Measure({
    position: 'topleft'
}, {
    activeColor: '#ABE67E'
}, {
    completedColor: '#C8F2BE'
}, {
    // primaryLengthUnit: 'meters',
    secondaryLengthUnit: 'kilometers',
    primaryAreaUnit: 'sqmeters'
    // secondaryAreaUnit: 'hectares'
});
measureControl.addTo(map);
var bounds_group = new L.featureGroup([]);
var basemap0 = L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
    maxZoom: 22,
    subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
});
basemap0.addTo(map);
var basemap1 = L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
    maxZoom: 22,
    subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
});
// basemap1.addTo(map);
var basemap2 = L.tileLayer('http://server.arcgisonline.com/ArcGIS/rest/services/World_Terrain_Base/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri &mdash; Source: USGS, Esri, TANA, DeLorme, and NPS',
    maxZoom: 13
});
// basemap2.addTo(map);
function setBounds() {}

function geoJson2heat(geojson, weight) {
    return geojson.features.map(function(feature) {
        return [
            feature.geometry.coordinates[1],
            feature.geometry.coordinates[0],
            feature.properties[weight]
        ];
    });
}

function pop_DrainageBasin0(feature, layer) {
    layer.on({
        mouseout: function(e) {
            layer.setStyle(style_DrainageBasin0_0(feature));

        }
        // mouseover: highlightFeature,
    });
    var popupContent = '<table>\
            <tr>\
                <td colspan="2"><b>Drainage Basin</b><br>Area: 1134 sqkm</td>\
            </tr>\
        </table>';
    layer.bindPopup(popupContent);
}

function style_DrainageBasin0_0() {
    return {
        pane: 'pane_DrainageBasin0',
        opacity: 1,
        color: 'rgba(0,53,118,1.0)',
        dashArray: '',
        lineCap: 'butt',
        lineJoin: 'miter',
        weight: 1.0,
        fillOpacity: 1,
        fillColor: 'rgba(115,213,232,0.517647058824)',
    }
}
map.createPane('pane_DrainageBasin0');
map.getPane('pane_DrainageBasin0').style.zIndex = 400;
map.getPane('pane_DrainageBasin0').style['mix-blend-mode'] = 'normal';
var layer_DrainageBasin0 = new L.geoJson(json_DrainageBasin0, {
    attribution: '<a href=""></a>',
    pane: 'pane_DrainageBasin0',
    onEachFeature: pop_DrainageBasin0,
    style: style_DrainageBasin0_0,
});
bounds_group.addLayer(layer_DrainageBasin0);
map.addLayer(layer_DrainageBasin0);

function pop_DetroitLake1(feature, layer) {
    layer.on({
        mouseout: function(e) {
            layer.setStyle(style_DetroitLake1_0(feature));

        },
        mouseover: highlightFeature,
    });
    var popupContent = '<table>\
            <tr>\
                <td colspan="2"><b>Detroit Reservoir</b><br> Area: 8.5 sqkm</td>\
            </tr>\
            </table>';
    layer.bindPopup(popupContent);
}

function style_DetroitLake1_0() {
    return {
        pane: 'pane_DetroitLake1',
        opacity: 1,
        color: 'rgba(0,0,0,1.0)',
        dashArray: '',
        lineCap: 'butt',
        lineJoin: 'miter',
        weight: 1.0,
        fillOpacity: 1,
        fillColor: 'rgba(18,133,255,1.0)',
    }
}
map.createPane('pane_DetroitLake1');
map.getPane('pane_DetroitLake1').style.zIndex = 401;
map.getPane('pane_DetroitLake1').style['mix-blend-mode'] = 'normal';
var layer_DetroitLake1 = new L.geoJson(json_DetroitLake1, {
    attribution: '<a href=""></a>',
    pane: 'pane_DetroitLake1',
    onEachFeature: pop_DetroitLake1,
    style: style_DetroitLake1_0,
});
bounds_group.addLayer(layer_DetroitLake1);
map.addLayer(layer_DetroitLake1);

function pop_DetroitDam2(feature, layer) {
    layer.on({
        mouseout: function(e) {
            layer.setStyle(style_DetroitDam2_0(feature));

        },
        mouseover: highlightFeature,
    });
    var popupContent = '<table>\
            <tr>\
                <td colspan="2"><b>Detroit Dam</b><br>Year of Completion: 1953 <br> Dam Height: 450 ft<br>Turbines: Two 50 MW Francis type<br>Turbine Capacity: 5340 cfs <br>Spillway Gates: Six, radial Tainter<br>Spillway Capacity: 176,000 cfs</td>\
            </tr>\
        </table>';
    layer.bindPopup(popupContent, {
        maxWidth: 550
    });
}

function style_DetroitDam2_0() {
    return {
        pane: 'pane_DetroitDam2',
        radius: 4.0,
        opacity: 1,
        color: 'rgba(0,0,0,1.0)',
        dashArray: '',
        lineCap: 'butt',
        lineJoin: 'miter',
        weight: 1,
        fillOpacity: 1,
        fillColor: 'rgba(255,0,0,1.0)',
    }
}
map.createPane('pane_DetroitDam2');
map.getPane('pane_DetroitDam2').style.zIndex = 402;
map.getPane('pane_DetroitDam2').style['mix-blend-mode'] = 'normal';
var layer_DetroitDam2 = new L.geoJson(json_DetroitDam2, {
    attribution: '<a href=""></a>',
    pane: 'pane_DetroitDam2',
    onEachFeature: pop_DetroitDam2,
    pointToLayer: function(feature, latlng) {
        var context = {
            feature: feature,
            variables: {}
        };
        return L.circleMarker(latlng, style_DetroitDam2_0(feature))
    },
});
bounds_group.addLayer(layer_DetroitDam2);
map.addLayer(layer_DetroitDam2);
var baseMaps = {
    'Google Streets': basemap0,
    'Google Satellites': basemap1,
    'ESRI World Terrain': basemap2
};
var layerControl = L.control.layers(baseMaps, {
    '<img src="legend/DetroitDam2.png" /> Dam': layer_DetroitDam2,
    '<img src="legend/DetroitLake1.png" /> Reservoir': layer_DetroitLake1,
    '<img src="legend/DrainageBasin0.png" /> Drainage Basin': layer_DrainageBasin0,
}, {
    collapsed: false
}).addTo(map);
setBounds();

function initMap() {
    map.setView(new L.LatLng(44.6354, -122.0794), 10);
    layer_DrainageBasin0 = new L.geoJson(json_DrainageBasin0, {
        pane: 'pane_DrainageBasin0',
        style: style_DrainageBasin0_0,
    });
    layer_DetroitLake1 = new L.geoJson(json_DetroitLake1, {
        pane: 'pane_DetroitLake1',
        onEachFeature: pop_DetroitLake1,
        style: style_DetroitLake1_0,
    });
    layer_DetroitDam2 = new L.geoJson(json_DetroitDam2, {
        pane: 'pane_DetroitDam2',
        onEachFeature: pop_DetroitDam2,
        pointToLayer: function(feature, latlng) {
            var context = {
                feature: feature,
                variables: {}
            };
            return L.circleMarker(latlng, style_DetroitDam2_0(feature))
        },
    });
    if (document.getElementById('dam').value == "-1") {
        alert('Please select a dam')
        map.removeLayer(layer_DrainageBasin0);
        map.removeLayer(layer_DetroitLake1);
        map.removeLayer(layer_DetroitDam2);
        // map.setView(new L.LatLng(44.6354, -122.0794), 10);

        // map.addLayer(layer_DrainageBasin0);
        // map.addLayer(layer_DetroitLake1);
        // map.addLayer(layer_DetroitDam2);
        // layerControl.addTo(map);
    }
}
