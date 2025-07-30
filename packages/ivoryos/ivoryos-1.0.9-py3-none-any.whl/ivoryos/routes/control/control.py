import os

from flask import Blueprint, redirect, url_for, flash, request, render_template, session, current_app, jsonify, \
    send_file
from flask_login import login_required

from ivoryos.utils.client_proxy import export_to_python, create_function
from ivoryos.utils.global_config import GlobalConfig
from ivoryos.utils import utils
from ivoryos.utils.form import create_form_from_module, format_name
from ivoryos.utils.task_runner import TaskRunner

global_config = GlobalConfig()
runner = TaskRunner()

control = Blueprint('control', __name__, template_folder='templates/control')


@control.route("/control/home/deck", strict_slashes=False)
@login_required
def deck_controllers():
    """
    .. :quickref: Direct Control; controls home interface

    deck control home interface for listing all deck instruments

    .. http:get:: /control/home/deck
    """
    deck_variables = global_config.deck_snapshot.keys()
    deck_list = utils.import_history(os.path.join(current_app.config["OUTPUT_FOLDER"], 'deck_history.txt'))
    return render_template('controllers_home.html', defined_variables=deck_variables, deck=True, history=deck_list)


@control.route("/control/new/", strict_slashes=False)
@control.route("/control/new/<instrument>", methods=['GET', 'POST'])
@login_required
def new_controller(instrument=None):
    """
    .. :quickref: Direct Control; connect to a new device

    interface for connecting a new <instrument>

    .. http:get:: /control/new/

    :param instrument: instrument name
    :type instrument: str

    .. http:post:: /control/new/

    :form device_name: module instance name (e.g. my_instance = MyClass())
    :form kwargs: dynamic module initialization kwargs fields

    """
    device = None
    args = None
    if instrument:

        device = find_instrument_by_name(instrument)
        args = utils.inspect.signature(device.__init__)

        if request.method == 'POST':
            device_name = request.form.get("device_name", "")
            if device_name and device_name in globals():
                flash("Device name is defined. Try another name, or leave it as blank to auto-configure")
                return render_template('controllers_new.html', instrument=instrument,
                                       api_variables=global_config.api_variables,
                                       device=device, args=args, defined_variables=global_config.defined_variables)
            if device_name == "":
                device_name = device.__name__.lower() + "_"
                num = 1
                while device_name + str(num) in global_config.defined_variables:
                    num += 1
                device_name = device_name + str(num)
            kwargs = request.form.to_dict()
            kwargs.pop("device_name")
            for i in kwargs:
                if kwargs[i] in global_config.defined_variables:
                    kwargs[i] = global_config.defined_variables[kwargs[i]]
            try:
                utils.convert_config_type(kwargs, device.__init__.__annotations__, is_class=True)
            except Exception as e:
                flash(e)
            try:
                global_config.defined_variables[device_name] = device(**kwargs)
                # global_config.defined_variables.add(device_name)
                return redirect(url_for('control.controllers_home'))
            except Exception as e:
                flash(e)
    return render_template('controllers_new.html', instrument=instrument, api_variables=global_config.api_variables,
                           device=device, args=args, defined_variables=global_config.defined_variables)


@control.route("/control/home/temp", strict_slashes=False)
@login_required
def controllers_home():
    """
    .. :quickref: Direct Control; temp control home interface

    temporarily connected devices home interface for listing all instruments

    .. http:get:: /control/home/temp

    """
    # defined_variables = parse_deck(deck)
    defined_variables = global_config.defined_variables.keys()
    return render_template('controllers_home.html', defined_variables=defined_variables)


@control.route("/control/<instrument>/methods", methods=['GET', 'POST'])
@login_required
def controllers(instrument: str):
    """
    .. :quickref: Direct Control; control interface

    control interface for selected <instrument>

    .. http:get:: /control/<instrument>/methods

    :param instrument: instrument name
    :type instrument: str

    .. http:post:: /control/<instrument>/methods

    :form hidden_name: function name (hidden field)
    :form kwargs: dynamic kwargs field

    """
    inst_object = find_instrument_by_name(instrument)
    _forms = create_form_from_module(sdl_module=inst_object, autofill=False, design=False)
    functions = list(_forms.keys())

    order = get_session_by_instrument('card_order', instrument)
    hidden_functions = get_session_by_instrument('hide_function', instrument)

    for function in functions:
        if function not in hidden_functions and function not in order:
            order.append(function)
    post_session_by_instrument('card_order', instrument, order)
    forms = {name: _forms[name] for name in order if name in _forms}
    if request.method == 'POST':
        all_kwargs = request.form.copy()
        method_name = all_kwargs.pop("hidden_name", None)
        # if method_name is not None:
        form = forms.get(method_name)
        kwargs = {field.name: field.data for field in form if field.name != 'csrf_token'}
        function_executable = getattr(inst_object, method_name)
        if form and form.validate_on_submit():
            try:
                kwargs.pop("hidden_name")
                output = runner.run_single_step(instrument, method_name, kwargs, wait=True,
                                                current_app=current_app._get_current_object())
                # output = function_executable(**kwargs)
                flash(f"\nRun Success! Output value: {output}.")
            except Exception as e:
                flash(e.__str__())
        else:
            flash(form.errors)
    return render_template('controllers.html', instrument=instrument, forms=forms, format_name=format_name)

@control.route("/control/download", strict_slashes=False)
@login_required
def download_proxy():
    """
    .. :quickref: Direct Control; download proxy interface

    download proxy interface

    .. http:get:: /control/download
    """
    snapshot = global_config.deck_snapshot.copy()
    class_definitions = {}
    # Iterate through each instrument in the snapshot
    for instrument_key, instrument_data in snapshot.items():
        # Iterate through each function associated with the current instrument
        for function_key, function_data in instrument_data.items():
            # Convert the function signature to a string representation
            function_data['signature'] = str(function_data['signature'])
        class_name = instrument_key.split('.')[-1]  # Extracting the class name from the path
        class_definitions[class_name.capitalize()] = create_function(request.url_root, class_name, instrument_data)
    # Export the generated class definitions to a .py script
    export_to_python(class_definitions, current_app.config["OUTPUT_FOLDER"])
    filepath = os.path.join(current_app.config["OUTPUT_FOLDER"], "generated_proxy.py")
    return send_file(os.path.abspath(filepath), as_attachment=True)

@control.route("/api/control/", strict_slashes=False, methods=['GET'])
@control.route("/api/control/<instrument>", methods=['POST'])
def backend_control(instrument: str=None):
    """
    .. :quickref: Backend Control; backend control

    backend control through http requests

    .. http:get:: /api/control/

    :param instrument: instrument name
    :type instrument: str

    .. http:post:: /api/control/

    """
    if instrument:
        inst_object = find_instrument_by_name(instrument)
        forms = create_form_from_module(sdl_module=inst_object, autofill=False, design=False)

    if request.method == 'POST':
        method_name = request.form.get("hidden_name", None)
        form = forms.get(method_name, None)
        if form:
            kwargs = {field.name: field.data for field in form if field.name not in ['csrf_token', 'hidden_name']}
            wait = request.form.get("hidden_wait", "true") == "true"
            output = runner.run_single_step(component=instrument, method=method_name, kwargs=kwargs, wait=wait,
                                            current_app=current_app._get_current_object())
            return jsonify(output), 200

    snapshot = global_config.deck_snapshot.copy()
    # Iterate through each instrument in the snapshot
    for instrument_key, instrument_data in snapshot.items():
        # Iterate through each function associated with the current instrument
        for function_key, function_data in instrument_data.items():
            # Convert the function signature to a string representation
            function_data['signature'] = str(function_data['signature'])
    return jsonify(snapshot), 200

# @control.route("/api/control", strict_slashes=False, methods=['GET'])
# def backend_client():
#     """
#     .. :quickref: Backend Control; get snapshot
#
#     backend control through http requests
#
#     .. http:get:: /api/control/summary
#     """
#     # Create a snapshot of the current deck configuration
#     snapshot = global_config.deck_snapshot.copy()
#
#     # Iterate through each instrument in the snapshot
#     for instrument_key, instrument_data in snapshot.items():
#         # Iterate through each function associated with the current instrument
#         for function_key, function_data in instrument_data.items():
#             # Convert the function signature to a string representation
#             function_data['signature'] = str(function_data['signature'])
#     return jsonify(snapshot), 200


@control.route("/control/import/module", methods=['POST'])
def import_api():
    """
    .. :quickref: Advanced Features; Manually import API module(s)

    importing other Python modules

    .. http:post:: /control/import/module

    :form filepath: API (Python class) module filepath

    import the module and redirect to :http:get:`/ivoryos/control/new/`

    """
    filepath = request.form.get('filepath')
    # filepath.replace('\\', '/')
    name = os.path.split(filepath)[-1].split('.')[0]
    try:
        spec = utils.importlib.util.spec_from_file_location(name, filepath)
        module = utils.importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        classes = utils.inspect.getmembers(module, utils.inspect.isclass)
        if len(classes) == 0:
            flash("Invalid import: no class found in the path")
            return redirect(url_for("control.controllers_home"))
        for i in classes:
            globals()[i[0]] = i[1]
            global_config.api_variables.add(i[0])
    # should handle path error and file type error
    except Exception as e:
        flash(e.__str__())
    return redirect(url_for("control.new_controller"))


# @control.route("/disconnect", methods=["GET"])
# @control.route("/disconnect/<device_name>", methods=["GET"])
# def disconnect(device_name=None):
#     """TODO handle disconnect device"""
#     if device_name:
#         try:
#             exec(device_name + ".disconnect()")
#         except Exception:
#             pass
#         global_config.defined_variables.remove(device_name)
#         globals().pop(device_name)
#         return redirect(url_for('control.controllers_home'))
#
#     deck_variables = ["deck." + var for var in set(dir(deck))
#                       if not (var.startswith("_") or var[0].isupper() or var.startswith("repackage"))
#                       and not type(eval("deck." + var)).__module__ == 'builtins']
#     for i in deck_variables:
#         try:
#             exec(i + ".disconnect()")
#         except Exception:
#             pass
#     globals()["deck"] = None
#     return redirect(url_for('control.deck_controllers'))


@control.route("/control/import/deck", methods=['POST'])
def import_deck():
    """
    .. :quickref: Advanced Features; Manually import a deck

    .. http:post:: /control/import_deck

    :form filepath: deck module filepath

    import the module and redirect to the previous page

    """
    script = utils.get_script_file()
    filepath = request.form.get('filepath')
    session['dismiss'] = request.form.get('dismiss')
    update = request.form.get('update')
    back = request.referrer
    if session['dismiss']:
        return redirect(back)
    name = os.path.split(filepath)[-1].split('.')[0]
    try:
        module = utils.import_module_by_filepath(filepath=filepath, name=name)
        utils.save_to_history(filepath, current_app.config["DECK_HISTORY"])
        module_sigs = utils.create_deck_snapshot(module, save=update, output_path=current_app.config["DUMMY_DECK"])
        if not len(module_sigs) > 0:
            flash("Invalid hardware deck, connect instruments in deck script", "error")
            return redirect(url_for("control.deck_controllers"))
        global_config.deck = module
        global_config.deck_snapshot = module_sigs

        if script.deck is None:
            script.deck = module.__name__
    # file path error exception
    except Exception as e:
        flash(e.__str__())
    return redirect(back)


@control.route('/control/<instrument>/save-order', methods=['POST'])
def save_order(instrument: str):
    """
    .. :quickref: Control Customization; Save functions' order

    .. http:post:: /control/save-order

    save function drag and drop order for the given <instrument>

    """
    # Save the new order for the specified group to session
    data = request.json
    post_session_by_instrument('card_order', instrument, data['order'])
    return '', 204


@control.route('/control/<instrument>/<function>/hide')
def hide_function(instrument, function):
    """
    .. :quickref: Control Customization; Hide function

    .. http:get:: //control/<instrument>/<function>/hide

    Hide the given <instrument> and <function>

    """
    back = request.referrer
    functions = get_session_by_instrument("hidden_functions", instrument)
    order = get_session_by_instrument("card_order", instrument)
    if function not in functions:
        functions.append(function)
        order.remove(function)
    post_session_by_instrument('hidden_functions', instrument, functions)
    post_session_by_instrument('card_order', instrument, order)
    return redirect(back)


@control.route('/control/<instrument>/<function>/unhide')
def remove_hidden(instrument: str, function: str):
    """
    .. :quickref: Control Customization; Remove a hidden function

    .. http:get:: /control/<instrument>/<function>/unhide

    Un-hide the given <instrument> and <function>

    """
    back = request.referrer
    functions = get_session_by_instrument("hidden_functions", instrument)
    order = get_session_by_instrument("card_order", instrument)
    if function in functions:
        functions.remove(function)
        order.append(function)
    post_session_by_instrument('hidden_functions', instrument, functions)
    post_session_by_instrument('card_order', instrument, order)
    return redirect(back)


def get_session_by_instrument(session_name, instrument):
    """get data from session by instrument"""
    session_object = session.get(session_name, {})
    functions = session_object.get(instrument, [])
    return functions


def post_session_by_instrument(session_name, instrument, data):
    """
    save new data to session by instrument
    :param session_name: "card_order" or "hidden_functions"
    :param instrument: function name of class object
    :param data: order list or hidden function list
    """
    session_object = session.get(session_name, {})
    session_object[instrument] = data
    session[session_name] = session_object


def find_instrument_by_name(name: str):
    """
    find instrument class object by instance name
    """
    if name.startswith("deck"):
        name = name.replace("deck.", "")
        return getattr(global_config.deck, name)
    elif name in global_config.defined_variables:
        return global_config.defined_variables[name]
    elif name in globals():
        return globals()[name]
