import os
import sys
import json
import boto3
from fire import Fire


def convert(table_data):
    """
    Generate MySQL like DDL from glue table output json
    """
    table_name = table_data["Name"]
    db_name = table_data["DatabaseName"]
    columns = table_data["StorageDescriptor"]["Columns"]

    column_defs = []
    for column in columns:
        column_defs.append("`{}` {}".format(column["Name"], column["Type"]))

    create_table_stmt = (
        "CREATE TABLE `{db_name}`.`{table_name}` ({column_defs})".format(
            db_name=db_name, table_name=table_name, column_defs=", ".join(column_defs)
        )
    )
    print(create_table_stmt)
    return create_table_stmt


def iter_tables(glue_client, db_name):
    next_token = ""
    while next_token is not None:
        res = glue_client.get_tables(DatabaseName=db_name, NextToken=next_token)
        for table in res["TableList"]:
            yield table

        next_token = res.get("NextToken")


def create_context_with_dbname(db_name, aws_profile):
    context_filename = "context.json"
    context = {}
    if os.path.exists(context_filename):
        with open(context_filename) as f:
            context = json.load(f)

    glue_client = boto3.Session(profile_name=aws_profile).client("glue")
    context[db_name] = "\n".join(list(map(convert, iter_tables(glue_client, db_name))))

    with open(context_filename, "w") as f:
        json.dump(context, f)


if __name__ == "__main__":
    Fire({"dbname": create_context_with_dbname})
