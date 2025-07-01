# converter
# from txt to wav
# for laser310 color computer
# version 1
# by odorajbotoj

import sys
import struct
import wave

allowInput = list(" QWERTYUIOPASDFGHJKLZXCVBNM1234567890!\"#$%&'()@-=[]/?;+:*\\,<.>")

specialChars = {
    "{rd}": 0x8E,
    "{ld}": 0x8D,
    "{ru}": 0x8B,
    "{lu}": 0x87,
    "{d}": 0x8C,
    "{u}": 0x83,
    "{r}": 0x8A,
    "{l}": 0x85,
    "{ard}": 0x81,
    "{ald}": 0x82,
    "{aru}": 0x84,
    "{alu}": 0x88,
    "{ldru}": 0x89,
    "{lurd}": 0x86,
    "{aa}": 0x8F,
    "{a}": 0x80,
    "{arr}": 0xD1,
}
systemBasicDict = {
    "CLS": 0x84,
    "RUN": 0x8E,
    "VERIFY": 0x98,
    "CRUN": 0x9C,
    "LIST": 0xB4,
    "CLOAD": 0xB9,
    "CSAVE": 0xBA,
    "NEW": 0xBB,
}
processBasicDict = {
    "END": 0x80,
    "FOR": 0x81,
    "NEXT": 0x87,
    "GOTO": 0x8D,
    "IF": 0x8F,
    "GOSUB": 0x91,
    "RETURN": 0x92,
    "STOP": 0x94,
    "ELSE": 0x95,
    "CONT": 0xB3,
    "TO": 0xBD,
    "THEN": 0xCA,
    "STEP": 0xCC,
}
ioBasicDict = {
    "DATA": 0x88,
    "INPUT": 0x89,
    "READ": 0x8B,
    "RESTORE": 0x90,
    "OUT": 0xA0,
    "PRINT": 0xB2,
    "INP": 0xDB,
}
printerBasicDict = {"COPY": 0x96, "LPRINT": 0xAF, "LLIST": 0xB5}
memoryBasicDict = {"POKE": 0xB1, "CLEAR": 0xB8, "USR": 0xC1, "PEEK": 0xE5}
mediaBasicDict = {
    "RESET": 0x82,
    "SET": 0x83,
    "COLOR": 0x97,
    "MODE": 0x9D,
    "SOUND": 0x9E,
    "POINT": 0xC6,
}
variableBasicDict = {"DIM": 0x8A, "LET": 0x8C}
operatorBasicDict = {
    "NOT": 0xCB,
    "+": 0xCD,
    "-": 0xCE,
    "*": 0xCF,
    "/": 0xD0,
    "AND": 0xD2,
    "OR": 0xD3,
    ">": 0xD4,
    "=": 0xD5,
    "<": 0xD6,
    "'": 0xFB,
}
mathBasicDict = {
    "SGN": 0xD7,
    "INT": 0xD8,
    "ABS": 0xD9,
    "SQR": 0xDD,
    "RND": 0xDE,
    "LOG": 0xDF,
    "EXP": 0xE0,
    "COS": 0xE1,
    "SIN": 0xE2,
    "TAN": 0xE3,
    "ATN": 0xE4,
}
stringBasicDict = {
    "TAB(": 0xBC,
    "USING": 0xBF,
    "INKEY$": 0xC9,
    "LEN": 0xF3,
    "STR$": 0xF4,
    "VAL": 0xF5,
    "ASC": 0xF6,
    "CHR$": 0xF7,
    "LEFT$": 0xF8,
    "RIGHT$": 0xF9,
    "MID$": 0xFA,
}
blockedBasicDict = {
    "CMD": 0x85,
    "RANDOM": 0x86,
    "DEFINT": 0x99,
    "DEFSNG": 0x9A,
    "DEFDBL": 0x9B,
    "RESUME": 0x9F,
    "ON": 0xA1,
    "OPEN": 0xA2,
    "FIELD": 0xA3,
    "GET": 0xA4,
    "PUT": 0xA5,
    "CLOSE": 0xA6,
    "LOAD": 0xA7,
    "NAME": 0xA9,
    "KILL": 0xAA,
    "LSET": 0xAB,
    "RSET": 0xAC,
    "SAVE": 0xAD,
    "SYSTEM": 0xAE,
    "DEF": 0xB0,
    "DELETE": 0xB6,
    "AUTO": 0xB7,
    "FN": 0xBE,
    "VARPTR": 0xC0,
    "ERL": 0xC2,
    "ERR": 0xC3,
    "STRING$": 0xC4,
    "INSTR": 0xC5,
    "TIME": 0xC7,
    "MEM": 0xC8,
    "FRE": 0xDA,
    "POS": 0xDC,
    "CVI": 0xE6,
    "CVS": 0xE7,
    "CVD": 0xE8,
    "EOF": 0xE9,
    "LOC": 0xEA,
    "LOF": 0xEB,
    "MKI$": 0xEC,
    "MKS$": 0xED,
    "MKD$": 0xEE,
    "CINT": 0xEF,
    "CSNG": 0xF0,
    "CDBL": 0xF1,
    "FIX": 0xF2,
}
allBasicDict = {
    **specialChars,
    **systemBasicDict,
    **processBasicDict,
    **ioBasicDict,
    **printerBasicDict,
    **memoryBasicDict,
    **mediaBasicDict,
    **variableBasicDict,
    **operatorBasicDict,
    **mathBasicDict,
    **stringBasicDict,
    **blockedBasicDict,
}

if __name__ == "__main__":
    # check args
    if len(sys.argv) != 5:
        print("need TxtFile and Name and HexStartAddr and WavFile.")
        exit(1)
    file = sys.argv[1]
    name = sys.argv[2]
    startaddr = int(sys.argv[3], 16)
    wav = sys.argv[4]
    # check name
    if len(name) > 15:
        print("Name too long.")
        exit(1)
    elif name[0] not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        print("invalid first char in Name.")
        exit(1)
    else:
        nameCopy = name
        for i in list(specialChars.keys()):
            nameCopy = nameCopy.replace(i, "")
        for i in nameCopy:
            if i not in allowInput:
                print("invalid char {} in Name.".format(i))
                exit(1)
    # check startaddr
    if startaddr < 0x7AE9 or startaddr > 0xFFFF:
        print("invalid HexStartAddr.")
        exit(1)
    # convert begin
    bytesArrA = []
    bytesArrB = []
    # fill start
    for i in range(255):
        bytesArrA.append(0x80)
    for i in range(5):
        bytesArrA.append(0xFE)
    bytesArrA.append(0xF0)  # BASIC text file
    # fill name
    nameCopy = name
    for k, v in specialChars.items():
        nameCopy = nameCopy.replace(k, chr(v))
    for i in list(nameCopy):
        bytesArrA.append(ord(i))
    bytesArrA.append(0x00)
    # prepare for checksum
    checksum = 0
    # read input file
    fi = open(file, "r", encoding="utf-8")
    content = fi.read().split("\n")
    # generate program bin code
    basicBytes = []
    nowAddr = startaddr
    for line in content:
        line = line.strip()
        lineSplit = line.split(" ", 1)
        if len(lineSplit) != 2:
            continue
        lineNum = 0
        try:
            lineNum = int(lineSplit[0])
        except:
            print("invalid line number {}.".format(lineSplit[0]))
            exit(1)
        packedLineNum = struct.pack("<I", lineNum).hex()
        # generate header of a line
        bs = [0x00, 0x00, int(packedLineNum[:2], 16), int(packedLineNum[2:4], 16)]
        # fill the code
        lineSplit[1] = lineSplit[1].strip()
        if lineSplit[1].startswith("REM "):
            bs.append(0x93)  # REM is 0x93
            lineSplit[1] = lineSplit[1].removeprefix("REM")
            for k, v in specialChars.items():
                lineSplit[1] = lineSplit[1].replace(k, chr(v))
            for i in list(lineSplit[0]):
                if ord(i) < 0x80 and i not in allowInput:
                    print("invalid char {}.".format(i))
                    exit(1)
                bs.append(ord(i))
        else:
            blocks = lineSplit[1].split('"')
            for i in range(len(blocks)):
                if i % 2 == 0:
                    for k, v in allBasicDict.items():
                        blocks[i] = blocks[i].replace(k, chr(v))
                else:
                    for k, v in specialChars.items():
                        blocks[i] = blocks[i].replace(k, chr(v))
            lineContent = '"'.join(blocks)
            for i in list(lineContent):
                if ord(i) < 0x80 and i not in allowInput:
                    print("invalid char {}.".format(i))
                    exit(1)
                bs.append(ord(i))
        # add end
        bs.append(0x00)
        # compute address
        nowAddr += len(bs)
        addr = struct.pack("<I", nowAddr).hex()
        bs[0] = int(addr[:2], 16)
        bs[1] = int(addr[2:4], 16)
        # all in one
        basicBytes.extend(bs)
    basicBytes.extend([0x00, 0x00])
    # checksum
    for i in basicBytes:
        checksum += i
    # fill start and end address
    endAddr = startaddr + len(basicBytes)
    startAddrHex = struct.pack("<I", startaddr).hex()
    endAddrHex = struct.pack("<I", endAddr).hex()
    addrArr = [
        int(startAddrHex[:2], 16),
        int(startAddrHex[2:4], 16),
        int(endAddrHex[:2], 16),
        int(endAddrHex[2:4], 16),
    ]
    for i in addrArr:
        checksum += i
    bytesArrB.extend(addrArr)
    # fill code content
    bytesArrB.extend(basicBytes)
    # fill checksum
    checksumHex = struct.pack("<I", checksum).hex()
    bytesArrB.extend([int(checksumHex[:2], 16), int(checksumHex[2:4], 16)])
    with wave.open(wav, "w") as wavf:
        wavf.setnchannels(1)
        wavf.setsampwidth(1)
        wavf.setframerate(22050)
        wavf.writeframes(b"\x80" * 20)
        for data in bytesArrA:
            binaries = bin(data)[2:].zfill(8)
            for b in binaries:
                if b == "0":
                    wavf.writeframes(b"\xff" * 6)
                    wavf.writeframes(b"\x00" * 6)
                    wavf.writeframes(b"\xff" * 12)
                    wavf.writeframes(b"\x00" * 12)
                if b == "1":
                    wavf.writeframes(b"\xff" * 6)
                    wavf.writeframes(b"\x00" * 6)
                    wavf.writeframes(b"\xff" * 6)
                    wavf.writeframes(b"\x00" * 6)
                    wavf.writeframes(b"\xff" * 6)
                    wavf.writeframes(b"\x00" * 6)
        wavf.writeframes(b"\x00" * 58)  # magic space
        for data in bytesArrB:
            binaries = bin(data)[2:].zfill(8)
            for b in binaries:
                if b == "0":
                    wavf.writeframes(b"\xff" * 6)
                    wavf.writeframes(b"\x00" * 6)
                    wavf.writeframes(b"\xff" * 12)
                    wavf.writeframes(b"\x00" * 12)
                if b == "1":
                    wavf.writeframes(b"\xff" * 6)
                    wavf.writeframes(b"\x00" * 6)
                    wavf.writeframes(b"\xff" * 6)
                    wavf.writeframes(b"\x00" * 6)
                    wavf.writeframes(b"\xff" * 6)
                    wavf.writeframes(b"\x00" * 6)
        wavf.writeframes(b"\x80" * 20)
