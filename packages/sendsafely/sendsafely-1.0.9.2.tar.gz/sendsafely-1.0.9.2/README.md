# SendSafely Python SDK (INTERNAL)
Install Python 3 or higher if not already installed
```
python3 --version
```
```
brew install python
```
The Python command to install pip (as pip3) and Setuptools
```
python3 -m pip install --upgrade setuptools
```
To create a source distribution
```
python3 setup.py sdist --dist-dir=dist
```
To install the source distribution
```
python3 -m pip install ./dist/sendsafely-x.y.z.tar.gz
```
To run unittests, update SendSafely instance in the test/*.py scripts, and then run the following from /src:
```
python3 -m unittest tests/*.py
```
To run integration scripts, cd to /scripts and run the python script with the following command
```
python3 sendsafely_python_example.py
```
_When testing, create and activate a [Python virtual environment](https://docs.python.org/3/tutorial/venv.html) and then install the source distribution_
```
python3 -m venv ./test/dir
source test/dir/bin/activate
```
To create pydocs, run
```
pydoc3 -w SendSafely sendsafely/*.py
```
Remove absolute path names from generated HTML prior to sharing with customer

---

## Prepare for public release
### 1. Bump Version in `setup.py`
### 2. Choose a Deployment Method
Proceed with one of the following paths:

#### A. Local Build & Release
From the **Python-Client-API** directory, run:
```
python3 setup.py sdist --dist-dir=dist
```

#### B. CI/CD or PROD Deployment via GitHub Actions

#### CI/CD Workflow
- **Triggers:** On pull request to `master`, or manually via **manual trigger**
- **Uploads to:**  
  `s3://integrations-deployment/python-client-api/`

#### PROD Workflow
- **Triggers:** On push to `master` (e.g., after PR merge), or via **manual trigger**
- **Uploads to:**  
  `s3://sendsafely/python-client-api/`

### 3. Test package 
- upload and install by uploading to https://test.pypi.org/ and installing in virtual environment. 
- In virtual environment, run test script to verify working as expected. 

### 4. Upload package to pypi


