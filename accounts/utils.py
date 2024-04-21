
def detectuser(user):
    if user.role == 1:
        redirecturl = 'vendordashboard'
        return redirecturl
    elif user.role == 2:
        redirecturl = 'customerdashboard'
        return redirecturl
    elif user.role == None and user.is_admin:
        redirecturl = '/admin'
        return redirecturl