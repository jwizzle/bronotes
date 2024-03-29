# Bronotes

Basically a wrapper to access notes in a directory on your system anywhere from the commandline. And keep it in sync with git.

Functionality so far:
  * Create a note directory on your system on first start
  * Add new notes
  * Remove notes
  * Move notes and directories around
  * Edit notes with your $EDITOR
  * List notes dir in a tree
  * Generate autocompletions for zsh
  * Execute arbitrary commands in the notes directory
  * The show and edit actions search for matching notes if no valid path is given

## Installation

```bash
$ pip install bronotes
```

On first command a folder to be used is asked.

### Completions

For now there's no built-in completions.
ZSH completions can be generated so you can place them where needed:
```bash
$ bnote completions | tee ~/.oh-my-zsh/completions/_BRONOTES
```

## Usage

By default this wraps any shell command you feed it and executes it in your notes directory. When using any of the defined actions (see bnote -h) it will do that instead.
The default can be changed, and the regular shell alternatives for actions like 'rm' can be used by just using the 'exec' action manually.

```bash
$ bnote -h # For actions overview, actions have their own sub help-pages.
```

```bash
$ bnote list
.notes/ 
|-- baewfweiogn 
|-- testblaat.md 
|-- blarpblarp.md
```

```bash
$ bnote madness # madness is a great way to browse your markdown files in a local server
       start  the madness
         env  production
      listen  0.0.0.0:3000
```

* Subcommands have their own help pages.
* When using the edit or show subcommand, it falls back on the -s option if the path to your note is not valid.
* If the first argument given is not recognized by bronotes, a default action will be taken and the first argument will be fed to that action instead. This is configurable with the 'set' action and defaults to 'exec'

### Git

You can use the sync command to keep a repo in sync with git. Using basic pull/push on master.
If you want to have more control simply don't use this.
If the repo isn't a git repo yet you will be asked to initialize an empty one and set up remotes.
When quit halfway through this process it's probably better to either start over or just fix it manually.

Autosyncing is possible, but will do so after every edit or add action. So figure out if you want that yourself.
