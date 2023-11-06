#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            int ave = round(((float)image[h][w].rgbtRed + image[h][w].rgbtGreen + image[h][w].rgbtBlue) / 3);

            image[h][w].rgbtRed = ave;
            image[h][w].rgbtGreen = ave;
            image[h][w].rgbtBlue = ave;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE tem[height][width];

    for (int i = 0; i < height; i++) //repeat on every row
    {

        for(int j = 0; j < width; j++)
        {
            tem[i][j] = image[i][width - 1 - j];
        }

        for (int k = 0; k < width; k++)
        {
            image[i][k] = tem[i][k];
        }
    }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE tem_image[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
           //loop over every pixel

            int totR = 0;
            int totG = 0;
            int totB = 0;

            int pixel_count = 9;

            // 1. caculate RGB average(round)
            for (int k = i - 1; k <= i + 1; k++)
            {
                for (int l = j -1; l <= j + 1; l++)
                {
                    //if edge, pixel_count -1
                    if (k < 0 || k > height - 1|| l < 0 || l > width - 1)
                    {
                        pixel_count -= 1;
                    }

                    //if in range, caculate color ave
                    else
                    {
                        totR += image[k][l].rgbtRed;
                        totG += image[k][l].rgbtGreen;
                        totB += image[k][l].rgbtBlue;
                    }
                }
            }


            // 2. store color to tem_image
            tem_image[i][j].rgbtRed = round((float)totR / pixel_count);
            tem_image[i][j].rgbtGreen = round((float)totG / pixel_count);
            tem_image[i][j].rgbtBlue = round((float)totB / pixel_count);

        }
    }

    //3. copy tem_image to original image
    for (int a = 0; a < height; a++)
    {
        for (int b = 0; b < width; b++)
        {
            image[a][b].rgbtRed = tem_image[a][b].rgbtRed;
            image[a][b].rgbtGreen = tem_image[a][b].rgbtGreen;
            image[a][b].rgbtBlue = tem_image[a][b].rgbtBlue;
        }
    }

    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{

    RGBTRIPLE tem_image[height][width];

    //loop over each pixel
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            RGBTRIPLE focus[3][3];

            //append 9 blocks to focus[]
            for (int a = i - 1, s = 0; a <= i + 1; a++, s++)
            {
                for (int b = j -1, t = 0; b <= j + 1; b++, t++)
                {
                    if (a >= 0 && a <= height - 1 && b >= 0 && b <= width - 1)
                    {
                        focus[s][t] = image[a][b];
                    }
                    else
                    {
                        focus[s][t].rgbtRed = 0;
                        focus[s][t].rgbtGreen = 0;
                        focus[s][t].rgbtBlue = 0;
                    }
                }
            }

            //gx-r, g, b
            int gx_red = -1*(focus[0][0].rgbtRed+focus[2][0].rgbtRed) -2*(focus[1][0].rgbtRed) +1*(focus[0][2].rgbtRed+focus[2][2].rgbtRed) +2*(focus[1][2].rgbtRed);
            int gx_green = -1*(focus[0][0].rgbtGreen+focus[2][0].rgbtGreen) -2*(focus[1][0].rgbtGreen) +1*(focus[0][2].rgbtGreen+focus[2][2].rgbtGreen) +2*(focus[1][2].rgbtGreen);
            int gx_blue = -1*(focus[0][0].rgbtBlue+focus[2][0].rgbtBlue) -2*(focus[1][0].rgbtBlue) +1*(focus[0][2].rgbtBlue+focus[2][2].rgbtBlue) +2*(focus[1][2].rgbtBlue);


            //gy-r, g, b
            int gy_red = -1*(focus[0][0].rgbtRed+focus[0][2].rgbtRed) -2*(focus[0][1].rgbtRed) +1*(focus[2][0].rgbtRed+focus[2][2].rgbtRed) +2*(focus[2][1].rgbtRed);
            int gy_green = -1*(focus[0][0].rgbtGreen+focus[0][2].rgbtGreen) -2*(focus[0][1].rgbtGreen) +1*(focus[2][0].rgbtGreen+focus[2][2].rgbtGreen) +2*(focus[2][1].rgbtGreen);
            int gy_blue = -1*(focus[0][0].rgbtBlue+focus[0][2].rgbtBlue) -2*(focus[0][1].rgbtBlue) +1*(focus[2][0].rgbtBlue+focus[2][2].rgbtBlue) +2*(focus[2][1].rgbtBlue);

            //compute new-r, g, b (cap to 255)
            int new_red = round(sqrt((gx_red*gx_red) + (gy_red*gy_red)));
            if (new_red > 255)
            {
                new_red = 255;
            }

            int new_green = round(sqrt((gx_green*gx_green) + (gy_green*gy_green)));
            if (new_green > 255)
            {
                new_green = 255;
            }

            int new_blue = round(sqrt((gx_blue*gx_blue) + (gy_blue*gy_blue)));
            if (new_blue > 255)
            {
                new_blue = 255;
            }

            //store new value to tem_image
            tem_image[i][j].rgbtRed = new_red;
            tem_image[i][j].rgbtGreen = new_green;
            tem_image[i][j].rgbtBlue = new_blue;

        }
    }

    //copy tem_image to original image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = tem_image[i][j].rgbtRed;
            image[i][j].rgbtGreen = tem_image[i][j].rgbtGreen;
            image[i][j].rgbtBlue = tem_image[i][j].rgbtBlue;
        }
    }

    return;
}
