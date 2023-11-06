from PIL import Image

class Texture3dstException(Exception):
    def __init__(self, message):
        super().__init__(message)

class Texture3dst:
    def __init__(self):
        return

    def new(self, width: int, height: int, maxmiplevel: int):
        if type(width) != int:
            raise Texture3dstException("Width expected to be an integer.")
        if type(height) != int:
            raise Texture3dstException("Height expected to be an integer.")
        if type(maxmiplevel) != int:
            raise Texture3dstException("MaxMipLevel expected to be an integer.")
        if width <= 0:
            raise Texture3dstException("Width must be greater than 0.")
        if width > 61440:
            raise Texture3dstException("Width cannot be greater than 61440.")
        if height <= 0:
            raise Texture3dstException("Height must be greater than 0.")
        if height > 61440:
            raise Texture3dstException("Height cannot be greater than 61440.")
        if maxmiplevel <= 0:
            raise Texture3dstException("MaxMipLevel must be greater than 0.")
        if not ((width / (2 ** (maxmiplevel - 1)) >= 8) and (height / (2 ** (maxmiplevel - 1)) >= 8)):
            raise Texture3dstException("MaxMipLevel value greater than supported.")
        if width % 8 != 0:
            raise Texture3dstException("Width must be a multiple of 8.")
        if height % 8 != 0:
            raise Texture3dstException("Height must be a multiple of 8.")
        self.width = width
        self.height = height
        self.maxmiplevel = maxmiplevel
        self.texturemode = 3
        self.data = []
        for i in range(0, height):
            for j in range(0, width):
                for k in range(0, 4):
                    self.data.append(0)
        self.convertedData = []
        self.mipoutput = []
        self.output = []
        return self

    def setPixelRGBA(self, x: int, y: int, red: int, green: int, blue: int, alpha: int):
        if type(x) != int:
            raise Texture3dstException("x coordinates expected to be an integer.")
        if type(y) != int:
            raise Texture3dstException("y coordinates expected to be an integer.")
        if x < 0 or x >= self.width:
            raise Texture3dstException("x coordinates out of range.")
        if y < 0 or y >= self.height:
            raise Texture3dstException("y coordinates out of range.")
        if type(red) != int:
            raise Texture3dstException("red value expected to be an integer.")
        if type(green) != int:
            raise Texture3dstException("green value expected to be an integer.")
        if type(blue) != int:
            raise Texture3dstException("blue value expected to be an integer.")
        if type(alpha) != int:
            raise Texture3dstException("alpha value expected to be an integer.")
        if red < 0 or red > 255:
            raise Texture3dstException("red value must be between 0 and 255.")
        if green < 0 or green > 255:
            raise Texture3dstException("green value must be between 0 and 255.")
        if blue < 0 or blue > 255:
            raise Texture3dstException("blue value must be between 0 and 255.")
        if alpha < 0 or alpha > 255:
            raise Texture3dstException("alpha value must be between 0 and 255.")
        listPosition = ((y * self.width) + x) * 4
        self.data[listPosition] = red
        self.data[listPosition + 1] = green
        self.data[listPosition + 2] = blue
        self.data[listPosition + 3] = alpha
        return

    def getPixelData(self, x: int, y: int):
        if type(x) != int:
            raise Texture3dstException("x coordinates expected to be an integer.")
        if type(y) != int:
            raise Texture3dstException("y coordinates expected to be an integer.")
        if x < 0 or x >= self.width:
            raise Texture3dstException("x coordinates out of range.")
        if y < 0 or y >= self.height:
            raise Texture3dstException("y coordinates out of range.")
        listPosition = ((y * self.width) + x) * 4
        r = self.data[listPosition]
        g = self.data[listPosition + 1]
        b = self.data[listPosition + 2]
        a = self.data[listPosition + 3]
        return [r, g, b, a]
    
    def getPixelDataFromList(self, data: list, x: int, y: int, width: int, height: int):
        if type(data) != list:
            raise Texture3dstException("data expected to be a list.")
        if type(x) != int:
            raise Texture3dstException("x coordinates expected to be an integer.")
        if type(y) != int:
            raise Texture3dstException("y coordinates expected to be an integer.")
        if type(width) != int:
            raise Texture3dstException("width expected to be an integer.")
        if type(height) != int:
            raise Texture3dstException("height expected to be an integer.")
        if x < 0 or x >= width:
            raise Texture3dstException("x coordinates out of range.")
        if y < 0 or y >= height:
            raise Texture3dstException("y coordinates out of range.")
        listPosition = ((y * width) + x) * 4
        r = data[listPosition]
        g = data[listPosition + 1]
        b = data[listPosition + 2]
        a = data[listPosition + 3]
        return [r, g, b, a]

    def convertFunction(self, data: list, width: int, height: int):
        if type(data) != list:
            raise Texture3dstException("data expected to be a list.")
        if type(width) != int:
            raise Texture3dstException("width expected to be an integer.")
        if type(height) != int:
            raise Texture3dstException("height expected to be an integer.")
        convertedData = []
        x = 0
        y = 0
        for i in range(0, height // 8):
            for j in range(0, width // 8):
                for k in range(0, 2):
                    for l in range(0, 2):
                        for m in range(0, 2):
                            for n in range(0, 2):
                                for o in range(0, 2):
                                    for p in range(0, 2):
                                        pixelData = self.getPixelDataFromList(data, x, y, width, height)
                                        if pixelData[3] == 0:
                                            for q in range(0, 4):
                                                convertedData.append(0)
                                        else:
                                            convertedData.append(pixelData[3])
                                            convertedData.append(pixelData[2])
                                            convertedData.append(pixelData[1])
                                            convertedData.append(pixelData[0])
                                        x += 1
                                    x -= 2
                                    y += 1
                                x += 2
                                y -= 2
                            x -= 4
                            y += 2
                        x += 4
                        y -= 4
                    x -= 8
                    y += 4
                x += 8
                y -= 8
            x = 0
            y += 8

        return convertedData

    def flipX(self):
        return

    def flipY(self):
        return

    def getData(self):
        return self.data
    
    def getOutputData(self):
        return self.output

    def convertData(self):        
        self.convertedData = []
        self.convertedData = self.convertFunction(self.data, self.width, self.height)

        if self.maxmiplevel > 1:
            mipToExport = []
            self.mipoutput = []
            width = self.width
            height = self.height
            resizedwidth = self.width
            resizedheight = self.height

            # Copia la información de data a una imagen temporal
            tmpImage = Image.new("RGBA", (width, height))
            tmpImagePixels = tmpImage.load()
            x = 0
            y = 0
            for i in range(0, height):
                for j in range(0, width):
                    pixelData = self.getPixelDataFromList(self.data, x, y, width, height)
                    r = pixelData[0]
                    g = pixelData[1]
                    b = pixelData[2]
                    a = pixelData[3]
                    tmpImagePixels[x, y] = (r, g, b, a)
                    x += 1
                x = 0
                y += 1

            for i in range(0, self.maxmiplevel):
                # Se reescala la imagen
                resizedwidth = resizedwidth // 2
                resizedheight = resizedheight // 2
                wpercent = (resizedwidth/float(width))
                hsize = int((float(height)*float(wpercent)))
                tmpImage = tmpImage.resize((resizedwidth, hsize), Image.Resampling.LANCZOS)

                # Se obtiene los datos de la imagen reescalada
                mipToExport = []
                mipTmpData = []
                x = 0
                y = 0
                for j in range(0, resizedheight):
                    for k in range(0, resizedwidth):
                        pixelData = tmpImage.getpixel((x, y))
                        mipTmpData.append(pixelData[0])
                        mipTmpData.append(pixelData[1])
                        mipTmpData.append(pixelData[2])
                        mipTmpData.append(pixelData[3])
                        x += 1
                    x = 0
                    y += 1

                # Se convierte los datos usando la funcion
                mipToExport = self.convertFunction(mipTmpData, resizedwidth, resizedheight)

                # Se copian los datos a la lista de salida
                for j in range(0, len(mipToExport)):
                    self.mipoutput.append(mipToExport[j])

                # Se reducen las dimensiones en caso de usarse de nuevo
                width = width // 2
                height = height // 2

            mipToExport = []
            mipTmpData = []
            
        return
    
    def export(self, directory: str):
        if type(directory) != str:
            raise Texture3dstException("directory expected to be a string.")
        
        self.output = []

        # Convierte las dimensiones al formato de 16, 256
        width2 = self.width // 256
        height2 = self.height // 256
        width1 = self.width - (width2 * 256)
        height1 = self.height - (height2 * 256)

        # Se crea la cabecera
        ## Marca de formato
        self.output = [51, 68, 83, 84]
        self.output.append(self.texturemode)
        for i in range(0, 7):
            self.output.append(0)

        ## Se repite dos veces para las dimensiones y el checksum
        for i in range(0, 2):
            self.output.append(width1)
            self.output.append(width2)
            for j in range(0, 2):
                self.output.append(0)
            self.output.append(height1)
            self.output.append(height2)
            for j in range(0, 2):
                self.output.append(0)
        self.output.append(self.maxmiplevel)
        for i in range(0, 3):
            self.output.append(0)

        ## Se copia la lista de convertedData a output (Nivel primario)
        for i in range(0, len(self.convertedData)):
            self.output.append(self.convertedData[i])
        
        ## Se copia la lista mipoutput (Niveles de mip)
        if self.maxmiplevel > 1:
            for i in range(0, len(self.mipoutput)):
                self.output.append(self.mipoutput[i])

        # Convierte los numeros de informacion a bytes
        fileData = bytearray(self.output)

        # Se escriben los bytes en un archivo
        with open(f"{directory}", "wb") as f:
            f.write(fileData)

        return