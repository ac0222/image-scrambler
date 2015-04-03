########################IMAGE SCRAMBLER#####################################
"""
Purpose of this program is to scramble an image so it is completely
unrecognizable; however, this should be done in a way that is reversible,
so that the image can be later unscrambled successfully

BRIEF EXPLANATION

All the rows and columns are 'tagged' with their original positions
Positions are stored as binary values:
- Rows stored at LSB of intensity values
- Columns stored at bit 1 of intensity values

After being tagged, rows and columns are mixed randomly

Then, the intensity values are modified using bitwise inverting and splitting.
However, this process leaves bits 0 and 1 untouched, so info containing row and
column data remains intact.

To unscramble, the reverse process is simply applied, i.e.
Intensity values unscrambled first
Columns, then rows, are unscrambled
"""
################################################################################


import bits
import SimpleImage as sim
from random import randint
from PIL import Image

def scramble(image):
    sliced_and_diced = mix(image)
    scrambled = int_mix(sliced_and_diced)
    return scrambled

def unscramble(image):
    clean_int = unmix_int(image)
    all_clean = unmix(clean_int)
    return all_clean

def tagger(image,position):
    new_image = []
    row_n = 0

    for row in image:
        row_bits = bits.message_to_bits(str(row_n))
        i = 0
        new_row = []
        # Nested 'for' loop iterates over each pixel in the current row-list
        # (r,g,b) matches r,g,b to the three intenstiy values in each pixel
        # respectively, so r = first intensity value (red), and so on.
        
        for (r,g,b) in row:
            # Use codebit function to set the LSB of the
            # new intensity values to match the bit being indexed 
            new_r = bits.set_bit(r,bits.codebit(i,row_bits),position)
            new_g = bits.set_bit(g,bits.codebit(i + 1,row_bits),position)
            new_b = bits.set_bit(b,bits.codebit(i + 2,row_bits),position)
            # Amalgamate the three new intensity values into a new pixel
            new_pixel = (new_r,new_g,new_b)
            # Append new pixel to new row-list
            new_row.append(new_pixel)
            # increment counter by 3, as each pixel has 3 intensity values
            i += 3
        
        # attach new row-list to new image-list
        new_image.append(new_row)
        row_n += 1
    return new_image

def extractor(line,position):
    bit_str = ''
    for pixel in line:
        for intensity in pixel:
            bit_str += bits.get_bit(intensity,position)
    line_str = bits.bits_to_message(bit_str)
    line_n = int(line_str)
    return line_n

def mix_rows(image):
    # tags all rows first, so they can be unscrambled later
    # then jumbles rows randomly
    tagged_image = tagger(image,0)
    dummy_copy = list(tagged_image)
    new_image = []
    while dummy_copy:
        num_rows = len(dummy_copy)
        row_index = randint(0,num_rows - 1)
        old_row = dummy_copy[row_index]
        new_image.append(old_row)
        del dummy_copy[row_index]
    return new_image

def unmix_rows(tagged_image):
    template = list(tagged_image)
    for row in tagged_image:
        row_n = extractor(row,0)
        template[row_n] = row
    return template

def transpose(image):
    new_image = []
    num_rows = len(image)
    num_cols = len(image[0])
    for j in range(num_cols):
        new_row = []
        for i in range(num_rows):
            new_pixel = image[i][j]
            new_row.append(new_pixel)
        new_image.append(new_row)
    return new_image


def mix_cols(image):
    trans_copy = transpose(image)
    tagged_image = tagger(trans_copy,1)
    new_image = []
    while tagged_image:
        num_rows = len(tagged_image)
        row_index = randint(0,num_rows - 1)
        new_image.append(tagged_image[row_index])
        del tagged_image[row_index]  
    return transpose(new_image)

def unmix_cols(tagged_image):
    trans_tagged = transpose(tagged_image)
    template = list(trans_tagged)
    for row in trans_tagged:
        row_n = extractor(row,1)
        template[row_n] = row
    new_image = transpose(template)
    return new_image

def mix(image):
    rowed = mix_rows(image)
    doublemix = mix_cols(rowed)
    return doublemix

def unmix(image):
    clean_cols = unmix_cols(image)
    all_clean = unmix_rows(clean_cols)
    return all_clean

"""
mixing the intensity values of the pixels
"""

def digitwise_flip(str_x):
    result = ''
    for digit in str_x:
        ans = str(int(digit)^1)
        result += ans
    return result

def zero_padder2(x):
    if len(x) < 8:
        x = '0'*(8-len(x)) + x
    return x

def int_mod(n):
    binary = bin(n)[2:]
    byte = zero_padder2(binary)
    roi = byte[:6]
    info = byte[6:]
    inv_roi = digitwise_flip(roi)
    new_bin = inv_roi[4:] + inv_roi[:4] + info   
    new_int = int('0b' + new_bin,2)
    return new_int

def int_mix(image):
    new_image = []
    for row in image:
        new_row = []
        for r,g,b in row:
            new_r = int_mod(r)
            new_g = int_mod(g)
            new_b = int_mod(b)
            new_pixel = (new_r,new_g,new_b)
            new_row.append(new_pixel)
        new_image.append(new_row)
    return new_image

def unmix_int(image):
    mix = int_mix(image)
    for i in range(4):
        mix = int_mix(mix)
    return mix

# function wrapper for gui
def scramblePILimage(PILimage):
    image = sim.to_rectangle(PILimage)
    return sim.to_flat(scramble(image))

def unscramblePILimage(PILimage):
    image = sim.to_rectangle(PILimage)
    return sim.to_flat(unscramble(image))