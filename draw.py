from PIL import Image;
from color import *;



pal1 = list(map(color, [ "#77021D", "#F6B339", "#DA7B27", "#D7572B", "#C23028" ]))
pal2 = list(map(color, [ "#F88F52", "#FBCE9E", "#7ACFB0", "#00BDC8", "#1C5588" ]))
pal3 = list(map(color, [ "#ECF39E", "#90A955", "#4F772D", "#31572C", "#132A13" ]))
pal4 = list(map(color, [ "#598B8E", "#FFFFFF", "#FFDCCB", "#F39440", "#CA5940" ]))
pal5 = list(map(color, [ "#0D1220", "#1C2A42", "#3C5772", "#6F86A7", "#ECE6CE" ]))
pal6 = list(map(color, [ "#F0604D", "#F38071", "#F79F95", "#FBBFB8", "#FFDFDB" ]))
pal7 = list(map(color, [ "#F88F52", "#FBCE9E", "#7ACFB0", "#00BDC8", "#1C5588" ]))
pal8 = list(map(color, [ "#FE895E", "#F99F72", "#CD6889", "#96527A", "#5B374D" ]))
pal9 = list(map(color, [ "#5DA5B3", "#E0E2E8", "#B0C0D4", "#4E5772", "#1C1C1F" ]))

sens = 1








def draw(image_path:str="", path_result:str="result.png", palette:Union[list[color], list[str]]=[], soft_edges:bool=False) -> str:
    
    # Test if the file path is correct else raise error
    # Then convert the image to rgb and prepare the other image
    if image_path == "":
        raise ValueError(f"path does not lead to an image")
        
    image = Image.open(image_path)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    newimage = Image.new(mode="RGB", size=image.size, color = (255, 255, 255))

    
    #list(map(color, [ "#5DA5B3", "#E0E2E8", "#B0C0D4", "#4E5772", "#1C1C1F" ]))
    # Setting up our constant
    PAL:list[color] = [color("FFFFFF"), color("000000")] + list(map(color, palette))     # custom palette
    VALUES  = ([color("FFFFFF"), color("000000")] + list(map(color, [ "#FF0000", "#FF00FF", "#0000FF", "#00FFFF", "#00FF00" ])))     # beacon of the circle of color
    WIDTH, HEIGHT = image.size


    for x in range(WIDTH):
        for y in range(HEIGHT):
            c = color(image.getpixel((x, y)))

            # If the color is a round color put the corresponding value
            # to avoid make all the calculus
            if(c in VALUES):
                newimage.putpixel((x, y), PAL[VALUES.index(c)].value)
                continue


            # To find the corresponding color we take the 2 closest color
            # Make the complex function corresponding to a line from the first to the second
            # Then we take the percentage of the line our color in on
            # We make the complex function for our PALette and get the color at N% 
            start, sub = find_closest_color(c, VALUES)
            end = VALUES[(VALUES.index(start) + (-1 if ((c.hsv()[0] > start.hsv()[0])) else 1))%len(VALUES)]
            final = getcolor(PAL[VALUES.index(start)], PAL[(VALUES.index(start) + (-1 if ((c.hsv()[0] > start.hsv()[0])) else 1))%len(PAL)], getpourcent(start, end, c))
            newimage.putpixel((x, y), final.value)
            
    
    # Blend edge of the shape
    if soft_edges:
        for x in range(1, WIDTH-1):
            for y in range(1, HEIGHT-1):
                if(newimage.getpixel((x, y)) == (0, 0, 0)):
                    newimage.putpixel((x,y), color_moy(*[color(newimage.getpixel((x+i, y+j))) for i in range(-1, 2) for j in range(-1, 2)]).value)

            

    newimage.save(path_result)
    return path_result



    
    
draw("moule.png", palette=pal9, soft_edges=False)