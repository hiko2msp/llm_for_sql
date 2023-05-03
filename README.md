# Creating SQL from Natural Language

## Background and Objectives

+ Data utilization within the company is important for business success
+ One hurdle for non-engineers using data marts is understanding the schema of internal data
+ We will create a program that generates SQL from natural language using OpenAI's chat API

## Assumptions

+ We are using AWS as a cloud service
+ The schema of the data mart is stored in Glue Table

## Usage

### Environment setup

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=<key>
```

+ Tested on Python 3.9.9

### Creating a Context

```bash
Usage: create_context.py dbname <DB_NAME> <AWS_PROFILE>
```

+ Right now the only way is to create a context file using Glue Tables on AWS.
+ If you want to create a context yourself, add a context to `context.json` in the following format.

  ```
  {
    "<context_name>": "<DDL>"
  }
  ```

  ChatAPI then interprets the DDL and generates SQL based on it.

### Generate SQL

```bash
$ python create_sql.py create "Get a list of 400 errors in the last 30 minutes from the WAF log" sample
Consumed Tokens: 386
SELECT *
FROM `sample`.`waf_logs`
WHERE `timestamp` >= UNIX_TIMESTAMP() - 1800
AND `httpresponsecode` = 400
```



