# 50-Shades-of-py
Librairy to convert template pixel art or picture with a palette of color automatically

# Definition
The function is defined like this

```py
def draw(image_path:str="", path_result:str="resultat.png", palette:list[color]=[], soft_edges:bool=False) -> str:
  return # file path of the convert image
```

# Usage

To use it , just import the module named *draw* and it's function *draw*.

```py
from draw import draw;

print(draw(image_path="moule.png", palette=[ "#5DA5B3", "#E0E2E8", "#B0C0D4", "#4E5772", "#1C1C1F" ], soft_edges=False)))

>>> resultat.png
```
**image_path** point to the mold picture
**palette** list can be a list of color or a list of hexadecimal values, the function auto convert to color
**soft_edges** define if the function will blend the edge base on the median value of the environning color

# DocString

draw(image_path:str="", path_result:str="resultat.png", palette:list[color]|list[str]=[], soft_edges:bool=False) -> str:

* `image_path` - path of the mold picture
  * if the path if not correct it will raise a ValueError()
  
* `path_result` - name of the result file
  * `true` return the algebric form of the function
  * `false` return the logic / boolean form of the function
  
* `soft_edges` - blending option
  * `true` will blend the black edge of the shape
  * `false` will keep the edge black
