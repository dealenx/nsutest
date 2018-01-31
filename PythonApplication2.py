import subprocess
import os
import difflib
import signal
class Compiler():
    def __init__(self,name,lang,task_id):
        self.compilers_dictionary = {"cl":'"D:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\bin\\cl.exe" '} #TODO : add more compilers
        self.task_id = task_id
        self.file = name
        self.batname = "help.bat"
        self.exe_name = self.file[0:self.file.find(".")] +".exe" #TODO: it looks so ugly....
        self.verdict = "OK" 
        self.tests_dictionary = {     1:"C:\\Users\\akutalev\\Documents\\Visual Studio 2015\\Projects\\PythonApplication2\\PythonApplication2\\test1",
                                      2:"C:\\Users\\akutalev\\Documents\\Visual Studio 2015\\Projects\\PythonApplication2\\PythonApplication2\\test2", 
                                      3:"C:\\Users\\akutalev\\Documents\\Visual Studio 2015\\Projects\\PythonApplication2\\PythonApplication2\\test3",
                                      4:"C:\\Users\\akutalev\\Documents\\Visual Studio 2015\\Projects\\PythonApplication2\\PythonApplication2\\test4"
                                }                                                                                                                                   
        fin = open(self.batname,"w")
        if lang=="cl":
            fin.write('call "D:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\bin\\vcvars32.bat"' + '\n')
        fin.write(self.compilers_dictionary[lang]+ '"'  +"C:\\Users\\akutalev\\Documents\\Visual Studio 2015\\Projects\\PythonApplication2\\PythonApplication2"+'\\'+ name+ '"')
        fin.close()


    def compile(self):
        try:
            compile_proc = subprocess.run(self.batname,stderr=subprocess.PIPE)
            compile_proc.check_returncode()
        except OSError:
            return("Unknown compiler")
        except subprocess.CalledProcessError as exc:
            return (exc.stderr.decode("utf-8",'ignore'))
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

            try:
                testing_process = subprocess.run(self.exe_name,stdout =outfile,stdin =current_input,stderr=subprocess.PIPE,shell=True)
                testing_process.check_returncode()
            except subprocess.CalledProcessError as exc:  
                if exc.returncode == -signal.SIGSEGV:
                    os.rename(newfile,oldfile)
                    return exc.stderr.decode("utf-8","ignore")

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
                   return "ebat' ty loh: Test" +str(tests_number+1)+" Wrong answer" +'\n'
                else:
                   os.rename(newfile,oldfile)
                   return "vse kul'turno"

            os.rename(newfile,oldfile)

          
TestCode = Compiler("adsd.c","cl",2)
compile_rezult= TestCode.compile()
if compile_rezult == "OK":
    x = TestCode.testing()

print('\n\n\n\n')
print (x)