import os
import sys
from typing import List

PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)


def my_on_click_function(my_arg, key=None):
    print("You clicked me!", my_arg, key)


def ajax_table_example():
    import streamlit as st
    from streamlit_datatables_net import (
        st_datatable,
        reload_ajax_data,
        stringify_javascript_function,
        stringify_file,
        generate_js_function_from_json,
    )
    st.set_page_config(initial_sidebar_state="collapsed", layout="wide")
    print("script run")
    st.button("Rerun script")

    JAVASCRIPT_FILE_PATH = 'renderFunctions.js'
    CSS_LABELS_FILE_PATH = "css_labels.css"
    css_file = stringify_file(CSS_LABELS_FILE_PATH)

    col_l, content_column, col_r = st.columns([1, 10, 1])
    with content_column:
        delay = st.selectbox("delay", [100, 2000], index=0)
        with st.container(border=True):
            if st.button("Reload Ajax data"):
                reload_ajax_data()
            options = {}
            options["keys"] = True
            options["scroller"] = True
            options["scrollY"] = 400
            options["scrollCollapse"] = True
            options["ajax"] = {
                "url": f"https://dummyjson.com/products?delay={delay}",
                "type": "GET",
                "dataSrc": "products",
            }
            options["language"] = {
                "processing": "Loading...",
                "loadingRecords": "Please wait - loading...",
                "searchPlaceholder": "type here",
                "search": "Test Search:"
            },
            streamlit_action_function = stringify_javascript_function(
                JAVASCRIPT_FILE_PATH, 'streamlit_action_function')
            on_click_submit_table_values = stringify_javascript_function(
                JAVASCRIPT_FILE_PATH, 'on_click_submit_table_values')

            streamlit_action_button = {
                "text": "Trigger Streamlit Action", "action": streamlit_action_function}
            return_table_values_button = {
                "text": "Return Table Values", "action": on_click_submit_table_values}

            options["buttons"] = ['pageLength', 'colvis',
                                  'excel', streamlit_action_button, return_table_values_button]
            options["layout"] = {
                "top2Start": "buttons",
                "top1": {'searchPanes': {"initCollapsed": True}},
                'topEnd': 'search',
                'bottomStart': 'info',
                'bottomEnd': 'paging'
            }

            options["scrollX"] = True
            options["responsive"] = False
            options["processing"] = True
            options["rowReorder"] = {
                "dataSrc": "id",
                "update": False
            }

            price_settings = {"taxRate": 7.0}

            price_settings_function = generate_js_function_from_json(
                price_settings, "getPriceSettings")

            truncate_text = stringify_javascript_function(
                JAVASCRIPT_FILE_PATH, 'truncateText')

            price_plus_tax = stringify_javascript_function(
                JAVASCRIPT_FILE_PATH, 'pricePlusTax')

            show_ellipsis = stringify_javascript_function(
                JAVASCRIPT_FILE_PATH, 'showEllipsis')

            show_hamburger = stringify_javascript_function(
                JAVASCRIPT_FILE_PATH, 'showHamburger')

            render_learn_more_link = stringify_javascript_function(
                JAVASCRIPT_FILE_PATH, "renderLearnMoreLink")
            render_label = stringify_javascript_function(
                JAVASCRIPT_FILE_PATH, "renderLabel")

            common_js_functions = {
                "addPrefix": stringify_javascript_function(JAVASCRIPT_FILE_PATH, 'addPrefix'),
                "getPriceSettings": price_settings_function,
                "setViewHref": stringify_javascript_function(
                    JAVASCRIPT_FILE_PATH, 'setViewHref'),
                "setEditHref": stringify_javascript_function(
                    JAVASCRIPT_FILE_PATH, 'setEditHref'),
                "setDownloadHref": stringify_javascript_function(
                    JAVASCRIPT_FILE_PATH, 'setDownloadHref'),
                "setSearchHref": stringify_javascript_function(
                    JAVASCRIPT_FILE_PATH, 'setSearchHref'),
                "displayContextMenuItem": stringify_javascript_function(JAVASCRIPT_FILE_PATH, "displayContextMenuItem")
            }

            options["columns"] = [
                {"data": "id", "title": "id", "width": '20%'},
                {"data": "title", "title": "title", "width": '10%'},
                {"data": "category", "title": "category",
                    "render": render_label, "width": '10%'},
                {"data": None, "defaultContent": "", "title": "Learn More", "name": "learn_more",
                    "render": render_learn_more_link, "width": '10%'},
                {"data": "description", "title": "description",
                    "render": truncate_text, "width": '10%'},
                {"data": "price", "title": "price",
                    "className": "secondmenu", "width": '10%'},
                {"data": "price", "title": "price + tax",
                    "render": price_plus_tax, "width": '10%'},
                {"data": "reviews", "title": "reviews",
                    "render": "[, ].rating", "width": '10%'},
                {"data": None, "defaultContent": "",
                    "title": "", "orderable": False, "render": show_ellipsis, "width": '10%'},
            ]

            options["columnDefs"] = [
                {
                    "className": 'reorder',
                    "render": show_hamburger,
                    "targets": 0
                },
                {"searchPanes": {"orthogonal": "sp"},
                    "targets": "learn_more:name"},
            ]
            context_menu = []

            context_menu_1 = {}
            context_menu_1["className"] = "fa-ellipsis-v"
            context_menu_1["items"] = [
                {
                    "name": "View",
                    # "hrefFunctionName": "setViewHref",
                    # "target": "_blank"
                },
                {
                    "name": "Edit",
                    "hrefFunctionName": "setEditHref",
                    "target": "_blank"
                },
                {
                    "name": "See Special Sale Price",
                    "conditionalDisplayFunctionName": "displayContextMenuItem",
                },
                {
                    "name": "Download",
                    "hrefFunctionName": "setDownloadHref",
                    "target": "_blank"
                },
                {
                    "name": "Search",
                    "hrefFunctionName": "setSearchHref",
                    "target": "_blank"
                },
            ]

            ajax_setup = {
                "headers": {
                    'Content-type': "application/x-www-form-urlencoded",
                    'X-CSRFToken': "csrf_token"
                }
            }

            context_menu.append(context_menu_1)
            context_menu_2 = {}
            context_menu_2["className"] = "secondmenu"
            context_menu_2["items"] = [
                {
                    "name": "Open",
                    # "hrefFunctionName": "setViewHref",
                    # "target": "_blank"
                },
                {
                    "name": "Delete",
                    "hrefFunctionName": "setEditHref",
                    "target": "_blank"
                },
            ]

            context_menu.append(context_menu_2)

            filename = st.text_input("filename", "test")

            dt_click = st_datatable(None,
                                    options=options,
                                    context_menu=context_menu,
                                    css_files=[css_file],
                                    common_js_functions=common_js_functions,
                                    ajax_setup=ajax_setup,
                                    ajax_auto_refresh_period=None,
                                    key="ajax_table",
                                    on_select=my_on_click_function,
                                    args=["args are here"],
                                    kwargs={"key": "ajax_table"},
                                    export_file_name=filename,
                                    key_focus_column_index=2,
                                    enable_diagnostics=True,
                                    )
            if isinstance(dt_click, dict) and dt_click.get("customComponentValue"):
                print(dt_click)
            if isinstance(dt_click, List):
                for click in dt_click:
                    print(click["data"]["id"],
                          click.get("rowReorderDetails"))
            st.write(dt_click)
            st.write(st.session_state)


if __name__ == "__main__":
    ajax_table_example()
