<?php
require 'vendor/autoload.php';

use Aws\S3\S3Client;
use Aws\Exception\AwsException;

// Create an S3Client
$s3Client = new S3Client([
    'region' => 'eu-north-1',
    'version' => 'latest'
]);

$bucketName = 'dist-s3bucket';

echo "<style>
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f4f4f4;
}

h1 {
    color: #333;
    text-align: center;
    padding: 20px 0;
}

p {
    text-align: center;
    padding: 20px;
    font-size: 18px;
}
</style>";

if($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_FILES['fileToUpload'], $_POST['processingType'])) {
    $uploadedFileName = $_FILES['fileToUpload']['name'];
    $processingType = $_POST['processingType'];
    echo "<h1>Uploaded file name: $uploadedFileName</h1><br>";
    echo "<h1>Processing type: $processingType</h1><br>";
    
    $file = $_FILES['fileToUpload']['tmp_name'];
    $originalName = basename($_FILES['fileToUpload']['name']);
    // Randome seed
    $seed = rand(1000, 9999);

    //encode the file name
    $encodedName = md5($originalName.$seed);

    $keyName = "to-process/" . $processingType . "_" . $encodedName. ".jpg";

    $sendingAttempts = 2;
    for ($sattempt = 0; $sattempt < $sendingAttempts; $sattempt++){
        try {
            // Upload a file.
            $result = $s3Client->putObject([
                'Bucket' => $bucketName,
                'Key'    => $keyName,
                'SourceFile' => $file,
            ]);

            // // Print the URL to the object.
            // echo '<p>File uploaded successfully. You can view the file here: ' . $result['ObjectURL'] . "</p>\n";
            // Maximum number of attempts to check if the image is ready
            $maxAttempts = 30;
            $found = false;

            for ($attempt = 0; $attempt < $maxAttempts; $attempt++) {
                try {
                    // Fetch the processed image from the S3 bucket
                    $processedImageKey = "processed/$encodedName.jpg";

                    // Create a presigned URL
                    $cmd = $s3Client->getCommand('GetObject', [
                        'Bucket' => $bucketName,
                        'Key'    => $processedImageKey
                    ]);

                    $request = $s3Client->createPresignedRequest($cmd, '+10 minutes');

                    // Get the presigned URL
                    $presignedUrl = (string)$request->getUri();
                    $found = true;
                    // If the image is ready, break the loop
                    break;
                } catch (Exception $e) {
                    // If the image is not ready, wait for 2 seconds before the next attempt
                    sleep(2);
                }
            }
            if (!$found) {
                throw new AwsException('The processed image is not ready yet. Please try again later.');
            }
            
            sleep(5);
            // Print the URL to the processed image
            echo '<p>Processed image is available here: <a href="' . $presignedUrl . '" download>Download Image</a></p>';

            // Display the image
            echo '<div style="display: flex; justify-content: center; align-items: center; height: 100vh;">';
            echo '<img src="' . $presignedUrl . '" alt="Processed image" style="width: 600px; height: 600px;">';
            echo '</div>';
            break;
        } catch (AwsException $e) {
            // output error message if fails
            echo "<p>" . $e->getMessage() . "</p>\n";
        }
    }

}
?>


