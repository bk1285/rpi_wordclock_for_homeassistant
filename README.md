# rpi_wordclock_for_homeassistant
Makes a rpi_wordclock available to homeassistant as light 

If you build a rpi_wordclock like this one, you can make use of this repository to integrate it to your homeassistant framework as follows:

* Go to the config-directory of your homeassistant instance:
  
  E.g. ```cd ~/.homeassistant/custom_components/```
  
 * Create a directory called light, if not existent:
   ```
   mkdir light
   ```
  
 * Place the rpi_wordclock.py file from this repository inside this folder:
 
   ```
   cd light
   wget https://raw.githubusercontent.com/bk1285/rpi_wordclock_for_homeassistant/master/rpi_wordclock.py
   ```
   
 * Now you're ready to add a rpi_wordclock to your configuration.yaml

    ```
    light:                                                                                                                                                               
    - platform: rpi_wordclock
      host: 192.168.1.101
      name: "Wordclock"
    ```

 * Finish by restarting homeassistant.
