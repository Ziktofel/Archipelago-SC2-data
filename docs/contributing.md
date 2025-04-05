# Contributing
We generally accept contributions from people, but please be a good steward of the codebase.
* Stick to our naming conventions for data. This means any new data entries for Archipelago should start with an `AP_` prefix.
* When overriding vanilla data, leave a comment explaining it's a vanilla override so we know the lack of prefix is intentional.
* Don't make direct changes to generated .galaxy files. Changing just the .galaxy file without updating the corresponding Triggers file will mean the next time someone saves in the editor, your changes will be erased.
* The editor modifies certain binary files that aren't actually important to commit and can cause merge conflicts. Try to avoid committing changes to them:
  * `*.version` files, such as Triggers.version or DocumentInfo.version
  * The `<Optimized/>` line in `ComponentList.SC2Components` isn't important to commit
  * The `DocumentHeader` file doesn't need to be committed, unless updating a mod or map's mod dependencies

## Project structure
There are two main components to Archipelago StarCraft 2: the client and the data. The client is part of the Archipelago project, with the live version at the ArchipelagoMW repository and the beta client in Ziktofel's fork of that repository. The data lives in the Archipelago-SC2-Data repository.

The client is deployed by being merged into the main Archipelago project, being released as part of the main Archipelago release cycle, and being downloaded from the Archipelago Releases page. The data is deployed by an automated github action that updates the releases page, and downloaded automatically by the client when running the `/download_data` command. The beta client doesn't have a formal release; it is acquired by git cloning the beta repository and is considered under active development. Beta and live mod data is stored separately and downloaded by separate client versions.

We generally work off the `sc2-next` branch for beta development; make PRs (Pull Requests) for new features there. The `master` branch is used for the live version of the data pulled in with the Archipelago installer; generally only bugfix PRs should be merged there.

## Getting started with git
The [playing the beta instructions](https://github.com/MatthewMarinets/ap_sc2_notes/blob/main/playing_the_beta.md) cover installing git and Python and downloading the client repository. You will also need to clone the data repository to make map or mod changes.

### Workflow
We use a branching workflow. This means that to develop a feature, you will:
* Start with the base branch, generally `sc2-next` from Ziktofel's fork for beta development
  * Remember to update it before starting
* Create a new feature branch, which you will make your changes on
* Push your feature branch to your fork, and make a pull request
* The project maintainer, Ziktofel, will review your pull request, possibly identify issues to address, and merge the PR into sc2-next when it is ready

### First Time Setup -- Clone the data repository
* In github, make a fork of [Ziktofel's Archipelago-SC2-data repository](https://github.com/Ziktofel/Archipelago-SC2-data.git).
* Note the Clone url on your fork (click the big green "Code" button and copy the url under HTTPS)
* Locally, run these commands to get a local version of your repository and also get a link to Ziktofel's fork for easier base branch updates:
```bash
# In your project's parent directory
git clone <your fork url>
cd Archipelago-SC2-Data
git remote add ziktofel https://github.com/Ziktofel/Archipelago-SC2-data.git
git fetch ziktofel sc2-next
git checkout sc2-next
```

### Per-feature setup
#### Make a branch
```bash
# In your data repository
# Get the latest changes on sc2-next
git checkout sc2-next
git pull
# Create a new branch
## Give it a descriptive name so you can identify it later, such as "dig_base_locations"
git checkout -b my_cool_branch_name
```

#### After making changes
Make sure you made your changes to your repo folder, and not so some other copy of the files. A common mistake is to have separate deployed files and open those in the editor, only to find your changes have not affected your repository and you must find a way to copy-paste your changes over.

```bash
# See what changed
git status

# Stage changes
## All files changed
git add *
## Specific files
git add <filenames>
## Undo changes to files
git restore <filenames>

# Commit staged changes
## Give a descriptive commit message, such as "Fixing a bug where Fenix didn't spin properly when doing whirlwind"
## The git recommendation of keeping messages under 80 characters is bad and few teams stick with it; 120 is a more reasonable maximum
git commit -m "My super cool commit message"

# Push changes to your fork
## First push of this branch -- point at your fork and make a remote branch
git push -u origin my_cool_branch_name
## Later pushes remember the branch you pointed to earlier
git push
```

#### When ready for review
* Push all your changes
* Make sure you've done some local testing and there are no glaring bugs
* In github, make a pull request
  * The `git push -u <stuff>` command will output a url you can follow to immdiately start making a PR
  * Otherwise, for recently-pushed branches, your github fork page will have a banner prompting you to make a PR
  * Otherwise, you can make a PR from the "Pull Requests" tab of your fork page
* If the change also requires a client change, make a PR there and provide a link to each PR in the others' description
* It's not strictly necessary, but it can be nice to post a link to your pull request in the #SC2-dev thread in the Archipelago discord
* Respond to feedback and address issues identified in review

#### Cleanup
You can have multiple feature branches active locally and switch between them. It's good to clean up branches for already-merged features so they don't clutter up your selection.

```bash
git branch -d my_cool_branch_name
```

## Testing locally
The client starts missions by running the map files in your StarCraft 2 installation's Maps/ folder. These maps in turn depend on the Mods in the Mods/ folder. To deploy your changes locally for testing:
* For **mods**, simply copy-paste your mod files into the Mods/ folder.
  * You can write a script to do this automatically or create a symlink to automatically keep your repo folder and Mods/ folder in sync.
  * Note that with a symlink or with your repo directly in the Mods/ folder, running `/download_data` can overwrite some local changes
* **Maps** can only be run in a packaged format, so the folders must be built into an MPQ format first.
  * This can be done locally with the `./build_release_package.sh` script, but it can only be run in linux environments and with the `smpq` package installed. On Windows this can be done with WSL (Windows Subsystem for Linux) with the `smpq` and `parallel` packages installed.
    * Files are output to the target/ directory. A symlink is even more useful here, as there is no risk of your local changes being overwritten by `/download_data`.
  * Otherwise, it is possible to push your changes and an automatic github action will run to compile the maps. Download them from the Actions tab of your github fork page.
* Place the maps within the Maps/ folder of your StarCraft 2 installation

It is not necessary, but it can be helpful to include screenshots of your feature working in-game as part of the PR description.
