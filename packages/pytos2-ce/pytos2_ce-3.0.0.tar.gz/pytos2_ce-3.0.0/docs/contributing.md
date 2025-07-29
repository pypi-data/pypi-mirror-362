# Before You Begin

Before you start contributing, we require some pre reqs to enforce consistency.

We use Black to enforce, formatting anf nb-clean to clear Jupyter notebooks of hidden metadata and output

To accomplish this we use pre-commit which will automatically perform these actions with git hooks

## Getting Started

You will need [pre-commit](https://pre-commit.com) installed on your machine, you can use pip or brew. Its included in our dev-requirements, so you dont have to install it globally. I personally seperat venv by project so I install project requirements by running 

```bash
pip install -r requirements.txt -r dev-requirements.txt
```

Once installed run `pre-commit install` to add our hook to your git