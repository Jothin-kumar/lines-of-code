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


def start():
    if exists("results"):
        rmtree("results")
    mkdir("results")


def end():
    rmtree("results")


class Repository:
    def __init__(self, git_clone_url):
        self.git_clone_url = git_clone_url
        self.id = sha256(git_clone_url.encode()).hexdigest()
        Thread(target=self.clone_and_get_log).start()

    def clone_and_get_log(self):
        system(f'cd repos && git clone --bare {self.git_clone_url} {self.id}')
        system('cd repos/' + self.id + " && git log --pretty=format:'%H, %an, %ae' > logs.txt")
