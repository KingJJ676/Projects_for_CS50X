#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "wav.h"

int check_format(WAVHEADER header);
int get_block_size(WAVHEADER header);

int main(int argc, char *argv[])
{
    // Ensure proper usage
    if (argc != 3)
    {
        printf("Usage: ./reverse input.wav output.wav\n");
        return 1;
    }

    // Open input file for reading
    FILE *input_file = fopen(argv[1], "r");
    if (input_file == NULL)
    {
        printf("cannot open %s\n", argv[1]);
        return 1;
    }

    // Read header
    WAVHEADER header;
    fread(&header, sizeof(header), 1, input_file);

    // Use check_format to ensure WAV format
    int format_check = check_format(header);
    if (format_check == 1)
    {
        printf("Input is not a WAV file");
        fclose(input_file);
        return 1;
    }

    // Open output file for writing
    FILE *output_file = fopen(argv[2], "w");
    if (output_file == NULL)
    {
        printf("unable to open %s", argv[2]);
        fclose(input_file);
        return 1;
    }

    // Write header to file
    int a = fwrite(&header, sizeof(header), 1, output_file);
    if (a < 1)
    {
        printf("unable to write header to %s", argv[2]);
        fclose(input_file);
        fclose(output_file);
        return 1;
    }

    // Use get_block_size to calculate size of block
    int BlockSize = get_block_size(header);

    // Write reversed audio to file

    BYTE tem[BlockSize];

    fseek(input_file, sizeof(header) + header.subchunk2Size - BlockSize, SEEK_SET);

    for (int i = 0; i < header.subchunk2Size / BlockSize; i++)
    {
        fread(&tem, BlockSize, 1, input_file);   ///read auditory data into array
        fwrite(&tem, BlockSize, 1, output_file);   ///write data in array to output file
        fseek(input_file, - (BlockSize * 2), SEEK_CUR);   ///set pointer to correct place
    }


    //free memory & close file
    fclose(input_file);
    fclose(output_file);
}

int check_format(WAVHEADER header)
{
    if (memcmp(header.format, "WAVE", 4) == 0)
    {
        return 0;
    }
    else
    {
        return 1;
    }
}

int get_block_size(WAVHEADER header)
{
    //get bytes per sample
    int bytesPerSample = header.bitsPerSample / 8;

    //caculate block size
    int BlockSize = header.numChannels * bytesPerSample;

    //return block size
    return BlockSize;
}