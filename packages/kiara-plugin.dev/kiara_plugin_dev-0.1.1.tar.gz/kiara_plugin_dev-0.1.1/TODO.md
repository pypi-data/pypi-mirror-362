# Tasks for the 'dev' kiara plugin

This file contains open (and completed) tasks for this project

### Todo

- [ ] migrate the main cli subcommands from the old `kiara_plugin.develop` project

### In Progress

### Done

- [x] create project directory structure
- [x] create local git repository
- [x] create remote git repository on https://github.com/new:
  - settings to use:
    - `Owner`: `DHARPA-Project`
    - `Repository name`: `kiara_plugin.dev`
    - `Description`: `A kiara plugin to help with development related tasks (modules, pipelines, widgets,...).`
- [x] create [trusted publisher](https://docs.pypi.org/trusted-publishers/) on https://pypi.org/manage/account/publishing/
  - settings to use:
    - `PyPI Project Name`: `kiara_plugin.dev`
    - `Owner`: `DHARPA-Project`
    - `Repository name`: `kiara_plugin.dev`
    - `Workflow name`: `build-linux.yaml`
    - `Environment name`: `pypi`
- [x] configure conda package publishing
    - [ ] create an account on https://anaconda.org (if necessary)
    - [ ] create API token to allow Github actions to push to anaconda: https://anaconda.org/dharpa/settings/access
      - settings to use:
        - `Token Name`: choose anything, maybe `kiara_plugin.dev Github Action`
        - `Strength`: Strong
        - `Scopes`:
          - `Allow write access to the API site`
        - `Expiration date`: choose whatever you deem sensible
    - [x] create new repository secret at: https://github.com/DHARPA-Project/kiara_plugin.dev/settings/secrets/actions
        - `Name`: `ANACONDA_PUSH_TOKEN`
        - `Secret`: the token you created above
