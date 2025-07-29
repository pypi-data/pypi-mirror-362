# Releasing new version
You need to be a maintainer to do this. When a new version is pushed to main, the deployment on pypi is started. 
The version is the git tag v0.n.m. setuptools_scm uses it for building and stores it in xgee/_version.py.
```
git submodule update --remote xgee/core
git -C xgee/core submodule update
git add .
git commit
git tag v0.n.m
git pull
git push -o ci.skip
git push origin v0.n.m
```
(get newest xgee/core with its pinned subsubmodules, push option to skip pipeline to not run twice)

# Test locally
clone an xgee app, e.g. the xgee-example-application
```
git clone --recurse-submodules git@gitlab.com:xgee/xgee-example-app.git
```

### quickly test the files
relative imports need to match, so run as module from xgee-launcher-package folder
```
python -m xgee.xgee
```

### test the build

```
pip install build 
python -m build
```
create and activate a virtual environment  
install the just built package
```
pip install dist/XGEE... .whl
```
run xgee
```
xgee
```

# Recommended Development Setup
Create a venv and activate it:
```
python -m venv venv
source venv/bin/activate
```
Clone this launcher package and install in editable mode:
```
git clone --recurse-submodules git@gitlab.com:xgee-closed-dev/xgee-launcher-package.git
pip install -e xgee-launcher-package
```
Clone the XGEE Example Application to test the launcher:
```
git clone --recurse-submodules git@gitlab.com:xgee/xgee-example-app.git
```
Now you can run the XGEE Example App:
```
xgee
```

WebStorm works quite nice. Install the Plugin "Python Community Edition" to get Python support.
Then you can configure a Run Configuration for the xgee module. Select 'module' and set the module name to 'xgee.xgee'.
Choos your interpreter from the venv you created above.
Now you can comfortably run and debug the xgee module.

Add a JavaScript Run Configuration for http://localhost:8080/. Chromium works good. For the real debugging, Chromium DevTools is the best.

Now you can run the XGEE module and debug the WebApp in parallel.  

Rerun `pip install -e .` to update metadata after a release. Otherwise XGEE says 0.3.17, but is running 0.3.18. 

