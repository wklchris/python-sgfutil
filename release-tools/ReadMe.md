# How to release

1. Open the `release.py` and **edit the version string**.
2. Check the args (especially the uploading location) and excute `release.py`.
3. If upload it to TestPypi, we can install the package through:

   ```
   pip install -i https://test.pypi.org/simple/ sgfutil
   ```
4. After testing on the downloaded package, we can remove the package and continuing coding:
   
   ```
   pip uninstall sgfutil
   ```