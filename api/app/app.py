from models.modules.core import app
from views.route import *


if __name__ == "__main__":
    app.run(
        # host = app.config['IP'],
        # port = app.config['PORT'],
        debug = True,
        use_reloader = True
    )