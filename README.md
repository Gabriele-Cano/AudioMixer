# Audio Mixer
A simple smart device to control the volume on your PC.

The project is based upon ESP32-C3, which communicates with the PC using BLE and sends the values it reads from the linear sliders. Since the maximum voltage the C3 is able to read using analogRead is lower that 3.3V it's necessary to add a voltage divider on the input or output of the sliders. Doing so will reduce accuracy but at least it's possible to use the full lenght of the sliders. The battery used is a 18650 and the board used to charge it is based on TC4056 chip.

The code for the C3 is in the file mixer.ino, while the Python application is in the folder AudioMixer. 

The Python code is modular, you can implement your preferred control by inheriting the Interface class, currently I wrote 3 Interfaces: 
- BrightnessInterface: can change the brightness of an external monitor using screen_brightness_control library;
- ComputerVolumeInterface: useful if you need to change the volume of any application running on the PC;
- HomeAssistantInterace: allows to change the volume (or actually any other value) of a smart device connected to a HomeAssistant server.

The case was modeled using Fusion 360 and then 3D printed in white PLA. For the handles I used a 3D model found on on Thingiverse. 

![20240514_191908](https://github.com/user-attachments/assets/bc32cdb7-7569-4ef5-b38c-791640f5a1a3)

![20240501_194658](https://github.com/user-attachments/assets/fe1d8541-af98-469a-8ecb-51cbae6c13f7)

