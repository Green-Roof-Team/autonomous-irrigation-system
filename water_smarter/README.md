# Water Smarter
Giving plants the right amount of water is not only good for the plant but good for the planet. Our project aims to create an adaptive automated watering system using soil moisture sensors and valves.

## Inspiration
Inspired by [SIU Carbondale's Green Roof](https://greenroof.siu.edu/siu-green-roof/), we wanted to create an automated garden watering system that would help address issues ranging from food deserts to lack of agricultural space to storm water runoff.

## What it does
This hardware solution takes in moisture data from soil and determines whether or not the plant needs to be watered. If the soil's moisture is too low, the valve will dispense water and will send a message via Twilio to notify the user that their plant has been watered.

## How we built it
First, we tested the sensor and determined the boundaries between dry, damp, and wet based on the sensor's output values. Then, we took the boundaries and divided them by percentage soil moisture. Specifically, the sensor that measures the conductivity of the material around it, so water being the most conductive had the highest values and air being the least conductive had the lowest. Soil would fall in the middle and the ranges in moisture were defined by the pure air and pure water boundaries.

From there, we visualized the hardware set up with the sensor connected to an Arduino UNO microcontroller connected to a Raspberry Pi 4 controlling a solenoid valve that releases water when the soil moisture meter is less than 40% wet.
