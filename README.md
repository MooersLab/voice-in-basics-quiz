![version](https://img.shields.io/static/v1?label=voice-in-basics-quiz&message=0.6&color=brightcolor)
[![license: mit](https://img.shields.io/badge/license-mit-blue.svg)](https://opensource.org/licenses/mit)


# voice-in-basics-quiz

## Propose
An interactive quiz with spaced repeated runs can improve recall of the basic commands for the dictation plugin Voice In for Google Chrome.

## Explanation
To become productive quickly, the quiz can be taken five times or more in a single day; however, memory of the commands will fade quickly.
It is better to take the quiz every 2-3 days.

## Features
- Randomizes questions on each run
- Reports the number of correct answers
- Reports time spent on quiz

## Disclaimer
This is a programming tool, not an educational tool.
It provides no explanations and no context.
The `quiz` improves recall of computer commands in a quote manner.


## Prerequisites
You need a recent version of Python3.
You also need one external module.
Install the module *pytictoc* with pip.

```bash
pip install --user --upgrade pytictoc
```

or with a conda environment

```bash
conda activate <env name>
pip install --upgrade pip 
pip install pytictoc
```

If you have an older version of Python3, install the module *tictoc* instead.

## Run one of two ways.
You will be asked to enter a number between 1 and 1. Enter 1.
Then the interactive quiz will run.

### Run in terminal

```bash
./qVoiceIn.py
```

Enter control-D to interrupt the quiz.

### Run in Jupyter
Use in Jupyter Notebook, JupyterLab, [JupyterLab.app](https://blog.jupyter.org/jupyterlab-desktop-app-now-available-b8b661b17e9a), or [nteract.app](https://nteract.io/).
The last two options are stand-alone desktop applications that do not use the browser.
You still need a Python3 kernel available that is mapped to a Python interpreter with the module `pytictoc` installed via pip.
Probably works in Colab, too, but you may have to load the quiz onto your Google Drive.
Select the appropriate Python kernel that taps into the Python interpreter with *pytictoc* installed.

The advantages of this approach are that the results can be stored in the Notebook, and it is more fun to run the quiz in Jupyter.

Check on the present working directory in Jupyter by entering the following in a code cell.

```bash
!pwd
```

The file *qVoiceIn.py* must be in your working directory, or you must provide the full file path.
Enter the following in another code cell.

```bash
%run -i "qVoiceIn.py"
```
## Updates

|Version      | Changes                                                                                                                                    | Date                 |
|:-----------:|:------------------------------------------------------------------------------------------------------------------------------------------:|:--------------------:|
| Version 0.6 |  Added update table and funding sources. Edited typos in README.md                                                                         | 2024 April 13        |

## Funding

- NIH: R01 CA242845, R01 AI088011
- NIH: P30 CA225520 (PI: R. Mannel); P20GM103640 and P30GM145423 (PI: A. West)

