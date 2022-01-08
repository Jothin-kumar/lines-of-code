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
import tkinter as tk
from tkinter import simpledialog, messagebox
from requests import get

users_or_orgs = []


def add_users_or_org():
    users_or_org = simpledialog.askstring('Add a GitHub user or an organization',
                                          'Enter a GitHub username or an organization:')
    request = get(f'https://api.github.com/users/{users_or_org}')
    try:
        request.json()['login']
        users_or_orgs.append(users_or_org)
        refresh_usernames_and_orgs()
    except KeyError:
        messagebox.showerror('An error occurred', f'{users_or_org} is not a valid GitHub user or organization.')


root = tk.Tk()
root.title("Lines of Code - Jothin Kumar")
root.resizable(False, False)
top_frame = tk.Frame(root)
add_GitHub_user_or_org_button = tk.Button(top_frame, text="Add a GitHub user / organisation", command=add_users_or_org)
add_GitHub_user_or_org_button.grid(row=0, column=0, padx=3)
add_email_button = tk.Button(top_frame, text="Add an Email")
add_email_button.grid(row=0, column=1, padx=3)
add_repo_button = tk.Button(top_frame, text="Add a Repository")
add_repo_button.grid(row=0, column=2, padx=3)
max_thread_button = tk.Button(top_frame, text="Max Threads: 10")
max_thread_button.grid(row=0, column=3, padx=3)
purge_button = tk.Button(top_frame, text="Purge repositories")
purge_button.grid(row=0, column=4, padx=3)
top_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
main_frame = tk.Frame(root, bg="lightgrey")

user_and_email_selectors = tk.Frame(main_frame)
usernames_and_orgs = tk.Listbox(user_and_email_selectors, height=15)
usernames_and_orgs.pack(side=tk.TOP)


def refresh_usernames_and_orgs():
    usernames_and_orgs.delete(0, tk.END)
    for user in users_or_orgs:
        usernames_and_orgs.insert(tk.END, user)


emails = tk.Listbox(user_and_email_selectors, height=15)
emails.pack(side=tk.TOP)
user_and_email_selectors.grid(row=0, column=0, padx=5, pady=2)

repo_selector = tk.Listbox(main_frame, height=30, width=50)
repo_selector.grid(row=0, column=1, padx=5, pady=2)

result_viewer = tk.Frame(main_frame, bg='lightgrey')
status_label = tk.Label(result_viewer, text="Status", bg='lightgrey')
status_label.pack(side=tk.TOP, fill=tk.X)
total_commits = tk.Label(result_viewer, text="Total Commits", bg='lightgrey')
total_commits.pack(side=tk.TOP, fill=tk.X)
total_lines_added = tk.Label(result_viewer, text="Total Lines Added", bg='lightgrey')
total_lines_added.pack(side=tk.TOP, fill=tk.X)
total_lines_deleted = tk.Label(result_viewer, text="Total Lines Deleted", bg='lightgrey')
total_lines_deleted.pack(side=tk.TOP, fill=tk.X)
overall_stats = tk.Label(result_viewer, text="Overall Stats", bg='lightgrey')
overall_stats.pack(side=tk.BOTTOM, fill=tk.X)
result_viewer.grid(row=0, column=2, padx=5, pady=2, sticky=tk.NSEW)

main_frame.pack(side=tk.TOP, fill=tk.X, expand=True)
tk.Label(root, text="Made by Jothin kumar", font=("Ariel", 15)).pack(side=tk.TOP, fill=tk.X)
root.mainloop()
