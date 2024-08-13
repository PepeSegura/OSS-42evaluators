from django.utils.crypto import get_random_string

def csp_nonce(request):
    nonce = get_random_string(16)
    request.csp_nonce = nonce
    return {'csp_nonce': nonce}
