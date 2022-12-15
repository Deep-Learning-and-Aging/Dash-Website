# Welcome to the repository of the [Website](https://www.multidimensionality-of-aging.net/) that shows the paper's results

[![Website](https://img.shields.io/website?url=https%3A%2F%2Fmultidimensionality-of-aging.net%2F)](https://multidimensionality-of-aging.net/)
[![Super linter](https://github.com/Deep-Learning-and-Aging/Website/actions/workflows/linter.yml/badge.svg)](https://github.com/Deep-Learning-and-Aging/Website/actions/workflows/linter.yml)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/a23507ac9d9b47feaf9ed05306d0a71c)](https://www.codacy.com/gh/Deep-Learning-and-Aging/Website/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Deep-Learning-and-Aging/Website&amp;utm_campaign=Badge_Grade)

The website is coded in Python, using the framework Dash. The data is stored on AWS s3. We use Cloud Run from Google Cloud Platform to host our website.

## Contribute to the project

The fact that you cannot have access to the data stored on AWS (since we don't share the credentials) makes it harder to contribute to the project. However, you can still propose the some changes with a pull request.

Once you have forked the repository and cloned it, you can install the package with its development dependencies using:
```bash
pip install -e .[env]
```

The command `launch_local_website` allows you to test the website locally.

If you are using Visual Studio Code, a [.devcontainer](.devcontainer) folder is already prepared so that you can work in a dedicated container.

Feel free to discuss about you ideas in the [discussion section](https://github.com/Deep-Learning-and-Aging/Website/discussions).

## Structure of the website
The website is constructed as follows :

```bash
📜Dockerfile (calls index.py)
📦dash_website
 ┣ 📂age_prediction_performances
 ┃ ┗ 📜age_prediction_performances.py
 ┣ 📂datasets
 ┃ ┣ 📜images.py
 ┃ ┣ 📜scalars.py
 ┃ ┣ 📜time_series.py
 ┃ ┗ 📜videos.py
 ┣ 📂... (the other folders)
 ┃ ┗ 📜 ... (the page of that folder)
 ┣ 📜app.py (define the app)
 ┗ 📜index.py (calls the different pages)
```
There are two different organisations of the pages :
- the one showed in the website. This organisation is that same as the one from actual paper.
- the one from the data storage. This organisation is inherited from the way we store the data on AWS. It is shaping the way the folders are organized in this repository.

Each page has the same structure : a layout python object, and some attributes of this layout can be modified using callbacks.

## How to deploy

A CI / CD workflow has been created with Git Actions in order to deploy the website automatically on demand.
You can find the development version of the website [here](https://dev---website-4mfjnp4fjq-uc.a.run.app).
