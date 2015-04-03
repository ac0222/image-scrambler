################################################################################
#
# Description:
#
# This module implements various bit manipulation functions.
# The main purpose of the module is to help students of The University
# of Melbourne subject COMP10001 "Foundations of Computing" with their
# project for steganography. When working with characters we assume they
# are within the ASCII set, and will be encoded in exactly 8 bits, with
# zeros padding on the left where necessary.
#
# Authors:
#
# Bernie Pope (bjpope@unimelb.edu.au)
# Adrian Cheung
#
# Date created:
#
# 1 August 2013
#
# Date modified and reason:
#
# 10 Aug 2013: Generalised functions for setting bits to any bit in
#              an integer, not just the LSB.
# 13 Sep 2013: Update code for COMP10001 project 2, semester 2 2013.
#              Added comments.
#
# Updates by Adrian Cheung:
#
# 25 Feb 2014: Added extra functionality, i,e, converting a string of ASCII
#              characters into a string of binary, and vice versa
#
################################################################################

def char_to_bits(char):
    """char_to_bits(char) -> string

    Convert the input ASCII character to an 8 bit string of 1s and 0s.

    >>> char_to_bits('A')
    '01000001'
    """
    result = ''
    char_num = ord(char)
    for index in range(8):
        result = get_bit(char_num, index) + result
    return result

def bits_to_char(bits):
    """bits_to_char(bit_string) -> char
     
    Convert a string of bits (1s and 0s) into its corresponding integer value,
    and then convert that integer value to its corresponding ASCII character.

    The input bit_string should be non-empty, and must contain only the characters
    1 and 0.

    >>> bits_to_char('01000001')
    'A'
    """
    return chr(int(bits, 2))

def get_bit(int, position):
    """get_bit(int, position) -> bit

    Return the bit (as a character, '1' or '0') from a given position
    in a given integer (interpreted in base 2).

    The least significant bit is at position 0. The second-least significant
    bit is at position 1, and so forth.

    >>> for pos in range(8):
    ...     print(b.get_bit(167, pos))
    ... 
    1
    1
    1
    0
    0
    1
    0
    1
    """
    if int & (1 << position):
        return '1'
    else:
        return '0'

def set_bit_on(int, position):
    """set_bit_on(int, position) -> int

    Set the bit at a given position in a given integer to 1,
    regardless of its previous value, and return the new integer
    as the result.

    The least significant bit is at position 0. The second-least significant
    bit is at position 1, and so forth.

    >>> set_bit_on(0, 0)
    1
    >>> set_bit_on(0, 1)
    2
    >>> set_bit_on(167, 3)
    175
    """
    return int | (1 << position)

def set_bit_off(int, position):
    """set_bit_off(int, position) -> int

    Set the bit at a given position in a given integer to 0,
    regardless of its previous value, and return the new integer
    as the result.

    The least significant bit is at position 0. The second-least significant
    bit is at position 1, and so forth.

    >>> set_bit_off(0, 0)
    0
    >>> set_bit_off(1, 0)
    0
    >>> set_bit_off(167, 0)
    166
    >>> set_bit_off(175, 3)
    167
    """
    return int & ~(1 << position)

def set_bit(int, bit, position):
    """set_bit(int, bit, position) -> int

    Set the bit at a given position to the given bit (as a char, either
    '1' or '0') regardless of its previous value, and return the new integer
    as the result.

    The least significant bit is at position 0. The second-least significant
    bit is at position 1, and so forth.

    >>> set_bit(0, '1', 0)
    1
    >>> set_bit(0, '1', 1)
    2
    >>> set_bit(0, '1', 2)
    4
    >>> set_bit(0, '1', 3)
    8
    >>> set_bit(175, '0', 3)
    167
    >>> set_bit(175, '1', 3)
    175
    """

    if bit == '1':
        return set_bit_on(int, position)
    else:
        return set_bit_off(int, position)

def message_to_bits(message):
    """
    Takes a string of ASCII characters as its argument (message) and returns
    a STRING of binary digits ('1's or '0's) as its result.
     
    Inputs:
        message: The string of ASCII characters to be converted into binary
    
    Result:
        A string of binary digits, the 'bitstream'
    
    Examples:
        >>> message_to_bits('')
        ''
        >>> message_to_bits('A')
        '01000001'
        >>> message_to_bits('hello')
        '0110100001100101011011000110110001101111'
        >>> message_to_bits("\n!@%&'")
        '000010100010000101000000001001010010011000100111'
        
    """
    bitstream = ''
    # For loop to iterate over each character in message
    for char in message:
        # Apply char_to_bits function from bits.py library,
        # which converts a single character to its ASCII binary
        # representation.
        char_bits = char_to_bits(char)
        # Append each chunk to growing string of bits
        bitstream += char_bits
    return bitstream

def slicer(bits):
    """
    Takes a string of bits, splits it into 8-bit chunks, and
    returns a list containing each chunk as a seperate element
    as its result. If length of bit string is not divisible by 8,
    remainder is NOT added to list.
    
    Inputs:
        String of binary numbers
    
    Result:
        List of strings, with the first string being the first 8 
        bits of the input, the second string being the next 8, and
        so on.
    
    Examples:
        >>> slicer('')
        []
        >>> slicer('01000001')
        ['01000001']
        >>> slicer('010000')
        []
        >>> slicer('123456781234567812345678')
        ['12345678', '12345678', '12345678']
        >>> slicer('1234567812345678123456781234')
        ['12345678', '12345678', '12345678']
         
    """
    # Initialise variables
    chunk = ''
    chunk_list = []
    for bit in bits:
        chunk += bit
        # Build up chunk with bits from input until 
        # chunck length is 8
        if len(chunk) == 8:
            # Append this 8-bit chunk to the list, and
            # reset chunk to empty string, to build up
            # next chunk
            chunk_list.append(chunk)
            chunk = ''        
    # Return list of chunks
    return chunk_list

def bits_to_message(bitstream):
    """
    Takes a string of binary digits ('1's or '0's) as input and returns
    a string of ASCII chracters as its result. 
    Input string is processed 8 bits at a time, with each 8-bit chunk 
    being converted into its corresponding ASCII character. 
    Function stops processing input, and returns everything it has converted 
    so far as the result, when:
    - There are fewer than 8 bits left
    - It decodes a character with the ASCII code of 0 (i.e. 00000000, 
    starting at an index which is a multiple of 8). This sequence of bits 
    marks the end of the encoded message. The character 0 itself is not
    included in the result; it is used purely as a stop signal.
    
    Inputs:
        A string of binary bits
    
    Results:
        A string of ASCII characters
    
    Examples:
        >>> bits_to_message('')
        ''
        >>> bits_to_message('0100000')
        ''
        >>> bits_to_message('01000001')
        'A'
        >>> bits_to_message('011010000110010101')
        'he'
        >>> bits_to_message('01101000000000000110010101')
        'h'
        
    """
    # Split bit string into list containing 8-bit chunks,
    # using slicer function 
    chunk_list = slicer(bitstream)
    message = ''
    for chunk in chunk_list:
        if chunk == '00000000':
            # Stop code reached; function stops and returns
            # everything decoded so far
            return message
        else:
            # Use bits_to_char function to convert each
            # 8-bit chunk into its corresponding ASCII
            # character.
            char = bits_to_char(chunk)
            message += char
    return message

def codebit(i,indexable):
    """
    Takes an index and an indexable (list, string etc) as arguments.
    If index is within range of indexable, indexable is indexed
    at the value specified. 
    If index is out of range, the integer zero is returned.
    
    Inputs:
        Index; some POSITIVE integer value
        Indexable; an object which can be indexed such as a list or string
    
    Result:
        The value at the index specified; or, if index is out of range
        the integer value 0 is returned.
    
    Examples:
        >>> codebit(3,'123456789')
        '4'
        >>> codebit(11,'123456789')
        0
        >>> codebit(0,'')
        0
    """
    # Indexing is zero-based, hence the greater than or equal to sign
    if i >= len(indexable):
        return 0
    else:
        return indexable[i]
