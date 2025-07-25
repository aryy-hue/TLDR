import streamlit as st
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from heapq import nlargest
import string

def summarize_text(text, num_sentences):
    original_sentences = sent_tokenize(text)

    if len(original_sentences) <= num_sentences:
        return text

    stop_words = set(stopwords.words('indonesian') + stopwords.words('english') + list(string.punctuation))

    words = word_tokenize(text.lower())

    word_frequencies = {}
    for word in words:
        if word not in stop_words:
            if word not in word_frequencies:
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    if not word_frequencies:
        return "Text is not relevant enough to be summarized."
    
    max_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word] / max_frequency)

    sentence_scores = {}
    for sent in original_sentences:
        sentence_words = word_tokenize(sent.lower())
        for word in sentence_words:
            if word in word_frequencies:
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores:
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]

    summary_sentences = nlargest(num_sentences, sentence_scores, key=sentence_scores.get)

    summary = ' '.join(summary_sentences)
    return summary

def main():
    st.set_page_config(page_title='TLDR', page_icon='✍️', layout='wide')

    st.title('✍️ TLDR: Text Summarizer')
    st.write('Paste your text or an article below to get a quick summary.')

    text_input = st.text_area('Insert your text here:', height=250, placeholder='Type or paste your text here...')

    num_sentences_to_summarize = st.slider(
        "Choose the summary length (in sentences):",
        min_value=1,
        max_value=10,
        value=3,
        step=1
    )

    if st.button("Create Summary"):
        if text_input.strip():
            with st.spinner('Summarizing...'):
                summary_result = summarize_text(text_input, num_sentences_to_summarize)
                st.subheader("Your Summary:")
                st.success(summary_result)
        else:
            st.warning("Please insert some text first.")

if __name__ == '__main__':
    try:
        stopwords.words('indonesian')
        stopwords.words('english')
    except LookupError:
        st.info('Downloading language data for the first time...')
        nltk.download('stopwords')
        nltk.download('punkt')
        st.rerun()

    main()

