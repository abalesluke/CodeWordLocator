import os, sys
from platform import system as my_system 

class FoxParse:
    def __init__(self):
        self.args = {}
        self.new_args = {}

    def __parser(self, num, arg):
        try:
            self.args[arg] = sys.argv[(num+1)]
        except IndexError:
            self.args[arg] = True

    def parse_args(self):
        num = 0
        for arg in sys.argv[1:]:
            num+=1
            if((num % 2) == 1):
                if(not arg.startswith('-')):
                    continue
                self.__parser(num, arg)

    def set_args(self, arg):
        arg_val = self.args.get(arg)
        if(arg_val != None):
            self.new_args[arg] = arg_val
    
    def get_args(self)->exec:return (self.new_args if(bool(self.new_args)) else 0) # 0 means dictionary is empty


class WordLocator:
    def __init__(self, folder, xfolder, word):
        self.folder = folder
        self.xfolder = xfolder
        self.word = word
    
    def __filter(self, fn):
        dirs = fn.split('/')
        if(self.xfolder in dirs):
            return True

    def __word(self, fn):
        line_no = 0
        if(self.__filter(fn)):
            return
        try:
            for line in open(fn).read().splitlines():
                line_no+=1
                if(self.word in line):
                    print(f"Line [{line_no}]\t File: {fn}")
        except Exception as err:
            pass    

    def find(self):
        for root, dirs, files in os.walk(self.folder):
            path = root.split(os.sep)
            for file in files:
                file = "./"+"/".join(path)+"/"+file
                # print("/".join(path)+str(file))
                self.__word(file)


def clear():
    if(my_system == "Windows"):
        os.system("cls")
    else:
        os.system("clear")

def banner():
    clear()
    banner = "================================\n"
    banner+= " Word/Variable/Function Locator\n"
    banner+= "\tBy: Anikin Luke\n"
    banner+= "================================"
    print(banner)

def help(err_msg=''):
    banner()
    print(f"""
Arguments:

    -d       |     : Directory (Where to find the word)[Default directory = './']
    -w       |     : Word (to find)
    -x       |     : Exclude a folder to be scanned
Usage: python3 {os.path.basename(__file__)} -d <target_directory> -w "<word_to_find>"
Example: python3 {os.path.basename(__file__)} -d ./downloads -w "anikin_luke"
\n{err_msg}""")


if(__name__=="__main__"):
    parser = FoxParse()
    parser.parse_args()
    parser.set_args('-d')
    parser.set_args('-w')
    parser.set_args('-x')
    args = parser.get_args()

    folder = "./"
    xfolder = None
    if(args == 0):
        help()
        exit(0)
    elif((args.get('-w') == True) or (args.get('-w') == None)):
        help("[ERROR]: '-w' argument is required, please input a word to find!")
        exit(0)
    elif((args.get('-d') != True) or (args.get('-d') != None)):
        folder = args.get('-d')
    if((args.get('-x') == True) or (args.get('-x') == None)):
        xfolder = args.get('-x')

    search = WordLocator(folder, xfolder, args.get('-w'))
    search.find()
