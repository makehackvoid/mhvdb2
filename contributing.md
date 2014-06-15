#Contributing to mhvdb2

Please make your own fork the repository and use pull requests to submit changes. This lets [TravicCi](https://travis-ci.org/makehackvoid/mhvdb2) check for errors before the changes are committed to master.

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

Fork the reporitory to your own account so that you can make pull requests. Clone it to your computer. 

On your computer add a new remote 'upstream' so you can update your fork from the original makehackvoid project. If you want to be able to see (fetch) and pull down pull requests from the original makehackvoid project for testing, add a second fetch line to .git/config
```fetch = +refs/pull/*/head:refs/remotes/upstream/pr/*```

In .git/config I have:

```
[remote "upstream"]
    url = https://github.com/makehackvoid/mhvdb2.git
    fetch = +refs/heads/*:refs/remotes/upstream/*
    fetch = +refs/pull/*/head:refs/remotes/upstream/pr/*
```

