import secrets
import random
import time
from math import gcd, lcm



def multiplicative_inverse(a, m):
    if gcd(a, m) != 1:
        return None  # The modular inverse doesn't exist
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (
            u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m


class rsa:
    def __gen_rsa_primes(self, bit_length):
        def is_prime(number, k=5):
            """
            Miller-Rabin primality test.
            Returns True if `number` is likely to be prime, False otherwise.
            The parameter `k` determines the accuracy of the test.
            """
            if number == 2 or number == 3:
                return True
            if number < 2 or number % 2 == 0:
                return False

            # Write (number - 1) as 2^r * d
            r, d = 0, number - 1
            while d % 2 == 0:
                r += 1
                d //= 2

            # Perform the Miller-Rabin test `k` times
            for _ in range(k):
                a = random.randint(2, number - 2)
                x = pow(a, d, number)
                if x == 1 or x == number - 1:
                    continue
                for _ in range(r - 1):
                    x = pow(x, 2, number)
                    if x == number - 1:
                        break
                else:
                    return False
            return True

        while True:
            number = secrets.randbits(bit_length)
            # Set the highest and lowest bits
            number |= (1 << bit_length - 1) | 1
            if is_prime(number):
                return number

    def generate_keys(self, bit_length):

        p = self.__gen_rsa_primes(bit_length)
        q = self.__gen_rsa_primes(bit_length)

        # p = 61
        # q = 53
        # print(len(str(p)), len(str(q)))

        n = p * q
        # print(n)
        # print(len(str(n)))

        phi = lcm((p - 1), (q - 1))
        # print(phi)
        # print(len(str(phi)))

        # Find e such that 1 < e < phi and gcd(e, phi) = 1
        e = 65537 if phi > 65337 else 16
        while e < phi:
            if gcd(e, phi) == 1:
                break
            e += 1

        # print(e)

        # Find d such that d is the multiplicative inverse of e modulo phi
        d = multiplicative_inverse(e, phi)
        # print(d)

        # d = 2
        # while True:
        #     if (d * e) % phi == 1:
        #         break
        #     d += 1

        # Return public and private keys
        public_key = (e, n)
        private_key = (d, n)

        return public_key, private_key


def modular_exponentiation(base, exponent, modulus):
    result = 1
    base = base % modulus

    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent = exponent // 2

    return result


def encrypt(plain_text, public_key):
    e, n = public_key
    encrypted_data = modular_exponentiation(plain_text, e, n)
    return encrypted_data


def decrypt(encrypted_data, private_key):
    d, n = private_key
    decrypted_data = modular_exponentiation(encrypted_data, d, n)
    return decrypted_data



if __name__ == "__main__":
    # public_key, private_key = rsa().generate_keys(2048)
    public_key,private_key =(65537, 694833475156731655233709545902914710818813911732141503549480387006418018425141556330523895148922310053197985471293011520698083679319018585593166563227655631018216664426734919779942151886970469275296625193157845459254021716876199853551241624143099859074477974678811223398263570616569198141266301266767543748270525682592974111315955430725841402871279230658394241072840635231661691750243366064687217141116826986503281540587415876751611618244872620158735325629890664682162417216463879794542258515129164945306511302191433928313850709465938646842599593920933198132912603523315126998801007106902307567403704375279145638839075717424078698133110189062680476257777268697159913646372818858941025346638590294419923882597397144024290305629224614364661172768761792396989168625839168455419487609162730824109275171893870718999227704482115828257123503349333069590183372748520798632622753582287165939302443957978944368864804443993547512358734144380804782553004803804561482603840578323772420180811002000114800081438761741976102598627424919333898526729383992096044511130256227015470789541405698387181459377046666678177944436357871482283965192850851129987399370560261482982855211404742603093740443192573364201360005312841632338706516927248820416018112151) ,(108415876701306820846402920459367309261151022970041203061574299364681471332922776926670668443937847661916073868174168082794022013378240244236255180246356539667472022028020611774260724804372779606394923068206253994314993826487173255857089455445778445390935899152179843985332614592214075387331822518125950853907304533458178653787912287339426581608270486384398071982300423614748419715418215982063272674705949615629107320858804698409791748267935567210988209978134340732649941021397941480370224125801073986753744706415092310887224799933072579044477923628430902572706646090943537281768150792793869826200096337298655672040140825306879534506470126065549915257691037449021404843746711076272612283288163625526306357678191739531660499353458734715292964074944943063103961738380851778645121176716140996849481810833560762649967448682481371452222431212114535616342274303436871739749970219445459258961775224901640269074831360313018196133622766675991475836803364023638130713168529220586694943835754618249988818005810354332515287415069268228568442559043390781716130326849584293334085358436641157017548827007700970937072405783817250943460418652385805110832264953188768794243376622816230807674008219362524829679511852304232272579562690304934484217780833, 694833475156731655233709545902914710818813911732141503549480387006418018425141556330523895148922310053197985471293011520698083679319018585593166563227655631018216664426734919779942151886970469275296625193157845459254021716876199853551241624143099859074477974678811223398263570616569198141266301266767543748270525682592974111315955430725841402871279230658394241072840635231661691750243366064687217141116826986503281540587415876751611618244872620158735325629890664682162417216463879794542258515129164945306511302191433928313850709465938646842599593920933198132912603523315126998801007106902307567403704375279145638839075717424078698133110189062680476257777268697159913646372818858941025346638590294419923882597397144024290305629224614364661172768761792396989168625839168455419487609162730824109275171893870718999227704482115828257123503349333069590183372748520798632622753582287165939302443957978944368864804443993547512358734144380804782553004803804561482603840578323772420180811002000114800081438761741976102598627424919333898526729383992096044511130256227015470789541405698387181459377046666678177944436357871482283965192850851129987399370560261482982855211404742603093740443192573364201360005312841632338706516927248820416018112151)
    
    message = 'This is a test message'

    
    st = time.perf_counter()
    ec_l = []
    for m in message:
        ec_l.append(encrypt(ord(m),public_key))

    # encrypted_message = encrypt(message, public_key)
    # print("Encrypted message:", encrypted_message)
    et = time.perf_counter()
    print(f'Encrypting time = {et-st:.5f}')


    st = time.perf_counter()

    res = ''

    for ec in ec_l:
        res += chr(decrypt(ec,private_key))
    
    # decrypted_message = decrypt(encrypted_message, private_key)
    print("Decrypted message:", res)
    et = time.perf_counter()
    print(f'Decryption time = {et-st:.5f}')


