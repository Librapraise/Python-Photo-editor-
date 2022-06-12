from image import Image
import numpy as np

def brighten_img(image, factor):
    # when we brighten, we just want to make each channel higher by some amount 
    # factor is a value > 0, how much you want to brighten the image by (< 1 = darken, > 1 = brighten)
    x_px, y_px, rgb_channels = image.array.shape
    new_img = Image(x_px=x_px, y_px=y_px, rgb_channels=rgb_channels)
    for x in range(x_px):
        for y in range(y_px):
            for r in range(rgb_channels):
                new_img.array[x, y, r] = image.array[x, y, r] * factor
    return new_img


def adjust_img_contrast(image, factor, mid):
    # adjust the contrast by increasing the difference from the user-defined midpoint by factor amount
    x_px, y_px, rgb_channels = image.array.shape
    new_img = Image(x_px=x_px, y_px=y_px, rgb_channels=rgb_channels)
    for x in range(x_px):
        for y in range(y_px):
            for r in range(rgb_channels):
                new_img.array[x, y, r] = (image.array[x, y, r] - mid) * factor + mid

    return new_img

def blur_img(image, kernel_size):
    # kernel size is the number of pixels to take into account when applying the blur
    # (ie kernel_size = 3 would be neighbors to the left/right, top/bottom, and diagonals)
    # kernel size should always be an *odd* number
    x_px, y_px, rgb_channels = image.array.shape
    new_img = Image(x_px=x_px, y_px=y_px, rgb_channels=rgb_channels)
    neighbors_range = kernel_size // 2
    for x in range(x_px):
        for y in range(y_px):
            for r in range(rgb_channels):

                total = 0
                for x_r in range(max(0,x-neighbors_range), min(new_img.x_px-1, x+neighbors_range)+1):
                    for y_r in range(max(0,y-neighbors_range), min(new_img.y_px-1, y+neighbors_range)+1):
                        total += image.array[x_r, y_r, r]
                new_img.array[x, y, r] = total / kernel_size ** 2 

    return new_img
    

def apply_kernel_img(image, kernel):
    # the kernel should be a 2D array that represents the kernel we'll use!
    # for the sake of simiplicity of this implementation, let's assume that the kernel is SQUARE
    # for example the sobel x kernel (detecting horizontal edges) is as follows:
    # [1 0 -1]
    # [2 0 -2]
    # [1 0 -1]
    x_px, y_px, rgb_channels = image.array.shape
    new_img = Image(x_px=x_px, y_px=y_px, rgb_channels=rgb_channels)

    neighbors_range = kernel.shape[0] // 2
    for x in range(x_px):
        for y in range(y_px):
            for r in range(rgb_channels):

                total = 0
                for x_r in range(max(0,x-neighbors_range), min(new_img.x_px-1, x+neighbors_range)+1):
                    for y_r in range(max(0,y-neighbors_range), min(new_img.y_px-1, y+neighbors_range)+1):
                        x_k = x_r + neighbors_range - x
                        y_k = y_r + neighbors_range - y
                        kernel_val = kernel[x_k, y_k]
                        total += image.array[x_r, y_r, r] * kernel_val
                new_img.array[x, y, r] = total 

    return new_img

def combine_images(image1, image2):
    # let's combine two images using the squared sum of squares: value = sqrt(value_1**2, value_2**2)
    # size of image1 and image2 MUST be the same
    x_px, y_px, rgb_channels = image.array.shape
    new_img = Image(x_px=x_px, y_px=y_px, rgb_channels=rgb_channels)
    neighbors_range = kernel_size // 2
    for x in range(x_px):
        for y in range(y_px):
            for r in range(rgb_channels):
                new_img.array[x, y, r] = (image1.array[x, y, r]**2 + image2[x, y, r]**2)**0.5 

    return new_img
    
if __name__ == '__main__':
    lake = Image(filename='lake.png')
    city = Image(filename='city.png')
    


  # brightening
    brightened_im = brighten_img(lake, 1.7)
    brightened_im.write_img('brightened.png')

    # darkening
    darkened_im = brighten_img(lake, 0.3)
    darkened_im.write_img('darkened.png')

    # increase contrast
    incr_contrast = adjust_img_contrast(lake, 2, 0.5)
    incr_contrast.write_img('increased_contrast.png')

    # decrease contrast
    decr_contrast = adjust_img_contrast(lake, 0.5, 0.5)
    decr_contrast.write_img('decreased_contrast.png')

    # blur using kernel 3
    blur_3 = blur_img(city, 3)
    blur_3.write_img('blur_k3.png')


    # blur using kernel size of 15
    blur_15 = blur_img(city, 15)
    blur_15.write_img('blur_k15.png')

    # let's apply a sobel edge detection kernel on the x and y axis
    sobel_x = apply_kernel_img(city, np.array([
        [1, 2, 1], 
        [0, 0, 0], 
        [-1, -2, -1]
    ]))
    sobel_x.write_img('edge_x.png')
    #edge_y
    sobel_y = apply_kernel_img(city, np.array([
        [1, 0, -1], 
        [2, 0, -2], 
        [1, 0, -1]
    ]))
    sobel_y.write_img('edge_y.png')

    # let's combine these and make an edge detector!
    sobel_xy = combine_images(sobel_x, sobel_y)
    sobel_xy.write_img('edge_xy.png')

