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

Author: Jothin kumar (https://jothin.tech)
Github repository of this project: https://github.com/Jothin-kumar/lines-of-code
"""
import tkinter as tk
from tkinter import simpledialog, messagebox
from requests import get
from os import mkdir
from threading import Thread
from time import sleep
from webbrowser import open_new_tab

from _lines_of_code import init, clear_repos, Repository
from _github_repos import get_all_repos_of_user, get_number_of_public_repos, set_token

users_or_orgs = []
email_list = []
repo_urls = []
repos = []
total_threads = 0
max_threads = 5
access_token = None
selected_repo = None
overall_additions = 0
overall_deletions = 0
overall_commits = 0
init()


def add_user_or_org():
    users_or_org = simpledialog.askstring('Add a GitHub user or an organization',
                                          'Enter a GitHub username or an organization:')
    if users_or_org:
        if users_or_org in users_or_orgs:
            messagebox.showwarning('Already exists', 'User/organisation already added!')
        else:
            try:
                if access_token:
                    request = get(f'https://api.github.com/users/{users_or_org}',
                                  headers={'Authorization': f'token {access_token}'})
                else:
                    request = get(f'https://api.github.com/users/{users_or_org}')
                request.json()['login']
                if get_number_of_public_repos(users_or_org) <= 50:
                    users_or_orgs.append(users_or_org)
                    refresh_usernames_and_orgs()

                    def add_repos_from_GitHub_user_or_org(user_or_org):
                        for repo in get_all_repos_of_user(user_or_org):
                            if repo not in repo_urls:
                                repo_urls.append(repo)
                                repos.append(Repository(repo, emails=email_list, auto_analyze=False))
                                refresh_repo_urls()
                                sleep(0.01)

                    Thread(target=add_repos_from_GitHub_user_or_org, args=(users_or_org,)).start()
                else:
                    messagebox.showwarning('Too many repos',
                                           'The user/organization has more than 50 public repositories.\n'
                                           'Please add the repos manually.')
            except KeyError:
                messagebox.showerror('An error occurred', f'{users_or_org} is not a valid GitHub user or organization.')


def add_email():
    email = simpledialog.askstring('Add Email', 'Enter an email:')
    if email:
        if email in email_list:
            messagebox.showwarning('Already exists', 'Email already added!')
        else:
            email_list.append(email)
            refresh_emails()
            global overall_additions
            global overall_deletions
            global overall_commits
            overall_additions = 0
            overall_deletions = 0
            overall_commits = 0
            for repo in repos:
                repo.set_emails(email_list)
                repo.set_status('Not analyzed')


def add_repo_url():
    repo_url = simpledialog.askstring('Add git repository URL', 'Enter a git repository URL:')
    if repo_url:
        if repo_url in repo_urls:
            messagebox.showwarning('Already exists', 'Repo URL already added!')
        else:
            try:
                get(repo_url)
                repo_urls.append(repo_url)
                repos.append(Repository(repo_url, emails=email_list, auto_analyze=False))
                refresh_repo_urls()
            except:
                messagebox.showerror('An error occurred', f'{repo_url} is likely not a valid git repository URL.')


def purge_repos():
    if messagebox.askokcancel('Confirmation', 'Are you sure you want to clear all repositories?'):
        if total_threads == 0:
            clear_repos()
            mkdir('repos')
            messagebox.showinfo('Success', 'All repositories have been successfully cleared.')
        else:
            messagebox.showerror('Cannot purge repositories',
                                 'Repositories can be cleared only when all threads are finished.')


def auto_analyze_repos():
    global total_threads
    total_threads = 0
    try:
        while True:
            for repo in repos:
                if repo.status == 'Not analyzed' and total_threads < max_threads:
                    Thread(target=repo.analyse).start()
                    total_threads += 1
                elif repo.status == 'Analyzed':
                    total_threads -= 1
                    repo.set_status('Successfully analyzed')
                    global overall_additions
                    global overall_deletions
                    global overall_commits
                    overall_additions += repo.additions
                    overall_deletions += repo.deletions
                    overall_commits += len(repo.commits)
            try:
                set_status(f'{total_threads} thread(s) running...')
            except NameError:
                pass
            sleep(0.1)
    except RuntimeError:
        pass


Thread(target=auto_analyze_repos).start()

root = tk.Tk()
root.title("Lines of Code - Jothin Kumar")
root.resizable(False, False)

top_frame = tk.Frame(root)
add_GitHub_user_or_org_button = tk.Button(top_frame, text="Add a GitHub user / organisation", command=add_user_or_org)
add_GitHub_user_or_org_button.grid(row=0, column=0, padx=3)
add_email_button = tk.Button(top_frame, text="Add an Email", command=add_email)
add_email_button.grid(row=0, column=1, padx=3)
add_repo_button = tk.Button(top_frame, text="Add a Repository", command=add_repo_url)
add_repo_button.grid(row=0, column=2, padx=3)


def change_max_threads():
    new_max_threads = simpledialog.askinteger('Change max threads', 'Enter the new max threads:')
    try:
        if int(new_max_threads) > 0:
            global max_threads
            max_threads = new_max_threads
            max_thread_button.config(text=f'Max threads: {max_threads}')
        else:
            messagebox.showwarning('Invalid max threads specified.', 'Max threads must be >= 1.')
    except TypeError:
        pass


max_thread_button = tk.Button(top_frame, text=f"Max Threads: {max_threads}", command=change_max_threads)
max_thread_button.grid(row=0, column=3, padx=3)
purge_button = tk.Button(top_frame, text="Purge repositories", command=purge_repos)
purge_button.grid(row=0, column=4, padx=3)


def add_github_token():
    github_token = simpledialog.askstring('Add GitHub access token', 'Enter your GitHub access token:')
    if github_token:
        set_token(github_token)
        global access_token
        access_token = github_token


add_github_token_button = tk.Button(top_frame, text="Add GitHub access token", command=add_github_token)
add_github_token_button.grid(row=0, column=5, padx=3)
top_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

status_bar_label = tk.Label(root)
status_bar_label.pack(side=tk.TOP, fill=tk.X)


def set_status(status):
    status_bar_label.config(text=status)


main_frame = tk.Frame(root, bg="lightgrey")

user_and_email_selectors = tk.Frame(main_frame)
usernames_and_orgs = tk.Listbox(user_and_email_selectors, height=15)
usernames_and_orgs.bind('<Double-Button-1>', lambda event: add_user_or_org())


def on_username_and_org_del(evt):
    w = evt.widget
    index = int(w.curselection()[0])
    usernames_or_org = w.get(index)
    window = tk.Toplevel()
    window.title(f'Delete GitHub user: {usernames_or_org}')
    window.resizable(False, False)
    tk.Label(window, text=f'Are you sure you want to delete the GitHub user or organization "{usernames_or_org}"?\nhere are the repositories owned by {usernames_or_org}', font=('Helvetica', 20)).pack(side=tk.TOP, pady=5)
    repo_list = tk.Listbox(window, height=20)
    for repo in get_all_repos_of_user(usernames_or_org):
        if repo in repo_urls:
            repo_list.insert(tk.END, repo)
    repo_list.pack(side=tk.TOP, fill=tk.X)
    def remove_user_or_org_only():
        usernames_and_orgs.delete(index)
        users_or_orgs.remove(usernames_or_org)
        window.destroy()
    def delete_all_repos():
        usernames_and_orgs.delete(index)
        users_or_orgs.remove(usernames_or_org)
        global overall_additions
        global overall_deletions
        global overall_commits
        overall_additions = 0
        overall_deletions = 0
        overall_commits = 0
        overall_commits_label.config(text='Overall commits: 0')
        overall_lines_added_label.config(text='Overall additions: 0')
        overall_lines_deleted_label.config(text='Overall deletions: 0')
        for repo_url in repo_list.get(0, tk.END):
            repo_ = get_repo_by_url(repo_url)
            repo_urls.remove(repo_url)
            repos.remove(repo_)
            status_label.config(text='', bg='lightgrey')
            total_commits.config(text='', bg='lightgrey')
            total_lines_added.config(text='', bg='lightgrey')
            total_lines_deleted.config(text='', bg='lightgrey')
            global selected_repo
            selected_repo = None
            refresh_repo_urls()
        for repo_ in repos:
            repo_.set_status('Not analyzed')
        window.destroy()
    tk.Button(window, text='Delete user or organization only', command=remove_user_or_org_only).pack(side=tk.LEFT, pady=10)
    tk.Button(window, text='Delete all repositories of this user / organization.', command=delete_all_repos).pack(side=tk.LEFT, pady=10)
    tk.Button(window, text='Cancel', command=window.destroy).pack(side=tk.LEFT, pady=10)
    window.mainloop()


usernames_and_orgs.bind('<Delete>', on_username_and_org_del)
usernames_and_orgs.pack(side=tk.TOP)


def refresh_usernames_and_orgs():
    usernames_and_orgs.delete(0, tk.END)
    for user in users_or_orgs:
        usernames_and_orgs.insert(tk.END, user)


emails = tk.Listbox(user_and_email_selectors, height=15)
emails.bind('<Double-Button-1>', lambda evt: add_email())


def on_del_key_email(evt):
    w = evt.widget
    index = int(w.curselection()[0])
    email = w.get(index)
    if email in email_list:
        confirmation = messagebox.askokcancel('Delete email', f'Are you sure you want to delete {email}?')
        if confirmation:
            email_list.remove(email)
            refresh_emails()
            global overall_additions
            global overall_deletions
            global overall_commits
            overall_additions = 0
            overall_deletions = 0
            overall_commits = 0
            overall_commits_label.config(text='Overall commits: 0')
            overall_lines_added_label.config(text='Overall additions: 0')
            overall_lines_deleted_label.config(text='Overall deletions: 0')
            for repo in repos:
                repo.set_emails(email_list)
                repo.set_status('Not analyzed')


emails.bind('<Delete>', on_del_key_email)
emails.pack(side=tk.TOP)


def refresh_emails():
    emails.delete(0, tk.END)
    for email in email_list:
        emails.insert(tk.END, email)


user_and_email_selectors.grid(row=0, column=0, padx=5, pady=2)

repo_selector = tk.Listbox(main_frame, height=30, width=50)
repo_selector.bind('<Double-Button-1>', lambda evt: add_repo_url())


def get_repo_by_url(url):
    for repo in repos:
        if repo.git_clone_url == url:
            return repo


def on_repo_select(evt):
    try:
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        global selected_repo
        selected_repo = get_repo_by_url(value)
    except IndexError:
        pass


repo_selector.bind('<<ListboxSelect>>', on_repo_select)


def on_repo_selector_del(evt):
    try:
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        confirmation = messagebox.askokcancel('Delete repository', f'Are you sure you want to delete {value}?')
        if confirmation:
            repo_selector.delete(index)
            repo = get_repo_by_url(value)
            repos.remove(repo)
            repo_urls.remove(value)
            global overall_additions
            global overall_deletions
            global overall_commits
            overall_additions -= repo.additions
            overall_deletions -= repo.deletions
            overall_commits -= len(repo.commits)
            overall_commits_label.config(text=f'Overall commits: {overall_commits}')
            overall_lines_added_label.config(text=f'Overall additions: {overall_additions}')
            overall_lines_deleted_label.config(text=f'Overall deletions: {overall_deletions}')
            status_label.config(text='', bg='lightgrey')
            total_commits.config(text='', bg='lightgrey')
            total_lines_added.config(text='', bg='lightgrey')
            total_lines_deleted.config(text='', bg='lightgrey')
            global selected_repo
            selected_repo = None
    except IndexError:
        pass


repo_selector.bind('<Delete>', on_repo_selector_del)
repo_selector.grid(row=0, column=1, padx=5, pady=2)


def refresh_repo_urls():
    repo_selector.delete(0, tk.END)
    for repo_url in repo_urls:
        repo_selector.insert(tk.END, repo_url)


result_viewer = tk.Frame(main_frame, bg='lightgrey')
status_label = tk.Label(result_viewer, bg='lightgrey', font=('Helvetica', 15))
status_label.pack(side=tk.TOP, fill=tk.X)
total_commits = tk.Label(result_viewer, bg='lightgrey')
total_commits.pack(side=tk.TOP, fill=tk.X)
total_lines_added = tk.Label(result_viewer, bg='lightgrey')
total_lines_added.pack(side=tk.TOP, fill=tk.X)
total_lines_deleted = tk.Label(result_viewer, bg='lightgrey')
total_lines_deleted.pack(side=tk.TOP, fill=tk.X)
overall_stats = tk.Frame(result_viewer, bg='lightgrey')
overall_commits_label = tk.Label(overall_stats, bg='lightgrey', font=('Ariel', 15))
overall_commits_label.pack(side=tk.TOP, fill=tk.X)
overall_lines_added_label = tk.Label(overall_stats, bg='lightgrey', font=('Ariel', 15))
overall_lines_added_label.pack(side=tk.TOP, fill=tk.X)
overall_lines_deleted_label = tk.Label(overall_stats, bg='lightgrey', font=('Ariel', 15))
overall_lines_deleted_label.pack(side=tk.TOP, fill=tk.X)
overall_stats.pack(side=tk.BOTTOM, fill=tk.X)
result_viewer.grid(row=0, column=2, padx=5, pady=2, sticky=tk.NSEW)


def refresh_result_viewer():
    try:
        while True:
            try:
                status_label.config(text=f'Status: {selected_repo.status}')
                if selected_repo.status == 'Successfully analyzed':
                    status_label.config(bg='green', fg='white')
                elif selected_repo.status == 'Analyzing':
                    status_label.config(bg='yellow', fg='black')
                elif selected_repo.status == 'Not analyzed':
                    status_label.config(bg='orange', fg='black')
                total_commits.config(text=f'Total commits: {len(selected_repo.commits)}', bg='white')
                total_lines_added.config(text=f'Additions: {selected_repo.additions}', bg='green')
                total_lines_deleted.config(text=f'Deletions: {selected_repo.deletions}', bg='red')
            except AttributeError:
                status_label.config(text='', bg='lightgrey')
            if overall_commits:
                overall_commits_label.config(text=f'Total commits: {overall_commits}', bg='white')
                overall_lines_added_label.config(text=f'Additions: {overall_additions}', bg='green')
                overall_lines_deleted_label.config(text=f'Deletions: {overall_deletions}', bg=r'red')

            def get_index(url):
                count = 0
                for repo_ in repos:
                    if repo_.git_clone_url == url:
                        return count
                    count += 1

            for repo_url in repo_urls:
                repo = get_repo_by_url(repo_url)
                try:
                    if repo.status == 'Successfully analyzed':
                        repo_selector.itemconfig(get_index(repo_url), {'bg': 'green', 'fg': 'white'})
                    elif repo.status == 'Analyzing':
                        repo_selector.itemconfig(get_index(repo_url), {'bg': 'yellow', 'fg': 'black'})
                    elif repo.status == 'Not analyzed':
                        repo_selector.itemconfig(get_index(repo_url), {'bg': 'red', 'fg': 'black'})
                except RuntimeError:
                    break
                except Exception as e:
                    print(e)
            sleep(0.1)
    except RuntimeError:
        pass


Thread(target=refresh_result_viewer).start()
main_frame.pack(side=tk.TOP, fill=tk.X, expand=True)
tk.Button(root, text='View in GitHub', font=("Ariel", 15), fg='black', bg='lightgray',
          command=lambda: open_new_tab('https://github.com/Jothin-kumar/lines-of-code')).pack(side=tk.TOP, padx=5,
                                                                                              pady=2)
tk.Button(root, text="Made by Jothin kumar", font=("Ariel", 20, 'bold'), fg='white', bg='black',
          command=lambda: open_new_tab('https://jothin.tech')).pack(side=tk.TOP, fill=tk.X)
root.mainloop()
