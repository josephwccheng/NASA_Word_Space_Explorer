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
2. PDF to XML
3. Extract Paragraph, Header information from the XML file
4. Create a NLP Vector Space model on:
    4.1. Title (High Level Detail)
    4.2. Abstract (Mid Level Detail)
    4.3. Paragraph (Detailed Detail)
5. Create a search engine using the Vector Space Model above
    5.1. Use Cosin Similarity to recommend the top x Titles / Abstracts / Paragraphs
6. Implement Front-End that Provides:
    6.1. Search Text used to search for most relevant Document (Title)
    6.2. Search Text used to search for most relevant Document (Abstract)
    6.3. Search Text used to search for most relevant Paragraph within Documents (Paragraph)
    6.4. Word Vector Space visualisation


## 4. How to Run:
1. (Optional) create a python virtual environment  
    python -m venv env
2. (Optional) activate into the environment  
    (Windows) .\env\Scripts/activate  
    (Mac / Linux) source env/bin/activate
3. Install required packages  
    pip install -r requirements.txt
4. Install ＧloVe word embed
    cd model/
    wget http://nlp.stanford.edu/data/glove.6B.zip
    unzip -q model/glove.6B.zip