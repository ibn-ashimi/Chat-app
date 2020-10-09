from views.users_route import *
from views.files_route import *
from views.email_route import *

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'url not found'}), 404)

@app.route('/', methods=['GET'])
def get():
    return jsonify({
        'routes': {
            "users": {
                "POST": "/users",
                "GET": ["/users", "/users/<uid>"],
                "DELETE": '/remove/<authid>',
                "PUT": '/users/<authid>'
            }
        }
    })
