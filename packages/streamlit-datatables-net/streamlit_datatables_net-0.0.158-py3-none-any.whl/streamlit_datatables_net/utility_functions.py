import streamlit as st
import streamlit.components.v1 as components
import json
from typing import Dict, List
import time


def allow_top_navigation(iframe_title):
    """Allow links embedded in iframes to open in the same tab (target='_parent' or '_blank')"""
    st.markdown('''<style>
        .element-container:has(iframe[height="0"]) {display: none;}
        </style>
        ''', unsafe_allow_html=True)

    components.html('''
        <script language="javascript">
        var updateAndReloadIframes = function () {
            var reloadRequired = false;
            // Grab all iFrames, add the 'allow-top-navigation' property and reload them
            var iframes = parent.document.querySelectorAll('iframe[title="<<<TITLE>>>"]');
            console.log("allow_top_navigation", iframes.length);
            for (var i = 0; i < iframes.length; i++) {
                if (!iframes[i].sandbox.contains('allow-top-navigation')) {
                    reloadRequired = true;
                    iframes[i].setAttribute("sandbox", "allow-forms allow-modals allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts allow-downloads allow-top-navigation-by-user-activation allow-top-navigation");
                }
            }
            if (reloadRequired) {
                setTimeout(function() {
                    for (var i = 0; i < iframes.length; i++) {
                        iframes[i].contentWindow.location.reload();
                    }
                }, 300)
            }
        }
        updateAndReloadIframes()

    </script>
    '''.replace("<<<TITLE>>>", iframe_title), height=0)


def stringify_javascript_function(js_file_path, function_name):
    """Converts the specified JavaScript function in a JavaScript file to a string for use in JSON serializaion.
    JavaScript functions must be defined as: 

    function _function_name_( _args_ ) { _javascript_code_ }"""
    with open(js_file_path, 'r') as file:
        js_code = file.read()
        start_marker = f"function {function_name}("
        start_idx = js_code.find(start_marker)
        if start_idx == -1:
            raise ValueError(
                f"Function {function_name} not found in {js_file_path}")

        # Find the start of the function body
        body_start_idx = js_code.find("{", start_idx) + 1
        if body_start_idx == 0:
            raise ValueError(
                f"Function body for {function_name} not found in {js_file_path}")

        # Initialize a counter for opening and closing braces
        open_braces = 1
        end_idx = body_start_idx

        # Iterate through the code to find the matching closing brace
        while open_braces > 0 and end_idx < len(js_code):
            if js_code[end_idx] == '{':
                open_braces += 1
            elif js_code[end_idx] == '}':
                open_braces -= 1
            end_idx += 1

        if open_braces != 0:
            raise ValueError(
                f"Unmatched braces in function {function_name} in {js_file_path}")

        # Extract the full function code
        function_code = js_code[start_idx:end_idx]

        return function_code


def stringify_file(file_path):
    """Converts the specified file to a string for use in JSON serializaion."""
    with open(file_path, 'r') as file:
        file_string = file.read()
        return file_string


def generate_js_function_from_json(object_to_jsonify: Dict | List, function_name):
    """Returns a stringified JavasScript function that returns the object_to_jsonify when called.  Useful for passing configuration information
    in JSON compatible formats.  Example function:

    function {function_name}() {
        const customObjectBasedOnJSONObject = {json_str};
        console.log('object',customObjectBasedOnJSONObject);
        return customObjectBasedOnJSONObject;
        }

    """
    json_str = json.dumps(object_to_jsonify, indent=2)
    js_function_template = f"""
function {function_name}() {{
  const customObjectBasedOnJSONObject = {json_str};
  return customObjectBasedOnJSONObject;
}}
"""
    return js_function_template.strip()


def reload_ajax_data(key: str = None):
    """Executing this function triggers a reload of ajax data on the next app run.

    key is required if the key is defined on the st_datatable component."""
    ajax_reload_key = "_st_datatable_ajax_reload_key"
    if key:
        key=str(key)
        ajax_reload_key = f'{ajax_reload_key}_{key.replace(" ","_")}'
    st.session_state[ajax_reload_key] = str(
        round(time.time()*1000))
