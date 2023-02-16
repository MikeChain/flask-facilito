from api.app import create_app
from api.config import config


env = config['development']
app = create_app(env)

if __name__ == '__main__':
    app.run()
