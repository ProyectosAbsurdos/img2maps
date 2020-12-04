import nbt, numpy, os
from PIL import Image

######################### CONFIG ##########################
NBT_FILE = "nbt_map_reference.dat" #This file is required to make the maps. (yeah, im lazy)
MAP_PREV = True #Generate preview.png?
MAP_PRFX = "map_" #Produces map_#.dat
IMG_ALPH = True  #Make transparent pixels transparent on the map too?
MAP_SIZE = 128   #The map X & Y size
MAP_INDX = None    #start index for <image>_<index>.dat resulting files
MAP_COLORS = numpy.array([[87,123,38],[107,150,47],[124,175,55],[66,92,28],[171,161,113],[209,197,137],[242,228,160],[127,121,84],[137,137,137],[168,168,168],[195,195,195],[103,103,103],[176,0,0],[216,0,0],[250,0,0],[132,0,0],[110,110,176],[135,135,216],[157,157,250],[82,82,132],[115,115,155],[141,141,141],[164,164,164],[86,86,86],[0,85,0],[0,104,0],[0,122,0],[0,64,0],[176,176,176],[216,216,216],[250,250,250],[132,132,132],[113,116,126],[138,141,155],[161,165,180],[84,86,95],[104,74,53],[127,92,65],[148,107,75],[77,56,39],[77,77,77],[94,94,94],[110,110,110],[58,58,58],[39,39,155],[44,44,176],[54,54,216],[63,63,250],[32,32,132],[98,82,49],[121,100,61],[140,117,71],[74,62,37],[176,174,169],[216,213,207],[250,247,240],[132,130,126],[149,87,35],[182,107,43],[212,124,50],[112,66,26],[123,52,149],[150,64,182],[175,74,212],[92,39,112],[71,106,149],[86,129,182],[100,150,212],[53,79,112],[158,158,35],[193,193,43],[224,224,50],[119,119,26],[87,141,17],[107,173,21],[124,200,25],[66,106,13],[167,87,114],[204,107,139],[237,124,162],[125,66,85],[52,52,52],[64,64,64],[74,74,74],[39,39,39],[106,106,106],[129,129,129],[150,150,150],[79,79,79],[52,87,106],[64,107,129],[74,124,150],[39,66,79],[87,43,123],[107,53,150],[124,62,175],[66,32,92],[35,52,123],[43,64,150],[50,74,175],[26,39,92],[71,52,35],[86,64,43],[100,74,50],[53,39,26],[71,87,35],[86,107,43],[100,124,50],[53,66,26],[106,35,35],[129,43,43],[150,50,50],[79,26,26],[17,17,17],[21,21,21],[25,25,25],[13,13,13],[173,165,53],[211,201,65],[245,233,75],[129,124,39],[63,151,147],[77,184,179],[90,215,209],[47,113,110],[51,88,176],[62,108,216],[73,125,250],[38,66,132],[0,150,39],[0,183,49],[0,213,57],[0,112,29],[89,59,33],[109,73,41],[126,84,48],[67,44,25],[77,1,0],[94,1,0],[110,2,0],[58,1,0],[144,122,111],[176,149,135],[205,174,158],[108,91,83],[110,56,25],[134,69,30],[156,80,35],[82,42,19],[103,60,74],[125,74,91],[146,85,106],[76,45,56],[77,74,95],[94,91,117],[110,106,135],[58,56,72],[128,91,25],[157,112,30],[182,130,35],[96,69,19],[71,80,36],[86,98,44],[101,115,52],[53,60,27],[110,53,54],[135,65,66],[157,75,76],[82,39,40],[39,27,24],[48,34,29],[56,40,34],[29,21,18],[93,74,68],[114,90,82],[132,105,96],[70,55,50],[60,63,63],[74,77,77],[85,90,90],[45,47,47],[84,50,61],[103,61,74],[120,72,86],[63,37,45],[52,42,63],[64,52,77],[74,61,90],[39,31,47],[52,34,24],[64,42,29],[74,49,34],[39,25,18],[52,56,28],[64,69,35],[74,80,41],[39,42,22],[98,41,31],[120,50,38],[139,59,45],[74,30,24],[25,15,11],[30,18,13],[36,22,16],[19,11,8]])
###########################################################

def nearest_colour(INPUT):
	INPUT = numpy.array(INPUT)
	hypts = numpy.sqrt(numpy.sum((MAP_COLORS-INPUT)**2,axis=1))
	index = numpy.where(hypts==numpy.min(hypts))
	return {"color":MAP_COLORS[index][0], "id":index[0][0]+3}

def make_map(offsetX, offsetY, f_id):
	nbt_file = nbt.nbt.NBTFile(NBT_FILE)
	nbt_out = MAP_PRFX + f_id + ".dat"
	for y in range(0,MAP_SIZE):
		for x in range(0,MAP_SIZE):
			if not image[x+offsetX,y+offsetY][3] and IMG_ALPH:
				minecraft_color={"id":0x0,"color":[image[x+offsetX,y+offsetY][0], image[x+offsetX,y+offsetY][1], image[x+offsetX,y+offsetY][2] ,0]}
			else:
				minecraft_color = nearest_colour((image[x+offsetX,y+offsetY][0], image[x+offsetX,y+offsetY][1], image[x+offsetX,y+offsetY][2]))
			nbt_file["data"]["colors"][x+(y*MAP_SIZE)] = minecraft_color["id"]
			image[x+offsetX,y+offsetY] = tuple(minecraft_color["color"])
			print(nbt_out + " " + '%.1f'%((((x+(y*MAP_SIZE))+1)/MAP_SIZE**2)*100)+"%", end="\r", flush=True)
	nbt_file.write_file(os.path.join(file.split(".")[0], nbt_out))
	print("\r"+nbt_out+" [OK]   ")


file = input("Image (at least 128x128px): ")
image = Image.open(file)
w,h = (image.size)
Msize = [None, None]
nwimg = {"x":0, "y":0, "w":0, "h":0}
tmimg = None
if w%MAP_SIZE or h%MAP_SIZE:
	if w%MAP_SIZE:
		print("image WIDTH is not multiple of "+str(MAP_SIZE))
		print("Press '2' to make extra maps to FIT the image width and CENTER it. ("+str((w//MAP_SIZE)+1)+" maps width)")
		print("Press '1' to make extra maps to FIT the image width. ("+str((w//MAP_SIZE)+1)+" maps width)")
		print("Press '0' to CROP the image to fit the maps width. ("+str(w//MAP_SIZE)+" maps width)")
		optX = int(input(">> "))
		if optX == 2:
			Msize[0] = (w//MAP_SIZE)+1
			nwimg["w"] = Msize[0]*MAP_SIZE
			nwimg["x"] = (nwimg["w"]-w)//2
		elif optX == 1:
			Msize[0] = (w//MAP_SIZE)+1
			nwimg["w"] = Msize[0]*MAP_SIZE
		elif optX == 0:
			Msize[0] = w//MAP_SIZE
			nwimg["w"] = Msize[0]*MAP_SIZE
		else:
			print("Invalid option.")
			exit()
	else:
		Msize[0] = w//MAP_SIZE
		nwimg["w"] = Msize[0]*MAP_SIZE
	if h%MAP_SIZE:
		print("image HEIGHT is not multiple of "+str(MAP_SIZE))
		print("Press '2' to make extra maps to FIT the image height and CENTER it. ("+str((h//MAP_SIZE)+1)+" maps width)")
		print("Press '1' to make extra maps to FIT the image height. ("+str((h//MAP_SIZE)+1)+" maps width)")
		print("Press '0' to CROP the image to fit the maps height. ("+str(h//MAP_SIZE)+" maps width)")
		optY = int(input(">> "))
		if optY == 2:
			Msize[1] = (h//MAP_SIZE)+1
			nwimg["h"] = Msize[1]*MAP_SIZE
			nwimg["y"] = (nwimg["h"]-h)//2
		elif optY == 1:
			Msize[1] = (h//MAP_SIZE)+1
			nwimg["h"] = Msize[1]*MAP_SIZE
		elif optY == 0:
			Msize[1] = h//MAP_SIZE
			nwimg["h"] = Msize[1]*MAP_SIZE
		else:
			print("Invalid option.")
			exit()
	else:
		Msize[1] = h//MAP_SIZE
		nwimg["h"] = Msize[1]*MAP_SIZE
	tmimg = Image.new("RGBA", (nwimg["w"], nwimg["h"]))
	tmimg.paste(image, (nwimg["x"], nwimg["y"]))
	image = tmimg.load()
else:
	tmimg = image
	image = tmimg.load()
	Msize = [w//MAP_SIZE, h//MAP_SIZE]
MAP_INDX = int(input("Start map_(x).dat numeration at: "))
os.mkdir(file.split(".")[0])
for mapY in range(0,Msize[1]):
	for mapX in range(0,Msize[0]):
		make_map(offsetX=mapX*MAP_SIZE, offsetY=mapY*MAP_SIZE, f_id=str((mapX+(mapY*Msize[0]))+MAP_INDX))
if MAP_PREV:
	print("Saving preview...")
	tmimg.save(os.path.join(file.split(".")[0], "preview.png"), "PNG")
print("Replace the files in your '.minecraft/saves/<world name>/data/' with the ones on '" + file.split(".")[0] + "'.")
#print('\nRename "' + file.split(".")[0] + "_" + '*.dat" to "map_<last id>.dat" and copy(overwrite) them to your ".minecraft/saves/<world name>/data/" folder.')