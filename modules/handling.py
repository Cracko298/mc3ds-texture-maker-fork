import os
from pathlib import Path

from .tex3dst import *

class atlasTexture3dst():
    def __init__(self):
        pass

    def open(self, path: str | Path, atlas_type: str):
        if type(path) == str:
            path = Path(path)
        if not isinstance(path, Path):
            raise TypeError("Expected str or Path type for path.")
        if not atlas_type in ["Items", "Blocks"]:
            raise ValueError("Expected 'Items' or 'Blocks' type for atlas_type.")

        print("Opening atlas...")
        atlas = None
        if path.suffix == ".png":
            atlas = Texture3dst().fromImage(Image.open(path))
            if atlas_type == "Blocks":
                atlas.miplevel = 3
        elif path.suffix == ".3dst":
            atlas = Texture3dst().open(path)
            atlas.flipX()

        self.atlas = atlas
        self.atlas_type = atlas_type

        return self

    def addElement(self, position: tuple | list, new_texture: Image.Image):
        new_texture = new_texture.convert("RGBA")

        # Define las variables de posición
        x_atlas = position[0]
        y_atlas = position[1]

        if self.atlas_type == "Items":
            # Reemplazar la textura original por la nueva
            print("Replacing texture...")
            x = 0
            y = 0
            for y in range(0, 16):
                for x in range(0, 16):
                    r, g, b, a = new_texture.getpixel((x, y))
                    self.atlas.setPixelRGBA(x_atlas, y_atlas, (r, g, b, a))
                    x_atlas += 1
                x_atlas -= 16
                y_atlas += 1
        elif self.atlas_type == "Blocks":
            # Reemplazar la textura original por la nueva
            print("Replacing texture...")
            x = -2
            y = -2
            x2 = 0
            y2 = 0
            for i in range(0, 20):
                for i in range(0, 20):
                    if x < 0:
                        x2 = 0
                    if x > 15:
                        x2 = 15
                    if y < 0:
                        y2 = 0
                    if y > 15:
                        y2 = 15
                    if x >= 0 and x <= 15:
                        x2 = x
                    if y >= 0 and y <= 15:
                        y2 = y
                    r, g, b, a = new_texture.getpixel((x2, y2))
                    self.atlas.setPixelRGBA(x_atlas, y_atlas, (r, g, b, a))
                    x += 1
                    x_atlas += 1
                x = -2
                x_atlas -= 20
                y += 1
                y_atlas += 1

    def save(self, path: str | Path):
        if type(path) == str:
            path = Path(path)
        if not isinstance(path, Path):
            raise TypeError("Expected str or Path type for path.")
        
        if not os.path.exists(path.parent):
            os.makedirs(path.parent)

        print("Inverting x-axis atlas...")
        self.atlas.flipX()
        print("Converting data...")
        self.atlas.convertData()

        print("Saving atlas...")
        self.atlas.export(path)
        print("Success")

def getItemsFromIndexFile(filename):
    items = []
    with open(filename, "r") as f:
        content = f.read()
        items = content.split("\n")
    
    return items

def calculateGrid(value: int, grid_width: int, grid_height: int, cube_lenght: int):
    x_grid = value - ((value // grid_width) * grid_width)
    y_grid = value // grid_width
    if y_grid > grid_height:
        return -1
    x = x_grid * cube_lenght
    y = y_grid * cube_lenght

    return (x, y)

def createOutputDirectory(directoryName):
    if not os.path.exists(directoryName):
        os.makedirs(directoryName)

def addElementToFile(value, filePath: str):
    if os.path.exists(filePath):
        with open(filePath, "a") as f:
            f.write(f"{value}\n")
        return
    else:
        file = open(filePath, "w")
        file.write(f"{value}\n")

def addToItemAtlas(pixelPosition, textureImgPath, sourceFolder, output_folder):
    # Carga los archivos necesarios a la memoria
    if os.path.exists(f"{output_folder}/atlas/atlas.items.meta_79954554_0.3dst"):
        print("Opening modified atlas...")
        itemAtlas = Texture3dst().open(f"{output_folder}/atlas/atlas.items.meta_79954554_0.3dst")
        # El archivo previamente debe estar de cabeza entonces hay que voltearlo para usarlo normal
        itemAtlas.flipX()
    else:
        print("Creating new atlas file from original...")
        itemAtlas = Texture3dst().fromImage(Image.open(f"{sourceFolder}/atlas/atlas.items.vanilla.png"))

    print("Opening new texture...")
    textureImg = Image.open(textureImgPath).convert("RGBA")
        
    # Define las variables de posición
    x_atlas = pixelPosition[0]
    y_atlas = pixelPosition[1]

    # Reemplazar la textura original por la nueva
    print("Replacing new texture...")
    x = 0
    y = 0
    for y in range(0, 16):
        for x in range(0, 16):
            r, g, b, a = textureImg.getpixel((x, y))
            itemAtlas.setPixelRGBA(x_atlas, y_atlas, (r, g, b, a))
            x_atlas += 1
        x_atlas -= 16
        y_atlas += 1

    # Crea el directorio de salida si no existe
    if not os.path.exists(f"{output_folder}/atlas"):
        createOutputDirectory(f"{output_folder}/atlas")

    # Invierte el atlas en el eje x y convierte los datos del atlas antes de exportarlos
    print("Inverting x-axis atlas...")
    itemAtlas.flipX()
    print("Converting data...")
    itemAtlas.convertData()

    # Guarda el atlas modificado
    print("Saving changes...")
    itemAtlas.export(f"{output_folder}/atlas/atlas.items.meta_79954554_0.3dst")
    print("Success")

    return True

def addToBlockAtlas(pixelPosition, textureImgPath, sourceFolder, output_folder):
    # Carga los archivos necesarios a la memoria
    print("Starting...")
    if os.path.exists(f"{output_folder}/atlas/atlas.terrain.meta_79954554_0.3dst"):
        print("Opening modified atlas...")
        blockAtlas = Texture3dst().open(f"{output_folder}/atlas/atlas.terrain.meta_79954554_0.3dst")
        # El archivo previamente debe estar de cabeza entonces hay que voltearlo para usarlo normal
        blockAtlas.flipX()
    else:
        print("Creating new texture file from original...")
        blockAtlas = Texture3dst().fromImage(Image.open(f"{sourceFolder}/atlas/atlas.terrain.vanilla.png"))
        blockAtlas.miplevel = 3

    print("Opening new texture...")
    textureImg = Image.open(textureImgPath).convert("RGBA")
        
    # Define las variables de posición
    x_atlas = pixelPosition[0]
    y_atlas = pixelPosition[1]

    # Reemplazar la textura original por la nueva
    print("Replacing texture...")
    x = -2
    y = -2
    x2 = 0
    y2 = 0
    for i in range(0, 20):
        for i in range(0, 20):
            if x < 0:
                x2 = 0
            if x > 15:
                x2 = 15
            if y < 0:
                y2 = 0
            if y > 15:
                y2 = 15
            if x >= 0 and x <= 15:
                x2 = x
            if y >= 0 and y <= 15:
                y2 = y
            r, g, b, a = textureImg.getpixel((x2, y2))
            blockAtlas.setPixelRGBA(x_atlas, y_atlas, (r, g, b, a))
            x += 1
            x_atlas += 1
        x = -2
        x_atlas -= 20
        y += 1
        y_atlas += 1

    # Crea el directorio de salida si no existe
    if not os.path.exists(f"{output_folder}/atlas"):
        createOutputDirectory(f"{output_folder}/atlas")

    # Invierte el atlas en el eje x y convierte los datos del atlas antes de exportarlos
    print("Inverting x-axis atlas...")
    blockAtlas.flipX()
    print("Converting data...")
    blockAtlas.convertData()

    # Guarda el atlas modificado
    print("Saving changes...")
    blockAtlas.export(f"{output_folder}/atlas/atlas.terrain.meta_79954554_0.3dst")
    print("Success")

    return True