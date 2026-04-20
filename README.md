git init -> Initialized empty Git repository in /Users/rakumar2601/Desktop/ML_BASICS/.git/
git clone <url> ->url from the github or gitlab and used to clone the repo in your Local
git add . -> to add all the files in the staging area
git add <filename> -> to add a particular file
git commit -m "message" -> to commit the changes with a message
git status -> Shows which files are staged,unstaged or untracked
git remote add origin https://github.com/Rahul1309200/Machine-Learning-.git -> Add remote Url
git push origin <branchname> ->push to the remote from local
git push origin --all -> push all branches


## Branching

git branch -> List all Branches
git checkout -b <branchname> -> creates a new branch and switch to it as well
git switch <branchname> -> switch to branch
git merge <branchname> -> merge the branch to the current branch
git log --oneline ---graph -> Visualize your branch history in terminal