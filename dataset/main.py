from bs4 import BeautifulSoup as bs
import requests
from tqdm import tqdm
import re

def Preprocess(line):
    tempLine = line.replace("\n", "")
    tempLine = re.sub(r'<.+?>', '', tempLine)
    tempLine = tempLine.replace("  ", " ")
    tempLine = tempLine.replace("\t", " ")
    if tempLine.startswith(" "):
        tempLine = tempLine[1:]
    return tempLine

if __name__ == "__main__":
    linksFile = open("links.txt", "r")
    promptLinks = linksFile.readlines()
    linksFile.close()

    femalePositiveFile = open("female_positive.txt", 'a')
    femaleNegativeFile = open("female_negative.txt", 'a')

    for promptLink in tqdm(promptLinks, desc="Getting and Writing Prompts"):
        info = requests.get(promptLink).text
        soup = bs(info, "lxml")
        prompts = soup.findAll("pre", {"class":"mantine-Code-root mantine-Code-block mantine-2v44jn"})
        positiveLine = Preprocess(prompts[0].text)
        negativeLine = Preprocess(prompts[1].text)
        femalePositiveFile.write(f"{positiveLine}\n")
        femaleNegativeFile.write(f"{negativeLine}\n")
    
    femalePositiveFile.close()
    femaleNegativeFile.close()