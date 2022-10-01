# NASA 2022 Space App Challenge 

**Team Name:** Word Space Explorer  
**Author:** Joseph Cheng  
**Date:** 27/09/2022  

## 1. Theme: **Make Space - “there’s always space for one more”**
- S: Safe, Solve
- P: Possibility, People
- A: Access, Appreciation
- C: Collaboration, Culture
- E: Equity, Empowerment

## 2. Challenge:  
[CAN AI PRESERVE OUR SCIENCE LEGACY?](https://2022.spaceappschallenge.org/challenges/2022-challenges/science-legacy/details )

The NASA Technical Report Server (NTRS) includes hundreds of thousands of items containing scientific and technical information (STI) created or funded by NASA. Imagine how difficult it can be to locate desired information in such a large repository! Your challenge is to develop a technique using Artificial Intelligence (AI) to improve the accessibility and discoverability of records in the public NTRS.


## 3. Approach:

1. Building a corpus  
  1.1. Obtain PDF files & Meta Data via NTRS  
  1.2. Create a MVP corpus based on filtered criteria
2. Create a NLP Vector Space model on  
    2.1. V1 - Title + Abstract (Mid Level Detail)  
    2.2. Txt File (Detailed Detail)  
3. Create a search engine using the Vector Space Model above  
    3.1. Use Cosin Similarity to recommend the top x Titles + Abstracts / Paragraphs
4. Implement Front-End that Provides:
    4.1. Search Text used to search for most relevant Document (Title)  
    4.2. Search Text used to search for most relevant Document (Abstract)  
    4.3. Search Text used to search for most relevant Paragraph within Documents (Paragraph)  
    4.4. Word Vector Space visualisation


## 4. How to Run:
1. (Optional) create a python virtual environment  
    python -m venv env
2. (Optional) activate into the environment  
    (Windows) .\env\Scripts/activate  
    (Mac / Linux) source env/bin/activate
3. Install required packages  
    pip install -r requirements.txt
4. (IMPORTANT) Install ＧloVe word embed
    cd model/
    wget http://nlp.stanford.edu/data/glove.6B.zip
    unzip -q model/glove.6B.zip


## 5. Inspirations and Citation
1. [Word Embedding, Character Embedding and Contextual Embedding in BiDAF — an Illustrated Guide](https://towardsdatascience.com/the-definitive-guide-to-bidaf-part-2-word-embedding-character-embedding-and-contextual-c151fc4f05bb#:~:text=Character%20level%20embedding%20uses%20one,a%20word%2C%20character%20by%20character.)
2. [JFK Cognitive Search](https://jfk-demo-2019.azurewebsites.net/#/search?term=oswald)
3. [GloVe: Global Vectors for Word Representation](https://nlp.stanford.edu/projects/glove/)