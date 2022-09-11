from time import sleep
from webbrowser import Chrome
from selenium.webdriver.common.by import By
from selenium import webdriver
from typing import List
import string 
import sys 

class Problem:
    def __init__(self, name: string, desc: string, examples: List[tuple], func_name: string) -> None:
        self.name = name 
        self.desc = desc 
        self.examples = examples
        self.func_name = func_name

def generate_problem_suite(problem: Problem) -> string:
    tab_space = ' '*4 
    boilerplate_code = ''

    
    #Importing usefull modules
    possible_imports = "from collections import Counter, defaultdict, deque\nimport heapq\n\n"
    boilerplate_code += possible_imports

    #Adding multi-line comment for problem description
    problem_explanation = f"'''\n{problem.desc}\n'''\n\n"
    boilerplate_code += problem_explanation
    
    #Adding in the function definition for the function you'll write your solution in 
    formatted_func_params = ', '.join(list(problem.examples[0][0].keys())).replace("'","")
    func_def = f'def {problem.func_name}({formatted_func_params}):\n{tab_space}pass\n\n'
    boilerplate_code += func_def
    
    
    main_def = 'def main():\n'
    
    #Generating the test cases in the main method 
    main_content = ''
    for i in range(len(problem.examples)):
        inputs, output = problem.examples[i]
        func_call_var = ''
        
        for var, val in inputs.items():
            func_call_var += f'{var}_{i}, '
            main_content += tab_space + f'{var}_{i} = {val}\n'            
        
        main_content += tab_space + f'ans_{i} = {output}\n'        
        main_content += tab_space + f'sol_ans_{i} = {problem.func_name}({func_call_var[:-2]})\n'
        main_content += tab_space + f'print("Correct! Your Answer: {{sol_ans_{i}}}" '
        main_content += f'if ans_{i} == sol_ans_{i} '
        main_content += f'else f"Wrong! - Got: {{sol_ans_{i}}} Expected: {{ans_{i}}}")\n\n'
    
    #Adding some more boilerplate
    main_run = 'if __name__ == "__main__":\n' + tab_space + 'main()'
    boilerplate_code += main_def + main_content + main_run
        
    #Writing this out 
    with open(f'Leetcode_Problems\{problem.name}.py', 'w') as output_file:
        output_file.write(boilerplate_code)

def update_problem_data(browser: Chrome, problem: Problem) -> None:
    
    #Updating the function name and quesiton name directly 
    problem.func_name = browser.find_elements(By.CLASS_NAME, 'cm-variable')[1].text
    problem.name = browser.find_element(By.CLASS_NAME, 'css-v3d350').text.replace(' ', '_')

    #Grabbing all the content of the question description
    question_content = browser.find_element(By.CLASS_NAME, "question-content__JfgR").text
    
    
    #Finding the actual problem description
    desc_end = question_content.find('  ')
    problem.desc = question_content[:desc_end]

    content_list = question_content[desc_end:].split('\n')
    
    # Finding all the example inputs & outputs
    cur_example = []
    for item in content_list:
        cur_inputs = {}    
        if "Input" in item:
            inputs = item[7:].split(', ')
            for input in inputs:
                var, val = input.split(' = ')
                cur_inputs[var] = val 
            cur_example.append(cur_inputs)
        if "Output" in item:
            cur_example.append(item[8:])
            problem.examples.append((cur_example[0], cur_example[1]))
            cur_example = []
            
def generate_example_suite():
    test_examples = [
        ({"nums" : "[2,7,11,15]", "target" : "9" }, "[0,1]"),
        ({"nums" : "[3,2,4]", "target" : "6" }, "[1,2]")
    ]
    test_problem = Problem(name="1. Two Sum", desc="Given an array of integers nums\nFind something", examples=test_examples, func_name="twoSum")
    generate_problem_suite(test_problem)

def main(url: string) -> None:
    CHROME_DRIVER_PATH = "D:\ChromeDriver\chromedriver.exe"
    problem = Problem("","",[],"")
    
    options = webdriver.ChromeOptions();
    options.add_argument("headless");
    
    browser = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=options)
    browser.get(url)
    # wait page to load
    sleep(5)

    update_problem_data(browser, problem)
    generate_problem_suite(problem)
    
    # Browser Source Code (Uncomment to search)
    # source_code = browser.find_element(By.XPATH, "//*").get_attribute("outerHTML")

if __name__ == "__main__":
    DEBUG = False
    if DEBUG:
        main(sys.argv[1])
    else:
        try:
            URL = sys.argv[1]
        except:
            sys.stderr.write("Must provide one argument")
            sys.exit(1)
            
        if URL == '' or len(URL) < 30 or URL[0:30] != "https://leetcode.com/problems/":
            sys.stderr.write('Error: URL Must start with "https://leetcode.com/problems/"')
            sys.exit(1)
        else:
            main(URL)