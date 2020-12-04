# img2maps
A python script to make map.dat from images. Works on 1.14 and up.
This script does not accept command line arguments.
**WARNING:** This script is *really* slow. 
#Dependencies
```
NBT
Numpy
Pillow
```
## Steps
1. Scale any image you want using your preferred image editor and export it to the same folder where `img2maps.py` is. (ex: for a poster of 2x3 maps, your image needs to be at most 256x384 px)
2. In the game, make *n* filled_maps, where *n* is the size X times Y the size of the poster (ex: 2x3 = 6 filled_maps) 
3. Take the ID of the first filled_map you got in the step 2.
4. Run `python3 img2maps.py`.
5. Type the name of the image file. Hit `Enter`.
6. If your image width or height are not divisible by 128, the script will ask you if you want to crop the image or make extra maps and center the image. Hit `Enter`.
7. Type the ID you got on the step 3. This is for generate the respective file `map_x.dat`. Hit `Enter` and the script will make a folder with the name of your image with a bunch of `map_x.dat` files and a `preview.png` inside.
8. Restart/Stop your server (if you are on singleplayer, just Save and Quit).
9. Quickly drag and drop all the generated `map_x.dat` to ../world name/data/
10. Done!

## CONFIG
- **MAP_PREV** *True/False* Set it to false if you dont want the preview
- **IMG_ALPH** *True/False* If your image is a PNG with transparent pixels, keeps transparency in the maps too
