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
import _lines_of_code


token = input('Please enter you token: ')
user_id = input('Please enter an user id (Leave blank to scan your own account): ')
if user_id:
    user_id = int(user_id)
_lines_of_code.bind('<inform>', print)
_lines_of_code.bind('<report error>', print)
_lines_of_code.crawl(
    token=token,
    user_id=user_id
)
print('Results')
print('Lines in own repos')
total_lines_added_in_own_repos = 0
total_lines_deleted_in_own_repos = 0
for own_repo in _lines_of_code.own_repos:
    total_lines_added_in_own_repos += own_repo.total_lines_of_addition
    total_lines_deleted_in_own_repos += own_repo.total_lines_of_deletion
    print('*'*15)
    print('Name:', own_repo.name)
    print('Addition:', own_repo.total_lines_of_addition)
    print('Deletion:', own_repo.total_lines_of_deletion)
    print('-'*15)
print('Lines in other repos')
total_lines_added_in_other_repos = 0
total_lines_deleted_in_other_repos = 0
for contributed_repo in _lines_of_code.contributed_repos:
    total_lines_added_in_other_repos += contributed_repo.total_lines_of_addition_in_contribution
    total_lines_deleted_in_other_repos += contributed_repo.total_lines_of_deletion_in_contribution
    print('*'*15)
    print('Name:', contributed_repo.name)
    print('Addition:', contributed_repo.total_lines_of_addition_in_contribution)
    print('Deletion:', contributed_repo.total_lines_of_deletion_in_contribution)
    print('-'*15)
print('Total lines added in repos with write access (Owned repos or collaborated repos):', total_lines_added_in_own_repos)
print('Total lines deleted in repos with write access (Owned repos or collaborated repos):', total_lines_deleted_in_own_repos)
print('Total lines added in other repos (PRs):', total_lines_added_in_other_repos)
print('Total lines deleted in other repos (PRs):', total_lines_deleted_in_other_repos)
print('Total lines added:', total_lines_added_in_own_repos + total_lines_added_in_other_repos)
print('Total lines deleted:', total_lines_deleted_in_own_repos + total_lines_deleted_in_other_repos)
