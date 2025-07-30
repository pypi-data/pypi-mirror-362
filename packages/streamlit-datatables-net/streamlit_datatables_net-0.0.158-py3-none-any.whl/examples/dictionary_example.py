import os
import sys
from dateutil.parser import parse

PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)


def my_on_click_function(my_arg, key=None):
    print("You clicked me!", my_arg, key)


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
        st.write("Example: List of dictionaries")
        dt_container = st.container()
        with st.expander("Code"):
            with st.echo():
                data = [
                    {
                        "id": "1",
                        "name": "Tiger Nixon",
                        "position": "System Architect",
                        "salary": 320800,
                        "start_date": "2012/04/25",
                        "office": "Edinburgh",
                        "extn": "5421",
                        "address": {"street": "123 Main St", "city": "Anytown"}
                    },
                    {
                        "id": "2",
                        "name": "Garrett Summers",
                        "position": "Accountant",
                        "salary": 170750,
                        "start_date": "2011/07/25",
                        "office": "Tokyo",
                        "extn": "8422",
                        "address": {"street": "456 Main St", "city": "Anytown"}
                    },
                    {
                        "id": "3",
                        "name": "Clark Kent",
                        "position": "Reporter",
                        "salary": 170750,
                        "start_date": "2009/09/30",
                        "office": "Gotham",
                        "extn": "8523",
                        "address": {"street": "789 Main St", "city": "Anytown"}
                    },
                ]
                column_order = ["name", "position", "start_date", "salary",
                                "office", "extn", "address.street", "address.city"]

                options = {}
                options["lengthChange"] = False
                options["responsive"] = True
                options["scrollX"] = False
                options["stateSave"] = True
                options["stateDuration"] = -1
                options["order"] = [[4, "asc"]]
                render_group_count = stringify_javascript_function(JAVASCRIPT_FILE_PATH, "row_group_accordion")
                options["rowGroup"] = {"dataSrc": "office", "startRender": render_group_count}
                options["select"] = {"style": "single", "info": True}
                special_action_button = stringify_javascript_function(
                    JAVASCRIPT_FILE_PATH, "actionButton")
                options["buttons"] = [
                    {"extend": "excel",
                        "text": "Export to Excel",
                     },
                    {"extend": "csv",
                        "text": "Export to CSV",
                     },
                    {"text": "Special Action Button",
                        "action": special_action_button}
                ]
                options["layout"] = {
                    "top3Start":  "buttons",
                    "top2Start": {"buttons": ['pageLength']},
                    "top1": 'searchPanes',
                    'topEnd': 'search',
                    'bottomStart': 'info',
                    'bottomEnd': 'paging'
                }
                options["searchPanes"] = False
                for row in data:
                    row["start_date"] = (
                        parse(row["start_date"])).date()

                big_data = []
                for i in range(10):
                    big_data.extend(data)

                with dt_container:
                    on_select = st.selectbox("on_select", key="my-table-on-select", options=[
                        "ignore", "rerun", "callable"])
                    if on_select == "callable":
                        on_select = my_on_click_function
                    on_select = 'rerun'

                    dt_response = st_datatable(
                        big_data, 
                        column_order=column_order, 
                        options=options, 
                        key="example_1", 
                        dt_config="default", 
                        date_format="%m/%d/%Y", 
                        is_datetime=True, 
                        enable_top_navigation=False, 
                        export_file_name="Example 1", 
                        on_select=on_select, 
                        enable_diagnostics=False,
                        )
                    st.write(dt_response)


if __name__ == "__main__":
    run_example()
