import numpy as np 
import png

class Image():
    def __init__(self, x_px=0, y_px=0, rgb_channels=0, filename=''):
        # input the filename OR x_px, y_px, and rgb_channels
        self.input_path = 'input/'
        self.output_path = 'output/'
        if x_px and y_px and rgb_channels:
            self.x_px = x_px
            self.y_px = y_px
            self.rgb_channels = rgb_channels
            self.array = np.zeros((x_px, y_px, rgb_channels))
        elif filename:
            self.array = self.read_img(filename)
            self.x_px, self.y_px, self.rgb_channels = self.array.shape
        else:
            raise ValueError("Input either a filename OR specify the dimensions of the image")
    
    def read_img(self, filename, gamma=2.2):
        '''
        read PNG RGB image, return 3D numpy array organized along Y, X, channel
        values are float, gamma is decoded
        '''
        img = png.Reader(self.input_path + filename).asFloat()
        resize_img = np.vstack(list(img[2]))
        resize_img.resize(img[1], img[0], 3)
        resize_img = resize_img ** gamma
        return resize_img
    
    def write_img(self, output_file_name, gamma=2.2):
        '''
        3D numpy array (Y, X, channel) of values between 0 and 1 -> write to png
        '''
        img = np.clip(self.array, 0, 1)
        y, x = self.array.shape[0], self.array.shape[1]
        img = img.reshape(y, x*3)
        writer = png.Writer(x, y)
        with open(self.output_path + output_file_name, 'wb') as f:
            writer.write(f, 255*(img**(1/gamma)))
        self.array.resize(y, x, 3)  # we mutated the method in the first step of the function


if __name__ == '__main__':
    img = Image(filename='lake.png')
    img.write_img('test.png')