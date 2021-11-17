from Crypto.Util.number import *
from tqdm import tqdm
from sage.all import *

def inthroot(a, n):
    if a < 0:
        return 0
    return a.nth_root(n, truncate_mode=True)[0]

def solve(n, phi):
    tot = n - phi + 1
    dif = inthroot(Integer(tot * tot - 4 * n), 2)
    dif = int(dif)
    p = (tot + dif) // 2
    q = (tot - dif) // 2
    if p * q == n:
        return p, q
    return None, None

e = 77493305850606946966866586869701562747566137421194857276849326558383863716599
n_1 = 38214712801044280452242029022307023900010505700133304226967361821658293768459754887223522190673421124166486124464596635967747405359806642464884601455285823454970604600165907209542618963333642882524596571019916658676095313436156240684679902251615046617153094607425987125749225956361360222801251450373042579071
n_2 = 11918534754165556595562303500191427316052163288557481525821438608864207524482981704928088272082867228651327063972728644192877335261376841505970220897803876176646736511250339814035116162036800063521023303060582016775080988747746487028664050144843952770605999675734459531886474293242344088869877433555271258269
enc_1 = 15808757304442558489652709164051631267713593320560967145595438513675108079906680505924179038743563463272753097766933667737349956243897214853643343110837736923623483907392474855188388096345292952323482631367759757699216716624973244377786699291503949070419765404840454938181818882998235566160193218211345167102
enc_2 = 6376686158682997059741103218078544724010800198504747162290763103690338182777916072489234933936183210135919268370502287963945937266836059808775864844630371956704383598114953698187649635431791980376016420776898290168916806683089572655387949425292390749405301644222442142567586889975355029412203353803624681004

c = continued_fraction(Integer(n_2) / Integer(n_1))

for i in tqdm(range(1, 150)):
    k = c.numerator(i)
    x = c.denominator(i)
    if GCD(e, k) != 1:
        continue
    res = inverse(e - k, e)
    cc = crt(res, 0, e, x)
    md = e * x // GCD(e, x)

    st = cc + (n_1 // md) * md - 100 * md
    for j in range(200):
        if GCD(e, st) != 1:
            st += md
            continue
        d_1 = inverse(e, st)
        flag = long_to_bytes(int(pow(enc_1, d_1, n_1)))
        if "flag" in str(flag):
            print(flag)
        st += md