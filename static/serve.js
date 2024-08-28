function predict(e) {
    var data = new FormData();
    jQuery.each(jQuery('#imagefile')[0].files, function (i, file) {
        data.append('image', file);
    });

    $.ajax({
        type: "POST",
        url: "/predict",
        crossDomain: true,
        data: data,
        dataType: "json",
        contentType: "multipart/form-data",
        processData: false,
        contentType: false,
        headers: {
            "Accept": "application/json"
        },
        success: function (response) {
            document.getElementById("defect-class").innerHTML = 'Image is classified as ' + response;
        }
    }).done(function () {
        //prediction = response;
    }).fail(function () {
        alert('UPS! Error happened, please, try with another image.')
    });
};

function tile(e) {

    var data = new FormData();
    jQuery.each(jQuery('#imagefile')[0].files, function (i, file) {
        data.append('image', file);
    });

    $.ajax({
        type: "POST",
        url: "/tile",
        crossDomain: true,
        data: data,
        dataType: "json",
        contentType: "multipart/form-data",
        processData: false,
        contentType: false,
        headers: {
            "Accept": "application/json"
        }
    }).done(function (response) {
        confirm('Process of patches extraction done successfully! Images can be found in ' + response + ' .')
    }).fail(function () {
        alert('UPS! Error just happened, please, try with another image.')
    });
};

function tile_and_predict(e) {
    var data = new FormData();
    jQuery.each(jQuery('#imagefile1')[0].files, function (i, file1) {
        data.append('image', file1);
    });
    $("#predict-button").text("Loading").attr("disabled","disabled");
    $.ajax({
        type: "POST",
        url: "/tile-and-predict",
        crossDomain: true,
        data: data,
        processData: false,
        contentType: false,
        xhrFields: {
            responseType: 'blob'
        },
        success: function (response) {
            $('#img2').attr('src', URL.createObjectURL(response));
        }
    }).done(function (response) {
        $("#predict-button").text("Detektuj").removeAttr("disabled")
        console.log('Proces detekcije je uspješno završen! Slike se nalaze na lokaciji ' + response + ' .')
    }).fail(function (err) {
        $("#predict-button").text("Detektuj").removeAttr("disabled")
        alert('UPS! Error just happened, please, try with another image.')
        console.log("error: ", err)
    });
};