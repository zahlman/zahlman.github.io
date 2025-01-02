# Github deployment config
# There are other deploy options described in the original conf.py.
# https://getnikola.com/handbook.html#deploying-to-github
# You will need to configure the deployment branch on GitHub.
GITHUB_SOURCE_BRANCH = 'nikola'
GITHUB_DEPLOY_BRANCH = 'master'
GITHUB_REMOTE_NAME = 'origin'
# Commit to the source branch automatically before deploying?
# Disabled just to make sure that the SSH password isn't phished.
GITHUB_COMMIT_SOURCE = False
