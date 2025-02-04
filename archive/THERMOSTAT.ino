#include <PID_v1.h>

// Define pins
#define RELAY_PIN A5
#define TEMP_SENSOR_PIN A0

// Temperature Setpoint
double setpoint = 75; // Target temperature in Fahrenheit
double input, output;

// PID parameters
double Kp = 2, Ki = 5, Kd = 1;  // Tuning values for the PID
PID myPID(&input, &output, &setpoint, Kp, Ki, Kd, DIRECT);

void setup() {
    Serial.begin(9600);

    // Initialize relay pin
    pinMode(RELAY_PIN, OUTPUT);
    digitalWrite(RELAY_PIN, LOW); // Start with the relay off

    // Initialize the PID
    myPID.SetMode(AUTOMATIC);
    myPID.SetOutputLimits(0, 255);  // Adjust as necessary for relay control
}

void loop() {
    // Read temperature sensor data
    float VRT = analogRead(TEMP_SENSOR_PIN);
    float tempC = (VRT * 5.0 / 1024.0 - 0.5) * 100.0;  // Convert to Celsius
    input = (tempC * 9.0 / 5.0) + 32;  // Convert to Fahrenheit

    // Run PID computation
    myPID.Compute();

    // Use output to control relay (simple ON/OFF based on PID output)
    if (output > 128) {  // Adjust threshold as needed
        digitalWrite(RELAY_PIN, HIGH);  // Turn heating element on
        Serial.println("Heating ON");
    } else {
        digitalWrite(RELAY_PIN, LOW);  // Turn heating element off
        Serial.println("Heating OFF");
    }

    // Print current temperature and setpoint for debugging
    Serial.print("Current Temp: ");
    Serial.print(input);
    Serial.print(" F, Setpoint: ");
    Serial.println(setpoint);

    delay(1000);  // Adjust delay as needed
}
