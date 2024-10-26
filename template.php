<?php
// Set the content type to application/json
header('Content-Type: application/json');

// Define the array with the desired data structure
$data = [
    ["x" => 1, "y" => 1, "w" => 2, "h" => 0, "id" => "Turn on", "compType" => "PushButton"],
    ["x" => 1, "y" => 2, "w" => 4, "h" => 0, "id" => "press", "compType" => "PushButton"],
    ["x" => 1, "y" => 3, "w" => 3, "h" => 0, "id" => "activate", "compType" => "PushButton"],
    ["x" => 1, "y" => 4, "w" => 5, "h" => 0, "id" => "ON", "compType" => "PushButton"],
    ["x" => 0, "y" => 6, "w" => 12, "h" => 0, "id" => "Slider Value", "compType" => "SliderWidget", "min" => 0, "max" => 100],
    ["x" => 8, "y" => 2, "w" => 3, "h" => 2, "id" => "Sustem Output", "compType" => "ConsoleWidget"]
];

// Output the JSON-encoded data
echo json_encode($data, JSON_PRETTY_PRINT);
?>
