#Contributing to mhvdb2

Please make your own fork the repository and use pull requests to submit changes. This lets [TravisCi](https://travis-ci.org/makehackvoid/mhvdb2) check for errors before the changes are committed to master.

## Use issues to organise work

So that other people know what you are working on, either assign an existing issue to yourself or create a new issue and then assign it. Ask if you don't have access or need help doing this. Reference the issue number #nn in the pull request when you have something ready to share (this lets Github link back to the issue automatically).

## PEP8 compliance

Travis is now checking pep8 compliance before running the application tests. The ```setup.cfg``` includes the settings for flake8 - at this stage just that lines can be up to 99 characters instead of the default 80.

##Python Environment

To get a python3 virtualenvwrapper project I installed python3 (and virtualenvwrapper), checked where it was using

```which python3```

then told virtualenvwrapper to use that python by setting

```
export VIRTUALENV_PYTHON=/usr/local/bin/python3
```

then if you don't already have a project directory, use  
```mkproject mhvdb2``` 
to create it or, if it already exists, change to the project directory and use

```
mkvirtualenv mhvdb2
setvirtualenvproject
``` 

Once it is setup, to stop defaulting to python3, unset the python env variable using

```unset VIRTUALENV_PYTHON```

This has left my old environments using python 2.7 and the new one using 3.4.1


##Git remotes for testing

Fork the repository to your own account so that you can make pull requests. Clone it to your computer. 

On your computer add a new remote 'upstream' so you can update your fork from the original makehackvoid project. If you want to be able to see (fetch) and pull down pull requests from the original makehackvoid project for testing, add a second fetch line to .git/config
```fetch = +refs/pull/*/head:refs/remotes/upstream/pr/*```

In .git/config I have:

```
[remote "upstream"]
    url = https://github.com/makehackvoid/mhvdb2.git
    fetch = +refs/heads/*:refs/remotes/upstream/*
    fetch = +refs/pull/*/head:refs/remotes/upstream/pr/*
```

