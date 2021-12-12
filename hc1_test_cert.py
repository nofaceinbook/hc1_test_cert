# Creates HC1 certificate for testing
# Certificate will not be valid as it will not be signed by official CA

# Definition of Data for Test Certificate
family_name = "Matees"
given_name = "Costel"
birthdate = "1991-11-22"  # yyyy-mm-dd
country = "XX"  # two letter country code
last_vaccination_date = "2021-05-01"  # yyyy-mm-dd
cert_issuer = "Non Valid Test Certificate"
time_to_live = 180 * 24 * 3600  # validity period of cert, default 180 days
issuing_country = "XX"  # two letter country code
keyid = '01234567'  # first 8 hex values of SHA256 fingerprint of signing certificate, not relevant for test
# Private Signature Key for ecdsa-with-SHA256 for test certificate without password protection
# AS THIS IS JUST USED FOR PUBLIC TESTING IT IS NOT CRITICAL TO HAVE THIS PRIVATE KEY IN THIS CODE #
pem = b'-----BEGIN EC PRIVATE KEY-----\n' \
      b'MHcCAQEEIICXhlDKAkd37q3LEtYmjoCuaIvne9/FzV0BClH2X52AoAoGCCqGSM49\n' \
      b'AwEHoUQDQgAEL8eW9/mJUjRX0G6+dA2M9DHquAx5Q07wHFdZ0vM5WzkbOMNea2X2\n' \
      b'iirLZ+RmhRAuDMZ6SN7Gj5uRrOo89+7KFA==' \
      b'\n-----END EC PRIVATE KEY-----'
cert_id = "00XX/00000/1234567890/THISISATESTCERTIFICATEXXX#S"
vaccine_manufacturer = "ORG-100030215"
vaccine_id = "EU/1/20/1528"
dn = 2
sd = 2
tg = "840539006"
vp = "1119349007"
version = "1.0.0"

# Required imports
import unidecode
import json
from datetime import datetime
import cbor2
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cose.messages import Sign1Message
from cose.keys.curves import P256
from cose.algorithms import Es256
from cose.headers import Algorithm, KID
from cose.keys import CoseKey
from cose.keys.keyparam import KpAlg, EC2KpD, EC2KpCurve
from cose.keys.keyparam import KpKty
from cose.keys.keytype import KtyEC2
import zlib
from base45 import b45encode
import matplotlib.pyplot as plt
import qrcode

# Create upper case string without special characters and whitespace replaced by '<'
fnt = unidecode.unidecode(family_name).upper().replace(" ", "<")
gnt = unidecode.unidecode(given_name).upper().replace(" ", "<")

# Create json payload
json_issuance = '"v": [{"ci": "' + cert_id + '", "co": "' + country + '", "dn": ' + str(dn) + ', "dt": "' + \
                last_vaccination_date + '", "is": "' + cert_issuer + '", "ma": "' + vaccine_manufacturer + \
                '", "mp": "' + vaccine_id + '", "sd": ' + str(sd) + ', "tg": "' + tg + '", "vp": "' + vp + '"}]'
json_name = '"nam": {"fn": "' + family_name + '", "gn": "' + given_name + '", "fnt": "' + fnt + '", "gnt": "' + gnt + '"}'
json_payload = '{ ' + json_issuance + ', "dob": "' + birthdate + '", ' + json_name + ', "ver": "' + version + '"}'

# Make sure correct utf-8 was base   ######## NEEDED ???? ###############
json_payload = json_payload.encode("utf-8")
json_payload = json.loads(json_payload.decode("utf-8"))

# Add additional required info to json_payload
json_payload = {
    1: issuing_country,
    4: int(datetime.now().timestamp() + time_to_live),
    6: int(datetime.today().timestamp()),
    -260: {
        1: json_payload,
    },
}
print("\nFULL JSON PAYLOAD:")
print(json_payload)

# Convert to CBOR
#
payload = cbor2.dumps(json_payload)
print("\nCBOR FORMAT:")
print(payload)

# Read in the private key that we use to actually sign this
#
keyfile = load_pem_private_key(pem, password=None)
priv = keyfile.private_numbers().private_value.to_bytes(32, byteorder="big")

# Prepare a message to sign; specifying algorithm and keyid
# that we (will) use
#
msg = Sign1Message(phdr={Algorithm: Es256, KID: keyid}, payload=payload)
print("\nMSG TO BE SIGNED:")
print(msg)

# Create the signing key - use ecdsa-with-SHA256
# and NIST P256 / secp256r1
#
cose_key = {
    KpKty: KtyEC2,
    KpAlg: Es256,  # ecdsa-with-SHA256
    EC2KpCurve: P256,  # Ought to be pk.curve - but the two libs clash
    EC2KpD: priv,
}

# Encode the message (which includes signing)
#
msg.key = CoseKey.from_dict(cose_key)
out = msg.encode()
print("\nSIGNED MESSAGE:")
print(out)

# Compress with ZLIB
#
out = zlib.compress(out, 9)
print("\nCOMPRESSED MESSAGE:")
print(out)

# And base45 encode the result
#
out = b'HC1:' + b45encode(out)
print("\nBASE45 ENCODED:")
print(out)

# Finally create and show qr_code
#
qr_image = qrcode.make(out)
imgplot = plt.imshow(qr_image)
plt.show()



