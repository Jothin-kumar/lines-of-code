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
"""
from github import Github, Repository

function_binds = {}


def bind(id_, function):
    global function_binds
    function_binds[id_] = function


class NoBindForFunctionError(Exception):
    pass


def execute_bind(id_, message):
    try:
        function_binds[id_](message)
    except KeyError:
        raise NoBindForFunctionError(f'No bind is added for {id_}.')


class NotContributedError(Exception):
    pass

excepted_files = [
    'package.json',
    'package-lock.json',
    '.gitignore',
    'yarn.lock'
]
class ContributedRepository:
    def __init__(self, contributed_to: Repository, user):
        self.total_lines_of_addition_in_contribution = 0
        self.total_lines_of_deletion_in_contribution = 0
        self.name = contributed_to.full_name

        if contributed_to.get_commits().totalCount >= 100:
            execute_bind('<inform>', 'This repository has a lot of commits! This can take some time...')

        for commit in contributed_to.get_commits():
            if commit.author.id == user.id:
                for file in commit.files:
                    if not file.filename in excepted_files or file.filename.startswith('node_modules/'):
                        self.total_lines_of_addition_in_contribution += file.additions
                        self.total_lines_of_addition_in_contribution += file.deletions

        if not any([self.total_lines_of_addition_in_contribution, self.total_lines_of_deletion_in_contribution]):
            raise NotContributedError('User have not contributed to this repository.')


class OwnedRepository:
    def __init__(self, owned_repository: Repository, user):
        self.total_lines_of_addition = 0
        self.total_lines_of_deletion = 0
        self.name = owned_repository.name

        if (owned_repository.get_commits().totalCount >= 100):
            execute_bind('<inform>', 'This repository has a lot of commits! This can take some time...')

        for commit in owned_repository.get_commits():
            if commit.author.id == user.id:
                for file in commit.files:
                    if file.filename in excepted_files or file.filename.startswith('node_modules/'):
                        pass
                    else:
                        self.total_lines_of_addition += file.additions
                        self.total_lines_of_deletion += file.deletions

        if not any([self.total_lines_of_addition, self.total_lines_of_deletion]):
            raise NotContributedError('There aren\'t any commits that match your ID,'
                                      ' maybe you worked with other account or ID.')


contributed_repos = []
own_repos = []


def crawl(token: str, user_id=None):
    github = Github(token)

    if user_id:
        execute_bind('<inform>', f'Finding user using id: {user_id}...')
        user = github.get_user_by_id(user_id)

        if user.name:
            execute_bind('<inform>', f'Found user {user.name}!')
            execute_bind('<inform>', f'Scanning {user.name}\'s repos...')
        else:
            execute_bind('<inform>', f'Found user {user.login}!')
            execute_bind('<inform>', f'Scanning {user.login}\'s repos...')

        repos = user.get_repos()
        execute_bind('<inform>', f'Found {len(list(repos))} repos...')

        for repo in repos:
            execute_bind('<inform>', f'Crawling {repo.name}')
            if repo.fork:
                forked_from = repo.parent
                execute_bind(
                    '<inform>',
                    f'Since {repo.name} is forked from {forked_from.full_name}, crawling {forked_from.full_name}.'
                )

                try:
                    execute_bind('<inform>', f'Looking for contribution in {forked_from.full_name}')
                    try:
                        contributed_repo = ContributedRepository(contributed_to=forked_from, user=user)
                        execute_bind(
                            '<inform>',
                            f'Found {contributed_repo.total_lines_of_addition_in_contribution} additions'
                            f' and {contributed_repo.total_lines_of_deletion_in_contribution} deletions.'
                        )

                        contributed_repos.append(contributed_repo)

                    except Exception as e:
                        execute_bind('<report error>', e)

                except NotContributedError:
                    execute_bind('<inform>', f'No contribution found in {forked_from.full_name}.')

            else:
                execute_bind('<inform>', f'Looking for additions and deletions in {repo.name}...')

                try:
                    own_repo = OwnedRepository(owned_repository=repo, user=user)
                    execute_bind(
                        '<inform>',
                        f'Found {own_repo.total_lines_of_addition} additions and'
                        f' {own_repo.total_lines_of_deletion} deletions in {own_repo.name}.'
                    )
                    own_repos.append(own_repo)
                except Exception as e:
                    execute_bind('<report error>', e)
    else:
        user = github.get_user()

        if user.name:
            execute_bind('<inform>', f'Hello {user.name}!')
        else:
            execute_bind('<inform>', f'Hello {user.login}!')

        execute_bind('<inform>', 'Scanning your repos...')
        repos = user.get_repos()
        execute_bind('<inform>', f'Found {len(list(repos))} repos!')

        for repo in repos:
            execute_bind('<inform>', f'Crawling {repo.name}')

            if repo.fork:
                forked_from = repo.parent
                execute_bind(
                    '<inform>',
                    f'Since {repo.name} is forked from {forked_from.full_name}, crawling {forked_from.full_name}.'
                )
                try:
                    execute_bind('<inform>', f'Looking for contribution in {forked_from.full_name}')
                    try:
                        contributed_repo = ContributedRepository(contributed_to=forked_from, user=user)
                        execute_bind(
                            '<inform>',
                            f'Found {contributed_repo.total_lines_of_addition_in_contribution} additions'
                            f' and {contributed_repo.total_lines_of_deletion_in_contribution} deletions.'
                        )
                        contributed_repos.append(contributed_repo)

                    except Exception as e:
                        execute_bind('<report error>', e)

                except NotContributedError:
                    execute_bind('<inform>', f'No contribution found in {forked_from.full_name}')

            else:
                execute_bind('<inform>', f'Looking for additions and deletions in {repo.name}...')
                try:
                    own_repo = OwnedRepository(owned_repository=repo, user=user)
                    execute_bind(
                        '<inform>',
                        f'Found {own_repo.total_lines_of_addition} additions and '
                        f'{own_repo.total_lines_of_deletion} deletions in {own_repo.name}.'
                    )
                    own_repos.append(own_repo)
                except Exception as e:
                    execute_bind('<report error>', e)
