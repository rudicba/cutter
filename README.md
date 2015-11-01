# Cutter
Simple, tinny and secure containers for your projects.

**Cutter** is a simple and straightforward tool for create minimal Linux containers, it allows you to select folder and files from your current operative system to create a skeleton inside a folder that you could use for LXC, Docker or Chroot.

**Cutter** will automatically add to destination folder all necessary runtime libraries, system files or links to run your project inside a container without having a complete operative system inside container.

## Installation

### Create python 3 virtual environment
```sh
$ pyvenv-3.4 /path/to/.cutter_venv
```

### Clone the repository
```sh
$ git clone https://github.com/rudicba/cutter.git
$ git checkout develop
```

### Install requirements
```sh
$ . /path/to/.cutter_venv/bin/activate
$ pip install -r cutter/setup/requirements.txt
```

### Examples

#### Create skeleton containing only *bash* and *ls*

##### Create configuration file
Edit *cutter/config/cutter.ini* with:

```ini
[Global]
; Where to create Cutter image
destination: my_cutter
; Default to follow and copy symbolic links inside Cutter
follow_links: True
; Default to copy Dynamic Dependencies inside Cutter
copy_dd: True

; System files
[System]
paths: /bin/bash /bin/ls
```

##### Run cutter
```sh
(.cutter_venv) user@host: bin/cutter
```

##### Chroot to your minimal cutter skeleton
```sh
$ sudo chroot my_cutter /bin/bash
$ ls
```

### Development
Want to contribute? Great!

### Todos
- Allow to create Python and/or Node virtual environments.
- Use a container to create **cutter** skeleton.

### License
BSD 3-Clause License
