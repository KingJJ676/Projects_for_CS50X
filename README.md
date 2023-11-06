# Filters
This project focuses on what we can do with pixels. 4 kinds of filters are included: grayscale, reflection, blur, and identifying edges. 

Check out the **helpers.c** file to see the code.

## Grayscale
To convert a pixel to grayscale, we just need to make sure the red, green, and blue values are all the same value. To ensure each pixel of the new image still has the same general brightness or darkness as the old image, we can take the average of the red, green, and blue values to determine what shade of grey to make the new pixel.

## Reflection
The resulting image of a reflection filter is what you would get by placing the original image in front of a mirror. So any pixels on the left side of the image should end up on the right, and vice versa.

## Blur
For this project, I used the **box blur** --- take each pixel and, for each color value, give it a new value by averaging the color values of neighboring pixels.  

Consider the following grid of pixels, where we’ve numbered each pixel.  

![image](https://github.com/KingJJ676/Projects-for-CS50/assets/130853046/5e062edf-af0b-4681-a638-8190a8fd6568)

The new value of each pixel would be the average of the values of all of the pixels that are within 1 row and column of the original pixel (forming a 3x3 box). For example, each of the color values for pixel 6 would be obtained by averaging the original color values of pixels 1, 2, 3, 5, 6, 7, 9, 10, and 11 (note that pixel 6 itself is included in the average). Likewise, the color values for pixel 11 would be be obtained by averaging the color values of pixels 6, 7, 8, 10, 11, 12, 14, 15 and 16.

For a pixel along the edge or corner, like pixel 15, we would still look for all pixels within 1 row and column: in this case, pixels 10, 11, 12, 14, 15, and 16.

## Identifying Edges
This filter detects lines that create a boundary between one object and another using the **Sobel operator**.

Like image blurring, edge detection also works by taking each pixel, and modifying it based on the 3x3 grid of pixels that surrounds that pixel. But instead of just taking the average of the nine pixels, the Sobel operator computes the new value of each pixel by taking a weighted sum of the values for the surrounding pixels. And since edges between objects could take place in both a vertical and a horizontal direction, you’ll actually compute two weighted sums: one for detecting edges in the x direction, and one for detecting edges in the y direction. In particular, you’ll use the following two “kernels”:

![image](https://github.com/KingJJ676/Projects-for-CS50/assets/130853046/c65e2061-a68c-4a49-8644-af3aadd0c9cd) 

How to interpret these kernels? In short, for each of the three color values for each pixel, we’ll compute two values Gx and Gy. To compute Gx for the red channel value of a pixel, for instance, we’ll take the original red values for the nine pixels that form a 3x3 box around the pixel, multiply them each by the corresponding value in the Gx kernel, and take the sum of the resulting values.

Using these kernels, we can generate a Gx and Gy value for each of the red, green, and blue channels for a pixel. But each channel can only take on one value, not two: so we need some way to combine Gx and Gy into a single value. The Sobel filter algorithm combines Gx and Gy into a final value by calculating the square root of Gx^2 + Gy^2. 
