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
