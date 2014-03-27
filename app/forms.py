from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField
from wtforms.validators import Required
from models import User, ROLE_USER, ROLE_ADMIN

class LoginForm(Form):
    openid      = TextField('openid', validators = [Required()])
    TextField
    password    = PasswordField('password', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)
    #print openid
    #print password
    #print remember_me
    print "Login Form"

    def __init__(self, *args, **kwargs):
        #Form.__init__(self, *args, **kwargs)
        #self.user = None
        #kwargs['csrf_enabled'] = False
        super(LoginForm, self).__init__(*args, **kwargs)
    def validate(self):

        #rv = Form.validate(self)
        #if not rv:
            #print rv
            #return False
        
        user = User.query.filter_by(username=self.openid.data).first()

        #print user
        #self.user = user
        ####Add validators   http://flask.pocoo.org/snippets/64/

        return True


