from models.modules.core import app
from views.route import *


if __name__ == "__main__":
    app.run(
        debug = app.config['DEBUG'],
        use_reloader = app.config['DEBUG']
    )