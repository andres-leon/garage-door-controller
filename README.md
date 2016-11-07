# garage-door-controller
Using Raspberry Pi, Python, MQTT, Home Assistant, a relay, and a magnetic proximity sensor, I open, close, stop, and report the status of my garage door.

To view a video of the system in operation go to https://www.youtube.com/watch?v=m_tDeZUco10.

# Assumptions
- Home Assistant is already installed and running successfully (https://home-assistant.io/getting-started/)
- You have a MQTT broker configured and already setup in your Home Assistant (https://home-assistant.io/components/mqtt/)
- You have a Raspberry Pi (2 or 3, but better 3) already configured with Raspbian and able to control GPIO pins.

# Other hardware needed
- 2 Channel DC 5V Relay Module with Optocoupler (You can use a 1 channel module if you want, but I used a 2 channel because I plan to use the other relay to control a light.)
- Magnetic proximity switch
- Tools to secure magnetic switch to garage and support.

#Hardware setup and wiring
