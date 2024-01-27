from numpy import negative, positive
import pandas as pd
from bs4 import BeautifulSoup
import requests 
import os 
import nltk
nltk.download('punkt')
import syllables




def remove_stopwords(text):
    folder_path = 'StopWords'  # Replace with your folder path

# Get a list of all files in the folder
    all_files = os.listdir(folder_path)

    # Filter out only the files (not directories)
    file_paths = [os.path.join(folder_path, file) for file in all_files if os.path.isfile(os.path.join(folder_path, file))]
    all_stop_words=set()
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            stop_words = set(word.strip() for word in file.readlines())
            for x in stop_words:
                all_stop_words.add(x)
    words = text.split()
    cleaned_words = [word for word in words if word.lower() not in all_stop_words]
    cleaned_text = ' '.join(cleaned_words)
    return cleaned_text
    

def positive_negative_score(tokens):
    folder_path = 'MasterDictionary'  # Replace with your folder path

# Get a list of all files in the folder
    all_files = os.listdir(folder_path)

    # Filter out only the files (not directories)
    file_paths = [os.path.join(folder_path, file) for file in all_files if os.path.isfile(os.path.join(folder_path, file))]
    positive = set()
    negative = set()
    for file_path in file_paths:
        
        if file_path == 'MasterDictionary\positive-words.txt':
            
            with open(file_path, 'r') as file:
                positive = set(word.strip() for word in file.readlines())
        else :
            with open(file_path, 'r') as file:
                negative  = set(word.strip() for word in file.readlines())
   
    positive_score , negative_score = 0 ,0
    for word in tokens :
        if word in positive :
            positive_score += 1
        elif word in negative :
            negative_score += 1
    return positive_score , negative_score

def polarity_score(positive_score,negative_score):
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    return polarity_score

def subjective_score(positive_score,negative_score,tokens):
    subjectivity_score = (positive_score + negative_score) / (len(tokens) + 0.000001)
    return subjectivity_score

def average_sentence_length(text,tokens,sentences):
    
    average_sentence_length = len(tokens) / len(sentences)
    return average_sentence_length

def percentage_complex_words(complex_words,tokens):
    
    percentage_complex_words = len(complex_words) / len(tokens) * 100
    return percentage_complex_words

def fog_index(average_sentence_length_value, percentage_complex_words_value):
    fog_index = 0.4 * (average_sentence_length_value + percentage_complex_words_value)
    return fog_index

def average_words_per_sentence(tokens,sentences):
    average_words_per_sentence = len(tokens) / len(sentences)
    return average_words_per_sentence

def simple_syllable_count(word):
    vowels = "aeiouyAEIOUY"
    count = sum(1 for char in word if char in vowels)
    return count

def personal_pronouns(tokens):
    personal_pronouns = ["I", "we", "my", "ours", "us"] 
    personal_pronoun_count = sum(1 for word in tokens if word.lower() in personal_pronouns)
    return personal_pronoun_count

def average_word_length(tokens,word_count):
    average_word_length = sum(len(word) for word in tokens) / word_count
    return average_word_length


    


def main():
    df1 = pd.read_excel('Input.xlsx')
    
    df = pd.read_excel('Output Data Structure.xlsx')
    for x in range(len(df)):
        print(f"row number : {x}")
        URL = df1['URL'].iloc[x]
        r = requests.get(URL) 
        soup = BeautifulSoup(r.content, 'html5lib')
        data = soup.find('div',class_ = "td-post-content tagdiv-type")
        if data is not None:
            reviews_selector = data.get_text()
            # Your further processing of 'data' goes here
        else:
            print("Content not found on the page.")
            continue
        
        
        
        s = reviews_selector.split("\n")
        filtered_list = list(filter(lambda x: x.strip() != '', s))

        # Remove '\t' from each string
        filtered_list = [s.replace('\t', '') for s in filtered_list]
        filtered_list = [s.strip().replace('\t', '').replace('  ', ' ') for s in filtered_list if s.strip() != '']
        text = '\n'.join(filtered_list)
        cleaned_text = remove_stopwords(text)
        tokens = nltk.word_tokenize(cleaned_text)
        sentences = nltk.sent_tokenize(text)
        complex_words = [word for word in tokens if syllables.estimate(word) > 2]
        cleaned_text = remove_stopwords(text)
        complex_word_count = len(complex_words)
        word_count = len(tokens)
        #syllable_count_per_word = [syllable_count(word) for word in tokens]  taking too much time
        positive_score,negative_score = positive_negative_score(tokens)
        polarity_score_value = polarity_score(positive_score,negative_score)
        subjectivity_score_value = subjective_score(positive_score,negative_score,tokens)
        average_sentence_length_value = average_sentence_length(text,tokens,sentences)
        percentage_complex_words_value = percentage_complex_words(complex_words,tokens)
        fog_index_value = fog_index(average_sentence_length_value, percentage_complex_words_value)
        average_words_per_sentence_value = average_words_per_sentence(tokens,sentences)
        personal_pronoun_count_value = personal_pronouns(tokens)
        average_word_length_value = average_word_length(tokens,word_count)
        print("Cleaned Text:", cleaned_text)
        print("Positive Score:", positive_score)
        print("Negative Score:", negative_score)
        print("Polarity Score:", polarity_score_value)
        print("Subjectivity Score:", subjectivity_score_value)
        print("Average Sentence Length:", average_sentence_length_value)
        print("Average Words Per Sentence:", average_words_per_sentence_value)
        print("Complex Word Count:", complex_word_count)
        print("Word Count:", word_count)
        #print("Syllable Count Per Word:", syllable_count_per_word)
        print("Personal Pronoun Count:", personal_pronoun_count_value)
        print("Average Word Length:", average_word_length_value)
        print("Fog Index:", fog_index_value)
        print("percentage_complex_words:", percentage_complex_words_value)
        df['POSITIVE SCORE'].iloc[x] = positive_score
        df['NEGATIVE SCORE'].iloc[x] = negative_score
        df['POLARITY SCORE'].iloc[x] = polarity_score_value
        df['SUBJECTIVITY SCORE'].iloc[x] = subjectivity_score_value
        df['AVG SENTENCE LENGTH'].iloc[x] = average_sentence_length_value
        df['PERCENTAGE OF COMPLEX WORDS'].iloc[x] = percentage_complex_words_value
        df['FOG INDEX'].iloc[x] = fog_index_value
        df['AVG NUMBER OF WORDS PER SENTENCE'].iloc[x] = average_words_per_sentence_value
        df['COMPLEX WORD COUNT'].iloc[x] = complex_word_count
        df['WORD COUNT'].iloc[x] = word_count
        df['SYLLABLE PER WORD'].iloc[x] = 'taking too much time'
        df['PERSONAL PRONOUNS'].iloc[x] = personal_pronoun_count_value
        df['AVG WORD LENGTH'].iloc[x] = average_word_length_value
    
    # Add similar lines for other columns

    # Save the updated DataFrame to an Excel file
    df.to_excel('output.xlsx', index=False)


if __name__ == '__main__':
    main()







