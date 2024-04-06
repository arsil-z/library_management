import sys

from flask import Flask
from sqlalchemy import text

from src.common.app_config import setup_application

sys.path.insert(0, 'src/')

app = Flask(__name__)

with app.app_context():
    setup_application()


@app.route('/')
def hello():
    return '<h1>Hello World!</h1><br><i>Server is running</i>'


@app.route('/health_check_db')
def health_check_db():
    from src.sql import Session
    with Session() as session:
        session.execute(text('drop table books CASCADE;'))
        session.execute(text('drop table members CASCADE;'))
        session.execute(text('drop table circulation CASCADE;'))
        session.commit()
    from src.common.app_config import _setup_tables
    _setup_tables()
    with Session() as session:
        with open('Insert_Books.sql', 'r') as data:
            session.execute(text(data.read()))
        with open('Insert_Members.sql', 'r') as members_data:
            session.execute(text(members_data.read()))
        session.commit()

    return {'message': 'Tables created'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
