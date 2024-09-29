import customtkinter as ctk
import geopandas as gpd
from PIL import Image, ImageTk
import os
import sys

ctk.set_appearance_mode("Dark")


root = ctk.CTk()
root.geometry("2000x2000")
root.title("Homelessness Risk Prediction in OC")


root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=2)
root.grid_columnconfigure(1, weight=1)

mapFrame = ctk.CTkFrame(root)
mapFrame.grid(row = 0, column = 0, sticky = 'nsew')

mapCanvas = ctk.CTkCanvas(mapFrame, bg=root.cget("background"))
mapCanvas.pack(fill="both", expand=True)

if getattr(sys, 'frozen', False):
    mapPath = file=os.path.join(sys._MEIPASS, "map.png")
else:
    mapPath = file="map.png"


mapImage = Image.open(mapPath) 
mapPhoto = ImageTk.PhotoImage(mapImage)
mapCanvas_image = mapCanvas.create_image(0, 0, anchor="center", image=mapPhoto)
mapCanvas.image = mapPhoto 

def resize_image(event):
    newWidth = event.width
    newHeight = event.height

    newWidth = min(newWidth, mapImage.width)
    newHeight = min(newHeight, mapImage.height)

    img_resized = mapImage.resize((newWidth, newHeight), Image.LANCZOS)
    mapPhoto_resized = ImageTk.PhotoImage(img_resized)
    mapCanvas.itemconfig(mapCanvas_image, image=mapPhoto_resized)
    mapCanvas.image = mapPhoto_resized
    mapCanvas.coords(mapCanvas_image, newWidth // 2, newHeight // 2)

mapCanvas.bind("<Configure>", resize_image)


def update_label(*args):
    selectedTown = cityVar.get()
    townData = gdf.loc[gdf['NAME'] == selectedTown]
    displayColumns = ['iP', 'iUE', 'iNS', 'iSP', 'iRI'] 
    columnNames = {
        'iP': 'Poverty Index',
        'iUE': 'Unemployment Index',
        'iNS': 'Lack of Education Index',
        'iSP': 'Single Parent Index',
        'iRI': 'Rent Income Index'
    }
    displayText = "\n\n\n".join([f"{columnNames[col]}: {round(townData.iloc[0][col], 3)}" for col in displayColumns])
    displayText += '\n\n------------------------------------\n'
    displayText += f"Homelessness Index: {round(townData.iloc[0]['iH'], 3)}"
    displayText += '\n------------------------------------'
    dataLabel.configure(text=displayText)

if getattr(sys, 'frozen', False):
    dataPath = file=os.path.join(sys._MEIPASS, "completedHomelessData.zip")
else:
    dataPath = file="completedHomelessData.zip"

gdf = gpd.read_file(dataPath)
gdf = gdf.explode()
gdf = gdf.groupby('NAME').first().reset_index()

towns = gdf['NAME'].tolist()

cityFrame = ctk.CTkFrame(root)
cityFrame.grid(row=0, column=1, sticky="nsew")

cityLabel = ctk.CTkLabel(cityFrame, text="Select a Town")
cityLabel.pack(pady=20)

cityVar = ctk.StringVar()
cityVar.set('Select a town')

cityDropdown = ctk.CTkOptionMenu(cityFrame, variable=cityVar, values=towns)
cityDropdown.pack(pady=20)

cityVar.trace_add("write", update_label)

dataLabel = ctk.CTkLabel(cityFrame, text="", font=('Arial', 30))
dataLabel.pack(pady=(40, 20)) 

root.mainloop()
