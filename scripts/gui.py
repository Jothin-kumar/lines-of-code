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

root = tk.Tk()
root.title("Lines of Code - Jothin Kumar")
root.resizable(False, False)

user_and_email_selectors = tk.Frame(root)
usernames_and_orgs = tk.Listbox(user_and_email_selectors, height=15)
usernames_and_orgs.pack(side=tk.TOP)
emails = tk.Listbox(user_and_email_selectors, height=15)
emails.pack(side=tk.TOP)
user_and_email_selectors.grid(row=0, column=0, padx=5, pady=2)

repo_selector = tk.Listbox(root, height=30, width=50)
repo_selector.grid(row=0, column=1, padx=5, pady=2)

result_viewer = tk.Frame(root)
status_label = tk.Label(result_viewer, text="Status")
status_label.pack(side=tk.TOP, fill=tk.X)
total_commits = tk.Label(result_viewer, text="Total Commits")
total_commits.pack(side=tk.TOP, fill=tk.X)
total_lines_added = tk.Label(result_viewer, text="Total Lines Added")
total_lines_added.pack(side=tk.TOP, fill=tk.X)
total_lines_deleted = tk.Label(result_viewer, text="Total Lines Deleted")
total_lines_deleted.pack(side=tk.TOP, fill=tk.X)
overall_stats = tk.Label(result_viewer, text="Overall Stats")
overall_stats.pack(side=tk.BOTTOM, fill=tk.X)
result_viewer.grid(row=0, column=2, padx=5, pady=2, sticky=tk.NSEW)

root.mainloop()
