#include <DHT.h>
#define DHTPIN 7

#define DHTTYPE DHT22   // DHT 22  (AM2302)
DHT dht(DHTPIN, DHTTYPE); 
const int sensor_pin = A0;  /* Soil moisture sensor O/P pin */

float hum;
float temp;
void setup() {
  Serial.begin(9600); /* Define baud rate for serial communication */
    dht.begin();
    pinMode(DHTPIN,INPUT);
pinMode(sensor_pin,INPUT);
}

void loop() {
  float moisture_percentage;
  int sensor_analog;


    //Read data and store it to variables hum and temp
    hum = dht.readHumidity();
    temp= dht.readTemperature();
    //Print temp and humidity values to serial monitor
    // Serial.print("Humidity: ");
    // Serial.print(hum);
    // Serial.print(" %, Temp: ");
    // Serial.print(temp);
    // Serial.println(" Celsius");
    delay(1000); //Delay 2 sec.

  
  sensor_analog = analogRead(sensor_pin);
  moisture_percentage = ( 100 - ( (sensor_analog/1023.00) * 100 ) );
  

  // Serial.print(temp);
  // Serial.print('-');
  // Serial.print(hum);
  // Serial.print('-');
  // Serial.println(moisture_percentage);
  // delay(2000);

  // Serial.print("Moisture Percentage = ");
  // Serial.print(moisture_percentage);
  // Serial.print("%\n\n");
  // delay(1000);
}
