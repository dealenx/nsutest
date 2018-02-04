import subprocess
import os
import difflib
import signal
import ctypes
import http.client
import json
import requests
import codecs
import time

class Compiler():
    def __init__(self,name,lang,task_id,commit_id):
        self.compilers_dictionary = {2:'"D:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\bin\\cl.exe" '} #TODO : add more compilers
        self.task_id = task_id
        self.file = name
        self.lang = lang
        self.batname = "help.bat"
        self.exe_name = self.file[0:self.file.find(".")] +".exe" #TODO: it looks so ugly....
        self.verdict = "OK" 
        self.tests_dictionary = {   #  8:"C:\\Users\\akutalev\\Documents\\Visual Studio 2015\\Projects\\PythonApplication2\\PythonApplication2\\test1",
                                   #   9:"C:\\Users\\akutalev\\Documents\\Visual Studio 2015\\Projects\\PythonApplication2\\PythonApplication2\\test2", 
                                   #   3:"C:\\Users\\akutalev\\Documents\\Visual Studio 2015\\Projects\\PythonApplication2\\PythonApplication2\\test3",
                                   ##   4:"C:\\Users\\akutalev\\Documents\\Visual Studio 2015\\Projects\\PythonApplication2\\PythonApplication2\\test4",
                                   #   7:"C:\\Users\\akutalev\\Documents\\Visual Studio 2015\\Projects\\PythonApplication2\\PythonApplication2\\test7",
                                   #   2:"C:\\Users\\akutalev\\Documents\\Visual Studio 2015\\Projects\\PythonApplication2\\PythonApplication2\\test8",  
                                      1:"C:\\Users\\akutalev\\Documents\\Visual Studio 2015\\Projects\\PythonApplication2\\PythonApplication2\\test9",
                                      3:"C:\\Users\\akutalev\\Documents\\Visual Studio 2015\\Projects\\PythonApplication2\\PythonApplication2\\test10",
                                      4:"C:\\Users\\akutalev\\Documents\\Visual Studio 2015\\Projects\\PythonApplication2\\PythonApplication2\\test11",
                                      5:"C:\\Users\\akutalev\\Documents\\Visual Studio 2015\\Projects\\PythonApplication2\\PythonApplication2\\test11"                                           
                                }                                                                                                                                   
        fin = open(self.batname,"w")
        self.winkill_address = "C:\\Users\\akutalev\\Documents\\Visual Studio 2015\\Projects\\PythonApplication2\\PythonApplication2\\WinKill3.3.0.exe"
        if self.lang==2:
            fin.write('call "D:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\bin\\vcvars32.bat"' + '\n')
        fin.write(self.compilers_dictionary[self.lang]+ '"'  +"C:\\Users\\akutalev\\Documents\\Visual Studio 2015\\Projects\\PythonApplication2\\PythonApplication2"+'\\'+ self.file+ '"')
        fin.close()
        self.commit_id = commit_id



    def from_json(self, json_file):
        parsed_string = json_file
        self.lang = parsed_string["compiler_id"]
        self.compilers_dictionary = {2:'"D:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\bin\\cl.exe" '} #TODO : add more compilers
        self.task_id = parsed_string["task_id"]
        self.file =   parsed_string["filename"]
        print(parsed_string["source"])
        code_file = open (self.file,"w")
        code_file.write(parsed_string["source"])
        code_file.close()
        self.commit_id = parsed_string["commit_id"]
        self.batname = "help.bat"
        self.exe_name = self.file[0:self.file.find(".")] +".exe" #TODO: it looks so ugly....
        self.verdict = "OK" 
        fin = open(self.batname,"w")
        if self.lang==2:
            fin.write('call "D:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\bin\\vcvars32.bat"' + '\n')
     
        fin.write(self.compilers_dictionary[self.lang]+ '"'  +"C:\\Users\\akutalev\\Documents\\Visual Studio 2015\\Projects\\PythonApplication2\\PythonApplication2"+'\\'+ self.file+ '"')
        fin.close()
                
    def compile(self):
        try:
            compile_proc = subprocess.run(self.batname,stdout=subprocess.PIPE)
            compile_proc.check_returncode()
        except OSError:
            return("Unknown compiler")
        except subprocess.CalledProcessError as exc:
            compile_error = exc.stdout.decode("cp866")
            last_file = compile_error.rfind(self.file)
            self.verdict = compile_error[last_file:]
            return  "COMPILATION_ERROR"
        return "OK"


    def testing(self):

        input_files = []
        output_files = []
        checker_mod = False
        path = self.tests_dictionary[self.task_id]
        for f1le in os.listdir(self.tests_dictionary[self.task_id]):
            if f1le.endswith(".in"):
                input_files.append(f1le)
            elif f1le.endswith(".out"):
                output_files.append(f1le)
            elif f1le=="check.exe":
                checker_mod = True


        for tests_number in range(len(input_files)):
            print("Current test:",tests_number+1)
            oldfile = os.path.join(path,str(tests_number+1)+".in")
            newfile = os.path.join(path,"in"+str(tests_number+1)+".txt")
            os.rename(oldfile,newfile)
            
            current_input_name = path+"\\"+ "in"+str(tests_number+1)+".txt"
            current_output_name = '"'+ path + "\\" + str(tests_number+1) + ".out" + '"'
            current_input =  open(current_input_name,"r")
            outfile = open("task_out.txt","w")

            cmd_string =  " -m 20000000 -t 1 -r " + self.exe_name + " -n no_config.txt" #TODO: сделать считывание из файла конфига
            command_list = cmd_string.split()
            command_list.insert(0,self.winkill_address)
            try:
                testing_process = subprocess.run(command_list,stdout =outfile,stdin =current_input,shell = True)
                testing_process.check_returncode()              
            except subprocess.CalledProcessError as exc: 
                return_codes = {1:"RUNTIME_ERROR",
                                2:"TIME_LIMIT",   
                                3:"MEMORY_LIMIT",
                                4:"SYSTEM_TIME_LIMIT",
                                5:"SECURITY_VIOLATION"                   
                               }
                if exc.returncode in return_codes:
                    current_input.close();
                    outfile.close()
                    os.rename(newfile,oldfile)   
                    self.verdict = "TEST :" + str(tests_number+1)
                    return return_codes[exc.returncode]
            else:                                          #maybe the wost strings in this project.... need idea how to split stdout winkill and testing program
                current_input.close()
                outfile.close()
                outfile = open("task_out.txt","w")
                current_input = open(current_input_name,"r")
                subprocess.run(self.exe_name,stdout = outfile,stdin = current_input)



            current_input.close();
            outfile.close()

            if checker_mod:
                testing_bat_file_name = str(tests_number) + "testing_bat_file.bat"
                testing_bat_file = open(testing_bat_file_name,"w+")
                testing_bat_file.write('"'+path + "\\check.exe"+'" '+'"'+current_input_name+'" '+ current_output_name+" "+"task_out.txt")
                testing_bat_file.close()

                try:
                    testing_process = subprocess.run(testing_bat_file_name,stderr=subprocess.PIPE)
                    testing_process.check_returncode()
                except subprocess.CalledProcessError as exc:
                    os.rename(newfile,oldfile)
                    os.remove(testing_bat_file_name)
                    error_message = exc.stderr.decode("utf-8","ignore")
                    error_flag = error_message.split(' ',1)[0]
                    if error_flag == "FAIL":
                         self.verdict = "TEST :" + str(tests_number+1)
                         return "INVALID_INPUT"
                       # return "Invalid input on test:" + str(tests_number+1) + '\n'
                    elif error_flag == "wrong":
                         self.verdict = "TEST :" + str(tests_number+1)
                         return "WRONG_ANSWER"
                os.remove(testing_bat_file_name)

            else:
                correct_strings = open(path +"\\" + str(tests_number+1)+".out").read().splitlines(1)
                answer_strings = open("task_out.txt").read().splitlines(1)
                print(correct_strings)
                print(answer_strings)

                if answer_strings!= [] and (answer_strings[-1][-1] == '\n' or answer_strings[-1][-1] ==  ' '):
                   answer_strings[-1]=answer_strings[-1][:-1]
                if correct_strings!=[] and (correct_strings[-1][-1] == '\n' or correct_strings[-1][-1] == ' '):
                   correct_strings[-1]=correct_strings[-1][:-1]

                   print(correct_strings)
                if correct_strings!=answer_strings:
                   os.rename(newfile,oldfile)
                   self.verdict = "TEST :" + str(tests_number+1)  
                   return "WRONG_ANSWER"
                  # return str(tests_number+1)+" Wrong answer" +'\n'
               # else:
                   #os.rename(newfile,oldfile)
                   

            os.rename(newfile,oldfile)
        return "OK"
          
TestCode = Compiler("main.c",2,7,100500)
rezult= TestCode.compile()

while (1):
   print ("Request for task","\n")
   sub = requests.get("http://10.4.0.113:5005/get_not_tested_submit")
   submit = json.loads(sub.text)
   print (submit)
   if submit != "[]":
        submit = json.loads(submit) 
        if submit['compiler_id']!=2:
            print("mdee\n")
            time.sleep(5)
        else:
            TestCode.from_json(submit)
            rezult = TestCode.compile()
            if rezult == "OK":
                rezult = TestCode.testing()
                print('\n\n\n\n')
                print(rezult) 
                print('\n\n\n\n')
                print(TestCode.verdict)
                print('\n\n\n\n')
            post_req = requests.post("http://10.4.0.113:5005/push_result",json = {"commit_id":TestCode.commit_id,"result_code":rezult,"output":TestCode.verdict})
            print(rezult, TestCode.verdict)
   else:
        time.sleep(5)

