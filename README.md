# morse
Morse code encoding and decoding

Python based development code to begin to work out how to implement morse decoding

morse_win.py - windows based code that takes a message on the command line, writes it to a file beeping for dots/dashes, then reads the file back to parse

morse.py - embedded code that will be used on MicroPython (e.g. ESP8266)

# node-red flow, requires mosquitto on 127.0.0.1:1883

```
[{"id":"69154425.aee0fc","type":"mqtt-broker","z":"b0a93d30.ea8b6","broker":"127.0.0.1","port":"1883","clientid":"","usetls":false,"verifyservercert":true,"compatmode":true,"keepalive":"60","cleansession":true,"willTopic":"","willQos":"0","willRetain":null,"willPayload":"","birthTopic":"","birthQos":"0","birthRetain":null,"birthPayload":""},{"id":"5ffc872d.da6938","type":"mqtt in","z":"b0a93d30.ea8b6","name":"MQTT Test ","topic":"morsetweeter/+","broker":"69154425.aee0fc","x":312,"y":246,"wires":[["5b51d029.b44bd","e87c0878.0837e8"]]},{"id":"5b51d029.b44bd","type":"debug","z":"b0a93d30.ea8b6","name":"","active":true,"console":"false","complete":"false","x":914,"y":240,"wires":[]},{"id":"e87c0878.0837e8","type":"twitter out","z":"b0a93d30.ea8b6","twitter":"","name":"TweeterBot","x":910,"y":320,"wires":[]}]
```