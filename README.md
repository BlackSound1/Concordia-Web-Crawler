# COMP479P4

<hr />

## Setup

1. Navigate to this directory.

2. Create a virtual environment with:

    ```shell
    $ python -m venv COMP479
    ```

3. Activate it with:

    ```shell
    $ source COMP479\Scripts\activate.bat
    ```

4. Install the dependencies with:

    ```shell
    $ pip install -r requirements.txt
    ```

## To Run

First run the `crawl.py` module with:

```shell
$ python crawl.py -n 1000
```

The `-n` flag determines how many documents to crawl and download. Due to some potential errors found when performing 
clustering on a small numer of files, please set `-n` to a large number.

Then, run the `cluster.py` module with:

```shell
$ python cluster.py
```

Finally, run the `sentiment.py` module with:

```shell
$ python sentiment.py
```
