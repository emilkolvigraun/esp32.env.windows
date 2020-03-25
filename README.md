# Micropython environment for ESP32 | Windows

This is a tool for for uploading a set of scripts to a system chip on a microcontroller. Basically, it relieves you from the hassle of having to manually re-upload a scipt any time you have made a change to it. Furthermore, *the driver will take care of flashing your device for you*.

Requirements:
* pip install esptool
* pip install pyserial
* `OPTIONAL` pip install rshell

With *rshell* you can verify whether the scripts you wanted to upload, was actually uploaded.

## Get Started

To use it, simply execute `run.cmd`.<br>

However, make sure that you have entered the correct serial port. To do this, open `run.cmd` and substitude *COM5* with the port you are using. <br>

Furthermore, you need to make sure that you have entered the names of the scripts you want to upload in a textfile. The textfile must be fed to the `upload.py` through `run.cmd`, similar to updating the serial port. It is up to you, whether you want to create new textfiles (perhaps, one for each project) or manipulate the original one.<br>

`Important!` make sure you have the correct firmware for your device located in the firmware folder. Rename the downloaded firmware to *firmware.bin*, or alternatively, substitute *firmware.bin* with the name on your firmware file on line 3 in `run.cmd`. The current firmware is the generic ESP32 v1.10 without spiram. You can download the firmware from [this page](http://micropython.org/download).<br>

Remember that errors in your script _will_ produce exceptions while uploading.<br>

Press the `reset button` and the program wil automatically start.

Have fun!

### Verify that your scripts was uploaded

`This requires rshell`

Firstly, you must execute rshell on the correct serial port:

```
> rshell -p <serial port>
> rshell -p COM5
```

Secondly, you have two options to verify that the scripts were uploaded:

```
> ls /pyboard/ 
```

or to use *repl* which allows you to enter the environment of your device. In this case, micropython.

```python
> repl
> import os
> os.listdir()
```

In both cases, the output should be an overview of your scripts:

```
boot.py     main.py     external_temp.py
```

## Further

* *Note*:boot.py must be left empty, however, added to upload (e.g declared inside "temperature_project.txt") as first item.
* *Bug*: in some cases, the upload script throws an `OSError: [Errno 2] ENOENT` error. This is because a main.py script has not yet been created, and can be ignored. 
* *Note*: The driver has not yet been tested with any other firmware than the version stated in _Get Started_.