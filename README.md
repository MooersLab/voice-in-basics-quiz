# voice-in-basics-quiz

## Propose
Improve recall of the basic commands for the dictation plugin Voice In for Google Chrome via spaced repeated runs of an interactive quiz.

## Explanation
The quiz can be taken repeatedly five times or more in a single day become productive quickly; however, memory of the commands will fade quickly.
It is better to take the quiz every 2-3 days.

## Features
- Randomizes questions on each run
- Reports number of correct answers
- Reports time spent on quiz

## Disclaimer
This is a programming tool, not an educational tool.
It provides no explanations and no context.
The `quiz` impoves recall of computer commands in a quote manner.


## Prerequisites
You need a recent version of Python3.
You also need one external module.
Install the module **pytictoc** with pip.

```bash
pip install --user --upgrade pytictoc
```

or with a conda environement

```bash
conda activate <env name>
pip install --upgrade pip 
pip install pytictoc
```

If you have an older version of Python3, install the module **tictoc** instead.

## Run one of two ways.
You will be asked to enter a number between 1 and 1. Enter 1.
Then the interactive quiz will run.

### Run in terminal

```bash
./qVoiceIn.py
```

Enter control-D to interupt the quiz.

### Run in Jupyter
Use in Jupyter Notebook, JupyterLab, [JupyterLab.app](https://blog.jupyter.org/jupyterlab-desktop-app-now-available-b8b661b17e9a), or [nteract.app](https://nteract.io/).
The last two optioins are stand-a-lone desktop applications that do not use the browser.
You still have to have a Python3 kernel available that is mapped to a Python interpreter with the module `pytictoc` installed via pip.
Probably works in Colab, too, but you may have to load the quiz onto your Google Drive.
Select the approprite Python kernel that taps into the Python interpreter with pytictoc installed.

The advantages of this approach is that the results can be stored in the Notebook and it is more fun to run the quiz in Jupyter.

Check on present working directory in Jupyter by entering the following in a code cell.

```bash
!pwd
```

The file qVoiceTyping.py must be in your working direcotry or you must give the full file path to qVoiceTyping.py.
Enter the following in another code cell.

```bash
%run -i "qVoiceIn.py"
```
