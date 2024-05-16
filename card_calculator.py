#!/usr/bin/python3
# Usage: python3 card_calculator.py iclass 214 1236 26
# Updated: 5/16/2024

import sys

def bitCount(int_type):
    # return number 1's in a number when represented as binary
    count = 0
    while (int_type):
        int_type &= int_type - 1
        count += 1
    return (count)


def generate26bitIndala(facilityCode, cardCode, cardType, preamble):
    # generates a hex code for Indala 26 bit format card
    # Indala Format
    # B31  B30    B29   B28  B27  B26   B25   B24  B23  B22  B21  B20  B19  B18  B17  B16  B15  B14  B13  B12  B11  B10  B9    B8   B7  B6  B5  B4  B3  B2  B1  B0
    # 1    C6    P-Odd  C9   C10  C5   P-Odd  F1   C12  C0   C15  C13  F5   C14  C7   F4   F3   F6   C1   C8   C11  F2   C4  P-Odd  C3  F7  F0  C2  0   0   0   1

    # set bits 31,3,2,1
    cardData = 0x80000001

    # set bit 4
    if (2**2 & cardCode):
        cardData = 2**4 ^ cardData

    # set bit 5
    if (2**0 & facilityCode):
        cardData = 2**5 ^ cardData

    # set bit 6
    if (2**7 & facilityCode):
        cardData = 2**6 ^ cardData

    # set bit 7
    if (2**3 & cardCode):
        cardData = 2**7 ^ cardData

    # set bit 9
    if (2**4 & cardCode):
        cardData = 2**9 ^ cardData

    # set bit 10
    if (2**2 & facilityCode):
        cardData = 2**10 ^ cardData

    # set bit 11
    if (2**11 & cardCode):
        cardData = 2**11 ^ cardData

    # set bit 12
    if (2**8 & cardCode):
        cardData = 2**12 ^ cardData

    # set bit 13
    if (2**1 & cardCode):
        cardData = 2**13 ^ cardData

    # set bit 14
    if (2**6 & facilityCode):
        cardData = 2**14 ^ cardData

    # set bit 15
    if (2**3 & facilityCode):
        cardData = 2**15 ^ cardData

    # set bit 16
    if (2**4 & facilityCode):
        cardData = 2**16 ^ cardData

    # set bit 17
    if (2**7 & cardCode):
        cardData = 2**17 ^ cardData

    # set bit 18
    if (2**14 & cardCode):
        cardData = 2**18 ^ cardData

    # set bit 19
    if (2**5 & facilityCode):
        cardData = 2**19 ^ cardData

    # set bit 20
    if (2**13 & cardCode):
        cardData = 2**20 ^ cardData

    # set bit 21
    if (2**15 & cardCode):
        cardData = 2**21 ^ cardData

    # set bit 22
    if (2**0 & cardCode):
        cardData = 2**22 ^ cardData

    # set bit 23
    if (2**12 & cardCode):
        cardData = 2**23 ^ cardData

    # set bit 24
    if (2**1 & facilityCode):
        cardData = 2**24 ^ cardData

    # set bit 26
    if (2**5 & cardCode):
        cardData = 2**26 ^ cardData

    # set bit 27
    if (2**10 & cardCode):
        cardData = 2**27 ^ cardData

    # set bit 28
    if (2**9 & cardCode):
        cardData = 2**28 ^ cardData

    # set bit 30
    if (2**6 & cardCode):
        cardData = 2**30 ^ cardData

    # set even parity bit (8, 25, or 29)
    # set two bits if bitcount is odd
    if (bitCount(cardData) & 1):
        cardData = 2**29 ^ cardData
        cardData = 2**25 ^ cardData
    # set all three bits if bitcount is even
    else:
        cardData = 2**29 ^ cardData
        cardData = 2**25 ^ cardData
        cardData = 2**8 ^ cardData

    print("")
    print("Write the following to an Indala (T55x7) card:")
    cardData = cardData | preamble
    return "%08x" % cardData


def generate35bitHex(facilityCode, cardCode, cardType, preamble):
    # generates a hex code for HID 35 bit format card
    # see this page to understand formats:
    # http://www.pagemac.com/azure/data_formats.php
    cardData = (facilityCode << 21) + (cardCode << 1)
    # 2nd MSB even parity
    parity1 = bitCount(cardData & 0x1B6DB6DB6) & 1
    # add the parity bit (we need it for further parity calculations)
    cardData += (parity1 << 33)
    # MSB odd parity is the LSB
    parity2 = bitCount(cardData & 0x36DB6DB6C) & 1 ^ 1
    cardData += parity2  # add the parity bit
    # LSB odd parity (covers all 34 other bits)
    parity3 = bitCount(cardData) & 1 ^ 1
    cardData += (parity3 << 34)  # add the parity bit
    print("")
    if cardType == "prox":
        print("Write the following to a PROX (T55x7) card:")
        cardData = cardData | preamble
        print("%010x" % cardData)
    elif cardType == "iclass":
        # adjust preamble for encrypting with Proxmark3
        preamble = preamble ^ 0x2000000000
        cardData = cardData | preamble
        print("Write the following values to an iCLASS 2k card:")
        print("hf iclass wrbl --blk 6 -d 030303030003E014 --ki 0")
        print(f"hf iclass wrbl --blk 7 -d {cardData:016x} --ki 0")
        print("hf iclass wrbl --blk 8 -d 0000000000000000 --ki 0")
        print("hf iclass wrbl --blk 9 -d 0000000000000000 --ki 0")
    return ""


def generate26bitHex(facilityCode, cardCode, cardType, preamble):
    # generates a hex code for HID 26 bit format card
    # see this page to understand formats:
    # http://www.pagemac.com/azure/data_formats.php
    cardData = (facilityCode << 17) + (cardCode << 1)
    # MSB even parity (covers 12 MSB)
    parity1 = bitCount(cardData & 0x1FFE000) & 1
    # LSB odd parity (covers 12 LSB)
    parity2 = bitCount(cardData & 0x0001FFE) & 1 ^ 1
    cardData += (parity1 << 25) + (parity2)
    print("")
    if cardType == "prox":
        print("Write the following to a PROX (T55x7) card:")
        cardData = cardData | preamble
        print("%010x" % cardData)
    elif cardType == "iclass":
        # adjust preamble for encrypting with Proxmark3
        preamble = preamble ^ 0x2000000000
        cardData = cardData | preamble
        print("Write the following values to an iCLASS 2k card:")
        print("hf iclass wrbl --blk 6 -d 030303030003E014 --ki 0")
        print(f"hf iclass wrbl --blk 7 -d {cardData:016x} --ki 0")
        print("hf iclass wrbl --blk 8 -d 0000000000000000 --ki 0")
        print("hf iclass wrbl --blk 9 -d 0000000000000000 --ki 0")
    return ""


def main():
    if len(sys.argv) != 5:
        print("")
        print("Usage: " +
              sys.argv[0] + " <indala || prox || iclass> <FC> <CC> <26 || 35>")
    else:
        cardType = sys.argv[1]
        facilityCode = int(sys.argv[2])
        cardCode = int(sys.argv[3])
        if sys.argv[1] == "indala":
            preamble = 0xA000000000000000
            print(generate26bitIndala(facilityCode, cardCode, cardType, preamble))
        elif sys.argv[4] == "26":
            preamble = 0x2004000000
            print(generate26bitHex(facilityCode, cardCode, cardType, preamble))
        elif sys.argv[4] == "35":
            preamble = 0x2800000000
            print(generate35bitHex(facilityCode, cardCode, cardType, preamble))


if __name__ == "__main__":
    main()
