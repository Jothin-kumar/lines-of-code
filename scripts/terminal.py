"""
MIT License

Copyright (c) 2021 B.Jothin kumar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Author: Jothin kumar (https://jothin-kumar.github.io/)
Github repository of this project: https://github.com/Jothin-kumar/lines-of-code
"""
from _lines_of_code import Repository, init, clear_repos
from _github_repos import set_token, get_all_repos_of_user
from time import sleep

init()
print('--------------------Welcome--------------------')
git_clone_urls = []
emails = input('Please enter your email(s) that you use for git commits. If you use more than one email, separate them with a space: ').split(' ')
if emails == ['']:
    print('Minimum one email is required. :(')
    print('Exiting...')
    exit()
print('')

GitHub_usernames_and_orgs = input('Please enter your GitHub username(s) and organization(s) separated with a space. (optional): ').split(' ')
if GitHub_usernames_and_orgs:
    GitHub_token = input('Please enter your GitHub API token (optional): ')
    for GitHub_username_or_org in GitHub_usernames_and_orgs:
        if GitHub_token:
            set_token(GitHub_token)
        print(f'Fetching GitHub repositories of GitHub user: "{GitHub_username_or_org}"...')
        git_clone_urls = get_all_repos_of_user(GitHub_username_or_org)
        print(f'Fetched {len(git_clone_urls)} repositories.')
print('')

git_clone_urls += input('Please enter git clone url(s) seperated by space (optional): ').split(' ')
print('')

git_clone_urls_ = []
for git_clone_url in git_clone_urls:
    if git_clone_url:
        git_clone_urls_.append(git_clone_url)
git_clone_urls = git_clone_urls_

if not git_clone_urls:
    print('No repositories to scan :(')
    print('Exiting...')
    exit()
repos = []
total_additions = 0
total_deletions = 0
for url in git_clone_urls:
    repos.append(Repository(url, emails))
print('Analyzing...', end='\n\n')
not_analyzed_repos = repos
while not_analyzed_repos:
    for repo in not_analyzed_repos:
        if repo.status == 'analyzed':
            total_additions += repo.additions
            total_deletions += repo.deletions
            print(
                f"""Repository: {repo.git_clone_url}
total commits: {len(repo.commits)}
Total lines added in commits: {repo.additions}
Total lines deleted in commits: {repo.deletions}
""")
            not_analyzed_repos.remove(repo)
    sleep(0.1)
print(f'Total lines added: {total_additions}')
print(f'Total lines deleted: {total_deletions}', end='\n\n')

print('Purging repositories...', end='\n\n')
clear_repos()

print('If you like this tool, kindly leave a star at https://github.com/Jothin-kumar/lines-of-code :-).')
print('Thank you!')
print('GUI version coming soon...')
