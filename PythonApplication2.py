import subprocess
import os
import difflib
import signal
import ctypes
import http.client
import json
import requests
import codecs
#!/usr/bin/env python
# -*- coding: utf8 -*-
class Compiler():
   # def __init__(self,name,lang,task_id):
   #     self.compilers_dictionary = {"cl":'"D:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\bin\\cl.exe" '} #TODO : add more compilers
   #     self.task_id = task_id
   #     self.file = name
   #     self.batname = "help.bat"
   #     self.exe_name = self.file[0:self.file.find(".")] +".exe" #TODO: it looks so ugly....
   #     self.verdict = "OK" 
   #     self.tests_dictionary = {     1:"C:\\Users\\akutalev\\Documents\\Visual Studio 2015\\Projects\\PythonApplication2\\PythonApplication2\\test1",
   #                                   2:"C:\\Users\\akutalev\\Documents\\Visual Studio 2015\\Projects\\PythonApplication2\\PythonApplication2\\test2", 
   #                                   3:"C:\\Users\\akutalev\\Documents\\Visual Studio 2015\\Projects\\PythonApplication2\\PythonApplication2\\test3",
   #                                   4:"C:\\Users\\akutalev\\Documents\\Visual Studio 2015\\Projects\\PythonApplication2\\PythonApplication2\\test4"
   #                             }                                                                                                                                   
   #     fin = open(self.batname,"w")
   #     self.winkill_address = "C:\\Users\\akutalev\\Documents\\Visual Studio 2015\\Projects\\PythonApplication2\\PythonApplication2\\WinKill3.3.0.exe"
   #    if lang=="cl":
   #         fin.write('call "D:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\bin\\vcvars32.bat"' + '\n')
   #     fin.write(self.compilers_dictionary[lang]+ '"'  +"C:\\Users\\akutalev\\Documents\\Visual Studio 2015\\Projects\\PythonApplication2\\PythonApplication2"+'\\'+ name+ '"')
   #     fin.close()
    
    def __init__(self, json_file):
        parsed_string = json.loads(json_file)
        self.compilers_dictionary = {3:'"D:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\bin\\cl.exe" '} #TODO : add more compilers
        self.task_id = parsed_string["task_id"]
        self.file =   parsed_string["filename"]
        code_file = open (self.file,"w")
        code_file.write(parsed_string["source"])
        code_file.close()
        self.lang = parsed_string["compiler_id"]
        self.batname = "help.bat"
        self.exe_name = self.file[0:self.file.find(".")] +".exe" #TODO: it looks so ugly....
        self.verdict = "OK" 
        self.tests_dictionary = {     1:"C:\\Users\\akutalev\\Documents\\Visual Studio 2015\\Projects\\PythonApplication2\\PythonApplication2\\test1",
                                      2:"C:\\Users\\akutalev\\Documents\\Visual Studio 2015\\Projects\\PythonApplication2\\PythonApplication2\\test2", 
                                      3:"C:\\Users\\akutalev\\Documents\\Visual Studio 2015\\Projects\\PythonApplication2\\PythonApplication2\\test3",
                                      4:"C:\\Users\\akutalev\\Documents\\Visual Studio 2015\\Projects\\PythonApplication2\\PythonApplication2\\test4"
                                } 
                                    
        #help .bat file to compile files                                                                                              
        fin = open(self.batname,"w")
        if self.lang==3:
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
            print('\n\n\n\n\n')
            return exc.stdout.decode("cp866")
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
            oldfile = os.path.join(path,str(tests_number+1)+".in")
            newfile = os.path.join(path,"in"+str(tests_number+1)+".txt")
            os.rename(oldfile,newfile)
            
            current_input_name = path+"\\"+ "in"+str(tests_number+1)+".txt"
            current_output_name = '"'+ path + "\\" + str(tests_number+1) + ".out" + '"'
            current_input =  open(current_input_name,"r")
            outfile = open("task_out.txt","w")

            cmd_string =  " -m 10 -t 1 -r " + self.exe_name + " -n no_config.txt" #TODO: сделать считывание из файла конфига
            command_list = cmd_string.split()
            command_list.insert(0,self.winkill_address)
            try:
                testing_process = subprocess.run(command_list,stdout =outfile,stdin =current_input,shell = True)
                testing_process.check_returncode()              
            except subprocess.CalledProcessError as exc: 
                return_codes = {1:": Runtime Error",
                                2:": Time limit",
                                3:": Memory limit",
                                4:": System time limit",
                                5:": Security violation"                   
                               }

                if exc.returncode in return_codes:
                    current_input.close();
                    outfile.close()
                    os.rename(newfile,oldfile)   
                    return "Test "+str(tests_number+1)+return_codes[exc.returncode]

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
                        return "Invalid input on test:" + str(tests_number+1) + '\n'
                    elif error_flag == "wrong":
                        return "Test "+str(tests_number+1) + ": Wrong Answer"
                    return exc.stderr.decode("utf-8","ignore")

                os.remove(testing_bat_file_name)

            else:
                correct_strings = open(path +"\\" + str(tests_number+1)+".out").read().splitlines(1)
                answer_strings = open("task_out.txt").read().splitlines(1)
                if answer_strings[-1][-1] == '\n':
                   answer_strings[-1]=answer_strings[-1][:-1]
                if correct_strings!=answer_strings:
                   os.rename(newfile,oldfile)
                   return str(tests_number+1)+" Wrong answer" +'\n'
                else:
                   os.rename(newfile,oldfile)
                   return "OK"

            os.rename(newfile,oldfile)
        return "OK"
          
#TestCode = Compiler("adsd.c","cl",2)
#compile_rezult= TestCode.compile()
#if compile_rezult == "OK":
#    x = TestCode.testing()
#
#    print('\n\n\n\n')
#    print (x)
h1 = http.client.HTTPConnection("10.4.0.113:1914")
h1.request("GET","")
r1 = h1.getresponse()
compilers = ["Visual Studio Compiler"];
resp = requests.get("http://10.4.0.113:5001/commit/not_tested")
data = json.loads(resp.text)
print (data)
TestCode = Compiler(resp.text)
compile_rezult= TestCode.compile()
print(compile_rezult)
if compile_rezult == "OK":
    x = TestCode.testing()