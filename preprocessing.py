# Importing and organizing required packages and libraries
# glob library is used to get a list of files matching a pattern
import glob;
# Pandas library is pretty widely used as a dataframe setup
import pandas as pd; 
#Initially setting a few options for our dataframes
pd.set_option('max_columns', 120);
pd.set_option('max_colwidth', 5000);
#Importing re which stands for regular expressions
import re;
#codecs defines base classes for standard Python codecs (encoders and decoders)
#and provides access to the internal Python codec registry, 
#which manages the codec and error handling lookup process.
import codecs;
import editdistance;

#Algorithm for loading our datasets
#STEP ONE: Get all the lists of filenames
filenames1 = glob.glob("Datasets/Dataset1/Tasks/*.txt");
filenames2 = glob.glob("Datasets/Dataset2/Tasks/*.txt");
filenames3 = glob.glob("Datasets/Dataset3/Tasks/*.txt");
filenames4 = glob.glob("Datasets/Dataset4/Tasks/*.txt");
filenames5 = glob.glob("Datasets/Dataset5/Tasks/*.txt");

ogfilenames1 = glob.glob("OGDatasets/Dataset1/Tasks/*.txt");
ogfilenames2 = glob.glob("OGDatasets/Dataset2/Tasks/*.txt");
ogfilenames3 = glob.glob("OGDatasets/Dataset3/Tasks/*.txt");
ogfilenames4 = glob.glob("OGDatasets/Dataset4/Tasks/*.txt");
ogfilenames5 = glob.glob("OGDatasets/Dataset5/Tasks/*.txt");

traindata1 = glob.glob("Datasets/Dataset1/Solutions/*.txt");
traindata2 = glob.glob("Datasets/Dataset2/Solutions/*.txt");
traindata3 = glob.glob("Datasets/Dataset3/Solutions/*.txt");
traindata4 = glob.glob("Datasets/Dataset4/Solutions/*.txt");
traindata5 = glob.glob("Datasets/Dataset5/Solutions/*.txt");

#Creating some empty arrays for storage.
arrayForStorage1 = [];
arrayForStorage2 = [];
arrayForStorage3 = [];
arrayForStorage4 = [];
arrayForStorage5 = [];

matrix1 = [];
matrix2 = [];
matrix3 = [];
matrix4 = [];
matrix5 = [];

replacementLines1 = [];
replacementLines2 = [];
replacementLines3 = [];
replacementLines4 = [];
replacementLines5 = [];

storage1 = [];
storage2 = [];
storage3 = [];
storage4 = [];
storage5 = [];

wrongLines1 = [];
wrongLines2 = [];
wrongLines3 = [];
wrongLines4 = [];
wrongLines5 = [];

correctReplcementLines1 = [];
correctReplcementLines2 = [];
correctReplcementLines3 = [];
correctReplcementLines4 = [];
correctReplcementLines5 = [];

#STEP TWO: Data preprocessing 
#Function used for preprocessing of the data
def preproccessingData(filenames):
    for file in filenames:
        strip_comments(filename = file);
             
#Function for overwritting the files without the comments
def strip_comments(filename):
    with codecs.open(filename, 'r', encoding="utf-8") as f:
        new_filename = commentRemover(f.read());
        
    with codecs.open(filename, 'w', encoding="utf-8") as f:
        f.write(new_filename);
        
    return filename;

def getWrongLine(filenames, array, newArray):
    for i in range(len(filenames)):
        newLine = int(array[i]) + 2;
        counter = 1;
        with codecs.open(filenames[i], 'r', encoding="utf-8") as f:
            for row in f:
                if counter == newLine:
                    newRow = re.sub('\s+', ' ', row);
                    newRow = newRow.strip();
                    newArray.append(newRow);
                counter = counter + 1;

def getFiles(filenames, array):
     for file in filenames:
         with codecs.open(file, 'r', encoding="utf-8") as f:
             firstLine = f.readline();
             secondLine = f.readline();
             new_file = f.read();
             array.append(new_file);

def compareString(dataframe, array, replacementLine):
    ticker = 0;
    for i in range(len(array)):
        counter = 0;
        df = dataframe[i]['LoC'];
        for row in df:
            if str(row) == str(array[i]):
                print(counter);
                dataframe[i]['Replacing_line_number'].replace(dataframe[i]['Replacing_line_number'], counter, inplace=True);
                dataframe[i]['LoC_Chars'] =  dataframe[i]['LoC'].apply(lambda x: characterCount(str(x)));
                dataframe[i]['Replacement_Line_Chars'] =  dataframe[i]['Replacing_line'].apply(lambda x: characterCount(str(x)));
                dataframe[i]['Similar_Chars'] =  dataframe[i]['LoC'].apply(lambda x: similarCharacterCount(str(x), str(replacementLine[i])));
                dataframe[i]['Similar_Tokens'] =  dataframe[i]['LoC'].apply(lambda x: similarTokenCount(str(x), str(replacementLine[i])));
                dataframe[i]['Edit_Distance'] =  dataframe[i]['LoC'].apply(lambda x: editDistance(str(x), str(replacementLine[i])));
                dataframe[i]['LoC_SemiColon'] =  dataframe[i]['LoC'].apply(lambda x: containsSemiColon(str(x)));
                dataframe[i]['Replacement_Line_SemiColon'] =  dataframe[i]['Replacing_line'].apply(lambda x: containsSemiColon(str(x)));
                dataframe[i]['LoC_Open_Bracket_Char'] =  dataframe[i]['LoC'].apply(lambda x: containsOpenBracket(str(x)));
                dataframe[i]['Replacement_Line_Open_Bracket_Char'] =  dataframe[i]['Replacing_line'].apply(lambda x: containsOpenBracket(str(x)));
                dataframe[i]['LoC_Close_Bracket_Char'] =  dataframe[i]['LoC'].apply(lambda x: containsCloseBracket(str(x)));
                dataframe[i]['Replacement_Line_Close_Bracket_Char'] =  dataframe[i]['Replacing_line'].apply(lambda x: containsCloseBracket(str(x)));
                print('Tick: ' + str(ticker));
            counter = counter + 1;
        ticker = ticker + 1;
             
def overwriteFile(filenames, array):
    for i in range(len(array)):
        with codecs.open(filenames[i], 'w', encoding="utf-8") as f:
            f.write(array[i]);
        
#Function for removing comments  
def commentRemover(text):
    def replacer(match):
        s = match.group(0);
        if s.startswith('/'):
            return " "; # note: a space and not an empty string
        else:
            return s;
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    );
    return re.sub(pattern, replacer, text);
                
def readFirstLineOfFile(filenames, array):
    for file in filenames:
        with codecs.open(file, 'r', encoding="utf-8") as f:
            firstLine = f.readline();
            array.append(firstLine);
                
def readTrainData(traindata, content):
    for file in traindata:
        with codecs.open(file, 'r', encoding="utf-8") as f:
            line = f.readline();
            content.append(line); 
   
def exportToCSV(array):
   df = pd.concat(array);
   df.to_csv(r'C:/Users/PC/.spyder-py3/dataframe2.csv');

def characterCount(string):
    count = len(string);
    return count;

def similarCharacterCount(string1, string2):
    count = 0;
    if len(string1) > len(string2):
        for i in range(len(string2)):
            if string1[i] == string2[i]:
                count = count + 1;
    else:
        for i in range(len(string1)):
            if string1[i] == string2[i]:
                count = count + 1;
    return count;

def similarTokenCount(string1, string2):
    tokens1 = re.findall(r"\w+(?:'\w+)*|[^\w\s']", string1);
    tokens2 = re.findall(r"\w+(?:'\w+)*|[^\w\s']", string2);
    count = 0;
    if len(tokens1) > len(tokens2):
        for i in range(len(tokens2)):
            if tokens1[i] == tokens2[i]:
                count = count + 1;
    else:
        for i in range(len(tokens1)):
            if tokens1[i] == tokens2[i]:
                count = count + 1;
    return count;

def editDistance(string1, string2):
    distance = editdistance.eval(string1, string2);
    return distance;

def containsSemiColon(string):
    if string.find(';') != -1:
        return 1;
    else:
        return 0;

def containsOpenBracket(string):
    if string.find('(') != -1:
        return 1;
    else:
        return 0;
    
def containsCloseBracket(string):
    if string.find(')') != -1:
        return 1;
    else:
        return 0;    
         
#STEP THREE: Creating dataframes with proccessed data    
#Creating a function which translates the lists of filenames into lists of datagrams
def translate(filenames, replacementLine, repLineNumber, array):
    for i in range(len(filenames)):
        list = pd.read_fwf(filenames[i] , names=['LoC','Replacing_line', 'Replacing_line_number', 'NaN2', 'NaN3', 'NaN4', 'NaN5', 'NaN6', 'NaN7', 'NaN8', 'NaN9', 'NaN10', 'NaN11', 'NaN12', 'NaN13', 'NaN14', 'NaN15', 'NaN16', 'NaN17', 'NaN18'], header = None);
        list.fillna({'Replacing_line' : str(replacementLine[i]), 'Replacing_line_number' : str(repLineNumber[i])}, inplace=True);
        new_df = list[pd.notnull(list['LoC'])];
        half_count = len(list)/2;
        new_ListOfData = new_df.dropna(thresh=half_count, axis=1);
        array.append(new_ListOfData);
    return array;  

def removeCorruptData(array, getWrongLineArray, replacementLine):
    n = len(array)
    for _i, d in enumerate(array[::-1], 1):
        if not 'LoC' in d or d.isnull().values.any():
            array.pop(n - _i);
            getWrongLineArray.pop(n - _i);
            replacementLine.pop(n - _i);
    d = d.dropna(subset=['LoC','Replacing_line', 'Replacing_line_number'], inplace=True);

#Calling the preprocessing function on all of our datasets
#preproccessingData(filenames = filenames1);
#preproccessingData(filenames = filenames2);
#preproccessingData(filenames = filenames3);
#preproccessingData(filenames = filenames4);
#preproccessingData(filenames = filenames5);

#Reading all of the replacement lines for all of the files
#readFirstLineOfFile(filenames = filenames1, array = replacementLines1);
readFirstLineOfFile(filenames = ogfilenames2, array = replacementLines2);
#readFirstLineOfFile(filenames = ogfilenames3, array = replacementLines3);
#readFirstLineOfFile(filenames = ogfilenames4, array = replacementLines4);
#readFirstLineOfFile(filenames = ogfilenames5, array = replacementLines5);
   
#Reading all of the train data    
#readTrainData(traindata = traindata1, content = arrayForStorage1);
readTrainData(traindata = traindata2, content = arrayForStorage2);
#readTrainData(traindata = traindata3, content = arrayForStorage3);
#readTrainData(traindata = traindata4, content = arrayForStorage4);
#readTrainData(traindata = traindata5, content = arrayForStorage5);

#THIS MUST ABSOLUTELY STAY HERE AND NOT MOVE
#getFiles(filenames = ogfilenames1, array = storage1); 
#getFiles(filenames = ogfilenames2, array = storage2);
#getFiles(filenames = ogfilenames3, array = storage3);
#getFiles(filenames = ogfilenames4, array = storage4);
#getFiles(filenames = ogfilenames5, array = storage5);
  
#overwriteFile(filenames = filenames1, array = storage1); 
#overwriteFile(filenames = filenames2, array = storage2);
#overwriteFile(filenames = filenames3, array = storage3);
#overwriteFile(filenames = filenames4, array = storage4);
#overwriteFile(filenames = filenames5, array = storage5);

getWrongLine(filenames = ogfilenames2, array = arrayForStorage2, newArray = wrongLines2);
#getWrongLine(filenames = ogfilenames3, array = arrayForStorage3, newArray = wrongLines3);
#getWrongLine(filenames = ogfilenames4, array = arrayForStorage4, newArray = wrongLines4);
#getWrongLine(filenames = ogfilenames5, array = arrayForStorage5, newArray = wrongLines5);

#Calling the translate function on all of our datasets
#translate(filenames = filenames1, array = arrayForStorage1);
translate(filenames = filenames2, replacementLine = replacementLines2, repLineNumber = arrayForStorage2, array = matrix2);#This one works fine
#translate(filenames = filenames3, replacementLine = replacementLines3, repLineNumber = arrayForStorage3, array = matrix3);#This one works fine
#translate(filenames = filenames4,replacementLine = replacementLines4, repLineNumber = arrayForStorage4, array = matrix4);#This one works fine
#translate(filenames = filenames5, replacementLine = replacementLines5, repLineNumber = arrayForStorage5, array = matrix5);#This one works fine           

removeCorruptData(array = matrix2, getWrongLineArray = wrongLines2, replacementLine = replacementLines2);
#removeCorruptData(array = matrix3, getWrongLineArray = wrongLines3, replacementLine = replacementLines3);
#removeCorruptData(array = matrix4, getWrongLineArray = wrongLines4, replacementLine = replacementLines4);
#removeCorruptData(array = matrix5, getWrongLineArray = wrongLines5, replacementLine = replacementLines5);

compareString(dataframe = matrix2, array = wrongLines2, replacementLine = replacementLines2);
#compareString(dataframe = matrix3, array = wrongLines3, replacementLine = replacementLines3);
#compareString(dataframe = matrix4, array = wrongLines4, replacementLine = replacementLines4);
#compareString(dataframe = matrix5, array = wrongLines5, replacementLine = replacementLines5);

#Exporting the datasets into CSV's    
exportToCSV(array = matrix2);