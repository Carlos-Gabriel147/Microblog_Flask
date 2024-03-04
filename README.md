# Microblog_Flask

### My repository for learning the Flask microframework. The goal is to create a simple but complete web blog. The reference for creating the blog is from: The Flask Mega-Tutorial from Miguel Grinberg

# 1. Create a New Virtual Environment:

On the new computer, navigate to your project directory where you copied the virtual environment. Create a new virtual environment using the same Python version you used on the original computer. You can do this by running the following command:

cmd command:

```bash
python -m venv venv # Replace 'venv' with the name you prefer for the new virtual environment
```

## 2. Activate the New Virtual Environment:

Activate the new virtual environment using the appropriate command for your operating system:

For Windows:

```bash
venv\Scripts\activate
```

For Linux/macOS:

```bash
source venv/bin/activate
```
## 3. Install Dependencies:

With the virtual environment activated, install the dependencies listed in the "requirements.txt" file using the following command:

```bash
pip install -r requirements.txt
```

## 4. Verify the Environment:

Ensure that the new virtual environment is set up correctly by checking that all the required dependencies are installed. You can run your Python scripts or Django/Flask applications to verify everything is working as expected.

After completing these steps, you should have successfully moved your Python virtual environment to the new computer. The virtual environment will now be isolated from the system-wide Python packages and will contain all the necessary dependencies for your project to run.

## 5. Possible error

Sometimes reusing a venv can cause trouble. When that happens, try the following steps: 

1) activate your virtual environment.
2) `python -m pip freeze > requirements.txt` to record your current dependencies. Make sure it records the environment in your virtual environment instead of your local environment. (make sure you activate virtual venv before freeze).
3) deactivate your virtual environment.
4) remove your current virtual environment folder. rm -r <folder name>
5) in the new location, install virtual env: python -m venv <name of env>
6) activate the new virtual env
7) reinstall the dependencies from the requirement file you just created: `python -m pip install -r ./requirements.txt`