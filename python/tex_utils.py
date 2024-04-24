'''
tex_utils.py
This script contains functions to convert Aiken formatted text files to tex files.
'''

# Imports

import os, io
import pandas as pd
import random
import re


# Functions

def get_data(file_path) -> str:
    '''
    This function reads the data from text file in Aiken formatand returns it as a string.
    '''
    # ensure the file exists
    if os.path.exists(file_path):
        # open the file and read its contents
        with io.open(file_path, 'r', encoding='utf8') as f:
            data = f.read()
    else:
        RuntimeWarning(f"File {file_path} does not exist.")

    return data



def create_dataframe(data: str) -> pd.DataFrame:
    '''
    This function takes a string of data in Aiken format and returns a pandas dataframe.
    '''
    # create a pandas dataframe from the substrings with columns 'Question', 'A', 'B', 'C', 'D', 'E', 'Correct'
    df = pd.DataFrame(columns=['Question', 'A', 'B', 'C', 'D', 'E', 'Correct'])

    # get the substrings
    substrings = get_substrings(data)

    # iterate over the substrings and extract the question, answers, and correct answer
    for i, substring in enumerate(substrings):

        # extract the question, answers, and correct answer
        question = substring[0]
        answers = substring[1:6]
        correct = substring[6]

        # strip answers of leading and trailing whitespaces
        answers = [answer.strip() for answer in answers]
        correct = correct.strip()

        # strip the answers of 'A)', 'B)', 'C)', 'D)', 'E)'
        answers = [answer[3:] for answer in answers]

        # strip 'ANSWER: ' from the entries in correct column
        correct = correct[8:] 

        # check the column name in the correct column and add '(correct)' to the entry in the respective column
        if correct == 'A':
            answers[0] += ' (correct)'
        elif correct == 'B':
            answers[1] += ' (correct)'
        elif correct == 'C':
            answers[2] += ' (correct)'
        elif correct == 'D':
            answers[3] += ' (correct)'
        elif correct == 'E':
            answers[4] += ' (correct)'
        else:
            raise ValueError(f'Invalid correct answer: {correct}') 

        new_data = {'Question': question, 'A': answers[0], 'B': answers[1], 'C': answers[2], 'D': answers[3], 'E': answers[4], 'Correct': correct}
        new_row = pd.DataFrame(new_data, index=[i])

        df = pd.concat([df, new_row], ignore_index=True)

    return df



def get_substrings(data: str) -> list:
    '''
    This function takes a string of data in Aiken format and returns a list of substrings.
    '''
    # split the text into substrings after every 7th line
    lines = data.split('\n')
    lines = [line for line in lines if line]  # remove empty lines
    n = 7
    substrings = [lines[i:i + n] for i in range(0, len(lines), n)]

    return substrings



def print_substrings(substrings: list):
    '''
    This function prints the substrings.
    '''
    for i, substring in enumerate(substrings):
        print(f"Substring {i+1}:")
        for line in substring:
            print(line)
        print()



def get_random_questions(df: pd.DataFrame, shuffle_answers=True) -> pd.DataFrame:
    '''
    This function takes a pandas dataframe and returns a random row.
    '''
    # get a random sample of n questions
    random_question = df.sample()

    if shuffle_answers:
        # get the answers from the question
        answers = random_question.iloc[0, 1:6]

        # convert the answers to a list
        answers_list = list(answers)

        # randomly shuffle the answers
        random.shuffle(answers_list)

        # update the answers in the question
        random_question.iloc[0, 1:6] = answers_list
    else:
        random_question = random_question

    return random_question



def create_string(questions_folder: str, random_question: pd.DataFrame) -> str:
    '''
    This function takes a random question and returns it as a string.
    '''

    # get the question
    question = random_question['Question'].values[0]

    # check if there are images in the question
    if check_for_image(question):
        # get the image name
        image_name = get_image_name(question)

        # remove the image name in brackets from the question
        question = re.sub(r'\[.*\]', '', question)

        # add the image path to the image name
        image_path = os.path.join('images', image_name) + '.png'

        # add the image to the question str
        question = question + '\n' + '\n' + '\includegraphics[width=0.4\\textwidth]{' + image_path + '}'
    
    # create the string
    str_question = ('\question ' + question + '\n'
      + '\n'
      + '\\begin{choices}' + '\n'
      + '\t' + '\choice ' + random_question['A'].values[0] + '\n'
      + '\t' + '\choice ' + random_question['B'].values[0] + '\n'
      + '\t' + '\choice ' + random_question['C'].values[0] + '\n'
      + '\t' + '\choice ' + random_question['D'].values[0] + '\n'
      + '\t' + '\choice ' + random_question['E'].values[0] + '\n'
      + '\end{choices}' + '\n')
    
    return str_question



def check_for_image(str_question: str) -> bool:
    '''
    This function checks if a question contains an image.
    '''
    return bool(re.search(r'\[.*\]', str_question))



def get_image_name(str_question: str) -> str:
    '''
    This function extracts the image name from a string.
    '''
    pattern = r'.*\[(.*?)\]$'
    match = re.search(pattern, str_question)
    return match.group(1) if match else None



def files_to_string(questions_folder: str) -> list:
    '''
    This function takes a folder with files and returns a list of questions as strings.
    '''
    # get number of txt files in the folder and ignore hidden files
    files_in_folder = [file for file in os.listdir(questions_folder) if file.endswith('.txt') and not file.startswith('.')]

    # check if there are five files in the folder
    if len(files_in_folder) == 5:
        # create list to store the strings
        str_questions = []
        print(questions_folder)

        # iterate over the files in the folder
        for file in files_in_folder:
            # get the file path
            file_path = os.path.join(questions_folder, file)
            print('Currect file: '+ file_path)

            # read the data from the file
            data = get_data(file_path)

            # create a dataframe from the data
            df = create_dataframe(data)

            # get a random question with shuffled answers
            random_question = get_random_questions(df, shuffle_answers=True)

            # create the string
            str_question = create_string(questions_folder, random_question)

            # append the string to the list
            str_questions.append(str_question)

        return str_questions
    
    elif len(files_in_folder) == 1:
        # create list to store the strings
        str_questions = []
        print(questions_folder)

        # get file name
        file = files_in_folder[0]

        # get the file path
        file_path = os.path.join(questions_folder, file)
        print('Currect file: '+ file_path)

        # read the data from the file
        data = get_data(file_path)

        # create a dataframe from the data
        df = create_dataframe(data)

        # iterate over the files in the folder
        for i in range(5):
            # get a random question with shuffled answers
            random_question = get_random_questions(df, shuffle_answers=True)

            # create the string
            str_question = create_string(questions_folder, random_question)

            # append the string to the list
            str_questions.append(str_question)

        return str_questions

    else:
        print(f"Folder {questions_folder} does not contain five files.")



def remove_solution(testat: str) -> str:
    '''
    This function removes the solution mark from the testat.
    '''
    # split the testat into substrings
    lines = testat.split('\n')

    # strip (correct) from lines
    testat = [line.replace(' (correct)', '') for line in lines]

    # join the lines to a string
    testat = '\n'.join(testat)

    return testat
        


def create_testat(question_folder: str, testat_name: str, output_folder) -> str:
    '''
    This function creates a testat with five questions and saves it as a tex file.
    '''
    str_questions_list = files_to_string(question_folder)

    # strip '- xx' from the testat name
    testat_name = re.sub(r'- \d+', '', testat_name)
    
    testat = ('\documentclass[11pt]{exam}' + '\n'
            + '\n'
            + '\\usepackage{amsmath}' + '\n'
            + '\\usepackage{graphicx}' + '\n'
            + '\\usepackage{geometry}' + '\n'
            + '\\usepackage{etoolbox}' + '\n'
            + '\\BeforeBeginEnvironment{choices}{\par\\nopagebreak\minipage{\linewidth}}' + '\n'
            + '\\AfterEndEnvironment{choices}{\endminipage}' + '\n'
            + '\\geometry{' + '\n'
            + 'a4paper,' + '\n'
            + 'total={185mm,257mm},' + '\n'
            + 'left=10mm,' + '\n'
            + 'top=25mm,' + '\n'
            + 'bottom=10mm' + '\n'
            + '}' + '\n'
            + '\n'
            + '\\begin{document}' + '\n'
            + '\setlength{\\voffset}{-0.5in}' + '\n'
            + '\setlength{\headsep}{5pt}' + '\n'
            + '\n'
            + '\\fbox{\\fbox{\parbox{8cm}{\centering' + '\n'
            + '\\vspace{2mm}' + '\n'
            + testat_name + '\n'
            + '\\vspace{2mm}' + '\n'
            + '}}}' + '\n'
            + '\\hspace{2mm}' + '\n'
            + '\makebox[0.25\\textwidth]{Name:\enspace\hrulefill} \hspace{5mm}' + '\n'
            + '\makebox[0.2\\textwidth]{Datum:\enspace\hrulefill}' + '\n'
            + '\\vspace{4mm}' + '\n'
            + '\n'
            + '\\begin{questions}' + '\n' 
            + '\n' 
            + str_questions_list[0]
            + '\n'
            + '\\vspace{3mm}'
            + str_questions_list[1]
            + '\n'
            + '\\vspace{3mm}'
            + str_questions_list[2]
            + '\n'
            + '\\vspace{3mm}'
            + str_questions_list[3]
            + '\n'
            + '\\vspace{3mm}'
            + str_questions_list[4]
            + '\n'
            + '\\vspace{3mm}'
            + '\\end{questions}' + '\n'
            + '\n'
            + '\\end{document}' + '\n')    
    
    if not os.path.exists(output_folder):
        print(f"Output folder {output_folder} does not exist.")
        print(f"Testat {testat_name} could not be created.")
    else:
        # save the testat as a tex file (version with solution)
        with open(os.path.join(output_folder, f'solution_{testat_name}.tex'), 'w') as f:
            f.write(testat)
        # save the testat as a tex file (version without solution)
        with open(os.path.join(output_folder, f'{testat_name}.tex'), 'w') as f:
            f.write(remove_solution(testat))

        print(f"Testat {testat_name} created successfully.")