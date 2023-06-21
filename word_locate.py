import os, sys, time, colorama
from tqdm import tqdm
from platform import system as my_system 

# This class here is my own argument parser
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
        self.file_results = []
        self.folder_results = []
    
    # use to exclude folders if argument -x is provided
    # use to filter excluded folder provided by -x argument
    def __filter(self, fn):
        dirs = fn.split('/')
        if(self.xfolder in dirs):
            return True
    
    def __highlight(self, key1, key2):
        return key1.replace(key2,f"{colorama.Back.YELLOW}{key2}{colorama.Style.RESET_ALL}")

    def __fromFolder(self, fp, fn):
        if(self.word == fn):
            folderpath = self.__highlight(fp, fn)
            self.folder_results.append(f"Folder path: {folderpath}")

    def __fromFile(self, fn):
        line_no = 0
        if(self.__filter(fn)):
            return
        try:
            for line in open(fn).read().splitlines():
                line_no+=1
                if(self.word in line):
                    self.file_results.append(f"Line [{line_no}]\tFile Path: {fn}")
        except Exception as err:
            pass
    
    def __divider_line(self, label):
        divider = "☶"*int((os.get_terminal_size().columns/2)-int(len(label))/2)
        return f"\n{divider}{label}{divider}"
 
    def __view_results(self):
        emptyResults = True
        if(len(self.file_results) > 0):
            emptyResults = False
            print(self.__divider_line("[-Results-for-matching-word-in-a-file-]"))
            for res in self.file_results:
                print(res)
        if(len(self.folder_results) > 0):
            emptyResults = False
            print(self.__divider_line("[-Results-for-matching-folder-name-]"))
            for res in self.folder_results:
                print(res)
        if(emptyResults):
            print("No results!/Word not found!")


    def find(self):
        for root, dirs, files in tqdm(os.walk(self.folder),desc="Scanning Files"):
            path = root.split(os.sep)

            for dir in dirs:
                foldername = "./"+"/".join(path)+"./"+dir
                self.__fromFolder(foldername, dir)

            for file in files:
                filename = "./"+"/".join(path)+"./"+file
                self.__fromFile(filename)

        self.__view_results()


def clear():
    if(my_system() == "Windows"):
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

    -d       |     : Directory (Where to find the word)[Default directory = './'
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

