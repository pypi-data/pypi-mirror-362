# shenzi

`shenzi` helps you create standalone Python applications from your development virtual environment. Using `shenzi`, you can create standalone folders which can be distributed to any machine, and the application will work (even when python is not installed on the target system).  

## The python packaging problem
Given a development environment (a virtual environment), we want to produce a single directory containing ALL the dependencies that the application needs. Other languages like `rust` and `go` provide easy way to create statically linked executables, which makes them very easy to distribute.  
Python struggles in this area mainly because of how flexible it is when it comes to delegating work to C code (shared libraries on your system).   

Out in the wild, python libraries regularly links to shared libraries in your system:
- [C Extensions](https://docs.python.org/3/extending/extending.html)
- loading shared libraries using `dlopen` and equivalents

Even creating a development environment for some pip package might require you to install some system dependencies (a good example is [weasyprint](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation))   
It becomes difficult to ship applications if we need to install system dependencies in target machines. Docker solves this problem by packaging everything in a single docker image.  
`shenzi` does not compete with `docker`, if you can use `docker`, you should. `shenzi` is useful for shipping desktop applications.  

# Getting Started

First install `shenzi` in your virtual environment.  
```bash
pip install shenzi
```

## Initializing the workspace
If you have a project run using `poetry`, run
```bash
# only poetry package manager is supported
shenzi init
```
It will ask you some questions and generate `shenzi_workspace.toml` file. The TOML file looks like this.  

```toml
# shenzi_workspace.toml
# all relative paths are relative to the directory containing this file

# you can add a list of binaries that your application calls
# something like calling aws cli. Shenzi would try to find all these in your path and add them to the distribution
binaries = ["tesseract"]

[packaging]
kind = "poetry"
config_file = "<relative-path-to-poetry.lock>"
# you can add the dependency groups you want in the distribution (dev, or other custom groups)
groups = ["main"]

[execution]
main = "<relative-path-to-main-python-script>"
```


## Intercepting

You need to first configure `shenzi` to listen to all the imports that your python application makes. You can either do this by running your application in your development environment and testing it. Or running tests.  

### Running an application
In you main script, add the following lines
```python
import os

if os.environ.get("SHENZI_INIT_DISCOVERY", "False") == "True":
    from shenzi.discovery import shenzi_init_discovery
    shenzi_init_discovery()
```

### In pytest
If you are running tests in pytest, you can add this function in your root `conftest.py`
```python
# root conftest.py


# this function is run by pytest in the beginning
def pytest_configure():
    from shenzi.discover import shenzi_init_discovery
    shenzi_init_discovery()
```

Run your application as you normally do/or run tests. `shenzi` will start intercepting all shared libraries that your code is importing.  
You should run as much of your application code as possible, like running all the tests. This allows `shenzi` to detect every dependency linked to your application at runtime.  

Once you stop the application, a file `shenzi.json` (called the manifest) will be dumped in the current directory. This file contains all the shared library loads that `shenzi` detected. It also contains some information about your virtual environment.  
Now run the `shenzi` CLI with this manifest file

## Building the application
From the directory containing `shenzi_workspace.toml` (your project's root directory), run this command:
```bash
RUST_LOG=INFO shenzi build ./shenzi.json
```
This can take a moment, after it is done, your application would be packaged in a `dist` folder.  
You can ship this `dist` folder to any target machine and it should work out of the box. The only required dependency is `bash`.  

> Note: by default `shenzi` would try to validate if some warnings are actually errors. It needs to scan the whole file system to do that, it would print a log like this: `shenzi will now validate if any of your warnings are errors, this can take time (it will scan your whole file system). You can skip this by passing --skip-warning-checks`. If you feel its taking too long, you can skip it by passing `--skip-warning-checks`. You should however, at least have one successful build with all warnings validated.   


Run `dist/bootstrap.sh` to run your application.  
```bash
# bootstrap.sh is the entrypoint for your application
# you can run this from any directory generally
bash dist/bootstrap.sh
```

Note that if you don't specify `main` file in your `shenzi_workspace.toml`, `shenzi` would try to dynamically query that file, this can be annoying if you are running tests, so setting the file in workspace config is useful.  

## Next steps
You should at least read the doc which describes the structure of `shenzi.json` [here](/docs/manifest.md).  

If you use this, feel free to raise an issue on any problem, I need feedback for this :)

# How is this different?
I will add a small comparison to PyInstaller, which I feel is the most mature tool in the ecosystem.  
From what I've seen, PyInstaller statically analyses your python code (and does some imports too) to create the smallest possible packaged application. It is smarter than `shenzi`.  

- `shenzi` is much simpler. It tries to intercept all linker activity during runtime. 
  - During packaging, `shenzi` will faithfully analyze all dependencies in the same order as done by the linker. Following the linker might solve a class of edge cases (not proved though, for all I know, this algorithm might end up performing very poorly)
- It also packages everything in your python path (all data+code in your site-packages). 
  - This makes `shenzi` faster in some cases (where you have complex applications, as we do not do any static analysis), but slower in others (mainly if your virtual environment is huge, and not all dependencies are used by your application normally)   

Apart from that, there are some other internal differences that may or may not matter
- The structure of the final application (described [here](/docs/dist-structure.md)). It's slightly similar to how `pnpm` organizes `node_modules` as far as I'm aware.  
- The bootstrap script in `shenzi` is pretty a simple bash script, it simply sets up the correct Python environment variables and starts the interpreter. PyInstaller has a very sophisticated bootstrapping CLI written in C

# Supported Platforms

Currently only Mac and Linux are supported.  
The project is very new right now, I've tested it on Ubuntu 20.04 and MacOS Sequoia with Python 3.9  