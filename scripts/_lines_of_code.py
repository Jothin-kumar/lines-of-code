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
from os import system, mkdir
from os.path import exists
from hashlib import sha256
from threading import Thread
from shutil import rmtree


def init():
    if exists("repos"):
        rmtree("repos")
    mkdir("repos")


def clear_repos():
    rmtree("repos")


class Commit:
    def __init__(self, commit_hash, repo_clone_url_hash):
        self.additions = 0
        self.deletions = 0
        self.commit_hash = commit_hash
        if not exists("repos/" + repo_clone_url_hash + "/commit_logs"):
            mkdir("repos/" + repo_clone_url_hash + "/commit_logs")
        system(
            'cd repos/' + repo_clone_url_hash + ' && git show --stat --oneline ' + commit_hash + ' >> commit_logs/' + commit_hash + '.txt')
        with open('repos/' + repo_clone_url_hash + '/commit_logs/' + commit_hash + '.txt') as f:
            commit_log = f.readlines()
            msg = commit_log[-1]
            words = msg.split(',')
            for word in words:
                word = word.strip()
                number = ''
                while word[0].isdigit():
                    number += word[0]
                    word = word[1:]
                word = word.strip()
                number = int(number)
                if word.startswith('insertion'):
                    self.additions += number
                elif word.startswith('deletion'):
                    self.deletions += number


class Repository:
    def __init__(self, git_clone_url, emails, auto_analyze=True):
        self.git_clone_url = git_clone_url
        self.id = sha256(git_clone_url.encode()).hexdigest()
        self.emails = emails
        self.commits = []
        self.additions = 0
        self.deletions = 0
        self.status = 'Not analyzed'

        if auto_analyze:
            Thread(target=self.analyse).start()

    def clone_and_get_log(self):
        if not exists("repos/" + self.id):
            system(f'cd repos && git clone --bare {self.git_clone_url} {self.id}')
        system('cd repos/' + self.id + " && git log --pretty=format:'%H%ae' > logs.txt")

    def analyse(self):
        self.status = 'Analyzing'
        self.clone_and_get_log()
        with open("repos/" + self.id + "/logs.txt") as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip('\n')
                email = line[40:]
                commit_hash = line[:40]
                if email in self.emails:
                    try:
                        self.commits.append(Commit(commit_hash, self.id))
                    except IndexError:
                        pass
        for commit in self.commits:
            self.additions += commit.additions
            self.deletions += commit.deletions
        self.status = 'Analyzed'

    def set_status(self, status):
        self.status = status

    def set_emails(self, emails):
        self.emails = emails
