from flask.ext.login import LoginManager, UserMixin, login_user
from mhvdb2.models import User as UserModel
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserModel, UserMixin):
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


login_manager = LoginManager()


@login_manager.user_loader
def load_user(userid):
    try:
        return User.get(User.id == userid)
    except:
        return None


def authenticate_user(email, password):
    users = User.select().where(User.email == email)
    if users.count() == 1 and users.get().check_password(password):
        return login_user(users.get())
    else:
        return False


def register_user(name, email, password):
    errors = []
    unique = User.select().where(User.email == email).count() == 0
    if not unique:
        errors.append("A user with that email address already exists")

    if len(password) <= 6:
        errors.append("Password must be 6 characters or longer")

    if len(errors) == 0:
        user = User()
        user.name = name
        user.email = email
        user.set_password(password)
        user.save()

    return errors
