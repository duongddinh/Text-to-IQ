# Text to IQ

Text to IQ prediction using NodeJS and python; this is a just for fun project (maybe i will do a research about this in the future).

The file ```IQ_predict.py``` is utilized to train the model and save data for future use by ```IQ_predict_run.py```.

The file ```merged_iq_data.csv```, containing quote and IQ columns, is employed to train the model.

## Run

```node app.js```

The server is running on port 3000.

If a Python environment error (```ModuleNotFoundError: No module named 'numpy'```) is returned, use the following solution:

```python
...
const pythonPath = "/usr/bin/python3"; # command to find python diectorty: $ where python3
....
const pythonProcess = spawn(`${pythonPath}`, ['IQ_predict_run.py', userInput]);
...

 ```

A Reverse Proxy can be used to forward requests from port 80 to 3000:

```
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

## Dependencies

```
pip3 install pandas numpy scikit-learn tensorflow keras-tuner joblib
```

```
npm install express multer
```

