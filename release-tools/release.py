import os, re, shutil
from pkg_resources import parse_version

ENCODING = 'utf-8'
PYTHON = "python"

def get_current_release_and_filestr(regex, file='setup.py'):
    with open(file, 'r', encoding=ENCODING) as f:
        file_str = f.read()
    
    regex_match = re.search(regex, file_str)
    if regex_match is None:
        raise Exception(f"None release tag found in {file}.")
    release = regex_match.group(1)
    return release, file_str


def replace_regex(regex, repl, file):
    """
    Read file and replace regex matching with repl and write back to the file.
    """
    _, file_str = get_current_release_and_filestr(regex, file)

    # Write back to the file
    new_str = re.sub(regex, repl, file_str)
    with open(file, 'w', encoding=ENCODING) as f:
        f.write(new_str)

def build_dist():
    # Clean the /dist folder first 
    shutil.rmtree('dist')
    os.mkdir('dist')
    os.system(f"{PYTHON} setup.py sdist bdist_wheel")
    return "Build finished"

def pip_install_editable():
    # For TestPypi cases, usually we use the following command instead: 
    #     pip install -i https://test.pypi.org/simple/ <package-name>
    os.system(f"{PYTHON} -m pip install -e .")
    return "Installed via pip editable mode."

def twine_upload(repo):
    os.system(f"{PYTHON} -m twine upload --repository {repo} --skip-existing dist/*")
    return f"Upload to {repo}"

def main(release_new, ignore_tag_conflict=False, build=True, pip=False, repo=None):
    regex = "version\s*=\s*[\'\"](.+?)[\'\"]"
    repl = f"version = '{release_new}'"
    release_previous, _ = get_current_release_and_filestr(regex)

    # Assert that new release tag is larger than the previous tag
    if not ignore_tag_conflict:
        assert parse_version(release_new) > parse_version(release_previous), \
            f"Invalid new release tag: '{release_new}' (not larger than '{release_previous}')."

    # Update files: setup.py, layout.html, conf.py
    replace_regex(regex, repl, 'setup.py')

    # Build the dist and the docs
    msg_build = build_dist() if build else "No build"
    msg_pip = pip_install_editable() if pip else "No installation via pip"


    # Upload to testPypi for testing
    msg_upload = twine_upload(repo) if repo else "No upload"
        
    # Print
    print('\n'.join([
        "\n---",
        f"Version:\t{release_previous}  -->  {release_new}",
        f"Build:\t\t{msg_build}.",
        f"Pip:\t\t{msg_pip}.",
        f"Upload:\t\t{msg_upload}." 
    ]))


# --- Main ----------------------------------------

# For the version naming, refer to setuptools' documentation:
# https://setuptools.readthedocs.io/en/latest/setuptools.html#specifying-your-project-s-version
#
# Simrofy version format:
#     2.4.1-r1 > 2.4.1 > 2.4.1pre1


release_new = "0.1.1"
main(release_new, ignore_tag_conflict=True, repo='testpypi')