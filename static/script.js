// Script.js for my application 

// Navbar 
document.getElementById("Home_nav_button").onclick = function () {
    location.href = "index";
};
document.getElementById("About_nav_button").onclick = function () {
    location.href = "about";
};
document.getElementById("Report_nav_button").onclick = function () {
    location.href = "report";
};

// SLIDERS
document.getElementById('sliderForm').addEventListener('submit', function (e) {
        
    var accuracy_slider = parseInt(document.getElementById("accuracy_slider").value);
    var outliers_slider = parseInt(document.getElementById("outliers_slider").value);
    var shape_slider = parseInt(document.getElementById("shape_slider").value);
    var time_slider = parseInt(document.getElementById("time_slider").value);
    var complexity_slider = parseInt(document.getElementById("complexity_slider").value);
    var naive_slider = parseInt(document.getElementById("naive_slider").value);

    var total = accuracy_slider + outliers_slider + shape_slider + time_slider + complexity_slider + naive_slider;

    if (total == 0) {
        alert("Sliders total should not be 0!");
        e.preventDefault(); // Prevent the form from submitting
        return;
    }
    else{
        // Form is submitted and the sliders can be referenced via the sliders' name! 
        var formData = new FormData(this); 
        e.preventDefault(); 
        $.ajax({
            type: 'POST',
            url: '/slider-form',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                console.log(response.message)
                document.getElementById("Slider_for_submission_result").innerText = "Configuration updated successfully!"
            },
            error: function(response) {
                console.log(response.message)
                document.getElementById("Slider_for_submission_result").innerText = "Something went wrong!"
            }
        });
    }
    });


function updateSliders() {
    var accuracy_slider = parseInt(document.getElementById("accuracy_slider").value);
    var outliers_slider = parseInt(document.getElementById("outliers_slider").value);
    var shape_slider = parseInt(document.getElementById("shape_slider").value);
    var time_slider = parseInt(document.getElementById("time_slider").value);
    var complexity_slider = parseInt(document.getElementById("complexity_slider").value);
    var naive_slider = parseInt(document.getElementById("naive_slider").value);

    document.getElementById("slider_1_value").innerText = "Accuracy: "  + accuracy_slider;
    document.getElementById("slider_2_value").innerText = "Outliers: "  + outliers_slider;
    document.getElementById("slider_3_value").innerText = "Shape similarity: "  + shape_slider;
    document.getElementById("slider_4_value").innerText = "Execution time: "  + time_slider;
    document.getElementById("slider_5_value").innerText = "Complexity: "  + complexity_slider;
    document.getElementById("slider_6_value").innerText = "Improvement over naive methods: "  + naive_slider;

    total = accuracy_slider + outliers_slider + shape_slider + time_slider + complexity_slider + naive_slider;

    if (total == 0){
        document.getElementById("total").innerText = total + " !";
    }
    else {
        document.getElementById("total").innerText = total;
    }
}

// VALIDATE FORM 
function validateForm() {
    var fileInput = document.querySelector('input[type="file"]');
    if (!fileInput.files || fileInput.files.length === 0) {
        alert("Please select a file before submitting.");
        return false;
    }
    return true;
}

// UPLOAD 
// Event listener for the form submission
document.getElementById('upload-form').addEventListener('submit', function (e) {
    e.preventDefault(); // Prevent the form from submitting normally

    if (!validateForm()){
        return;
    }

    var fileInput = document.querySelector('input[type="file"]');
    var fileSize = fileInput.files[0].size; // in bytes
    var maxSize = 20 * 1024 * 1024; // 20 MB

    if (fileSize > maxSize) {
        alert("File size exceeds 20 MB. Please upload a smaller file.");
        e.preventDefault(); // Prevent the form from submitting
        return;
    }
    else {
        var formData = new FormData(this); // Create a FormData object
        e.preventDefault(); // Prevent the form from submitting normally
        // Send an AJAX request to handle the file upload
        $.ajax({
            type: 'POST',
            url: '/upload-form',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                // Update the upload status div with the response message
                document.getElementById('upload-status').innerHTML = response.message;
            },
            error: function(response) {
                // console.error("Error: " + JSON.stringify(error));
                document.getElementById('upload-status').innerHTML = response.message;
            }
        });

    }
});


// FORECASTING
function callFunction(functionName) {
    console.log("Calling function: " + functionName);
    $.ajax({
        type: 'POST',
        url: '/' + functionName,
        success: function(response) {

            if (response.result.includes('Error')){
                alert(response.result);
            }
            else {
                // console.log("Response: " + response.result);
                document.getElementById('result').innerHTML = response.result + '<br>';
            }
        },
        error: function(error) {
            console.error("Error: " + JSON.stringify(error));
        }
    });
}

 // UPLOAD
function uploadFile(functionName) {
    console.log("Calling function: " + functionName);
    $.ajax({
        type: 'POST',
        url: '/' + functionName,
        success: function(response) {
            console.log("Response: " + response.result);
            document.getElementById('upload-status').innerHTML += response.result + '<br>';
        },
        error: function(error) {
            console.error("Error: " + JSON.stringify(error));
        }
    });
}

// EXPORTING
function exportResults(functionName) {
    // Implement export functionality here if needed
    console.log("Calling function: " + functionName);
    $.ajax({
        type: 'POST',
        url: '/' + functionName,
        success: function(response) {
            if ('export' in response){
                document.getElementById('Export_responses').innerHTML += response.result + '<br>';
                document.getElementById('result').insertAdjacentHTML('afterbegin', response.export);
                console.log("Response: " + response.result);
                console.log("Export: " + response.export);
            }
            else{
                document.getElementById('Export_responses').innerHTML += response.result + '<br>';
                console.log("Response: " + response.result);
            }
        },
        error: function(error) {
            console.error("Error: " + JSON.stringify(error));
        }
    });
}


// CLEAR SESSION
function clearAdditionalElements(functionName) {
    console.log("Calling function: " + functionName);
    $.ajax({
        type: 'POST',
        url: '/' + functionName,
        success: function(response) {
            console.log("Response: " + response.result);
            // Reset messages 
            var resultDiv = document.getElementById('result');
            var exportDiv = document.getElementById('Export_responses');
            var uploadDiv = document.getElementById('upload-status');
            // Clear its content
            resultDiv.innerHTML = '';
            exportDiv.innerHTML = '';
            uploadDiv.innerHTML = '';

            // Reset sliders 
            document.getElementById("slider_1_value").innerText = "Accuracy: 5";
            document.getElementById("slider_2_value").innerText = "Outliers: 5";
            document.getElementById("slider_3_value").innerText = "Shape similarity: 5"
            document.getElementById("slider_4_value").innerText = "Execution time: 5"
            document.getElementById("slider_5_value").innerText = "Complexity: 5"
            document.getElementById("slider_6_value").innerText = "Improvement over naive methods: 5"
            document.getElementById("total").innerText = "30";

            document.getElementById("accuracy_slider").value = "5";
            document.getElementById("outliers_slider").value = "5";
            document.getElementById("shape_slider").value = "5";
            document.getElementById("time_slider").value = "5";
            document.getElementById("complexity_slider").value = "5";
            document.getElementById("naive_slider").value = "5";

            document.getElementById("Slider_for_submission_result").innerText = " "

        },
        error: function(error) {
            console.error("Error: " + JSON.stringify(error));
        }
    });
}