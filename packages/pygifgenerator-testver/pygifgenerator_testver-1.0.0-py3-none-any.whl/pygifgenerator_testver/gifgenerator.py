
import glob
from PIL import Image

class GIFGenerator:
    def __init__(self, inputPath=None, outputPath=None, imgSize=(320, 240)):
        """
        inputPath: path of argument images
        outputPath : path of Generated GIF
        imgSize : Size of Images
        """
        self.inputPath = inputPath or './*png'
        self.outputPath = outputPath or './output.gif'
        self.imgSize = imgSize

    def generate_gif(self):
        img, *images = [Image.open(f).resize(self.imgSize, Image.LANCZOS) for f in sorted(glob.glob(self.inputPath))]

        try:
            img.save(
                fp=self.outputPath,
                format='GIF',
                append_images=images,
                save_all=True,
                duration=500,
                loop=0,
                disposal=2
            )
        except IOError:
            print(f'Can`t generate GIF File {img}')

if __name__ == "__main__":
    c = GIFGenerator(inputPath='./project/images/*.png', outputPath='./project/image_out/result.gif', imgSize=(640, 480))
    c.generate_gif()