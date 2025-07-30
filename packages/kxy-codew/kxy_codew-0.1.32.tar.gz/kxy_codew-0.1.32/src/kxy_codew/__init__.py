from .state import KXYState

kxy_state = KXYState()


def set_token(secret):
    kxy_state.set_secret(secret)

