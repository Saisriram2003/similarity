import math

def clean_text(txt):
    '''cleans the txt file by making everything lowercase, removing punctuation and splitting based on white spaces.'''
    txt = txt.lower()
    txt = txt.replace('.', '')
    txt = txt.replace(',', '')
    txt = txt.replace('?', '')
    txt = txt.replace('!', '')
    txt = txt.replace(';', '')
    txt = txt.replace(':', '')
    txt = txt.replace('"', '')
    txt = txt.replace('<', '')
    txt = txt.replace('>', '')
    txt = txt.replace('[', '')
    txt = txt.replace(']', '')
    txt = txt.replace('  ',' ')
    lst = txt.split(' ')
    return lst
def stem(s):
    '''returns the stem of the word'''
    prefixes = {'anti','de','dis','en','em','fore','in','im','il','ir','inter','mis','mid','non','over','pre','re','semi','sub','super','trans','un','under'}
    suffixes = {'able','ible','ed','en','er','est','ful','ic','ion','tion','ation','ition','ing','ity','ty','ive','ative','itive','less','ly','ment','ness','ous','eous','ious','s','es'}
    if len(s) > 3 and s[-1] == 'y':
        s=s[:-1]+'i'
        return s

    elif len(s) > 3 and s[-3:] == 'ies':
        s=s[:-3] + 'y'
        return s
    elif len(s) > 6 and s[-3:] == 'ing' : 
        s=s[:-3]
        return s
    
    
    elif len(s) > 6 and s[-3:] == 'ers':
        return stem(s[:-1])

    elif len(s) > 4 and s[-1] =='s':
        s=s[:-1]
        return s

    elif len(s) > 4 and s[-2:] == 'ed':
        s=s[:-2]
        return s
    elif len(s) > 4 and s[-2:] == 'er':
        s=s[:-2]
        return s

    elif len(s) > 6 and s[-4:] == 'tion':
        s=s[:-3]+'e'
        return s
    elif len(s) == 4 and s[-1] == 'e':
        s=s[:-1]
        return s
    else:
    
        for prefix in prefixes:
            if s[0:len(prefix)] == prefix:
                s = s[len(prefix):]
                break
        for suffix in suffixes:
            if s[len(s) - len(suffix):] == suffix:
                s = s[:-(len(suffix))]
                break
        return s
    
def compare_dictionaries(d1, d2):
    '''compares 2 dictionaries and gives the score between them'''
    score = 0
    total = 0
    for x in d1:
        total += d1[x]       
    for y in d2:
        if y in d1:
            score += d2[y] * math.log(d1[y]/total)
        else:
            score += d2[y] * math.log(0.5/total)
    return score
            

class TextModel:
    '''serves as a blueprint for objects that model a body of text'''
    def __init__(self, model_name):
        '''constructor for the TextModel class'''
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.punct = {}
    def __repr__(self):
        '''returns a string representation of the TextModel class'''
        s = ''
        s += 'text model name: ' + self.name
        s += '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'

        s += '  number of word lengths: ' + str(len(self.word_lengths))
        s += '\n'
        s += '  number of stems: ' + str(len(self.stems))
        s += '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths))
        s += '\n'
        s += '  number of punctuations: ' + str(len(self.punct))

        return s
    def add_string(self, s):
        """Analyzes the string txt and adds its pieces
         to all of the dictionaries in this text model."""
        pre_clean = s.split()
        senlen = 0
        for word in pre_clean:
            if word[-1] != '.' and word[-1] != '!' and word[-1] != '?':
                senlen += 1
            else:
                senlen += 1 
                if senlen not in self.sentence_lengths:
                    self.sentence_lengths[senlen] = 1
                else: 
                    self.sentence_lengths[senlen] += 1
                senlen = 0
        punc = {}
        punc['!'] = 0
        punc['.'] = 0
        punc['?'] = 0
        punc[';'] = 0
        punc[':'] = 0
        punc[','] = 0
        for pc in pre_clean:
            if pc[-1] == '.':
                punc['.'] += 1
            elif pc[-1] == '!':
                punc['!'] += 1
            elif pc[-1] == '?':
                punc['?'] += 1
            elif pc[-1] == ':':
                punc[':'] += 1
            elif pc[-1] == ';':
                punc[';'] += 1
            elif pc[-1] == ',':
                punc[','] += 1
        for i in punc:
            if punc[i] != 0:
                self.punct[i] = punc[i]
                
     
                
        
        word_list = clean_text(s)
    
        for w in word_list:
            if w not in self.words:
                self.words[w] = 1
            else:
                self.words[w] += 1
        for x in word_list:
            if len(x) not in self.word_lengths:
                self.word_lengths[len(x)] = 1
            else:
                self.word_lengths[len(x)] += 1
                
        for y in word_list:
            if stem(y) not in self.stems:
                self.stems[stem(y)] = 1
            else:
                self.stems[stem(y)] += 1
        
        
    def add_file(self, filename):
        '''adds file to the model'''
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        text = f.read()
        f.close()
        self.add_string(text)
    def save_model(self):
        '''saves model to a file'''
        filename = self.name + '_' + 'words'
        f = open(filename, 'w')
        f.write(str(self.words))
        f.close()
        filename = self.name + '_' + 'word_lengths'
        f = open(filename, 'w')
        f.write(str(self.word_lengths))
        f.close()
        filename = self.name + '_' + 'stems'
        f = open(filename, 'w')
        f.write(str(self.stems))
        f.close()
        filename = self.name + '_' + 'sentence_lengths'
        f = open(filename, 'w')
        f.write(str(self.sentence_lengths))
        f.close()
        filename = self.name + '_' + 'punct'
        f = open(filename, 'w')
        f.write(str(self.punct))
        f.close()

    def read_model(self):
        '''reads file and stores it in a dictionary'''
        filename = self.name + '_' + 'words'
        f = open(filename, 'r')    # Open for reading.
        d_str = f.read()           # Read in a string that represents a dict.
        f.close()
        d = dict(eval(d_str))
        self.words = d
        filename = self.name + '_' + 'word_lengths'
        f = open(filename, 'r')    # Open for reading.
        d_str = f.read()           # Read in a string that represents a dict.
        f.close()
        d = dict(eval(d_str))
        self.word_lengths = d
        filename = self.name + '_' + 'stems'
        f = open(filename, 'r')    # Open for reading.
        d_str = f.read()           # Read in a string that represents a dict.
        f.close()
        d = dict(eval(d_str))
        self.stems = d
        filename = self.name + '_' + 'sentence_lengths'
        f = open(filename, 'r')    # Open for reading.
        d_str = f.read()           # Read in a string that represents a dict.
        f.close()
        d = dict(eval(d_str))
        self.sentence_lengths = d
        filename = self.name + '_' + 'punct'
        f = open(filename, 'r')    # Open for reading.
        d_str = f.read()           # Read in a string that represents a dict.
        f.close()
        d = dict(eval(d_str))
        self.punct = d
    def similarity_scores(self, other):
        '''generates list of similarity scores between 2 dictionaries using various features'''
        fscore = []
        word_score = compare_dictionaries(other.words, self.words)
        word_lengths_score = compare_dictionaries(other.word_lengths, self.word_lengths)
        stems_score = compare_dictionaries(other.stems, self.stems)
        sentence_lengths_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        punct_score = compare_dictionaries(other.punct, self.punct)
        fscore += [word_score]
        fscore += [word_lengths_score]
        fscore += [stems_score]
        fscore += [sentence_lengths_score]
        fscore += [punct_score]
        return fscore
    def classify(self, source1, source2):
        '''checks between 2 sources to see which the text is more similar to'''
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        print("scores for",source1.name,":",scores1)
        print("scores for",source2.name,":",scores2)
        weighted_sum1 = 10*scores1[0] + 5*scores1[1] + 10*scores1[2] + 10*scores1[3] + 3*scores1[4]
        weighted_sum2 = 10*scores2[0] + 5*scores2[1] + 10*scores2[2] + 10*scores2[3] + 3*scores2[4]
        if weighted_sum1 > weighted_sum2:
            print(self.name,"is more likely to have come from",source1.name)
        else:
            print(self.name,"is more likely to have come from",source2.name)


def test():
    """ test for the similarity scores """
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)   

def run_tests():
    """ runs several tests for the project """
    source1 = TextModel('rowling')
    source1.add_file('jkr.txt')
    source1.save_model()
    
    source2 = TextModel('shakespeare')
    source2.add_file('shaks12.txt')
    source2.save_model()
    
    

    rowling = TextModel('jkrsample')
    rowling.add_file('jkrsample.txt')
    rowling.classify(source1, source2)
    
    shake = TextModel('shakesample')
    shake.add_file('shakesample.txt')
    shake.classify(source1, source2)
    
    cs = TextModel('cssample')
    cs.add_file('cssample.txt')
    cs.classify(source1, source2)
    
    dickens = TextModel('dickenssample')
    dickens.add_file('dickenssample.txt')
    dickens.classify(source1, source2)
    
    

 