# hc1_test_cert
Creating Digital Covid Vaccination Test Certificates

![Example Cert](https://github.com/nofaceinbook/hc1_test_cert/blob/main/JoeDoe_Cert.PNG)

This is a simple python code to create the QR code for digital covid vaccination certificates (Health Certificates) according to [EU specification](https://github.com/ehn-dcc-development/hcert-spec/blob/main/hcert_spec.md). Of course these are no real certificates as they will be just signed by some non official test key (included unprotectd inside the code). 

## Usage
You need to have the Python libraries installed defined in requirements.txt.
The code was tested under Python 3.8.
You just need to run the Python script and QR code will be shown.
By adapting the variables on top of the code you can easily create certificates as needed for testing purpose.

By following the text output of the program you can see the different encoding steps for needed for certificate creation.

### Creating Own Signing Key
In case you want to use an other sigining key you can import an ECDSA signing key in PEM format, e.g. by creating it via Open SSL:
`openssl ecparam -name prime256v1 -genkey -noout -out sign.key`

## Credits
Code snippets for creating the certificate have been taken from [Dirk-Willem van Gulik](https://github.com/dirkx) of his repo [ehn-sign-verify-python-trivial](https://github.com/ehn-dcc-development/ehn-sign-verify-python-trivial)

