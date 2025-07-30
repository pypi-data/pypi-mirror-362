import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)


def run_example():
    import streamlit as st
    from streamlit_datatables_net import (
        st_datatable,
        stringify_javascript_function,
    )
    st.set_page_config(initial_sidebar_state="collapsed", layout="wide")
    print("script run")
    st.button("Rerun script")

    JAVASCRIPT_FILE_PATH = 'renderFunctions.js'

    with st.container(border=True):
        st.write("Example: List of dictionaries with columns property")
        dt_container = st.container()
        with st.expander("Code"):
            with st.echo():
                data = [
                    {
                        "id": "1",
                        "name": "Tiger Nixon",
                        "score": '',
                        "salary": 320800,
                        "new_salary": 0,
                    },
                    {
                        "id": "2",
                        "name": "Garrett Summers",
                        "score": '',
                        "salary": 170750,
                        "new_salary": 0,
                    },
                    {
                        "id": "3",
                        "name": "Clark Kent",
                        "score": '',
                        "salary": 180750,
                        "new_salary": 0,
                    },
                ]

                def compute_raise():
                    data = st.session_state["example_1b"]["customComponentValue"]
                    if "allValues" in data:
                        data = data["allValues"]
                        for item in data:
                            if item["score"] == '' or item["score"] is None:
                                salary_multiplier = 1
                                item["score"] = ''
                            else:
                                salary_multiplier = float(
                                    item["score"])/100 + 1
                            item["new_salary"] = item["salary"] * \
                                salary_multiplier
                            print(item["new_salary"])
                        st.session_state["employee_salary_data"] = data

                def render_input_cell():
                    return stringify_javascript_function(JAVASCRIPT_FILE_PATH, "render_input_cell")
                common_js_functions = {}
                on_click_submit_table_values = stringify_javascript_function(
                    JAVASCRIPT_FILE_PATH, 'on_click_submit_table_values')
                common_js_functions["on_click_submit_table_values"] = on_click_submit_table_values
                columns = [
                    {"data": "name", "title": "name"},
                    {"data": "score", "title": "score",
                        "render": render_input_cell()},
                    {"data": "salary", "title": "salary",
                        "render": ['number', ',', '.', 0, '$']},
                    {"data": "new_salary", "title": "new salary",
                        "render": ['number', ',', '.', 0, '$']},
                ]
                options = {}
                options["columns"] = columns
                options["keys"] = True
                options["stateSave"] = True
                options["stateDuration"] = -1

                with dt_container:
                    if "employee_salary_data" not in st.session_state:
                        st.session_state["employee_salary_data"] = data
                    dt_response = st_datatable(
                        st.session_state["employee_salary_data"],
                        options=options,
                        key="example_1b",
                        enable_top_navigation=False,
                        common_js_functions=common_js_functions,
                        date_format="%b %d %Y",
                        is_datetime=True,
                        on_select=compute_raise,
                        override_click_response=True,
                        key_focus_column_index=1,
                        enable_diagnostics=True)
                    st.write(dt_response)


if __name__ == "__main__":
    run_example()
