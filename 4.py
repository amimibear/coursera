import urllib.request
import urllib.parse

TARGET = 'http://crypto-class.appspot.com/po?er='
c = 'f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4'

#--------------------------------------------------------------
# padding oracle
#--------------------------------------------------------------
class PaddingOracle(object):
    def query(self, q):
        target = TARGET + urllib.parse.quote(q)  # Create query URL
        req = urllib.request.Request(target)     # Send HTTP request to server
        try:
            f = urllib.request.urlopen(req)      # Wait for response
        except urllib.error.HTTPError as e:
            # print("We got: %d" % e.code)        # Print response code
            if e.code == 404:
                return True  # good padding
            return False     # bad padding

po = PaddingOracle()

c = bytes.fromhex(c)
m = [0]*48 # plaintext
for i in range(3):
    c0 = c[:16*i]
    c2 = c[16*(i+1):16*(i+2)] # the block to be decrypted
    for j in range(1,17):
        c10 = c[16*i:16*(i+1)-j] # no change
        c11 = bytes(m[16*(i+1)-j+l]^j^c[16*(i+1)-j+l] for l in range(1,j))
        az = list(range(ord('a'),ord('z')+1))
        AZ = list(range(ord('A'),ord('Z')+1))
        for k in [32]+az+AZ+list(set(range(256))-set(az)-set(AZ)-{32,1}): # if k=j=1, the original padding is always valid
            c1 = c10+bytes([k^c[16*(i+1)-j]^j])+c11 # change the byte
            cc = c1+c2 # we should only use 2 blocks, changing the IV.
            # cc = c0+c1+c2 # why can't we use 3 blocks and change the 2nd block?
            print(i,j,k,cc.hex())
            hex = bytes([k^c[16*(i+1)-j]^j]).hex()
            if po.query(cc.hex()):
                m[16*(i+1)-j] = k
                print(k,chr(k),bytes(m))
                break

print(bytes(m))
