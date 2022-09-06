import sys
import cv2 as cv
import numpy as np


def main(argv):
    print("""
    Zoom In-Out demo
    ------------------
    * [i] -> Zoom [i]n
    * [o] -> Zoom [o]ut
    * [ESC] -> Close program
    """)

    filename = argv[0] if len(argv) > 0 else 'a.jpg'
    # Load the image
    src = cv.imread(cv.samples.findFile(filename))
    # Check if image is loaded fine
    if src is None:
        print('Error opening image!')
        print(
            'Usage: pyramids.py [image_name -- default ../data/chicky_512.png] \n')
        return -1

    #src = cv.pyrUp(src, dstsize=(2 * cols, 2 * rows))
    src = down_scale(src, "nivel-1.jpg")
    src = down_scale(src, "nivel-2.jpg")
    src = down_scale(src, "nivel-3.jpg")
    src = cv.imread(cv.samples.findFile(filename))
    src = upscale(src, "nivel1.jpg")
    src = upscale(src, "nivel2.jpg")
    src = upscale(src, "nivel3.jpg")

    print('** Zoom In: Image x 2')

    return 0


def upscale(src, title):
    new_matrix = proccessImageUpscale(src)
    new_matrix = proccess_upscale(src, new_matrix)
    src = gaussBiggerLayer(new_matrix)
    cv.imwrite(title, src)
    return src


def proccess_upscale(image, new_image):
    k, z = 0, 0
    print(new_image.shape)
    for i in range(len(new_image)):
        for j in range(len(new_image)):
            if i % 2 != 0 and j % 2 != 0:
                new_image[i][j] = image[k][z]
                #print(f"{k} + {z}")
                if z < len(image) - 1:
                    z += 1
                else:
                    k += 1
                    z = 0

    return new_image


def down_scale(src, title):
    src = gaussSmallerLayer(src)
    src = processImage(src)
    cv.imwrite(title, src)
    return src


def gaussSmallerLayer(src):
    kernel_size = 5
    kernel = np.ones((kernel_size, kernel_size), dtype=np.float64)
    kernel = np.float64([[1/256, 4/256, 6/256, 4/256, 1/256],
                        [4/256, 16/256, 24/256, 16/256, 4/256],
                        [6/256, 24/256, 36/256, 24/256, 6/256],
                        [4/256, 16/256, 24/256, 16/256, 4/256],
                        [1/256, 4/256, 6/256, 4/256, 1/256]])
    dst = cv.filter2D(src, -1, kernel)
    return(dst)


def gaussBiggerLayer(src):
    kernel_size = 5
    kernel = np.ones((kernel_size, kernel_size), dtype=np.float64)
    kernel = np.float64([[1/64, 4/64, 6/64, 4/64, 1/64],
                        [4/64, 16/64, 24/64, 16/64, 4/64],
                        [6/64, 24/64, 36/64, 24/64, 6/64],
                        [4/64, 16/64, 24/64, 16/64, 4/64],
                        [1/64, 4/64, 6/64, 4/64, 1/64]])
    dst = cv.filter2D(src, -1, kernel)
    return(dst)


def processImage(image):
    new_image = []
    for i in range(len(image)):
        new_row = []
        for j in range(len(image)):
            if i % 2 != 0 and j % 2 != 0:
                new_row.append(image[i][j])
        if new_row:
            new_image.append(np.array(np.array(new_row)))
    return np.array(new_image)


def proccessImageUpscale(image):
    size = image.shape[0]*2
    basic = np.array([0, 0, 0], dtype=np.uint8)
    new_row = np.array([basic]*size)
    new_matrix = np.array([new_row]*size)

    return new_matrix


if __name__ == "__main__":
    main(sys.argv[1:])
