from collections import OrderedDict

max_weight = 0 #calculate max number of words in pages and queries for weight
global_word_list = {} #dictionary for storing words and the apge names they have occured
global_list_of_pages = {} #dictionary for storing pages per their page names
global_list_of_queries = [] #list for storing queries

class Group:
    
    ''' Group class for pages and queries'''
    
    def __init__(self):
        self.name = ""
        self.word_list = {}
        self.count = 99999
        self.listOfWords = []

    def getName(self):
        return self.name
    
    def getWordList(self):
        return self.word_list

    def setName(self,name):
        self.name = name

    def setCount(self,count):
        self.count = count
    
    def setList(self,words):
        self.listOfWords = words

    def includeToList(self):
        
        ''' Assign weight from a counter variable(set by maximimum number obtained earlier) to the words '''
        
        for word in self.listOfWords:
            if word not in self.word_list:
                self.word_list[word] = self.count - 1
                self.count -= 1

def add_to_global(words,pageName):
    
    ''' function to fill the global_word_list with words as keys and list of page name, where they have occuered.
    : Parameters :
    words: list of words
    pageName: current page name being processed. '''
    
    for word in words:
        if word in global_word_list:
            global_word_list[word].append(pageName)
        else:
            global_word_list[word] = [pageName]

def create(value,i,t):
    
    ''' create page or query object and adds it to their respective global lists.
    : Parameters :
    value: string from input
    i: index for creating name of the page/query
    t: type '''
    
    page = Group()
    words = value.split()
    findMax(len(words)+1)
    page.setList(words)
    if t == 'p':
        page.setName("P" + str(i + 1))
        add_to_global(words, page.getName())
        global_list_of_pages[page.getName()] = page
    else:
        page.setName("Q" + str(i + 1))
        global_list_of_queries.append(page)

def findMax(number):

    ''' function to check the current maximimum and update if less than given number.
    to be used as variable weight
    : Parameters :
    number: to be compared to the max_weight '''
    
    global max_weight
    if max_weight < number:
        max_weight = number

def searchMain():
    
    ''' Search for pages '''
    
    for query in global_list_of_queries:
        visited = []
        d = {}
        for word in query.getWordList():
            if word in global_word_list:
                for page in global_word_list[word]:
                    if page not in visited:
                        visited.append(page)
                        sop = sumOfProducts(query,global_list_of_pages[page])
                        d[page] = sop
        d = OrderedDict(sorted(d.items(),key = lambda x: (-x[1], (x[0][0], int(x[0][1:])))))
        forPrint(query.getName(),d)

def sumOfProducts(query,page):
    
    ''' function to calculate SOP of the query for this page.
    : Parameters :
    query: query object
    page: page object
    return: SOP of the entire query for that page '''
    
    sop = 0
    for qword in query.getWordList():
        if qword in page.getWordList():
            sop = sop + query.getWordList()[qword] * page.getWordList()[qword]
    return sop
        
def forPrint(name,D):
    
    ''' function for outputing the result.
    : Parameters :
    name: query name
    D: Result of operations to be printed '''
    
    print(name,':',end = " ")
    i = 0
    for key in D.keys():
        if i < 5:
            print(key,end = " ")
            i += 1
        if i >= 5:
            break
    print("")
     
def assignWeights():
    
    ''' assigns weights to each word of each query and object, based on the maximum number being  calculated earlier '''
    
    for key,page in global_list_of_pages.items():
        page.setCount(max_weight)
        page.includeToList()
    for query in global_list_of_queries:
        query.setCount(max_weight)
        query.includeToList()

def readFromFile():
    
    ''' read input from file in same directory and prints the obtained input in console.
    Name the file as input in txt format.'''
    
    print("input read from input.txt file:")
    file = open('input.txt','r')
    page_index = 0
    query_index = 0
    for line in file:
        print(line,end = "")
        if line[0] == 'P':
            create(line[1:],page_index,'p')
            page_index += 1
        if line[0] == 'Q':
            create(line[1:],query_index,'q')
            query_index += 1
    print("\n")

if __name__=='__main__':                  
    readFromFile()
    assignWeights()
    searchMain()

