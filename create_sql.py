import os
import json
import openai

openai.api_key = os.environ["OPENAI_API_KEY"]


prompt = """
Your task is to create SQL to realize the input order.
Output the code after understanding the following DDL as a premise.
Output format should be a SQL statement.

```
{schema}
```

Input Order: <{order}>
"""


def get_schema_from_context_name(context_name):
    with open("context.json") as f:
        context = json.load(f)
    return context[context_name]


def create_sql(order, context_name):
    """
    Generate SQL
    """
    schema = get_schema_from_context_name(context_name)
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0,
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt.format(schema=schema, order=order)}
        ],
    )

    print(f'Consumed Tokens: {res["usage"]["total_tokens"]}')
    print("```")
    print(res["choices"][0]["message"]["content"])
    print("```")


def check_context(context_name):
    schema = get_schema_from_context_name(context_name)
    print(schema)


if __name__ == "__main__":
    from fire import Fire

    Fire(
        {
            "create": create_sql,
            "check": check_context,
        }
    )
