from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup

dim_script_path = "/home/pvini/projeto/.venv/src/dimensions"
fact_script_path = "/home/pvini/projeto/.venv/src/facts"
ml_script_path = "/home/pvini/projeto/.venv/src/ml"
util_script_path = "/home/pvini/projeto/.venv/src/util"
dataset_path = "/home/pvini/projeto/.venv/data/base"
output_path = "/home/pvini/projeto/.venv/data/dw"

with DAG(
    dag_id="pipeline",
    description="ETL Workflow",
    default_args={
        "owner": "pvo",
        "depends_on_past": False,
        "retries": 3,
        "retry_delay": timedelta(seconds=10),
    },
    schedule=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    start = EmptyOperator(task_id="start")

    with TaskGroup("download_dataset") as download_dataset_task:
        download_task = BashOperator(
            task_id="download_dataset",
            bash_command=f"""kaggle config set -n path -v {dataset_path}
            mkdir -p {dataset_path}
            kaggle datasets download -d pauloviniciusornelas/wwimporters"""
        )

        unzip_task = BashOperator(
            task_id="unzip_dataset",
            bash_command=f"""cd {util_script_path}
            python3 unzip_dataset.py"""
        )

        download_task >> unzip_task

    with TaskGroup("load_dimensions_tables") as load_dimensions_task:

        load_dim_calendar_task = BashOperator(
            task_id="load_calendar_dim",
            bash_command=f"""cd {dim_script_path}
            python3 load_calendar_dimension.py {dataset_path} {output_path}"""
        )

        load_dim_city_task = BashOperator(
            task_id="load_city_dim",
            bash_command=f"""cd {dim_script_path}
            python3 load_city_dimension.py {dataset_path} {output_path}"""
        )

        load_dim_customer_task = BashOperator(
            task_id="load_customer_dim",
            bash_command=f"""cd {dim_script_path}
            python3 load_customer_dimension.py {dataset_path} {output_path}
            """
        )

        load_dim_employee_task = BashOperator(
            task_id="load_employee_dim",
            bash_command=f"""cd {dim_script_path}
            python3 load_employee_dimension.py {dataset_path} {output_path}"""
        )

        load_dim_sales_person_task = BashOperator(
            task_id="load_sales_person_dim",
            bash_command=f"""cd {dim_script_path}
            python3 load_sales_person_dimension.py {dataset_path} {output_path}"""
        )

        load_dim_payment_method_task = BashOperator(
            task_id="load_payment_method_dim",
            bash_command=f"""cd {dim_script_path}
            python3 load_payment_method_dimension.py {dataset_path} {output_path}
            """
        )

        load_dim_stock_groups_task = BashOperator(
            task_id="load_stock_groups_dim",
            bash_command=f"""cd {dim_script_path}
            python3 load_stock_groups_dimension.py {dataset_path} {output_path}
            """
        )

        load_dim_stock_item = BashOperator(
            task_id="load_stock_item_dim",
            bash_command=f"""cd {dim_script_path}
            python3 load_stock_item_dimension.py {dataset_path} {output_path}
            """
        )

        load_dim_supplier_task = BashOperator(
            task_id="load_supplier_dim",
            bash_command=f"""cd {dim_script_path}
            python3 load_supplier_dimension.py {dataset_path} {output_path}
            """
        )

        load_dim_transaction_type_task = BashOperator(
            task_id="load_transaction_type_dim",
            bash_command=f"""cd {dim_script_path}
            python3 load_transaction_type_dimension.py {dataset_path} {output_path}
            """
        )

    with TaskGroup("load_facts_tables") as load_facts_task:

        load_fact_movement_task = BashOperator(
            task_id="load_movement_fact",
            bash_command=f"""cd {fact_script_path}
            python3 load_movement_fact.py {dataset_path} {output_path}
            """
        )

        load_fact_order_sale_task = BashOperator(
            task_id="load_order_sale_fact",
            bash_command=f"""cd {fact_script_path}
            python3 load_order_sale_fact.py {dataset_path} {output_path}
            """
        )

        load_fact_stock_holding_task = BashOperator(
            task_id="load_stock_holding_fact",
            bash_command=f"""cd {fact_script_path}
            python3 load_stock_holding_fact.py {dataset_path} {output_path}
            """
        )

        load_fact_forecast_task = BashOperator(
            task_id="load_fact_forecast",
            bash_command=f"""cd {ml_script_path}
            python3 forecasts.py {output_path}
            """
        )

        load_fact_order_sale_task >> load_fact_forecast_task

    end = EmptyOperator(task_id='end')

    start >> download_dataset_task >> load_dimensions_task >> load_facts_task >> end