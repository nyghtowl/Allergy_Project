from flask.ext.wtf import Form, TextField, BooleanField, TextAreaField
from flask.ext.wtf import Required, Length

class LoginForm(Form):
	openid = TextField('openid', validators = [Required()])
	remember_me = BooleanField('remember_me', default = False)

class EditProfile(Form):
    nickname = TextField('nickname', validators = [Required()])
    about_me = TextAreaField('about_me', validators = [Length(min = 0, max = 140)])

    def __init__(self, original_nickname, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname

        def validate(self):
            if not Form.validate(self):
                return False
            if self.nickname.data == self.original_nickname:
                return True
            if self.nickname.data != User.make_valid_nickname(self.nickname.data):
                self.nickname.errors.append(gettext('This nickname has invalid characters. Please use letters, numbers, dots and underscores only.'))
                return Fale
            user = User.query.filter_by(nickname = self.nickname.data).first()
            if user != None:
                self.nickname.errors.append(gettext('This nickname is already in use. Please choose another one.'))
                return False
            return True


class SearchForm(Form):
    search = TextField('search', validators = [Required()])