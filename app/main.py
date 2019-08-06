from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash
from app.__init__ import *

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'