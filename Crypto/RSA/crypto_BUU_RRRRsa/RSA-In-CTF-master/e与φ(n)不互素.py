''''
('n1=', '0xbf510b8e2b169fbce366eb15a4f6c71b370f02f2108c7feb482234a386185bce1a740fa6498e04edbdf2a639e320619d9f39d3e740ebaf578af0426bc3e851001a1d599108a08725347f6680a7f5581a32d91505023701872c3df723e8de9f201d3b17059bebff944b915045870d757eb6d6d009eb4561cc7e4b89968e4433a9L')
('e1=', '0x15d6439c6')
('c1=', '0x43e5cc4c99c3040aef2ccb0d4c45266f6b75cd7f9f1be105766689283f0886061c9cd52ac2b2b6c1b7d250c2079f354ca9b988db5556336201f3b5e489916b3b60b80c34bef8f608d7471fafaf14bee421b60630f42c5cc813356e786ff10e5efa334b8a73b7ea06afa6043f33be6a31010d306ba60516243add65c183da843aL')
('n2=', '0xba85d38d1bfc3fb281927c9246b5b771ac3344ca9fe1c2d9c793a886bffb5c84558f4a578cd5ba9e777a4e08f66d0cabe05b9aa2ae8d075778b5fbfff318a7f9b6f22e2eff6f79d8c1148941b3974f3e83a4a4f1520ad42336eddc572ec7ea04766eb798b2f1b1b52009b3eeea7741b2c55e3c7c11c5cf6a4e204c6b0d312f49L')
('e2=', '0x2c09848c6')
('c2=', '0x79ec6350649377f69b475eca83a7d9d5356a1d62e29933e9c8e2b19b4b23626a581037aba3be6d7f73d5bed049350e41c1ed4cdc3e10ee34ec576ef3449be2f7d930c759612e1c23c4db71d0e5185a80b548031e3857dd93eca4af017fcd25895fcc4e8a2b36c1dd36b8cd9cc9200e2879f025928fe346e2cfae5200e66de6ccL')
'''

# -*- coding:utf-8 -*-
import gmpy2
import binascii


def gcd(a, b):
    if a < b:
        a, b = b, a
    while b != 0:
        temp = a % b
        a = b
        b = temp
    return a

n1=0xbf510b8e2b169fbce366eb15a4f6c71b370f02f2108c7feb482234a386185bce1a740fa6498e04edbdf2a639e320619d9f39d3e740ebaf578af0426bc3e851001a1d599108a08725347f6680a7f5581a32d91505023701872c3df723e8de9f201d3b17059bebff944b915045870d757eb6d6d009eb4561cc7e4b89968e4433a9
n2=0xba85d38d1bfc3fb281927c9246b5b771ac3344ca9fe1c2d9c793a886bffb5c84558f4a578cd5ba9e777a4e08f66d0cabe05b9aa2ae8d075778b5fbfff318a7f9b6f22e2eff6f79d8c1148941b3974f3e83a4a4f1520ad42336eddc572ec7ea04766eb798b2f1b1b52009b3eeea7741b2c55e3c7c11c5cf6a4e204c6b0d312f49

p=gcd(n1,n2)
q1=n1//p
q2=n2//p



c1=0x43e5cc4c99c3040aef2ccb0d4c45266f6b75cd7f9f1be105766689283f0886061c9cd52ac2b2b6c1b7d250c2079f354ca9b988db5556336201f3b5e489916b3b60b80c34bef8f608d7471fafaf14bee421b60630f42c5cc813356e786ff10e5efa334b8a73b7ea06afa6043f33be6a31010d306ba60516243add65c183da843a
c2=0x79ec6350649377f69b475eca83a7d9d5356a1d62e29933e9c8e2b19b4b23626a581037aba3be6d7f73d5bed049350e41c1ed4cdc3e10ee34ec576ef3449be2f7d930c759612e1c23c4db71d0e5185a80b548031e3857dd93eca4af017fcd25895fcc4e8a2b36c1dd36b8cd9cc9200e2879f025928fe346e2cfae5200e66de6cc
e1 =0x15d6439c6
e2 =0x2c09848c6

#print(gcd(e1,(p-1)*(q1-1)))
#print(gcd(e2,(p-1)*(q2-1)))


e1=e1//gcd(e1,(p-1)*(q1-1))
e2=e2//gcd(e2,(p-1)*(q2-1))


phi1=(p-1)*(q1-1);phi2=(p-1)*(q2-1)
d1=gmpy2.invert(e1,phi1)
d2=gmpy2.invert(e2,phi2)
f1=pow(c1,d1,n1)
f2=pow(c2,d2,n2)


def GCRT(mi, ai):
    curm, cura = mi[0], ai[0]
    for (m, a) in zip(mi[1:], ai[1:]):
        d = gmpy2.gcd(curm, m)
        c = a - cura
        K = c // d * gmpy2.invert(curm // d, m // d)
        cura += curm * K
        curm = curm * m // d
        cura %= curm
    return (cura % curm, curm)


f3,lcm = GCRT([n1,n2],[f1,f2])
n3=q1*q2
c3=f3%n3
phi3=(q1-1)*(q2-1)

d3=gmpy2.invert(39929,phi3)#39929是79858//gcd((q1-1)*(q2-1),79858) 因为新的e和φ(n)还是有公因数2
m3=pow(c3,d3,n3)

if gmpy2.iroot(m3,2)[1] == 1:
    flag=gmpy2.iroot(m3,2)[0]
    print(binascii.unhexlify(hex(flag)[2:].strip("L")))