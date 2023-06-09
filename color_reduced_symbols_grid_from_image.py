import os, sys
os.chdir('/content')
os.system('git clone https://github.com/bxck75/diamond-art.git')
os.chdir('/content/diamond-art')
os.system('python setup.py install')
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('seaborn-white')
#%matplotlib inline
import numpy as np
import requests
from ast import Param
from PIL import Image, ImageColor, ImageEnhance

os.system('mkdir -p /content/diamondcanvas')
os.system('mkdir -p /content/diamondcanvas/images')
os.system('mkdir -p /content/diamondcanvas/images/canvas')

paper_formats= [ ['A0',[841,1180]],['A1',[594,840]],['A2',[420,594]], ['A3',[297,420]],
                 ['small_square',[50,50]], ['big_square',[1000,1000]] ]

# !!!!!!! choose a paper format !!!!!!!!
format = paper_formats[3] # A3
# !!!!!!! number of colors in palette !!!!!!!!
nr_of_colors = 64 
# !!!!!!! set this between 2.5 and 2.8 for round or squere drils !!!!!!!!
cell_size = 2.5
# to have a clean edge
cells_away_from_edge = 2

for i in range(len(paper_formats) -1):
  # calculate and split image and grid sizes
  format_name =  paper_formats[i][0]
  paper_format = paper_formats[i][1]
  max_x_cells = paper_format[1] / cell_size
  max_y_cells = paper_format[0] / cell_size
  #Store all values in arrays
  paper_formats[i].append([str(round(max_y_cells - cells_away_from_edge)), str(round(max_x_cells - cells_away_from_edge))])
  paper_formats[i].append(str(round((max_y_cells - cells_away_from_edge) * (max_x_cells - cells_away_from_edge))))

canvas_res = [format[1][1], format[1][0]] #resolution w/h 
grid_res = [format[2][1], format[2][0]] #grid w/h 

# 'https://assets.rebelmouse.io/media-library/junichi-shimodaira-s-rod-riguez.jpg?id=31159124&width={int(canvas_res[0])}&height={int(canvas_res[0])}&quality=100'
input_img_url = sys.argv[1]
#'https://as1.ftcdn.net/v2/jpg/05/57/06/50/1000_F_557065092_MLOigaEyhzfgKr5xxsn98IbRRaopL0Aw.jpg' #@param {type:"string"}

name, ext= os.path.splitext(input_img_url)

split_path = name.split('/')
split_filename = split_path.pop()
filename = "".join(split_filename)
param_split = ext.split('?')
ext = param_split.pop()
params ="?".join(param_split)

name = filename 

input_image = '/content/diamondcanvas/'+filename+'_images/'+filename+'.png'
os.makedirs('/content/diamondcanvas/'+filename+'_images', exist_ok=True)
#print("/".join(split_path)+"/")
    
       
print(input_img_url)
try:
  response = requests.get(input_img_url)
except requests.exceptions.Timeout:
  # Maybe set up for a retry, or continue in a retry loop
  print("TimeOut!")
except requests.exceptions.TooManyRedirects:
  # Tell the user their URL was bad and try a different one
  print("TooManyRedirects!")
except requests.exceptions.RequestException as e:
  # catastrophic error. bail.
  print("RequestException", end="")
  #print(e)
  #raise SystemExit(e)

with open(input_image, 'wb') as f:
  f.write(response.content)


im = Image.open(input_image)
fill_color = (120,8,220)  # your new background color
im = im.convert("RGBA")   # it had mode P after DL it from OP
if im.mode in ('RGBA', 'LA'):
    background = Image.new(im.mode[:-1], im.size, fill_color)
    background.paste(im, im.split()[-1]) # omit transparency
    im = background



im.save(r"/content/diamondcanvas/images/org_art_url.png")
im.convert("RGB").save(r"/content/diamondcanvas/images/RGBA_art_url.png")
# switch to RGBA image
input_image = '/content/diamondcanvas/images/RGBA_art_url.png'
# open the image
im = Image.open(input_image)
# using Image.ADAPTIVE to avoid dithering

out = im.convert('P', palette=Image.ADAPTIVE, colors=nr_of_colors)
#get name and ext
name, ext= os.path.splitext(input_image)
# morph inputname into outputname
output_image = input_image.replace(name, name + '_'+ str(nr_of_colors)+'_'+ str(grid_res[0] +'x'+ grid_res[1]))

#resize and save
resized = out.resize((int(grid_res[0]),int(grid_res[1])))
resized.save(output_image)

# build drill canvas
os.system("diamond_art "+output_image+" "+output_image.replace('images/','images/canvas/').replace('.png','_canvas.png') + " -d 200 -g 2.8")
