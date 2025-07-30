users = {'admin': 'admin123'}
def authenticate(u, p): return users.get(u) == p
