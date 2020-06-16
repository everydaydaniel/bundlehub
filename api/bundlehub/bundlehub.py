import os



ROOT_DIR = os.getcwd()
BUNDLEHUB_DIR = ROOT_DIR + "/bundlehub"
BUNDLEHUB_REPO = BUNDLEHUB_DIR + "/bundlehub"
BUNDLEHUB_REPO_FILES_DIRECTORY = BUNDLEHUB_REPO + "/generated_bundles"
BUNDLEHUB_LINK = "git@github.com:everydaydaniel/bundlehub.git"
if os.getenv("BUNDLEHUB_REPO_LINK"):
    BUNDLEHUB_LINK = os.getenv("BUNDLEHUB_REPO_LINK")


# Clone the repo from github
def clone_repo():
    print('CLONE_REPO\n\n', BUNDLEHUB_DIR)
    os.chdir(BUNDLEHUB_DIR)
    os.system("git clone {} -q".format(BUNDLEHUB_LINK))

def pull_repo():
    os.chdir(BUNDLEHUB_REPO)
    os.system("git pull origin master")

# check that the repo is in the directory
def check_repo_exists():
    try:
        os.chdir(BUNDLEHUB_REPO)
        pull_repo()
    except FileNotFoundError as e:
        set_email()
        clone_repo()

def create_bundle_json(bundle):
    number_of_files = len([f for f in os.listdir(BUNDLEHUB_REPO_FILES_DIRECTORY)])
    current_file_number = number_of_files + 1
    os.chdir(BUNDLEHUB_REPO_FILES_DIRECTORY)
    print(number_of_files, current_file_number)
    print("writing bundle to file: generated_bundle_{}.json".format(str(current_file_number)))
    file_name = "generated_bundle_{}.json".format(str(current_file_number))
    with open(file_name, "w") as f:
        f.write(bundle.serialize(indent=4))
    print("file written")
    commit_message = '"created {}.json"'.format(str(file_name))
    return commit_message, file_name


def commit_and_push(commit_message):
    os.chdir(BUNDLEHUB_REPO)
    os.system("git add .")
    git_command = "git commit -m {}".format(commit_message)
    print(git_command)
    os.system(git_command)
    os.system("git push origin master")

def create_link(file_name):
    return "https://raw.githubusercontent.com/everydaydaniel/bundlehub/master/generated_bundles/{}".format(file_name)

def set_email():
    os.system("git config --global user.email bundlehub@email.com")

def bundhub_main(bundle):
    # check for the repo and perform opperations
    check_repo_exists()
    commit_message, file_created = create_bundle_json(bundle)
    commit_and_push(commit_message)
    link = create_link(file_created)
    return link
