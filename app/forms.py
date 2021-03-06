from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField,validators,IntegerField
from wtforms.validators import Required
#from flask.ext.wtf.fields.html5 import RangeInput#,IntegerRangeField
#from wtforms.fields.html5 import IntegerField,DecimalField
from models import User, ROLE_USER, ROLE_ADMIN
import socket

class LoginForm(Form):
    openid      = TextField('openid', validators = [Required()])
    password    = PasswordField('password', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)
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

class pecosConfigForm(Form):
    
    #get from database???
    #temp =[]
    #for i in range(0,10):
        #temp.append(IntegerField('temp'+str(i), [validators.Required()] ))
    item0 = IntegerField('item0', [validators.Required()] )    #,validators.NumberRange(0,100) ))
    item1 = IntegerField('item1', validators = [Required()])

    print "PECoS Config Form"
    def __init__(self, *args, **kwargs):
        super(pecosConfigForm, self).__init__(*args, **kwargs)

    def validate(self):
        return True

class LocalControllerForm(Form):
    ipRpcXML      = TextField('ip', validators = [Required()])
    print "Local Form"
    def __init__(self, *args, **kwargs):
        super(LocalControllerForm, self).__init__(*args, **kwargs)

    def validate(self):
        print self.ipRpcXML.data
        address = self.ipRpcXML.data
        if address == "localhost":
            return True
        try:
            socket.inet_pton(socket.AF_INET, address)
        except AttributeError:  # no inet_pton here, sorry
            try:
                socket.inet_aton(address)
            except socket.error:
                return False
            return address.count('.') == 3
        except socket.error:  # not a valid address
            return False

        return True
