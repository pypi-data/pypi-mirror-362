import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)


def run_example():
    from streamlit_datatables_net import st_datatable

    data = [
        {"name": "John", "age": 30, "city": "New York"},
        {"name": "Jane", "age": 25, "city": "Los Angeles"},
        {"name": "Bob", "age": 40, "city": "San Francisco"}
    ]
    st_datatable(data, key="simple_example")


if __name__ == "__main__":
    run_example()
