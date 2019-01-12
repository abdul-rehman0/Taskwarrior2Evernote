#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
import sys, getopt
import glob
import os
import json


def process_files(inputfile, outputdir):
    enex_notes = []
    output_filename = 'json2Evernote.enex'
    with open(inputfile) as f:
        data = json.load(f)
        for entry in data:
            print(entry);
            title = entry["description"]
            html_note_body = entry["description"]
            created_date = entry["entry"] 
            updated_date = entry["modified"]
            enex_notes.append(make_enex(title, html_note_body, created_date, updated_date))
    multi_enex_body = make_multi_enex(enex_notes)
    save_to_file(outputdir, output_filename, multi_enex_body)
    print ("Evernote file location: " + outputdir + "/" + output_filename)

def make_enex(title, body, created_date, updated_date):
    return '''<note><title>''' + title + '''</title><content><![CDATA[<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">

<en-note style="word-wrap: break-word; -webkit-nbsp-mode: space; -webkit-line-break: after-white-space;">
''' + body + '''
</en-note>]]></content><created>''' + created_date + '''</created><updated>''' + updated_date + '''</updated></note>'''


def make_multi_enex(multi_enex_body):
    return '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export2.dtd">
<en-export export-date="20150412T153431Z" application="Evernote/Windows" version="5.x">
''' + ''.join(multi_enex_body) + '''</en-export>'''


def save_to_file(outputdir, filename, body):
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
    text_file = open(outputdir + '/' + filename, "w")
    text_file.write(body)
    text_file.close()


def get_help_line():
    print ('Usage: ', sys.argv[0], ' -i <inputfile> -o <outputdir>')


def get_input_params(argv):
    inputfile = ''
    outputdir = ''
    printhelpline = 0
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "odir="])
    except getopt.GetoptError:
        exit_with_error()
    for opt, arg in opts:
        if opt == '-h':
            get_help_line()
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--odir"):
            outputdir = arg
    if (inputfile == ""):
        print ("Error: Missing input file")
        printhelpline = 1
    if (outputdir == ""):
        print ("Error: Missing output folder")
        printhelpline = 1
    if printhelpline == 1:
        exit_with_error()
    return (inputfile, outputdir)


def exit_with_error():
    get_help_line()
    sys.exit(2)


def main(argv):
    inputfile, outputdir = get_input_params(argv)
    process_files(inputfile, outputdir)


if __name__ == "__main__":
    main(sys.argv[1:])

