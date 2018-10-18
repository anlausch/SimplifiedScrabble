#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, redirect, url_for, Response
from logging.handlers import RotatingFileHandler
from time import strftime
import traceback
import logging
from flask_bootstrap import Bootstrap
import scrabble
import json


class Server:
    def __init__(self):
        print("Server initialized")

    def set_game(self, scrabble):
        self.scrabble = scrabble


server = Server()
app = Flask(__name__)
Bootstrap(app)


@app.route('/init', methods=['POST'])
def create_board():
    '''
    Returns a board with random letters to be rendered in the template
    '''
    try:
        dimension = request.form["dimension"]
        if dimension is None or dimension == "" or dimension == " ":
            logger.error("No data provided")
            return render_template("index.html", error="Bitte gib die Dimension des zu erstellenden Spielfeldes ein.")

        logger.info("Selected dimension: " + json.dumps(dimension))
        dimension = int(dimension)
        server.scrabble.create_board(dim=dimension)
        #server.scrabble.get_solutions()
        return render_template("index.html", board=server.scrabble.board)
    except Exception as e:
        return str(e)


@app.route('/solution', methods=['POST'])
def show_solution():
    try:
        server.scrabble.get_solutions()
        return json.dumps(server.scrabble.allsolutions)
    except Exception as e:
        return str(e)


@app.route('/validate', methods=['POST'])
def validate():
    try:
        server.scrabble.get_solutions()
        word = request.form["data"]
        valid = server.scrabble.validate_solutions([word])
        if len(valid) == 0:
            return json.dumps(False)
        else:
            return json.dumps(True)
    except Exception as e:
        return str(e)


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
@app.route('/init', methods=['GET'])
@app.route('/solution', methods=['GET'])
@app.route('/validate', methods=['GET'])
def index():
    return render_template("index.html")



@app.after_request
def after_request(response):
    """ Logging after every request. """
    # This avoids the duplication of registry in the log,
    # since that 500 is already logged via @app.errorhandler.
    if response.status_code != 500:
        ts = strftime('[%Y-%b-%d %H:%M]')
        logger.error('%s %s %s %s %s %s',
                      ts,
                      request.remote_addr,
                      request.method,
                      request.scheme,
                      request.full_path,
                      response.status)
    return response


@app.errorhandler(Exception)
def exceptions(e):
    """ Logging after every Exception. """
    ts = strftime('[%Y-%b-%d %H:%M]')
    tb = traceback.format_exc()
    logger.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s',
                  ts,
                  request.remote_addr,
                  request.method,
                  request.scheme,
                  request.full_path,
                  tb)
    return "Internal Server Error", 500


if __name__ == '__main__':
    print("Starting server")
    scrb = scrabble.Scrabble()
    server.set_game(scrb)
    handler = RotatingFileHandler('./log/app.log', maxBytes=10000, backupCount=3)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    app.run(port=8000)