# coding=utf-8
import gmpy2

def ByteToHex(bins):
    return ''.join(["%02X" % x for x in bins]).strip()

def n2s(num):
    t = hex(num)[2:]
    if len(t) % 2 == 1:
        t = '0' + t
    return ''.join([chr(int(b, 16)) for b in [t[i:i + 2] for i in range(0, len(t), 2)]])

n = 0x00b0bee5e3e9e5a7e8d00b493355c618fc8c7d7d03b82e409951c182f398dee3104580e7ba70d383ae5311475656e8a964d380cb157f48c951adfa65db0b122ca40e42fa709189b719a4f0d746e2f6069baf11cebd650f14b93c977352fd13b1eea6d6e1da775502abff89d3a8b3615fd0db49b88a976bc20568489284e181f6f11e270891c8ef80017bad238e363039a458470f1749101bc29949d3a4f4038d463938851579c7525a69984f15b5667f34209b70eb261136947fa123e549dfff00601883afd936fe411e006e4e93d1a00b0fea541bbfc8c5186cb6220503a94b2413110d640c77ea54ba3220fc8f4cc6ce77151e29b3e06578c478bd1bebe04589ef9a197f6f806db8b3ecd826cad24f5324ccdec6e8fead2c2150068602c8dcdc59402ccac9424b790048ccdd9327068095efa010b7f196c74ba8c37b128f9e1411751633f78b7b9e56f71f77a1b4daad3fc54b5e7ef935d9a72fb176759765522b4bbc02e314d5c06b64d5054b7b096c601236e6ccf45b5e611c805d335dbab0c35d226cc208d8ce4736ba39a0354426fae006c7fe52d5267dcfb9c3884f51fddfdf4a9794bcfe0e1557113749e6c8ef421dba263aff68739ce00ed80fd0022ef92d3488f76deb62bdef7bea6026f22a1d25aa2a92d124414a8021fe0c174b9803e6bb5fad75e186a946a17280770f1243f4387446ccceb2222a965cc30b3929
e1 = 17
e2 = 65537
# gmpy2.gcdext(e1,e2)的运行结果为元组(mpz(1), mpz(30841), mpz(-8))，所以元组的第0个值不能取，第1个值才是s1，第2个值由于是负数，所以要取反，变为正数
# gcdext（a，b）返回一个3元素元组（g，s，t）
# g == gcd（a，b）最大公约数和g == a * s + b * t
s = gmpy2.gcdext(e1, e2)
s1 = s[1]
s2 = -s[2]
file1 = open("flag.enc1", 'rb').read()  # 这里的路径要自己修改
c1 = int(ByteToHex(file1), 16)
file2 = open("flag.enc2", 'rb').read()  # 这里的路径要自己修改
c2 = int(ByteToHex(file2), 16)
# 由于根据前面的运算，s1是正数，s2是负数，后面需要运算c2的s2次幂。因为在数论模运算中，要求一个数的负数次幂，与常规方法并不一样，比如此处要求c2的s2次幂，就要先计算c2的模反元素c2r，然后求c2r的-s2次幂。
c2 = gmpy2.invert(c2, n)
m = (pow(c1, s1, n) * pow(c2, s2, n)) % n
print(n2s(m))
