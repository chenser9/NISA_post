import sys
import task as c
import random
from textwrap import wrap
from My_box import *

def from_48_to_56(key):
    key_list=['x']*56
    i=0
    key=list(key)
    for x in KEY_P2:
        key_list[x-1]=key[i]
        i=i+1
    string=''.join(key_list)
    return string

def unshift(key):
    block=['']*2
    block[1]=key
    rotate=[1]
    for i in range(0,-1,-1):
        block[i]=right_shift(block[i+1][:28],rotate[i])+right_shift(block[i+1][28:],rotate[i])
    return block[0]

def right_shift(key,d):
    return key[len(key)-d:] + key[0:len(key)-d]

def left_shift(key,d):
    return key[d:] + key[0:]

def unpermutation(s_output):
    s_final = ""
    for x in Inv_P:
        s_final += s_output[x-1]
    return s_final

def enc(plain_text):
    sh.recvuntil("Your plain_text (8 bytes, in hex):")
    sh.sendline(plain_text)
    return sh.recvuntil("\n")[:-1].decode()

def xor(a,b):
    tmp=""
    for i in range(len(a)):
        tmp+=chr(a[i]^b[i])
    return tmp

flagc='86721c7c1ebe2d0af8aa8e073073931b4a5ae6dcf03c784e3c70b5f8ce71cf9eb87f9b836eea0118'

cipher=bin(int('77a35598c47aeea6',16))[2:].rjust(64,'0')
c_iv=c.permutation(cipher)
c_iv=bytes.fromhex(hex(int(c_iv,2))[2:].rjust(16,'0'))
L=c_iv[:4]
R=c_iv[4:]

P=b'testtest'
P=bin(int(P.hex(),16))[2:].rjust(64,'0')
P_p=c.permutation(P)
P_l=bytes.fromhex(hex(int(P_p[:32],2))[2:])
P_r=P_p[32:]

t1= bin(int(xor(P_l,R).encode('latin1').hex(),16))[2:].rjust(32,'0')
t1_ivp=unpermutation(t1)
resualt=[]

for i in range(8):
    res=[]
    s_out=t1_ivp[4*i:4*i+4]
    s_out=int(s_out,2)
    for j in range(4):
        tmp=""
        if s_out in S[i][j]:
            hang=j
            lie=S[i][j].index(s_out)
            hang=bin(hang)[2:].rjust(2,'0')
            lie=bin(lie)[2:].rjust(4,'0')
            tmp=hang[0]+lie+hang[1]
            res.append(tmp)
    resualt.append(res)

P_e=c.expand(P_r)
KEY=[]
for i in range(8):
    ikey=[]
    m=P_e[6*i:6*i+6]
    for eres in resualt[i]:
        ekey=int(m,2)*int(eres,2)
        ikey.append(bin(ekey)[2:].rjust(6,'0'))
    KEY.append(ikey)

print(KEY)

def brute_force(keyfinal,PP,CC):
    temp=PP
    cipher=CC
    for x in range(2**8):
        digits=bin(x)[2:].rjust(8,'0')
        digits=list(digits)
        counter=0
        key=list(keyfinal)
        for i in range(56):
            if key[i] =='x':
                key[i]=digits[counter]
                counter=counter+1
        key_56=''.join(key)
        key_64=['0']*64
        i=0
        for u in KEY_P1:
            key_64[u-1]=key[i]
            i+=1
        key_64=''.join(key_64)
        key_64=hex(int(key_64,2))[2:].rjust(16,'0')

        if c.enc2(temp,key_64) == cipher:
            print("Find euql key!")
            print(key_64)
            flag = '86721c7c1ebe2d0af8aa8e073073931b4a5ae6dcf03c784e3c70b5f8ce71cf9eb87f9b836eea0118'
            print(c.dec(flag,key_64))
            exit()
    return

index=0
print(brute_force(unshift(from_48_to_56("010100010001000111100010110110001010011010001010")),b'testtest'.hex(),'77a35598c47aeea6'))

for aa in (KEY[0]):
    for bb in (KEY[1]):
        for cc in (KEY[2]):
            for dd in (KEY[3]):
                for ee in (KEY[4]):
                    for ff in (KEY[5]):
                        for gg in (KEY[6]):
                            for hh in (KEY[7]):
                                tmpkey=aa+bb+cc+dd+ee+ff+gg+hh
                                index+=1
                                brute_force(unshift(from_48_to_56(tmpkey)),b'testtest'.hex(),'77a35598c47aeea6')
                                if index %100==0:
                                    print(index)
if __name__=='__main__':
    flag=exp(HOST,PORT)
    assert flag==FLAG
    print("Pass!")

                        

            
