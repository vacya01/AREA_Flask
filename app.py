from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mobility.decorators import mobile_template
from flask_mobility.mobility import Mobility
from flask_sqlalchemy import SQLAlchemy

from api import apis
from data import db_session
from data.users import User
from site_pages import pages_blueprints
from tools import use_subdomains

SCOPES = ['https://www.googleapis.com/auth/classroom.coursework.me.readonly']

app = Flask(__name__, subdomain_matching=True)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

for blueprint in pages_blueprints:
    app.register_blueprint(blueprint)
for blueprint in apis:
    app.register_blueprint(blueprint)

Mobility(app)
login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init('db/database.sqlite')


def main():
    app.run(host='0.0.0.0', port=80)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(408)
@app.errorhandler(500)
@mobile_template('/{mobile/}error-page.html')
@use_subdomains(subdomains=['area', 'market', 'edu'])
def page_not_found(error, template: str, subdomain: str):
    template = subdomain + template
    messages = {
        401: ['Вы не вошли в систему',
              'Через несколько секунд Вы будете направлены на страницу авторизации'],
        403: ['Ошибка при авторизации в ЭПОС.Школа',
              'Попробуйте ещё раз. При повторном возникновении ошибки проверьте пароль от '
              'ЭПОС.Школа и обновите его в профиле'],
        404: ['Страница не найдена',
              'Проверьте правильность введённого адреса'],
        408: ['Превышено время ожидания',
              'Попробуйте сделать запрос еще раз. Если проблема повторится, обратитесь в '
              'техподдержку'],
        500: ['Ошибка на стороне сайта',
              'Попробуйте сделать запрос еще раз. Если проблема повторится, обратитесь в '
              'техподдержку'],
    }

    return render_template(template,
                           code=error.code,
                           title=messages[error.code][0],
                           message=messages[error.code][1])


if __name__ == '__main__':
    main()
