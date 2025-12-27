from passlib.context import CryptContext

pass_context = CryptContext(schemes=['argon2'],deprecated = 'auto')

def hash_pass(plainTxt: str):
    return pass_context.hash(plainTxt)

def verify_pass(plainTxt: str, hashTxt: str):
    return pass_context.verify(plainTxt,hashTxt)