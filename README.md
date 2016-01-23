# ImageToBiome

An MCEdit filter that combines the data from an image and a json file into biomes on a Minecraft map.

Note: Coordinates are based on pixels, not chunks.
## Getting Started
1. Create an image file, the same size as your MCEdit selection, and populate it with colours
2. Create a mappings json file, with an RGB colour as they key, and the Biome ID as the value.
3. Open a world in MCEdit, and make your selection.
3. Open the filter in MCEdit, and direct both locations to where you saved the previous two files.
4. Click filter. If everything matches, the script will run and convert the blocks in each chunk.
5. Save your newly modified world, then text it in-game.

Note: This will not change the colours of your world, just the biomes. If you want the colours to match what you had in your image, modify the colormap/grass.png file in a Resource Pack.

## Example

Feek free to try this yourself with the files in the `/example` directory.

### The Image
![Alt text](/example/pixels.png?raw=true "Pixels.png")

### The Mappings JSON file

```json
{
	"255, 252, 0": 2,
	"179, 102, 20": 1,
	"20, 179, 76": 5,
	"20, 177, 179": 12,
	"179, 20, 91": 25,
	"119, 37, 140": 0,
	"37, 42, 140": 4,
	"121, 140, 37": 14
}
```

## If Python complains

It's possible you may need to install the following Python dependences (usually this just requires a `pip install`).
* [Pillow](http://pillow.readthedocs.org/en/3.0.x/installation.html)
* NumPy
 
## Credits

Original code based on SethBling's SetBiome filter. I would not have achieved this without his code.