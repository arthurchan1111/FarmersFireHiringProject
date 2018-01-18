#!/usr/bin/env python2.7
from flask import Flask, render_template, request, redirect, url_for, flash


app = Flask(__name__)








if __name__ == '__main__':
    app.debug= True
    app.run(host='0.0.0.0', port=5000)
