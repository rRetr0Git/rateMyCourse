# Author    :Albert Shen
# -*- coding: utf-8 -*-

import sys
import os

if __name__ == "__main__":
    print(os.popen("D: && "
                      "cd D:/GitHubFile/Homework-Software-engineering/rateMyCourse && "
                      "python manage.py runserver", "r").read())
    print("hello world")
