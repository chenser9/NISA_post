# from Crypto.Util.number import *
# import random
#
#
# def genPrime():
#     while True:
#         a = random.getrandbits(256)
#         b = random.getrandbits(256)
#
#         if b % 3 == 0:
#             continue
#
#         p = a ** 2 + 3 * b ** 2
#         if p.bit_length() == 512 and p % 3 == 1 and isPrime(p):
#             return p
#
#
# def add(P, Q, mod):
#     m, n = P
#     p, q = Q
#
#     if p is None:
#         return P
#     if m is None:
#         return Q
#
#     if n is None and q is None:
#         x = m * p % mod
#         y = (m + p) % mod
#         return (x, y)
#
#     if n is None and q is not None:
#         m, n, p, q = p, q, m, n
#
#     if q is None:
#         if (n + p) % mod != 0:
#             x = (m * p + 2) * inverse(n + p, mod) % mod
#             y = (m + n * p) * inverse(n + p, mod) % mod
#             return (x, y)
#         elif (m - n ** 2) % mod != 0:
#             x = (m * p + 2) * inverse(m - n ** 2, mod) % mod
#             return (x, None)
#         else:
#             return (None, None)
#     else:
#         if (m + p + n * q) % mod != 0:
#             x = (m * p + (n + q) * 2) * inverse(m + p + n * q, mod) % mod
#             y = (n * p + m * q + 2) * inverse(m + p + n * q, mod) % mod
#             return (x, y)
#         elif (n * p + m * q + 2) % mod != 0:
#             x = (m * p + (n + q) * 2) * inverse(n * p + m * q + 2, mod) % mod
#             return (x, None)
#         else:
#             return (None, None)
#
#
# def power(P, a, mod):
#     res = (None, None)
#     t = P
#     while a > 0:
#         if a % 2:
#             res = add(res, t, mod)
#         t = add(t, t, mod)
#         a >>= 1
#     return res
#
#
# def random_pad(msg, ln):
#     pad = bytes([random.getrandbits(8) for _ in range(ln - len(msg))])
#     return msg + pad
#
#
# p, q = genPrime(), genPrime()
# N = p * q
# phi = (p ** 2 + p + 1) * (q ** 2 + q + 1)
#
# print(f"N: {N}")
#
# d = getPrime(400)
# e = inverse(d, phi)
# k = (e * d - 1) // phi
#
# print(f"e: {e}")
#
# to_enc = input("> ").encode()
# ln = len(to_enc)
#
# print(f"Length: {ln}")
#
# pt1, pt2 = random_pad(to_enc[: ln // 2], 127), random_pad(to_enc[ln // 2 :], 127)
#
# M = (bytes_to_long(pt1), bytes_to_long(pt2))
# E = power(M, e, N)
#
# print(f"E: {E}")

from Crypto.Util.number import *

n = 144256630216944187431924086433849812983170198570608223980477643981288411926131676443308287340096924135462056948517281752227869929565308903867074862500573343002983355175153511114217974621808611898769986483079574834711126000758573854535492719555861644441486111787481991437034260519794550956436261351981910433997
e = 3707368479220744733571726540750753259445405727899482801808488969163282955043784626015661045208791445735104324971078077159704483273669299425140997283764223932182226369662807288034870448194924788578324330400316512624353654098480234449948104235411615925382583281250119023549314211844514770152528313431629816760072652712779256593182979385499602121142246388146708842518881888087812525877628088241817693653010042696818501996803568328076434256134092327939489753162277188254738521227525878768762350427661065365503303990620895441197813594863830379759714354078526269966835756517333300191015795169546996325254857519128137848289

P = PolynomialRing(Zmod(e), "k,s")
kk, ss = P.gens()
f = 1 + kk * (n ^ 2 + ss * (ss + n + 1) - n + 1)
load("~/workspace/coppersmith.sage")
k, s = small_roots(f, (2 ** 400, 2 ** 513), m=3, d=4)[0]  # take ~1min
k, s = ZZ(k), ZZ(s)
print(f"{k = }")
print(f"{s = }")

sol = solve(x ^ 2 - s * x + n, (x,))
p = ZZ(sol[0].rhs())
q = ZZ(sol[1].rhs())
print(f"{p = }")
print(f"{q = }")
assert p * q == n
d = inverse_mod(e, (p ^ 2 + p + 1) * (q ^ 2 + q + 1))
print(f"{d = }")

E = (
    123436198430194873732325455542939262925442894550254585187959633871500308906724541691939878155254576256828668497797665133666948295292931357138084736429120687210965244607624309318401630252879390876690703745923686523066858970889657405936739693579856446294147129278925763917931193355009144768735837045099705643710,
    47541273409968525787215157367345217799670962322365266620205138560673682435124261201490399745911107194221278578548027762350505803895402642361588218984675152068555850664489960683700557733290322575811666851008831807845676036420822212108895321189197516787046785751929952668898176501871898974249100844515501819117,
)


def add(P, Q, mod):
    m, n = P
    p, q = Q

    if p is None:
        return P
    if m is None:
        return Q

    if n is None and q is None:
        x = m * p % mod
        y = (m + p) % mod
        return (x, y)

    if n is None and q is not None:
        m, n, p, q = p, q, m, n

    if q is None:
        if (n + p) % mod != 0:
            x = (m * p + 2) * inverse_mod(n + p, mod) % mod
            y = (m + n * p) * inverse_mod(n + p, mod) % mod
            return (x, y)
        elif (m - n ** 2) % mod != 0:
            x = (m * p + 2) * inverse_mod(m - n ** 2, mod) % mod
            return (x, None)
        else:
            return (None, None)
    else:
        if (m + p + n * q) % mod != 0:
            x = (m * p + (n + q) * 2) * inverse_mod(m + p + n * q, mod) % mod
            y = (n * p + m * q + 2) * inverse_mod(m + p + n * q, mod) % mod
            return (x, y)
        elif (n * p + m * q + 2) % mod != 0:
            x = (m * p + (n + q) * 2) * inverse_mod(n * p + m * q + 2, mod) % mod
            return (x, None)
        else:
            return (None, None)


def power(P, a, mod):
    res = (None, None)
    t = P
    while a > 0:
        if a % 2:
            res = add(res, t, mod)
        t = add(t, t, mod)
        a >>= 1
    return res


a, b = power(E, d, n)
print(long_to_bytes(a))
print(long_to_bytes(b))

# pbctf{I_love_to_read_crypto_papers_and_implement_the_attacks_from_them}
