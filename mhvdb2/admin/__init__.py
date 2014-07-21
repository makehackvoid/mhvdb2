from flask import Blueprint

admin = Blueprint('admin', __name__,
                  template_folder='templates')


import mhvdb2.admin.routes   # noqa


from .authentication import login_manager


@admin.record_once
def on_load(state):
    login_manager.init_app(state.app)
    login_manager.login_view = "admin.login"
    login_manager.login_message_category = "danger"
