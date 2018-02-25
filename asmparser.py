#v1.0 asmparser by dogan can karatas

import sys,io,binascii

# TODO
# HEX SIKINTILI

def initialization():
    global nullchar,label,mnemonic,opcode,op1,op2,op3,comment,addr,count,undefined
    nullchar = ""
    label = []
    mnemonic = []
    opcode = []
    op1 = []
    op2 = []
    op3 = []
    comment = []

    addr = []
    count = []
    undefined = 0xa5

def parse_file(filename):
    fi = open(filename,"r")
    strlines = fi.read().splitlines()
    fi.close()
    return (len(strlines), strlines)

def check_instructions(codestr):
    mnemonicstr = codestr.split(" ")
    operands = codestr.split(",")
    if(len(mnemonicstr) == 1): #operand yok
        mnemonic = mnemonicstr[0].lstrip().rstrip()
        op1 = nullchar
        op2 = nullchar
        op3 = nullchar
    else:       # operand var 
        if(len(operands) == 1):
            op1 = mnemonicstr[1].split(",")[0]
            op2 = nullchar
            op3 = nullchar
        elif(len(operands) == 2):
            op1 = mnemonicstr[1].split(",")[0]
            op2 = operands[1]
            op3 = nullchar
        elif(len(operands) == 3):
            op1 = mnemonicstr[1].split(",")[0]
            op2 = operands[1]
            op3 = operands[2]
        else:
            op1 = mnemonicstr[1].split(",")[0]
            op2 = operands[1]
            op3 = operands[2]
        mnemonic = mnemonicstr[0].lstrip().rstrip()
    return (mnemonic,op1,op2,op3)

def parse(inputstr):
    labelarr = inputstr.split(":")
    if(len(labelarr) > 1):  #label varsa
        label = labelarr[0].rstrip()
        codecomment = labelarr[1]
        commentarr = codecomment.split(";")
        if(len(commentarr) > 1):    #label varsa comment varsa  1.durum
            comment = commentarr[1].lstrip()
            code = commentarr[0].lstrip().rstrip()
            (mnemonic,op1,op2,op3) = check_instructions(code)
        else:   #label varsa comment yoksa  2.durum
            comment = nullchar
            code = commentarr[0].lstrip().rstrip()
            (mnemonic,op1,op2,op3) = check_instructions(code)
    else:   #label yoksa
        label = nullchar
        codecomment = inputstr
        commentarr = codecomment.split(";")
        if(len(commentarr) > 1):    #label yoksa comment varsa  3.durum
            comment = commentarr[1].lstrip()
            code = commentarr[0].lstrip().rstrip()
            (mnemonic,op1,op2,op3) = check_instructions(code)
        else:       # hicbisey yoksa        4.durum
            comment = nullchar
            code = inputstr.lstrip().rstrip()
            (mnemonic,op1,op2,op3) = check_instructions(code)
    return (label,mnemonic,op1,op2,op3,comment)

def opcode_transform(mnemonic,op1,op2,op3):
    if(mnemonic.lower() == "nop"): # 1 byte
        return "0x"+("%0.2x"%(0x00)).upper()
    elif(mnemonic.lower() == "ret"): # 1 byte
        return "0x"+("%0.2x"%(0x22)).upper()
    elif(mnemonic.lower() == "reti"): # 1 byte
        return "0x"+("%0.2x"%(0x32)).upper()
    elif(mnemonic.lower() == "inc"): # 1 byte
        if(op1.lower() == "a"):
            return "0x"+("%0.2x"%(0x04)).upper()
        elif(op1.lower()[0:2].lower() == "0x"): # 2 byte
            opc = 0x05
            op1 = int(str(op1),16)
            opc = opc << 8
            return "0x"+("%0.4x"%(opc + op1)).upper()
        elif(op1.lower() == "@r0"): # 1 byte
            return "0x"+("%0.2x"%(0x06)).upper()
        elif(op1.lower() == "@r1"): # 1 byte
            return "0x"+("%0.2x"%(0x07)).upper()
        elif(op1.lower() == "r0"):  # 1 byte
            return "0x"+("%0.2x"%(0x08)).upper()
        elif(op1.lower() == "r1"):  # 1 byte
            return "0x"+("%0.2x"%(0x09)).upper()
        elif(op1.lower() == "r2"):  # 1 byte
            return "0x"+("%0.2x"%(0x0a)).upper()
        elif(op1.lower() == "r3"):  # 1 byte
            return "0x"+("%0.2x"%(0x0b)).upper()
        elif(op1.lower() == "r4"):  # 1 byte
            return "0x"+("%0.2x"%(0x0c)).upper()
        elif(op1.lower() == "r5"):  # 1 byte
            return "0x"+("%0.2x"%(0x0d)).upper()
        elif(op1.lower() == "r6"):  # 1 byte
            return "0x"+("%0.2x"%(0x0e)).upper()
        elif(op1.lower() == "r7"):  # 1 byte
            return "0x"+("%0.2x"%(0x0f)).upper()
        elif(op1.lower() == "dptr"):# 1 byte
            return "0x"+("%0.2x"%(0xa3)).upper()
        else:
            pass
    elif(mnemonic.lower() == "org"):# 1 byte
        addr.append(("%0.2x"%(int(op1,16))))
    else:
        pass

if __name__ == "__main__":
#while(True):
    initialization()
    print('asmparser - 8051 MODE - v0.1 \tdogan can karatas \t06.06.2016\n')
    print('line\topcode\tlabel\tinstrct\top1\top2\t[op3]\tcomment\n')
    (linecount,lines) = parse_file("test.asm")
    for i in range(linecount):
        (labelv,mnemonicv,op1v,op2v,op3v,commentv) = parse(lines[i])
        label.append(labelv)
        mnemonic.append(mnemonicv)
        op1.append(op1v)
        op2.append(op2v)
        op3.append(op3v)
        comment.append(commentv)

        # buradan sonra tum opcodelar belli.. opcode match ve islemler yapmaliyiz.
        # addr = org
        # memory map implementation
        # hex output
        # simulation controls...

        opcode.append(opcode_transform(mnemonic[i],op1[i],op2[i],op3[i]))
        print(str(i+1) + " \t["+ opcode[i] +"]\t" + label[i] + "\t" + mnemonic[i] + "\t" + op1[i] + " \t" + op2[i] + " \t" + op3[i] + " \t" + comment[i])

        #hex olusturma kismi:

    data = ""
    for kk in range(len(opcode)):
       data += opcode[kk][2:]

    data_parted = [data[i:i+32] for i in range(0, len(data), 32)] # bunda sikinti yok

    checksums = []
    
    for cs in range(len(data_parted)): #burada sikinti var
        checksums.append([data[i:i+2] for i in range(0, len(data), 2)])
    
    ''' burda cs degiskeni iterasyona girmiyor, ince bi olay var orda '''

    
    print "data: "
    print data
    print "data_parted: "
    print data_parted
    print "checksums: "
    print checksums

    checksum = []
    chk = 0

    '''
    for c in range(len(data_parted)):
        chk += int(data_parted[i],16)
    checksum.append(chk)
    '''
        
    count = []
    for s in range(len(data)):
        count.append(("%0.2x"%(len(data[s])/2)))

    print "count: "
    print count

    hexl = []
    for o in range(len(data)):
        hexl.append(count[o] + data[o])

    print "hex: "
    print hexl

        
    while(True):
        print("[S] STEP \t[R] RESET\t[X] EXIT")
        cmd = raw_input()
        if(cmd == "X" or cmd == "x"):
            break
        elif(cmd == "S" or cmd == "s"):
            print("stepmode")
        elif(cmd == "R" or cmd == "r"):
            print("resetmode")
        else:
            pass
        
