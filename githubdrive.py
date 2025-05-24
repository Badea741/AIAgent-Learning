from github import GitHub
import json
from dotenv import load_dotenv

pat=load_dotenv("github_pat")

github = GitHub(token=pat)

json.dumps(github.get_user_info('badea741'))