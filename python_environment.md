##Python Environment

To get a python3 virtualenvwrapper project I installed python3 (and virtualenvwrapper), checked where it was using

```which python3```

then told virtualenvwrapper to use that python by setting

```
export VIRTUALENV_PYTHON=/usr/local/bin/python3
mkproject mhvdb2
```

then unset they python env variable using

```unset VIRTUALENV_PYTHON```

This has left my old environments using python 2.7 and the new one using 3.4.1


##GitRemotes for testing

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

