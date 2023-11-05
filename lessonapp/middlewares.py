import bcrypt
from authentication.models import Teacher

def SimpleMiddleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = get_response(request)

        try:
            mail = request.headers['mail']
            password = request.headers['password']

            teacher = Teacher.objects.get(email=mail)

            if bcrypt.checkpw(password.encode('utf-8'), teacher.password.encode('utf-8')):
                return response
            else:
                return 'pass incorrect'
        except:
            return 'error'

        # Code to be executed for each request/response after
        # the view is called.
    return middleware