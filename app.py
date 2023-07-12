import time
import os
import account
from random import *
from flask import Flask, url_for, render_template, request, redirect, session, jsonify, flash, send_file
from datetime import datetime
from model2 import db
from bson.objectid import ObjectId

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('/index2.html')

if __name__ == '__main__':
    app.secret_key = "123"
    app.run('0.0.0.0', debug=True)
