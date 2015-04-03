"""
################################################################################
Project 2: Steganography

Author:

Adrian Cheung

Date created:
14 September 2013

Notes:

The purpose of this program is to encode a piece of text inside an existing
image, as well as decode a piece of text from a previously encoded image.
This is an example of steganography, where a message is concealed inside 
another piece of data (in this case, an image). This allows a secure line
of communication between 2 parties, as even if a transmission was intercepted,
a spy would only see the encoded image, and not the message hidden in it.

The encoding process is achieved through a number of steps:
FIRST STEP: CONVERTING TEXT MESSAGE INTO A STREAM OF BINARY NUMBERS

- Each character in the  text message to be encoded, is first converted into 
the binary representation of its ASCII code; For example 'a' corresponds to 
the base ten integer 97, which written in binary is 01100001. 8-bits are used
to keep each 'chunk' a uniform size.
- Once all the characters have been converted into 8-bit binary numbers, all
these chunks are appended together to form a long stream of binary digits (ones
and zeroes); a bitstream.

SECOND STEP: ENCODING THIS BITSTREAM INTO AN IMAGE

- Images in a computer are represented by a grid of pixels; each pixel contains
three integer values which correspond to the intensity of red, green and blue 
for that specific pixel. The intensity values range from 0-255 and they 
determine the colour of the pixel.
- In python, the image is basically a huge list of lists of tuples:
i.e., the entire image object itself is a list; each row of pixels in the 
image are lists within the whole image list, and each pixel is a 3-element 
tuple which is an element of a row list. To avoid confusion:
- Top level list representing image obhect will be referred to as 'image-lists'
- Inner lists representing rows referred to as 'row-lists'

The way in which the message is encoded, is that the intensity values are 
modified so their least significant bits are used to encode the string of
bits representing the ASCII characters of the text message. A more detailed
description is given in the encode function below.
Once the entire message has been encoded, the LSBs of the remaining 
intenstiy values in the image are all changed to 0; this is done to
signal the end of the message in the decoding process.

DECODING THE MESSAGE FROM AN ENCODED IMAGE:

To decode a message from an encoded image:
- Convert all intensity values of image to binary
- Index LSB of each intensity value and append it to a growing list
of bits to reconstruct original message.
- Split reconstructed bitstream into 8-bit chunks, then convert each chunk 
into its corresponding ASCII character.

COMMON CASES:

- Bitstream not exactly divisble by 8; e.g. bitstream is 65 bits long;
In this case, bitstream divided into eight 8-bit chunks and one 1-bit 
'remainder'. Function decodes all the chunks 8-bits long; once it 
encounters a chunk NOT 8-bits long, it immediately returns everything it
has decoded so far, and exits.
- Function encounters an 8-bit chunk consisting only of zeroes, i.e. 
00000000; function will immediately return everything it has decoded
so far, and exit.

The program is designed to be used with Python 2.7

Date modified and reason:
2 October 2013: Changed encode function slightly to streamline it and make it
                less confusing
                Added codebit function
4 October 2013: Added documentation
################################################################################
"""
import bits
import SimpleImage as sim
#from SimpleImage import read_image, write_image, to_flat, to_rectangle

def encode(image,message):
    """
    This function takes an image as its first argument, a message as its
    second argument, and returns an encoded image as its result.
    The input image is a rectangular two-dimensional list of pixels, in 
    zero-based row-major order. Each pixel is a 3-element tuple of integers 
    in the range [0,255]. Input message is a string of ASCII characters. 
    
    Encoding process:
    1: Convert the ASCII message into a string of binary digits using
    message_to_bits function
    2: Take the first intensity value (red intenstiy, of top-left pixel) 
    convert it into binary, and generate a new BINARY intenstiy value exactly 
    the same as the original, except change THE LEAST SIGNIFICANT BIT (LSB) 
    of this number to match the FIRST bit of the message bitstream. 
    3: Repeat the above step for intenstiy value 2, ( green intensity of 
    top-left pixel), for second bitstream bit, and same for third intenstiy 
    value, so you now have three new 'encoded' intenstiy values. 
    4: Put these values into a NEW three elemnt tuple, i.e an encoded PIXEL, 
    then  put this new pixel into a new row-list.
    5: Repeat steps 2-4 for the entire first row-list of the original image,
    to generate an  encoded row-list of tuples almost identical to the 
    original one, except for having (possibly) different LSBs for each 
    intensity value. Add this row-list to a new image-list, i.e. the 
    encoded image.
    6: Repeat 5 for each row-list of the original image, to build up an 
    entirely new, encoded image-list which the encode function will return 
    as its result.
    
    General cases:
    - NOT ENOUGH INTENSTIY VALUES TO ENCODE ENTIRE MESSAGE
    Program will encode as much of the message as possible
    - EXTRA INTENSTIY VALUES LEFTOVER
    Program will change the LSB of all 'unencoded' intensity values to 0 
    
    Inputs:
        image: a two-dimensional list of pixels, in zero-based row-major order.
               Each pixel is a three element tuple of integers in the range
               [0,255].
        message: a string of ASCII characters
    
    Result:
        new_image: a new image in the same format as the original, with the 
        same dimensions, but with the message coded into the LSBs of the
        intenstiy values in each pixel.
    
    Examples:
        >>> test_image = [[(15,103,255),(0,3,19)],[(22,200,1),(8,8,8)],
        [(0,0,0),(5,123,19)]]
        >>> encode(test_image, '')
        [[(14, 102, 254), (0, 2, 18)], [(22, 200, 0), (8, 8, 8)], 
        [(0, 0, 0), (4, 122, 18)]]
        >>> encode(test_image, 'hello')
        [[(14, 103, 255), (0, 3, 18)], [(22, 200, 0), (9, 9, 8)], 
        [(0, 1, 0), (5, 122, 19)]]
        >>> encode([], 'hello')
        []
    """
    bitstream = bits.message_to_bits(message)
    new_image = []
    i = 0
    # Set counter i to keep track of index location in bitstream
    # The ith bit is encoded
    for row in image:
        # First 'for' loop iterates over each row-list
        # Empty list intialised for each new row-list
        new_row = []
        # Nested 'for' loop iterates over each pixel in the current row-list
        # (r,g,b) matches r,g,b to the three intenstiy values in each pixel
        # respectively, so r = first intensity value (red), and so on.
        for (r,g,b) in row:
            # Use codebit function to set the LSB of the
            # new intensity values to match the bit being indexed 
            new_r = bits.set_bit(r,bits.codebit(i,bitstream),0)
            new_g = bits.set_bit(g,bits.codebit(i + 1,bitstream),0)
            new_b = bits.set_bit(b,bits.codebit(i + 2,bitstream),0)
            # Amalgamate the three new intensity values into a new pixel
            new_pixel = (new_r,new_g,new_b)
            # Append new pixel to new row-list
            new_row.append(new_pixel)
            # increment counter by 3, as each pixel has 3 intensity values
            i += 3
        # attach new row-list to new image-list
        new_image.append(new_row)
    return new_image

def decode(image):
    """
    Takes an image as its argument and returns a string of ASCII characters
    as its result.
    Decoding process:
    - Iterate over each intensity value in each pixel and do the following:
        - Convert intensity value of image to binary
        - Index LSB of intensity value and append it to a growing list
        of bits
    - After this operation, a string of bits is obtained, a part of which 
    (or all of it) is the bitstream of the coded message. 
    - Decode the entire string of bits using the bit_to_message function
    
    Inputs:
        image: a two-dimensional list of pixels, in zero-based row-major 
               order. Each pixel is a three element tuple of integers in the 
               range [0,255]
    
    Result:
        A string of ASCII characters, decoded from image using steganography 
        scheme described above.
    
    Examples:
        >>> decode(encode(test_image,''))
        ''
        >>> decode(encode(test_image,'hi'))
        'hi'
        >>> decode(encode(test_image,'hello'))
        'he'
    
    """
    bitstream = ''
    for row in image:
        for pixel in row:
            for intensity in pixel:
                # Use get_bit function from bits.py library
                # to select the LSB of each intensity value
                bitstream += bits.get_bit(intensity,0)
    # Decode message using bits_to_message function
    message = bits.bits_to_message(bitstream)
    return message  

def encode_ext(image, message, num_bits):
    """
    Essentially the same as the encode function, but:
    - in the original encode function, only the LSB was used to encode
    the message
    - in this function, an extra input, num_bits is introduced, which 
    controls how many bits per 8-bit chunk are used to encode the 
    message, up to using all 8 bits.
    
    Inputs:
        image: a two-dimensional list of pixels, in zero-based row-major order.
               Each pixel is a three element tuple of integers in the range
               [0,255].
        message: a string of ASCII characters
        num_bits: integer value between 1 and 8 inclusive,
                  which determines how many bits are used to encode
                  the message, starting with the LSB.
    
    Result:
        new_image: a new image in the same format as the original, with the 
        same dimensions, but with the message coded into the intenstiy values
        in each pixel. Number of bits used depends on value of num_bits.
    
    Examples:
        >>> encode_ext(test_image,'',4)
        [[(0, 96, 240), (0, 0, 16)], [(16, 192, 0), (0, 0, 0)], 
        [(0, 0, 0), (0, 112, 16)]]
        >>> encode_ext(test_image,'',8)
        [[(0, 0, 0), (0, 0, 0)], [(0, 0, 0), (0, 0, 0)], [(0, 0, 0), 
        (0, 0, 0)]]
        >>> encode_ext(test_image,'hello',4)
        [[(6, 97, 246), (10, 6, 19)], [(22, 195, 6), (15, 0, 0)], 
        [(0, 0, 0), (0, 112, 16)]]
        >>> encode_ext(test_image,'hello',8)
        [[(22, 166, 54), (54, 246, 0)], [(0, 0, 0), (0, 0, 0)],
        [(0, 0, 0), (0, 0, 0)]]
    
    """
    # Check num_bits is within accepted range
    if not(0 < num_bits <= 8):
        print ('Number of bits must be an integer between 1 and 8\
 inclusive')
        return None 
    bitstream = bits.message_to_bits(message)
    new_image = []
    i = 0
    for row in image:
        new_row = []
        for pixel in row:
            pre_pixel = []
            # Iterate over each intenstiy value in each pixel,
            # instead of iterating one pixel at a time
            for intensity in pixel:
                # need to set a seperate variable, as this may
                # be iterated over multiple times by next 'for'
                # loop
                new_i = intensity
                for pos in range(num_bits):
                    # bit position increases after each loop,
                    # until (num_bits -1) is reached 
                    new_i = bits.set_bit(new_i,bits.codebit(i,bitstream),pos)
                    # only need to increment by one, as we are now only
                    # setting one bit per loop
                    i += 1
                # append each intensity value to a list;
                # tuples cannot be used as they are immutable
                pre_pixel.append(new_i)
            # convert full pixel into three-element tuple
            new_pixel = (pre_pixel[0],pre_pixel[1],pre_pixel[2])
            new_row.append(new_pixel)
        new_image.append(new_row)
    return new_image

def decode_ext(image, num_bits):
    """
    Very slight change from original decode function;
    addition of extra nested 'for' loop allows iteration over
    one intensity value to extract multiple code bits, as 
    determined by num_bits input
    """
    if not(0 < num_bits <= 8):
        print ('Number of bits must be an integer between 1 and 8\
 inclusive')
        return None 
    bitstream = ''
    for row in image:
        for pixel in row:
            for intensity in pixel:
                # Extra 'for' loop so more than one bit can be
                # selected from each intensity value 
                for pos in range(num_bits):
                    bitstream += bits.get_bit(intensity,pos)
    message = bits.bits_to_message(bitstream)
    return message  


"""
TESTS
"""
# Image used for large-scall testing of program
# Uncomment only if 'floyd.png' exits in current directory
# floyd_image = read_image('floyd.png')

# Image used for small-scale testing of program
test_image = [[(15,103,255),(0,3,19)],
              [(22,200,1),(8,8,8)],
              [(0,0,0),(5,123,19)]]

def round_trip(message):
    """
    - Used to test bits_to_message and message_to_bits functions
    - Should always return True
    """
    return bits.bits_to_message(bits.message_to_bits(message)) == message


def encode_decode_test(image,message):
    """
    - Test only works if entire message can be coded into image
    - Use large images, e.g. 'floyd.png'
    - Given the above, should always return true
    """
    return decode(encode(image,message)) == message

def ext_test(image,message,num_bits):
    """
    - Test only works if entire message can be coded into image
    - Use large images, e.g. 'floyd.png'
    - Given the above, should always return true
    """
    return decode_ext(encode_ext(image,message,num_bits),num_bits)\
    == message

"""
Extra Stuff
"""

def encode_direct(image_name,message,num_bits,coded_image_name):
    image = sim.read_image(image_name)
    encoded_image = encode_ext(image,message,num_bits)
    sim.write_image(encoded_image, coded_image_name)
    return None

def decode_direct(image_name, num_bits):
    image = sim.read_image(image_name)
    message = decode_ext(image,num_bits)
    return message

def decode_to_file(image_name, num_bits, filename):
    image = sim.read_image(image_name)
    message = decode_ext(image, num_bits)
    file = open(filename,'w')
    file.write(message)
    file.close
    return message 

# function wrapper api for use in gui
def encodePILimage(PILimage, message):
    image = sim.to_rectangle(PILimage)
    output = encode(image, message)
    return sim.to_flat(output)

def decodePILimage(PILimage):
    image = sim.to_rectangle(PILimage)
    return decode(image)












































