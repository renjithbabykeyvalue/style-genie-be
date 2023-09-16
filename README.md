# Style Genie Server

### Server

```
gunicorn -b 0.0.0.0:7500 server:app --reload
```

# Environment setup

- install conda. https://docs.anaconda.com/free/anaconda/install/linux/
- Execute commands commands:
  ```
    # create a python environment
    conda create -n style-genie python=3.11.4
    # activate environment
    conda activate style-genie
    # install python dependencies
    pip install -r requirements.txt
  ```
- run server:
  `gunicorn --timeout 120 -b 0.0.0.0:7500 server:app --reload`
- test helth endpoint at: http://localhost:7500/api/health
