$(document).ready(function() {
    // Wait for 1 second before fetching and rendering data
    setTimeout(function() {
        // Fetch data using AJAX
        $.get('/fetch_data', function(data) {
            populateTable(data);
            updateGraph(data.graph_path);  // Update the graph image
        });
    }, 1000);  // Wait for 1000 milliseconds (1 second)

    // Function to update the graph image
    function updateGraph(graphPath) {
        $('#graph-image').attr('src', graphPath);  // Update the 'src' attribute
    }

    function populateTable(data) {
        var tableBody = $('#table-body');  // Assuming you have a <tbody> element with id 'table-body'

        $.each(data, function(song, count) {
            var row = '<tr><td>' + song + '</td><td>' + count + '</td></tr>';
            tableBody.append(row);
        });
    }
});