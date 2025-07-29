
def nonce_wrapper(f):
    return f

def command(f=None):
    if f is None:
        return nonce_wrapper
    return f

def option(*args, **kwargs):
    return nonce_wrapper
