esptool.py --port COM5 flash_id
esptool.py --port COM5 erase_flash
esptool.py --chip esp32 --port COM5 write_flash 0x1000 ./firmware/firmware.bin

python upload.py 115200 0.1 COM5 assignment2.txt