<?php
// Check if the form is submitted via POST method
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Get form data
    $name = $_POST['name'];
    $email = $_POST['email'];
    $branch = $_POST['branch'];
    $description = $_POST['description'];

    // Prepare the data to be sent to the Flask API
    $data = array(
        'name' => $name,
        'email' => $email,
        'branch' => $branch,
        'description' => $description
    );

    // URL of your Flask API endpoint
    $url = 'http://192.168.100.190:5000/thank_you';  // Update this with your Flask API URL

    // Initialize cURL session to send POST request to the Flask API
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($data));  // Send form data as POST fields
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/x-www-form-urlencoded'));  // Content-Type header

    // Execute cURL and capture the response from the Flask API
    $response = curl_exec($ch);
    
    // Check if the cURL request was successful
    if (curl_errno($ch)) {
        // In case of error, show the error message
        echo "Error: " . curl_error($ch);
    } else {
        // Handle response from Flask API (you can modify this based on your Flask response)
        if ($response) {
            echo "<h3>✅ تم تقديم الطلب بنجاح! شكراً لك.</h3>";  // Success message in Arabic
        } else {
            echo "<h3>❌ حدث خطأ أثناء إرسال الطلب.</h3>";  // Error message in Arabic
        }
    }

    // Close cURL session
    curl_close($ch);
}
?>
