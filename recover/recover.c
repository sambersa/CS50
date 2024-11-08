#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover (name of image)");
        return 1;
    }

    // Open the memory card
    FILE *mem_card = fopen(argv[1], "r");

    if (mem_card == NULL)
    {
        printf("Memory Card could not be opened.\n");
        return 1;
    }

    // While there's still data left to read from the memory card
    uint8_t buffer[512];
    int counter = 0;
    FILE *jpg = NULL;

    while (fread(buffer, 1, 512, mem_card) == 512)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            if (jpg != NULL)
            {
                fclose(jpg);
            }

            else if (jpg == NULL)
            {
                printf("Could not open JPG file.\n");
            }

            // Open new file and write buffer
            char filename[8];
            sprintf(filename, "%03i.jpg", counter);
            jpg = fopen(filename, "w");

            counter++;
        }
        if (jpg != NULL)
        {
            fwrite(buffer, 1, 512, jpg);
        }
    }
    fclose(jpg);
    fclose(mem_card);
}
