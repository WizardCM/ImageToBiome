# WizardCM's Image to Biome Map Filter

# Heavily based on SethBling's beautifully simple SetBiome filter

from pymclevel import MCSchematic
from pymclevel import TAG_Compound
from pymclevel import TAG_Short
from pymclevel import TAG_Byte
from pymclevel import TAG_Byte_Array
from pymclevel import TAG_String
from numpy import zeros
from PIL import Image
import json
from pprint import pprint

displayName = "Image to Biome Map"

# input = image filename (relative path probably best)
inputs = (
("Created by WizardCM, based on SethBling's SetBiome", "label"),
("Full Image Path", ("string", "value=C:/image.png")),
("Full Colour Mappings Path", ("string", "value=C:/mappings.json")),
("If your client freezes, the script is running perfectly fine. The larger your world/image, the longer it takes. Check MCEdit's console for progress if you're worried.", "label"),
)

def perform(level, box, options):
	
	imageFile = options["Full Image Path"]
	colorMapFile = options["Full Colour Mappings Path"]
	
	
	image = Image.open(imageFile)

	with open(colorMapFile) as data_file:    
		colorMap = json.load(data_file)
	
	# We need the Minecraft coords of the top left corner of the selection to determine
	# the offset so we can safely determine the coordinates of the image's top left corner
	minx = int(box.minx / 16) * 16
	minz = int(box.minz / 16) * 16
	
	
	# compare the width and height of the image to the selection
	# warn and confirm with the user that it's fine if they don't match
	# displaying the values would be helpful
	selectionWidth = box.maxx - box.minx
	selectionHeight = box.maxz - box.minz
	totalBlocks = selectionWidth * selectionHeight
	currentPercent = 0
	currentBlocks = 0
	
	imageWidth,imageHeight = image.size
	
	print('=====================================')
	print('= Starting Image to Biome filter... =');
	print('=====================================')
	
	if selectionWidth == imageWidth and selectionHeight == imageHeight:
		print('Image and selection size match! Starting..');
		# loop through the x axis of the user's selection (of chunks?)
		for x in xrange(minx, box.maxx, 16):
			# loop through the z axis of the user's selection  (of chunks?)
			for z in xrange(minz, box.maxz, 16):
				# get the top corner coords of the chunk, or the chunk id
				chunk = level.getChunk(x / 16, z / 16)
				
				# mark the chunk as 'modified'
				chunk.dirty = True
				
				# get the current biome IDs of the chunk (I think)
				# this is probably so if a biome of a column/block within a chunk
				# does not get replaced, the original data is kept
				array = chunk.root_tag["Level"]["Biomes"].value
				
				# store the chunk's coordinates, again why / then *
				chunkx = int(x / 16) * 16
				chunkz = int(z / 16) * 16
				
				# loop through the x axis of the selected blocks within the chunk
				for bx in xrange(max(box.minx, chunkx), min(box.maxx, chunkx + 16)):
					xcoord = minx;
					# loop through z axis of selected blocks within chunk
					for bz in xrange(max(box.minz, chunkz), min(box.maxz, chunkz + 16)):
						# get the ID of the column/block within the chunk (I think)
						idx = 16 * (bz - chunkz) + (bx - chunkx)
						# set the biome of the column/block to the biome in the image
						progress = int(100 * float(currentBlocks + 1)/float(totalBlocks))
						# originally we were going to show a progress bar IN MCEdit - turns out just rendering it slows down this task
						if progress > currentPercent:
							print("Completed " + str(progress) + '%')
							currentPercent = progress
						currentBlocks = currentBlocks + 1
						loc = str(image.getpixel((bx - minx, bz - minz))).strip('()')
						if loc.count(',') == 3:
							loc = loc[:-5]
						try:
							array[idx] = colorMap[loc]
						except KeyError, e:
							raise Exception("The colour rgb" + str(e) + " at " + str(1+bx-minx) + "," + str(1+bz-minz) + " (image coordinates) doesn't exist. Please update your mappings.json or change the colour of the pixel.")
				# save the biome data in the array to the chunk itself
				chunk.root_tag["Level"]["Biomes"].value = array
	elif selectionWidth > imageWidth or selectionHeight > imageHeight: 
		raise Exception("Image size (" + str(imageWidth) + "x" + str(imageHeight) + ") is smaller than the selection (" + str(selectionWidth) + "x" + str(selectionHeight) + "). Please make your selection smaller or make your image larger.")
		return None
	else:
		# TODO Show a dialog asking if we should continue anyway.
		raise Exception("Image size (" + str(imageWidth) + "x" + str(imageHeight) + ") & selection size (" + str(selectionWidth) + "x" + str(selectionHeight) + ") don't match. ")
		return None