import datetime
from pydriller import RepositoryMining
from collections import Counter
from wordcloud import WordCloud
from services.utilities import Util
import matplotlib.pyplot as plt

# Class to analysis all commits from a branch of git repository
class CheckCommits:
    # constructor pass the path of repository
    def __init__(self, repository, name):
        self.repository = repository
        self.name = name
    
    # List all Commits from Authors
    # return a dictionary like this: hash, author, date, list of files in commit
    # dictionary = {'hash': ['author', 'date of commit', [file1, file2, ...]]}
    def dictionaryWithAllCommmits(self):
        dictionaryAux = {}
        for commit in RepositoryMining(self.repository).traverse_commits():
            commitAuthorNameFormatted = '{}'.format(commit.author.name)
            commitAuthorDateFormatted = '{}'.format(commit.author_date)
            listFilesModifiedInCommit = []
            for modification in commit.modifications:
                itemMofied = '{}'.format(modification.filename)
                listFilesModifiedInCommit.append(itemMofied)
            dictionaryAux[commit.hash] = [commitAuthorNameFormatted, commitAuthorDateFormatted, listFilesModifiedInCommit] 
        return dictionaryAux

    # Return a Counter with frequency of each file analysed
    # The Counter like this:
    # Counter({file1: frequency of file1, file2: frequence of file2, ...})
    def counterWithFrequencyOfFile(self):
        listFull = []
        for key, value in self.dictionaryWithAllCommmits().items():
            listAxu = []
            listAxu = value[2]
            for eachItem in listAxu:
                listFull.append(eachItem)
        return Counter(listFull)

    # Generate a Word of Cloud about each file according frequence
    def generateWordCloud(self):
        dictionaryOfFileFrequence = self.counterWithFrequencyOfFile()
        wordcloud = WordCloud(width = 3000, height = 2000, random_state=1, background_color='black', colormap='Set2', collocations=False)
        wordcloud.generate_from_frequencies(frequencies=dictionaryOfFileFrequence)
        # Display the generated image:
        plt.figure()
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        # Save the image in the img folder:
        pathFile = "/Users/armandosoaressousa/testes/sysrepomsr/img/"
        fileName = pathFile + self.name + ".png"
        wordcloud.to_file(fileName)