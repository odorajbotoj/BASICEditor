# BASIC Editor for LASER-310 by odorajbotoj
# version 1.0.2

import copy
import json
import struct
import tkinter
import tkinter.filedialog
import tkinter.messagebox
import tkinter.scrolledtext
import tkinter.simpledialog
import tkinter.ttk
import wave

allowInput = (
    " QWERTYUIOPASDFGHJKLZXCVBNM1234567890!\"#$%&'()@-=[]/?;+:*\\,<.>"
    "\u2580\u2584\u2588\u258C\u2590\u2596\u2597\u2598\u2599\u259A\u259B\u259C\u259D\u259E\u259F\u25A1"
)

allowNumInput = "QWERTYUIOPASDFGHJKLZXCVBNM1234567890().<>$%"

blockChrTransTable = {
    "\u2580": 0x8C,
    "\u2584": 0x83,
    "\u2588": 0x8F,
    "\u258C": 0x8A,
    "\u2590": 0x85,
    "\u2596": 0x82,
    "\u2597": 0x81,
    "\u2598": 0x88,
    "\u2599": 0x8B,
    "\u259A": 0x89,
    "\u259B": 0x8E,
    "\u259C": 0x8D,
    "\u259D": 0x84,
    "\u259E": 0x86,
    "\u259F": 0x87,
    "\u25A1": 0x80
}

systemBasicDict = {
    "CLS": 0x84,
    "RUN": 0x8E,
    "VERIFY": 0x98,
    "CRUN": 0x9C,
    "LIST": 0xB4,
    "CLOAD": 0xB9,
    "CSAVE": 0xBA,
    "NEW": 0xBB
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
    "STEP": 0xCC
}
ioBasicDict = {
    "DATA": 0x88,
    "INPUT": 0x89,
    "READ": 0x8B,
    "RESTORE": 0x90,
    "OUT": 0xA0,
    "PRINT": 0xB2,
    "INP": 0xDB
}
printerBasicDict = {
    "COPY": 0x96,
    "LPRINT": 0xAF,
    "LLIST": 0xB5
}
memoryBasicDict = {
    "POKE": 0xB1,
    "CLEAR": 0xB8,
    "USR": 0xC1,
    "PEEK": 0xE5
}
mediaBasicDict = {
    "RESET": 0x82,
    "SET": 0x83,
    "COLOR": 0x97,
    "MODE": 0x9D,
    "SOUND": 0x9E,
    "POINT": 0xC6
}
variableBasicDict = {
    "DIM": 0x8A,
    "LET": 0x8C
}
operatorBasicDict = {
    "NOT": 0xCB,
    "+": 0xCD,
    "-": 0xCE,
    "*": 0xCF,
    "/": 0xD0,
    "\u2191": 0xD1,
    "AND": 0xD2,
    "OR": 0xD3,
    ">": 0xD4,
    "=": 0xD5,
    "<": 0xD6,
    "'": 0xFB
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
    "ATN": 0xE4
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
    "\u2580": 0x00, # 8C
    "\u2584": 0x00, # 83
    "\u2588": 0x00, # 8F
    "\u258C": 0x00, # 8A
    "\u2590": 0x00, # 85
    "\u2596": 0x00, # 82
    "\u2597": 0x00, # 81
    "\u2598": 0x00, # 88
    "\u2599": 0x00, # 8B
    "\u259A": 0x00, # 89
    "\u259B": 0x00, # 8E
    "\u259C": 0x00, # 8D
    "\u259D": 0x00, # 84
    "\u259E": 0x00, # 86
    "\u259F": 0x00, # 87
    "\u25A1": 0x00 # 80
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
    "FIX": 0xF2
}
allBasicDict = {
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
    **blockedBasicDict
}
basicDicts = {
    "系统": systemBasicDict,
    "流程": processBasicDict,
    "输入输出": ioBasicDict,
    "打印机": printerBasicDict,
    "内存": memoryBasicDict,
    "媒体": mediaBasicDict,
    "变量": variableBasicDict,
    "运算符": operatorBasicDict,
    "数学": mathBasicDict,
    "字符串": stringBasicDict,
    "禁用": blockedBasicDict
}

# 创建窗口
root = tkinter.Tk()
root.title("BASIC Editor for LASER-310 v1.0.0 by odorajbotoj")
root.resizable(0, 0)

mainEntry = tkinter.StringVar()
lineNum = 0
lineInterval = tkinter.IntVar()
lineInterval.set(10)

fileVer = "1.0.0"

basicObj = {
    "fileVer": fileVer,
    "lineNum": 0,
    "lines": []
}
currentLineObj = {
    "lineNum": 0,
    "blocks": []
}

# 编辑区
editFrame = tkinter.LabelFrame(root, text="编辑")

basicFrame = tkinter.LabelFrame(editFrame, text="BASIC")
basicTextArea = tkinter.scrolledtext.ScrolledText(basicFrame, height=20, width=50, state="disabled")
basicTextArea.grid(row=0, column=0)
basicFrame.grid(row=0, column=0, rowspan=8)

def updateText():
    txt = ""
    for i in basicObj["lines"]:
        txt += str(i["lineNum"]) + " " + "".join(i["blocks"]) + "\n"
    txt += str(currentLineObj["lineNum"]) + " " + "".join(currentLineObj["blocks"]) + "\n"
    basicTextArea.configure(state="normal")
    basicTextArea.delete("1.0", tkinter.END)
    basicTextArea.insert("1.0", txt)
    basicTextArea.see(tkinter.END)
    basicTextArea.configure(state="disabled")

def entryDEL():
    txt = mainEntry.get()
    if len(txt) > 0:
        mainEntry.set(txt[:-1])

def checkEntry():
    for i in mainEntry.get():
        if i not in allowInput:
            tkinter.messagebox.showerror("不允许的字符", "不允许的字符：\n" + i)
            return False
    return True

def checkNumEntry():
    for i in mainEntry.get():
        if i not in allowNumInput:
            tkinter.messagebox.showerror("不允许的字符", "不允许的字符：\n" + i)
            return False
    return True

def insertREM():
    if checkEntry():
        basicObj["lineNum"] += lineInterval.get()
        txt = mainEntry.get()
        if len("{} REM \"{}\"".format(basicObj["lineNum"], txt)) > 60:
            tkinter.messagebox.showerror("超长", "行字符数 > 60")
            return
        basicObj["lines"].append({"lineNum": basicObj["lineNum"], "blocks": ["REM", " ", txt]})
        updateText()
        mainEntry.set("")

def insertRAW():
    if checkEntry():
        txt = mainEntry.get()
        if len("{} {}{}".format(basicObj["lineNum"] + lineInterval.get(), "".join(currentLineObj["blocks"]), txt)) > 60:
            tkinter.messagebox.showerror("超长", "行字符数 > 60")
            return
        currentLineObj["blocks"].append(txt)
        updateText()
        mainEntry.set("")

def insertSTR():
    if checkEntry():
        txt = mainEntry.get()
        if len("{} {} \"{}\"".format(basicObj["lineNum"] + lineInterval.get(), "".join(currentLineObj["blocks"]), txt)) > 60:
            tkinter.messagebox.showerror("超长", "行字符数 > 60")
            return
        currentLineObj["blocks"] += [" ", "\"" + txt + "\""]
        updateText()
        mainEntry.set("")

def insertNUM():
    if checkNumEntry():
        txt = mainEntry.get()
        if len("{} {}{}".format(basicObj["lineNum"] + lineInterval.get(), "".join(currentLineObj["blocks"]), txt)) > 60:
            tkinter.messagebox.showerror("超长", "行字符数 > 60")
            return
        currentLineObj["blocks"].append(txt)
        updateText()
        mainEntry.set("")

def insertSPACE():
    if len("{} {}".format(basicObj["lineNum"] + lineInterval.get(), "".join(currentLineObj["blocks"]))) > 59:
        tkinter.messagebox.showerror("超长", "行字符数 > 60")
        return
    currentLineObj["blocks"].append(" ")
    updateText()

def insertENTER(event=None):
    global basicObj, currentLineObj
    if basicObj["lineNum"] + lineInterval.get() > 65530:
        tkinter.messagebox.showerror("超长", "行号 > 65530")
        return
    basicObj["lineNum"] += lineInterval.get()
    currentLineObj["lineNum"] = basicObj["lineNum"]
    basicObj["lines"].append(copy.deepcopy(currentLineObj))
    currentLineObj["lineNum"] = 0
    currentLineObj["blocks"].clear()
    updateText()

def backspace():
    global currentLineObj
    if len(currentLineObj["blocks"]) > 0:
        poped = currentLineObj["blocks"].pop()
        if allBasicDict.get(poped) == None:
            mainEntry.set(poped)
    elif len(basicObj["lines"]) > 0:
        currentLineObj = basicObj["lines"].pop()
        if len(basicObj["lines"]) > 0:
            basicObj["lineNum"] = basicObj["lines"][-1]["lineNum"]
        else:
            basicObj["lineNum"] = 0
        currentLineObj["lineNum"] = 0
    updateText()

def buttonClick(name):
    kval = allBasicDict.get(name)
    if kval == None:
        return
    elif kval == 0x00:
        mainEntry.set(mainEntry.get() + name)
        return
    else:
        currentLineObj["blocks"].append(name)
        updateText()
        return

tkinter.Scale(editFrame, from_=1, to=20, resolution=1,
              variable=lineInterval, label="行间隔",
              orient="horizontal", length=500).grid(row=0, column=1, columnspan=6)

tkinter.Entry(editFrame, textvariable=mainEntry, width=30).grid(row=1, column=1)
tkinter.Button(editFrame, text="DEL", command=entryDEL).grid(row=1, column=2)
tkinter.Button(editFrame, text="REM", command=insertREM).grid(row=1, column=3)
tkinter.Button(editFrame, text="RAW", command=insertRAW).grid(row=1, column=4)
tkinter.Button(editFrame, text="STR", command=insertSTR).grid(row=1, column=5)
tkinter.Button(editFrame, text="NUM", command=insertNUM).grid(row=1, column=6)

tkinter.Button(editFrame, text="SPACE", command=insertSPACE).grid(row=2, column=1, columnspan=2)
tkinter.Button(editFrame, text="ENTER", command=insertENTER).grid(row=2, column=3, columnspan=2)
tkinter.Button(editFrame, text="BACKSPACE", command=backspace).grid(row=2, column=5, columnspan=2)
root.bind("<Return>", insertENTER)

notebook = tkinter.ttk.Notebook(editFrame)
notebook.grid(row=3, column=1, rowspan=5, columnspan=6)

for k1 in basicDicts:
    fr = tkinter.Frame(editFrame)
    ks = list(basicDicts[k1].keys())
    for i in range(len(ks)):
        tkinter.Button(fr, text=ks[i], command=lambda arg=ks[i]:buttonClick(arg)).grid(row=i//6, column=i%6)
    notebook.add(fr, text=k1)

editFrame.grid(row=1, column=0)

def openFile():
    global basicObj, fileVer
    filename = tkinter.filedialog.askopenfilename(title="打开", initialfile="basic_code.json")
    if filename == "":
        return
    backup = {}
    with open(filename, "r", encoding="utf-8") as f:
        backup = json.loads(f.read())
    if fileVer != backup["fileVer"]:
        tkinter.messagebox.showerror("错误", "数据版本不匹配")
        return
    basicObj = copy.deepcopy(backup)
    updateText()

def saveFile():
    filename = tkinter.filedialog.asksaveasfilename(title="保存", initialfile="basic_code.json")
    if filename == "":
        return
    with open(filename, "w", encoding="utf-8") as f:
        f.write(json.dumps(basicObj))

def checkName(name):
    if len(name) > 15:
        return False
    else:
        for i in name:
            if i not in allowInput:
                return False
    return True

def exportWAV():
    global basicObj
    basicName = tkinter.simpledialog.askstring("输入程序名", "请输入程序名\n15个以内合法字符")
    if basicName == "":
        return
    if not checkName(basicName):
        tkinter.messagebox.showerror("错误", "不合法的程序名")
        return
    bytesArrA = []
    bytesArrB = []
    # 填充开头
    for i in range(255):
        bytesArrA.append(0x80)
    for i in range(5):
        bytesArrA.append(0xFE)
    bytesArrA.append(0xF0) # BASIC text file
    # 填程序名
    for i in basicName:
        geti = blockChrTransTable.get(i)
        if geti == None:
            bytesArrA.append(ord(i))
        else:
            bytesArrA.append(geti)
    bytesArrA.append(0x00)
    # 问开始地址
    startAddr = tkinter.simpledialog.askinteger(title="输入起始地址", prompt="请输入程序起始地址\n默认 0x7AE9", initialvalue=0x7AE9, minvalue=0x7AE9, maxvalue=0xFFFF)
    if startAddr == 0:
        return
    # 准备校验
    checksum = 0
    # 生成程序字节码
    basicBytes = []
    nowAddr = startAddr
    for line in basicObj["lines"]:
        packedLineNum = struct.pack("<I", line["lineNum"]).hex()
        # 生成头
        bs = [0x00, 0x00, int(packedLineNum[:2], 16), int(packedLineNum[2:4], 16)]
        # 填充程序
        if line["blocks"][0] == "REM":
            bs.append(allBasicDict.get("REM"))
            for block in line["blocks"][1:]:
                for i in block:
                    get2 = blockChrTransTable.get(i)
                    if get2 != None:
                        bs.append(get2)
                    else:
                        bs.append(ord(i))
        else:
            for block in line["blocks"]:
                get1 = allBasicDict.get(block)
                if get1 != None:
                    bs.append(get1)
                else:
                    for i in block:
                        get2 = blockChrTransTable.get(i)
                        if get2 != None:
                            bs.append(get2)
                        else:
                            bs.append(ord(i))
        # 添加尾
        bs.append(0x00)
        # 计算地址偏移
        nowAddr += len(bs)
        addr = struct.pack("<I", nowAddr).hex()
        bs[0] = int(addr[:2], 16)
        bs[1] = int(addr[2:4], 16)
        # 合并
        basicBytes.extend(bs)
    basicBytes.extend([0x00, 0x00])
    # 计算校验
    for i in basicBytes:
        checksum += i
    # 填始末地址
    endAddr = startAddr + len(basicBytes)
    startAddrHex = struct.pack("<I", startAddr).hex()
    endAddrHex = struct.pack("<I", endAddr).hex()
    addrArr = [int(startAddrHex[:2], 16), int(startAddrHex[2:4], 16), int(endAddrHex[:2], 16), int(endAddrHex[2:4], 16)]
    for i in addrArr:
        checksum += i
    bytesArrB.extend(addrArr)
    # 填程序段
    bytesArrB.extend(basicBytes)
    # 填校验和
    checksumHex = struct.pack("<I", checksum).hex()
    bytesArrB.extend([int(checksumHex[:2], 16), int(checksumHex[2:4], 16)])
    # 填结束段
    #for i in range(20):
    #    bytesArrB.append(0x00)
    # DEBUG
    #print(bytesArr)
    #print(len(basicBytes), basicBytes)
    #print(len(addrArr), addrArr)
    #print(checksum, checksumHex)
    # 生成wav
    filename = tkinter.filedialog.asksaveasfilename(title="保存", initialfile="basic_code.wav")
    if filename == "":
        return
    with wave.open(filename, "w") as wavf:
        wavf.setnchannels(1)
        wavf.setsampwidth(1)
        wavf.setframerate(22050)
        wavf.writeframes(b"\x80" * 20)
        for data in bytesArrA:
            binaries = bin(data)[2:].zfill(8)
            for b in binaries:
                if b == "0":
                    wavf.writeframes(b"\xFF" * 6)
                    wavf.writeframes(b"\x00" * 6)
                    wavf.writeframes(b"\xFF" * 12)
                    wavf.writeframes(b"\x00" * 12)
                if b == "1":
                    wavf.writeframes(b"\xFF" * 6)
                    wavf.writeframes(b"\x00" * 6)
                    wavf.writeframes(b"\xFF" * 6)
                    wavf.writeframes(b"\x00" * 6)
                    wavf.writeframes(b"\xFF" * 6)
                    wavf.writeframes(b"\x00" * 6)
        wavf.writeframes(b"\x00" * 58) # magic space
        for data in bytesArrB:
            binaries = bin(data)[2:].zfill(8)
            for b in binaries:
                if b == "0":
                    wavf.writeframes(b"\xFF" * 6)
                    wavf.writeframes(b"\x00" * 6)
                    wavf.writeframes(b"\xFF" * 12)
                    wavf.writeframes(b"\x00" * 12)
                if b == "1":
                    wavf.writeframes(b"\xFF" * 6)
                    wavf.writeframes(b"\x00" * 6)
                    wavf.writeframes(b"\xFF" * 6)
                    wavf.writeframes(b"\x00" * 6)
                    wavf.writeframes(b"\xFF" * 6)
                    wavf.writeframes(b"\x00" * 6)
        wavf.writeframes(b"\x80" * 20)
    tkinter.messagebox.showinfo("成功", "成功保存到 wav 文件")

# 文件操作区
fileActionFrame = tkinter.LabelFrame(root, text="文件操作")
tkinter.Button(fileActionFrame, text="打开文件", command=openFile).grid(row=0, column=0)
tkinter.Button(fileActionFrame, text="保存文件", command=saveFile).grid(row=0, column=1)
tkinter.Button(fileActionFrame, text="导出WAV", command=exportWAV).grid(row=0, column=2)
fileActionFrame.grid(row=0, column=0)

# 窗口事件循环
root.mainloop()
