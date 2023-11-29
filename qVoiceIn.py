#!/opt/local/bin/python3.11
# -*- coding: utf-8 -*-
# https://en.wikipedia.org/wiki/Mathematical_operators_and_symbols_in_Unicode
# For information on the q symbols package
# http://ftp.cvut.cz/tex-archive/macros/latex/contrib/qsymbols/qsymbols.pdf
# q symbols package

# prevent python2 from reading print('asd','add') as a tuple.

from __future__ import print_function

from random import shuffle
from fpdf import FPDF
from pytictoc import TicToc

import datetime
import sys
import inspect
import types

print(" ")
print("Usage: ./qVoiceIn.py")
print(" ")


'''
Note that raw_input() in Python2 is replaced with input() in Python3.

This is a very simple program that runs an interactive quiz
composed of fill in the blank and  short answers.

The quiz is assembled from a list of tuples
of questions, answers, and information source.

A List is a mutable type meaning that lists can
be modified after they have been created.
List keep order, which makes them amendable to shuffling.

A tuple is similar to a list except it is immutable.
Tuples have structure, lists have order.

Adding new tuples manually is error prone due to all of the
single quotes and commas. These are easy to omit.
Use a snippet like tup3 ior sublime text 3
with placeholders to avoid omitting this symbols.


<snippet>
    <content><![CDATA[
('${1:paster over me}','${2:paste here}','${3:paste here}'),
]]></content>
    <!-- Optional: Set a tabTrigger to define how to trigger the snippet -->
<tabTrigger>tup3</tabTrigger>
    <!-- Optional: Set a scope to limit where the snippet will trigger -->
<scope>source.python</scope>
</snippet>


Inspired by: https://www.youtube.com/watch?v=VR-yNEpGk3g

Modified to include source information in the tuple, and
to print more explanatory information such as the number
of questons in the quiz.

What is not allowed in an element of the tuple without escaping it:
    single quotes,
    double quotes,
    parentheses,
    curly braces,
    square brackets,
    colons,
    backslash,
    tilde,
    pound sign.


What is allowed?

Two ways to escape characters in a string.

escaped = a_string.translate(str.maketrans({"-":  r"\-",
  "]":  r"\]",
  "\": r"\",
  "^":  r"\^",
  "$":  r"\$",
  "*":  r"\*",
  ".":  r"\."}))


import re
escaped = re.escape(a_string)

unicode for writing equations to the terminal
source http://xahlee.info/comp/unicode_math_operators.html

α β γ δ ε ζ η θ ι κ λ μ ν ξ ο π ρ ς τ υ φ χ ψ

Superscript: ⁰ ¹ ² ³ ⁴ ⁵ ⁶ ⁷ ⁸ ⁹ ⁺ ⁻ ⁼ ⁽ ⁾

Natural Numbers ℕ,
Integers ℤ,
Rational Numbers ℚ,
Real Numbers ℝ,
Complex Numbers ℂ

circled {plus, times, …} ⊕ ⊖ ⊗ ⊘

empty set ∅

element of ∈ ∋

integrals ∫ ∬ ∭ ∮ ∯ ∰ ∱ ∲ ∳ ⨋ ⨌ ⨍ ⨎ ⨏ ⨐ ⨑ ⨒ ⨓ ⨔ ⨕ ⨖ ⨗ ⨘ ⨙ ⨚ ⨛ ⨜

n-nary sum ∑ ⨊ ⨁

n-nary product ⨀ ⨂ ∏ ∐ ⨉

Copyright Notice
================

Copyright (C) 2023
Blaine Mooers and University of Oklahoma Board of Regents

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details:
http://www.gnu.org/licenses/.
The source code in this file is copyrighted, but you can
freely use and copy it as long as you do not change or remove any of
the copyright notices.

Blaine Mooers, PhD
blaine-mooers@ouhsc.edu
975 NE 10th St, BRC 466
University of Oklahoma Health Sciences Center,
Oklahoma City, OK, USA 73104

Blaine Mooers

First version to write out a functional quiz using questions assembled
in a sqlite database of questions.
'''
__author__ = "Blaine Mooers"
__copyright__ = "2019 Board of Regents for the University of Oklahoma"
__license__ = "MIT Licencse"
__version__ = "0.1.0"
# Versioning follows follows MAJOR.MINOR[.PATCH] where major releases are
# not backward compatable.
__credits__ = [""]
# Credits are for people who have
#    tested the code,
#    reported bug fixes,
#    made suggestions, etc.
__date__ = "31 October 2019"
__maintainner__ = "Blaine Mooers"
__email__ = "blaine-mooers@ouhsc.edu"
__status__ = "Developement"

DT = datetime.datetime.now().strftime("yr%Ymo%mday%dhr%Hmin%Msec%S");

'''
The seconds are included so that the program can be rerun in less
than a minute without over writing a previous copy.
Note that the captial S gives the secconds in the current minute.
Lowercase s gives the number of seconds from some reference time.
'''

TSTAMP = str(DT);

def VoiceIn_q():
    q_VoiceIn = [
        ("Say ___ __ to introduce a line break in the Chrome browser.", "new line", "1", "1"),
    ("Say ___ __ to introduce a new paragraph in the Chrome browser.", "new paragraph", "1", "1"),
    ("Say ___ __ to paste from the clipboard in the Chrome browser.", "paste that", "1", "1"),
    ("Say ___ __ to turn on lowercase in the Chrome browser.", "caps off", "1", "1"),
    ("Say ___ __ to turn on uppercase in the Chrome browser.", "caps on", "1", "1"),
    ("Say ___ ____  _____to insert the close single quote in the Chrome browser.", "close single quote", "1", "1"),
    ("Say ___ ____ ____ to insert the open double quote in the Chrome browser.", "open double quote", "1", "1"),
    ("Say ___ ____ ____ to insert the open single quote in the Chrome browser.", "open single quote", "1", "1"),
    ("Say ___ ____ _____ to insert the close double quote in the Chrome browser.", "close double quote", "1", "1"),
    ("Say ___ ____ _____ to insert the left angle bracket < in the Chrome browser.", "open angle bracket", "1", "1"),
    ("Say ___ ____ ______ to insert the right paragraph > in the Chrome browser.", "close angle bracket", "1", "1"),
    ("Say ___ ____ to capitalize the next word in the Chrome browser.", "capitalize next", "1", "1"),
    ("Say ___ ____ to close tab in the Chrome browser.", "close tab", "1", "1"),
    ("Say ___ ____ to insert :-(", "sad face", "1", "1"),
    ("Say ___ ____ to insert :-/", "annoyed face", "1", "1"),
    ("Say ___ ____ to insert :-|", "straight face", "1", "1"),
    ("Say ___ ____ to insert ;-).", "wink face", "1", "1"),
    ("Say ___ ____ to insert a center dot.", "center dot", "1", "1"),
    ("Say ___ ____ to insert a forward slash.", "forward slash", "1", "1"),
    ("Say ___ ____ to insert a whitespace in the Chrome browser.", "insert space", "1", "1"),
    ("Say ___ ____ to insert an exclamation mark.", "exclamation mark", "1", "1"),
    ("Say ___ ____ to insert the close quote in the Chrome browser.", "close quote", "1", "1"),
    ("Say ___ ____ to insert the current date in the Chrome browser.", "insert date", "1", "1"),
    ("Say ___ ____ to insert the left brace { in the Chrome browser.", "open brace", "1", "1"),
    ("Say ___ ____ to insert the left parapgraph ( in the Chrome browser.", "open paragraph", "1", "1"),
    ("Say ___ ____ to insert the left parapgraph [ in the Chrome browser.", "open bracket", "1", "1"),
    ("Say ___ ____ to insert the open quote in the Chrome browser.", "open quote", "1", "1"),
    ("Say ___ ____ to insert the right brace } in the Chrome browser.", "close brace", "1", "1"),
    ("Say ___ ____ to insert the right paragraph ) in the Chrome browser.", "close paragraph", "1", "1"),
    ("Say ___ ____ to insert the right paragraph ] in the Chrome browser.", "close bracket", "1", "1"),
    ("Say ___ ____ to press the return or enter key in the Chrome browser.", "press enter", "1", "1"),
    ("Say ___ ____ to press the tab key in the Chrome browser.", "press tab", "1", "1"),
    ("Say ___ ____ to scroll down in the Chrome browser.", "scroll down", "1", "1"),
    ("Say ___ ____ to scroll to the bottom in the Chrome browser.", "scroll bottom", "1", "1"),
    ("Say ___ ____ to scroll to the top in the Chrome browser.", "scroll top", "1", "1"),
    ("Say ___ ____ to scroll up in the Chrome browser.", "scroll up", "1", "1"),
    ("Say ___ ____ to stop dictation in the Chrome browser.", "stop dictation", "1", "1"),
    ("Say ___ _____ to delete last word in the Chrome browser.", "delete word", "1", "1"),
    ("Say ___ to undo in the Chrome browser.", "undo", "1", "1"),
    ("Say ____ ___ to insert a vertical bar.", "vertical bar", "1", "1"),
    ("Say ____ to insert :-)", "smiley", "1", "1"),
    ("Say ____ to insert a comma.", "comma", "1", "1"),
    ("Say ____ to insert a degree sign.", "degree", "1", "1"),
    ("Say ____ to insert a em-dash.", "dash", "1", "1"),
    ("Say ____ to insert a en-dash.", "hyphen", "1", "1"),
    ("Say ____ to insert a hashtag.", "hashtag", "1", "1"),
    ("Say ____ to insert a period.", "period", "1", "1"),
    ("Say ____ to insert a semicolon.", "semicolon", "1", "1"),
    ("Say ____ to insert an ampersand sign.", "ampersand", "1", "1"),
    ("Say ____ to insert an ellipsis.", "ellipsis", "1", "1"),
    ("Say ____ to insert an underscore.", "underscore", "1", "1"),
    ]

    shuffle(q_VoiceIn)
    print('A quiz about VoiceIn.')
    print('The quiz is designed to refresh the memory.')
    print('Spending ten minutes with this quiz after a hiatas from Voice In could \
save you hours via improved efficiency.')
    print('\n')
    print('The non-home keystrokes are abbreviated as follows: ')
    print('\n')
    print('    S for shift key')
    print('    ^ for control key')
    print('    - for minus')
    print('    A for alternate key')
    print('    cmd for command key')
    print('    ret for return or enter')
    print('    del for delete')
    print('    bksp for backspace')
    print('    single quotes for quotes. Escape double quotes.')  
    print('\n')
    print('This quiz has %d fill-in-the-blank or \
short-answer questions.'  % (len(q_VoiceIn)) )
    print('Each question in the quiz is asked \
just once if it is answered correctly.')
    print('Incorrectly answered questions will \
be recycled until they are answered correctly.')
    print('The questions are randomly shuffled upon \
start-up of the script, so each quiz is a new adventure!')
    print('If you do not know the answer, \
enter "return", and it will be printed to the terminal.')
    print('\n')
    return q_VoiceIn
    
 

# %%%%%%%%%%%%%%%%%%%%%%%%% Utitlity functions %%%%%%%%%%%%%%%%%%%%%%%%%
def is_local(object):
    """This function is used to list the locally defined functions"""
    return isinstance(object,
                      types.FunctionType) and object.__module__ == __name__


def writeQtoTex(QUESTION_ANSWER_SOURCE):    
    """
    Write the questions to a Tex file.
    """
    output1 = open(homePath + fileStemName + "Questions" + TSTAMP + ".tex", "a")
    
    latexHead = r"""
\documentclass[11pt]{article}
\usepackage[portrvoicet, letterpaper, margin=0.75in]{geometry}
\usepackage{txfonts}
\usepackage{underscore}
\usepackage{titling}
\setlength{\droptitle}{-3cm}

\title{A quiz about SUBQUIZ in TOPIC \vspace{-2ex}}
\author{Blaine Mooers \vspace{-10ex}}
\date{\today \vspace{-2ex}}
\begin{document}
\maketitle
\noindent Date and Time: """ + TSTAMP + r"\\" + "\n"
    output1.write(latexHead)
    cited = set()
    for count, (question,
                correct_answer,
                explanation,
                source) in enumerate(QUESTION_ANSWER_SOURCE, start=1):
        if source not in cited:
            cited.add(source)
        outp1 = str(count) + ". " + question + r" \\" + "\n"
        output1.write(outp1)

    latexTvoicel = r"\end{document}"
    output1.write(latexTvoicel)
    output1.close()
    return


def writeAtoTex(QUESTION_ANSWER_SOURCE):    
    """
    Write the answers to a Tex file.
    """
    output1 = open(homePath + fileStemName + "Answers" + TSTAMP + ".tex", "a")
    
    latexHead = r"""
\documentclass[11pt]{article}
\usepackage[portrvoicet, letterpaper, margin=0.75in]{geometry}
\usepackage{txfonts}
\usepackage{underscore}
\usepackage{titling}
\setlength{\droptitle}{-3cm}

\title{A quiz about SUBQUIZ in TOPIC \vspace{-2ex}}
\author{Blaine Mooers \vspace{-10ex}}
\date{\today\vspace{-2ex}}
\begin{document}
\maketitle
\noindent Date and Time: """ + TSTAMP + r"\\" + "\n"

    output1.write(latexHead)
    cited = set()
    for count, (question,
                correct_answer,
                explanation,
                source) in enumerate(QUESTION_ANSWER_SOURCE, start=1):
        if source not in cited:
            cited.add(source)
        outp1 = str(count) + ". " + correct_answer + r" \\" + "\n"
        output1.write(outp1)

    latexTvoicel = r"\end{document}"
    output1.write(latexTvoicel)
    output1.close()
    return


def writeEtoTex(QUESTION_ANSWER_SOURCE):    
    """
    Write the explanations to a Tex file.
    """
    output1 = open(homePath + fileStemName + "Explanations" + TSTAMP + ".tex", "a")
    
    latexHead = r"""
\documentclass[11pt]{article}
\usepackage[portrvoicet, letterpaper, margin=0.75in]{geometry}
\usepackage{txfonts}
\usepackage{underscore}
\usepackage{titling}
\setlength{\droptitle}{-3cm}

\title{A quiz about SUBQUIZ in TOPIC \vspace{-2ex}}
\author{Blaine Mooers \vspace{-10ex}}
\date{\today\vspace{-2ex}}
\begin{document}
\maketitle
\noindent Date and Time: """ + TSTAMP + r"\\" + "\n"

    output1.write(latexHead)

    for count, (question,
                correct_answer,
                explanation,
                source) in enumerate(QUESTION_ANSWER_SOURCE, start=1):
#        if source not in cited:
#            cited.add(source)
        outp1 = str(count) + ". " + explanation + r" \\" + "\n"
        output1.write(outp1)

    latexTvoicel = r"\end{document}"
    output1.write(latexTvoicel)
    output1.close()
    return


def writeStoTex(QUESTION_ANSWER_SOURCE):    
    """
    Write the explanations to a Tex file.
    """
    output1 = open(homePath + fileStemName + "Sources" + TSTAMP + ".tex", "a")
    
    latexHead = r"""
\documentclass[11pt]{article}
\usepackage[portrvoicet, letterpaper, margin=0.75in]{geometry}
\usepackage{txfonts}
\usepackage{underscore}
\usepackage{titling}
\setlength{\droptitle}{-3cm}

\title{A quiz about SUBQUIZ in TOPIC \vspace{-2ex}}
\author{Blaine Mooers \vspace{-10ex}}
\date{\today\vspace{-2ex}}
\begin{document}
\maketitle
\noindent Date and Time: """ + TSTAMP + r"\\" + "\n"
    output1.write(latexHead)
    cited = set()
    for count, (question,
                correct_answer,
                explanation,
                source) in enumerate(QUESTION_ANSWER_SOURCE, start=1):
        if source not in cited:
            cited.add(source)
        outp1 = str(count) + ". " + source + r" \\" + "\n"
        output1.write(outp1)

    latexTvoicel = r"\end{document}"
    output1.write(latexTvoicel)
    output1.close()
    return


def write_pdf(QUESTION_ANSWER_SOURCE):
    """
    This function writes out the quiz to a pdf with
    the answers and refernces on separate pages.
    """
    pdf = FPDF(format='letter')
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 10)
    pdf.set_left_margin(20)
    outp11 = ('Quiz about ' + SUBQUIZ + ' in ' + TOPIC + ', Blaine Mooers   ')
    pdf.cell(0, 10, outp11 + TSTAMP, border=0, ln=1)
    # FPDF.set_auto_page_break(auto: bool, margin = 0.0)
    pdf.set_font('Arial', '', 10)
    """
    Note that the multi_cell method is required for
    text that spans multiple lines. The alternate is cell().
    The first parameter of multi_cell() controls the width of the text.

    """
    cited = set()
    for count, (question,
                correct_answer,
                explanation,
                source) in enumerate(QUESTION_ANSWER_SOURCE, start=1):
        if source not in cited:
            cited.add(source)
        outp1 = str(count) + '. ' + question + '\n'
        pdf.multi_cell(170, 5, outp1, 0)

    pdf.add_page()
    pdf.set_font('Arial', 'B', 10)
    outp12 = 'Answers to quiz about ' + SUBQUIZ + ' in ' + TOPIC + '     '
    pdf.cell(0, 10, outp12 + TSTAMP, border=0, ln=1)
    pdf.set_font('Arial', '', 10)
    for count, (question,
                correct_answer,
                explanation,
                source) in enumerate(QUESTION_ANSWER_SOURCE, start=1):
        outp2 = str(count) + '. ' + correct_answer + '\n'
        pdf.multi_cell(170, 5, outp2, 0)

    pdf.add_page()
    pdf.set_font('Arial', 'B', 10)
    outp13 = 'References cited in quiz about ' + SUBQUIZ + ' in ' + TOPIC + '     '
    pdf.cell(0, 10, outp13 + TSTAMP, border=0, ln=1)
    pdf.set_font('Arial', '', 10)
    sortcited = sorted(cited)
    for count, ref in enumerate(sortcited, start=1):
        outp3 = str(count) + '. ' + ref + '\n'
        pdf.multi_cell(170, 5, outp3, 0)

    pdf.output('voiceQuiz' + SUBQUIZ + TSTAMP + '.pdf')
    pdf.close()


def write_pdfall(QUESTION_ANSWER_SOURCE, SUBQUIZ, TOPIC):
    """
    This function writes out each quiz to a PDF with
    the answers and refernces on separate pages.
    It works with write_all() which writes out all of the quizzes at once.
    """
    pdf = FPDF(format='letter')
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 10)
    pdf.set_left_margin(20)
    outp11 = ('Quiz about voice control software. The subtopic is ' + SUBQUIZ + ' in ' + TOPIC + ', Blaine Mooers   ')
    pdf.cell(0, 10, outp11 + TSTAMP, border=0, ln=1)
    # FPDF.set_auto_page_break(auto: bool, margin = 0.0)
    pdf.set_font('Arial', '', 10)
    """
    Note that the multi_cell method is required for
    text that spans multiple lines. The alternate is cell().
    The first parameter of multi_cell() controls the width of the text.

    """
    cited = set()
    for count, (question,
                correct_answer,
                explanation,
                source) in enumerate(QUESTION_ANSWER_SOURCE, start=1):
        if source not in cited:
            cited.add(source)
        outp1 = str(count) + '. ' + question + '\n'
        pdf.multi_cell(170, 5, outp1, 0)

    pdf.add_page()
    pdf.set_font('Arial', 'B', 10)
    outp12 = 'Answers to quiz about ' + SUBQUIZ + ' in ' + TOPIC + '     '
    pdf.cell(0, 10, outp12 + TSTAMP, border=0, ln=1)
    pdf.set_font('Arial', '', 10)
    for count, (question,
                correct_answer,
                explanation,
                source) in enumerate(QUESTION_ANSWER_SOURCE, start=1):
        outp2 = str(count) + '. ' + correct_answer + '\n'
        pdf.multi_cell(170, 5, outp2, 0)

    pdf.add_page()
    pdf.set_font('Arial', 'B', 10)
    outp13 = 'References cited in quiz about ' + SUBQUIZ + ' in ' + TOPIC + '     '
    pdf.cell(0, 10, outp13 + TSTAMP, border=0, ln=1)
    pdf.set_font('Arial', '', 10)
    sortcited = sorted(cited)
    for count, ref in enumerate(sortcited, start=1):
        outp3 = str(count) + '. ' + ref + '\n'
        pdf.multi_cell(170, 5, outp3, 0)

    pdf.output('voiceQuiz' + SUBQUIZ + TSTAMP + '.pdf')
    pdf.close()


def quiz_me(QUESTION_ANSWER_SOURCE):
    """
    This is the function
    that runs the quizzes.
    """
    t = TicToc()
    t.tic()
    numCorrect = 0
    wrong = []
    for question, correct_answer, explanation, source in QUESTION_ANSWER_SOURCE:
        # answer = input(question.encode('utf-8').decode('utf-8') + ' ')

        answer = input(question + ' ')
        if answer == correct_answer:
            print('    Correct! :) \n')
            numCorrect += 1
        else:
            print('      The answer is "' + correct_answer + '".')
            print('        Explanation: "' + explanation + '".')
            print('          Find more information in ' + source + '.\n')
            redo = (question, correct_answer, explanation, source)
            wrong.append(redo)
            # When five wrong answers have accumulated, the questions are
            # repeated they are answered correctly then the next question
            # in the main list is invoked.
            if len(wrong) == 5:
                print('The last five wrongly-answered questions will \
be repeated once before advancing to new questions.')
                for question2, correct_answer2, explanation2, source2 in wrong[:]:
                    answer2 = input(question2 + ' ')
                    if answer2 == correct_answer2:
                        print('    Correct! :) \n')
                        wrong.remove((question2,
                                      correct_answer2, explanation2, source2))
                        print('                        Number of wrongly \
                              answered questions: ' +
                              str(len(wrong)) + '\n')
                    else:
                        print('      The answer is "'+ correct_answer2 + '".')
                        print('        Explanation: "' + explanation + '".')
                        print('            Find more information in '
                              + source2 + '.')
                        redo2 = (question2,
                                 correct_answer2,
                                 explanation2, source2)
                        wrong.append(redo2)
                        print('            Number of wrongly \
                        answered questions: ' + str(len(wrong)) + '\n')
            
# https://www.pythoncentral.io/how-to-slice-listsarrays-and-tuples-in-python

    print('End of quiz with %d questions.' % (len(QUESTION_ANSWER_SOURCE)))
    print('%d questions correct and %d wrong.' % (numCorrect,
                                                  len(QUESTION_ANSWER_SOURCE) -
                                                  numCorrect))
    t.toc()
    print('\n' + 'Time elapsed: ' + str(t.elapsed) + ' seconds.' + '\n' )
    if len(QUESTION_ANSWER_SOURCE) == numCorrect:
        print('Congratulations! You are ready to use voice control! :)')
    else:
        print('\n'
             + 'Please try until again until you get a perfect score three times in a row.' 
             + 'Try again with a spaced interval (two days is optimal). Repeat five times to improve your recall.'
             + 'You can use the alphabet in command mode to enter the letters by voice. Say "enter" in place of hitting "return".' 
             + 'This is a nice way to build "voice" memory of the alphabet. Cool, use your voice to take a quiz on voice control!'
             + 'You need have a terminal.talon configuration file in ~/.talon/user/<yourname>-talon/ with "tag: terminal" on the first line.'
             + '\n' 
             
             + '\n'
             + "Amateurs prepare until they can \
get it right. Professional prepare until they cannot \
get it wrong." 
             + '\n' 
             + '   -- Julie Andrews')
    print('\n')
    print('Literature Cited')
    print('\n')
    lambda cited: list(map(print, cited))
    return



# %%%%%%%%%%%%%%%%%%%%%%%%% Utitlity functions %%%%%%%%%%%%%%%%%%%%%%%%%
def is_local(object):
    """This function is used to list the locally defined functions"""
    return isinstance(object,
                      types.FunctionType) and object.__module__ == __name__


def writeQtoTex(QUESTION_ANSWER_SOURCE):    
    """
    Write the questions to a Tex file.
    """
    output1 = open(homePath + fileStemName + "Questions" + TSTAMP + ".tex", "a")
    
    latexHead = r"""
\documentclass[11pt]{article}
\usepackage[portrvoicet, letterpaper, margin=0.75in]{geometry}
\usepackage{txfonts}
\usepackage{underscore}
\usepackage{titling}
\setlength{\droptitle}{-3cm}

\title{A quiz about SUBQUIZ in TOPIC \vspace{-2ex}}
\author{Blaine Mooers \vspace{-10ex}}
\date{\today \vspace{-2ex}}
\begin{document}
\maketitle
\noindent Date and Time: """ + TSTAMP + r"\\" + "\n"
    output1.write(latexHead)
    cited = set()
    for count, (question,
                correct_answer,
                explanation,
                source) in enumerate(QUESTION_ANSWER_SOURCE, start=1):
        if source not in cited:
            cited.add(source)
        outp1 = str(count) + ". " + question + r" \\" + "\n"
        output1.write(outp1)

    latexTvoicel = r"\end{document}"
    output1.write(latexTvoicel)
    output1.close()
    return


def writeAtoTex(QUESTION_ANSWER_SOURCE):    
    """
    Write the answers to a Tex file.
    """
    output1 = open(homePath + fileStemName + "Answers" + TSTAMP + ".tex", "a")
    
    latexHead = r"""
\documentclass[11pt]{article}
\usepackage[portrvoicet, letterpaper, margin=0.75in]{geometry}
\usepackage{txfonts}
\usepackage{underscore}
\usepackage{titling}
\setlength{\droptitle}{-3cm}

\title{A quiz about SUBQUIZ in TOPIC \vspace{-2ex}}
\author{Blaine Mooers \vspace{-10ex}}
\date{\today\vspace{-2ex}}
\begin{document}
\maketitle
\noindent Date and Time: """ + TSTAMP + r"\\" + "\n"

    output1.write(latexHead)
    cited = set()
    for count, (question,
                correct_answer,
                explanation,
                source) in enumerate(QUESTION_ANSWER_SOURCE, start=1):
        if source not in cited:
            cited.add(source)
        outp1 = str(count) + ". " + correct_answer + r" \\" + "\n"
        output1.write(outp1)

    latexTvoicel = r"\end{document}"
    output1.write(latexTvoicel)
    output1.close()
    return


def writeEtoTex(QUESTION_ANSWER_SOURCE):    
    """
    Write the explanations to a Tex file.
    """
    output1 = open(homePath + fileStemName + "Explanations" + TSTAMP + ".tex", "a")
    
    latexHead = r"""
\documentclass[11pt]{article}
\usepackage[portrvoicet, letterpaper, margin=0.75in]{geometry}
\usepackage{txfonts}
\usepackage{underscore}
\usepackage{titling}
\setlength{\droptitle}{-3cm}

\title{A quiz about SUBQUIZ in TOPIC \vspace{-2ex}}
\author{Blaine Mooers \vspace{-10ex}}
\date{\today\vspace{-2ex}}
\begin{document}
\maketitle
\noindent Date and Time: """ + TSTAMP + r"\\" + "\n"

    output1.write(latexHead)

    for count, (question,
                correct_answer,
                explanation,
                source) in enumerate(QUESTION_ANSWER_SOURCE, start=1):
#        if source not in cited:
#            cited.add(source)
        outp1 = str(count) + ". " + explanation + r" \\" + "\n"
        output1.write(outp1)

    latexTvoicel = r"\end{document}"
    output1.write(latexTvoicel)
    output1.close()
    return


def writeStoTex(QUESTION_ANSWER_SOURCE):    
    """
    Write the explanations to a Tex file.
    """
    output1 = open(homePath + fileStemName + "Sources" + TSTAMP + ".tex", "a")
    
    latexHead = r"""
\documentclass[11pt]{article}
\usepackage[portrvoicet, letterpaper, margin=0.75in]{geometry}
\usepackage{txfonts}
\usepackage{underscore}
\usepackage{titling}
\setlength{\droptitle}{-3cm}

\title{A quiz about SUBQUIZ in TOPIC \vspace{-2ex}}
\author{Blaine Mooers \vspace{-10ex}}
\date{\today\vspace{-2ex}}
\begin{document}
\maketitle
\noindent Date and Time: """ + TSTAMP + r"\\" + "\n"
    output1.write(latexHead)
    cited = set()
    for count, (question,
                correct_answer,
                explanation,
                source) in enumerate(QUESTION_ANSWER_SOURCE, start=1):
        if source not in cited:
            cited.add(source)
        outp1 = str(count) + ". " + source + r" \\" + "\n"
        output1.write(outp1)

    latexTvoicel = r"\end{document}"
    output1.write(latexTvoicel)
    output1.close()
    return


def write_pdf(QUESTION_ANSWER_SOURCE):
    """
    This function writes out the quiz to a pdf with
    the answers and refernces on separate pages.
    """
    pdf = FPDF(format='letter')
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 10)
    pdf.set_left_margin(20)
    outp11 = ('Quiz about ' + SUBQUIZ + ' in ' + TOPIC + ', Blaine Mooers   ')
    pdf.cell(0, 10, outp11 + TSTAMP, border=0, ln=1)
    # FPDF.set_auto_page_break(auto: bool, margin = 0.0)
    pdf.set_font('Arial', '', 10)
    """
    Note that the multi_cell method is required for
    text that spans multiple lines. The alternate is cell().
    The first parameter of multi_cell() controls the width of the text.

    """
    cited = set()
    for count, (question,
                correct_answer,
                explanation,
                source) in enumerate(QUESTION_ANSWER_SOURCE, start=1):
        if source not in cited:
            cited.add(source)
        outp1 = str(count) + '. ' + question + '\n'
        pdf.multi_cell(170, 5, outp1, 0)

    pdf.add_page()
    pdf.set_font('Arial', 'B', 10)
    outp12 = 'Answers to quiz about ' + SUBQUIZ + ' in ' + TOPIC + '     '
    pdf.cell(0, 10, outp12 + TSTAMP, border=0, ln=1)
    pdf.set_font('Arial', '', 10)
    for count, (question,
                correct_answer,
                explanation,
                source) in enumerate(QUESTION_ANSWER_SOURCE, start=1):
        outp2 = str(count) + '. ' + correct_answer + '\n'
        pdf.multi_cell(170, 5, outp2, 0)

    pdf.add_page()
    pdf.set_font('Arial', 'B', 10)
    outp13 = 'References cited in quiz about ' + SUBQUIZ + ' in ' + TOPIC + '     '
    pdf.cell(0, 10, outp13 + TSTAMP, border=0, ln=1)
    pdf.set_font('Arial', '', 10)
    sortcited = sorted(cited)
    for count, ref in enumerate(sortcited, start=1):
        outp3 = str(count) + '. ' + ref + '\n'
        pdf.multi_cell(170, 5, outp3, 0)

    pdf.output('voiceQuiz' + SUBQUIZ + TSTAMP + '.pdf')
    pdf.close()


def write_pdfall(QUESTION_ANSWER_SOURCE, SUBQUIZ, TOPIC):
    """
    This function writes out each quiz to a PDF with
    the answers and refernces on separate pages.
    It works with write_all() which writes out all of the quizzes at once.
    """
    pdf = FPDF(format='letter')
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 10)
    pdf.set_left_margin(20)
    outp11 = ('Quiz about voice control software. The subtopic is ' + SUBQUIZ + ' in ' + TOPIC + ', Blaine Mooers   ')
    pdf.cell(0, 10, outp11 + TSTAMP, border=0, ln=1)
    # FPDF.set_auto_page_break(auto: bool, margin = 0.0)
    pdf.set_font('Arial', '', 10)
    """
    Note that the multi_cell method is required for
    text that spans multiple lines. The alternate is cell().
    The first parameter of multi_cell() controls the width of the text.

    """
    cited = set()
    for count, (question,
                correct_answer,
                explanation,
                source) in enumerate(QUESTION_ANSWER_SOURCE, start=1):
        if source not in cited:
            cited.add(source)
        outp1 = str(count) + '. ' + question + '\n'
        pdf.multi_cell(170, 5, outp1, 0)

    pdf.add_page()
    pdf.set_font('Arial', 'B', 10)
    outp12 = 'Answers to quiz about ' + SUBQUIZ + ' in ' + TOPIC + '     '
    pdf.cell(0, 10, outp12 + TSTAMP, border=0, ln=1)
    pdf.set_font('Arial', '', 10)
    for count, (question,
                correct_answer,
                explanation,
                source) in enumerate(QUESTION_ANSWER_SOURCE, start=1):
        outp2 = str(count) + '. ' + correct_answer + '\n'
        pdf.multi_cell(170, 5, outp2, 0)

    pdf.add_page()
    pdf.set_font('Arial', 'B', 10)
    outp13 = 'References cited in quiz about ' + SUBQUIZ + ' in ' + TOPIC + '     '
    pdf.cell(0, 10, outp13 + TSTAMP, border=0, ln=1)
    pdf.set_font('Arial', '', 10)
    sortcited = sorted(cited)
    for count, ref in enumerate(sortcited, start=1):
        outp3 = str(count) + '. ' + ref + '\n'
        pdf.multi_cell(170, 5, outp3, 0)

    pdf.output('voiceQuiz' + SUBQUIZ + TSTAMP + '.pdf')
    pdf.close()


def quiz_me(QUESTION_ANSWER_SOURCE):
    """
    This is the function
    that runs the quizzes.
    """
    t = TicToc()
    t.tic()
    numCorrect = 0
    wrong = []
    for question, correct_answer, explanation, source in QUESTION_ANSWER_SOURCE:
        # answer = input(question.encode('utf-8').decode('utf-8') + ' ')

        answer = input(question + ' ')
        if answer == correct_answer:
            print('    Correct! :) \n')
            numCorrect += 1
        else:
            print('      The answer is "' + correct_answer + '".')
            print('        Explanation: "' + explanation + '".')
            print('          Find more information in ' + source + '.\n')
            redo = (question, correct_answer, explanation, source)
            wrong.append(redo)
            # When five wrong answers have accumulated, the questions are
            # repeated they are answered correctly then the next question
            # in the main list is invoked.
            if len(wrong) == 5:
                print('The last five wrongly-answered questions will \
be repeated once before advancing to new questions.')
                for question2, correct_answer2, explanation2, source2 in wrong[:]:
                    answer2 = input(question2 + ' ')
                    if answer2 == correct_answer2:
                        print('    Correct! :) \n')
                        wrong.remove((question2,
                                      correct_answer2, explanation2, source2))
                        print('                        Number of wrongly \
                              answered questions: ' +
                              str(len(wrong)) + '\n')
                    else:
                        print('      The answer is "'+ correct_answer2 + '".')
                        print('        Explanation: "' + explanation + '".')
                        print('            Find more information in '
                              + source2 + '.')
                        redo2 = (question2,
                                 correct_answer2,
                                 explanation2, source2)
                        wrong.append(redo2)
                        print('            Number of wrongly \
                        answered questions: ' + str(len(wrong)) + '\n')
            
# https://www.pythoncentral.io/how-to-slice-listsarrays-and-tuples-in-python

    print('End of quiz with %d questions.' % (len(QUESTION_ANSWER_SOURCE)))
    print('%d questions correct and %d wrong.' % (numCorrect,
                                                  len(QUESTION_ANSWER_SOURCE) -
                                                  numCorrect))
    t.toc()
    print('\n' + 'Time elapsed: ' + str(t.elapsed) + ' seconds.' + '\n' )
    if len(QUESTION_ANSWER_SOURCE) == numCorrect:
        print('Congratulations! You are ready to use voice control! :)')
    else:
        print('\n'
             + 'Please try until again until you get a perfect score three times in a row.' 
             + 'Try again with a spaced interval (two days is optimal). Repeat five times to improve your recall.'
             + 'You can use the alphabet in command mode to enter the letters by voice. Say "enter" in place of hitting "return".' 
             + 'This is a nice way to build "voice" memory of the alphabet. Cool, use your voice to take a quiz on voice control!'
             + 'You need have a terminal.talon configuration file in ~/.talon/user/<yourname>-talon/ with "tag: terminal" on the first line.'
             + '\n' 
             
             + '\n'
             + "Amateurs prepare until they can \
get it right. Professional prepare until they cannot \
get it wrong." 
             + '\n' 
             + '   -- Julie Andrews')
    print('\n')
    print('Literature Cited')
    print('\n')
    lambda cited: list(map(print, cited))
    return


def write_all():
    """This function writes out all of the quizzes to PDFs.""" 
    hlimit = 1 + 1
    xxx = range(1,hlimit)
    for SELECTEDQ in xxx:
        if SELECTEDQ == 1:
            QUESTION_ANSWER_SOURCE = VoiceIn_q()
            SUBQUIZ = "VoiceIn"
            TOPIC = "Clojure"
            write_pdfall(QUESTION_ANSWER_SOURCE, SUBQUIZ, TOPIC)
    return


def interactive_quiz():
    """This function runs the quiz interactives.""" 
    while True:
        print("List of locally defined functions:")
        print("\n")
        # This should probably be an externally defined function.
        print([name for name,
               value in inspect.getmembers(sys.modules[__name__],
               predicate=is_local)])
        # Define settings 
        fileStemName = "qvoice"
        homePath = "/Users/blaine/6254qvoice/" 
        table_name = "qvoice"
        topic = "Clojure"
        print("\n")
        print("Select one quiz about Clojure:" + "\n")
        
        print("1.  VoiceIn")
        print("\n")
        while True:
            value = input("Enter integer between 1 and 1 :")
            try:
                SELECTEDQ = int(value)
            except ValueError:
                print("Enter an integer, please")
                continue
            if 1 <= SELECTEDQ <= 1:
                break
            else:
                print("Out of valid range. Please re-enter integer from this range: 1 - 1")
    
        if SELECTEDQ == 1:
            QUESTION_ANSWER_SOURCE = VoiceIn_q()
            SUBQUIZ = "VoiceIn"
            TOPIC = "Clojure"
            write_pdfall(QUESTION_ANSWER_SOURCE, SUBQUIZ, TOPIC)
        quiz_me(QUESTION_ANSWER_SOURCE)
        reply = input('Enter text, [type \"stop\" to quit or hit the Enter (or Return key) to select another quiz]: ')
        print(reply.lower())
        if reply == 'stop':
            break
    return


if __name__== "__main__":
    #writeQtoTex(QUESTION_ANSWER_SOURCE)
    #writeAtoTex(QUESTION_ANSWER_SOURCE)
    #writeEtoTex(QUESTION_ANSWER_SOURCE)
    #writeStoTex(QUESTION_ANSWER_SOURCE)
    #write_pdf(QUESTION_ANSWER_SOURCE)
    # To write all quizzes to PDFs, uncomment write_all() and
    # comment out all lines down to the bottom of the file.
    #write_all() 
    interactive_quiz()
        
