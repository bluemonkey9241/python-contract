from functools import wraps
from flask import (
    Flask, render_template, request, Response
)
import os
import shutil
# import matplotlib
# matplotlib.use('Agg')  # Needs to be right after 'import matplotlib'
# import mpld3  # Needs to be after 'import matplotlib'
# import MoneySupply  # Needs to be after 'import matplotlib'
import matplotlib
import MoneySupply  # Needs to be after 'import matplotlib'
import mpld3  # Needs to be after 'import matplotlib'
matplotlib.use('Agg')  # Needs to be right after 'import matplotlib'

app = Flask(__name__)

# ######################################################################################################################
# Basic auth
# http://flask.pocoo.org/snippets/8/
# ######################################################################################################################


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'neiblock' and password == 'showmethepelas'


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# ######################################################################################################################
# Disable caching
# https://stackoverflow.com/a/34067710
# ######################################################################################################################
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


# ######################################################################################################################
# Auxiliary functions
# ######################################################################################################################
def move_file_to_folder(file, folder):
    if os.path.exists(file):
        if not os.path.exists(folder):
            os.mkdir(folder)
        shutil.move(file, os.path.join(folder, file))


def get_request_parameter(parameter_name):
    result = None
    if request.args:
        if request.args[parameter_name]:
            result = request.args[parameter_name]
    if request.form:
        if request.form[parameter_name]:
            result = request.form[parameter_name]
    print('{} is {}'.format(parameter_name, result), flush=True)
    return result


# ######################################################################################################################
# Endpoints
# ######################################################################################################################
@app.route('/')
@requires_auth
def root():
    template = 'money_supply.html'

    # ############################################### Collect parameters ###############################################
    numeric_parameters = MoneySupply.get_numeric_parameters()
    numeric_list_parameters = MoneySupply.get_numeric_list_parameters()

    errors = []
    for parameter in numeric_parameters + numeric_list_parameters:
        input_value = get_request_parameter(parameter.name)
        if input_value:
            parameter.set_value_from_string(input_value)
            if parameter.error_message:
                errors.append(parameter.error_message)

    if errors:
        return render_template(template, errors=errors,
                               numeric_parameters=numeric_parameters,
                               numeric_list_parameters=numeric_list_parameters)

    # Call cryptoeconomics functions ##########################################
    figures_and_texts = MoneySupply.money_supply(
        numeric_parameters[0].value,
        numeric_parameters[1].value,
        numeric_parameters[2].value,
        numeric_parameters[3].value,
        numeric_parameters[4].value,
        numeric_parameters[5].value,
        numeric_parameters[6].value,
        numeric_parameters[7].value,
        numeric_list_parameters[0].value,
        numeric_list_parameters[1].value,
        numeric_list_parameters[2].value,
        numeric_list_parameters[3].value,
        numeric_list_parameters[4].value,
        numeric_list_parameters[5].value,
        numeric_list_parameters[6].value,
        numeric_list_parameters[7].value,
        numeric_list_parameters[8].value,
        numeric_list_parameters[9].value,
        numeric_list_parameters[10].value,
        numeric_list_parameters[11].value)
    # FIXME

    # Figures generated by MoneySupply(). They are generated in the same
    # folder as this script, so they need to be moved
    # to 'static' folder.
    image_names = ['Adoption.png', 'Costs.png', 'Money.png']  # FIXME: names are hard coded
    for image_name in image_names:
        move_file_to_folder(image_name, 'static')

    figures_as_html = ''
    for figure_and_text in figures_and_texts:
        figures_as_html += figure_and_text[1] + mpld3.fig_to_html(figure_and_text[0]) + '<hr>'

    # Call template passing all figures ################################################################################
    return render_template(template, figures=figures_as_html, image_names=image_names,
                           numeric_parameters=numeric_parameters, numeric_list_parameters=numeric_list_parameters)


# ######################################################################################################################
#  Debugging?
# ######################################################################################################################
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
