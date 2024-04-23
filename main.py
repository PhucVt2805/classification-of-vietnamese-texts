import joblib
import streamlit as st

def remove_number(sentence):
    return ' '.join(word for word in sentence.split() if not word.isdigit())

def remove_stop_words(sentence, stop_words_file):
    with open(stop_words_file, 'r', encoding='utf-8') as file:
        stop_words = file.read().split('\n')
    return ' '.join(word for word in sentence.split() if word not in stop_words)

def unconvert(dict, value):
    for k, v in dict.items():
        if value == v:
            return k
    return "Không xác định"

def run():
    model, tfidf_vectorizer, category_dict = joblib.load('Model/model.joblib')

    st.set_page_config(page_title="Hệ thống phân loại văn bản", page_icon="👋")

    st.write("# Hệ thống phân loại văn bản")

    sentence = st.text_input('Nhập tiêu đề văn bản:')

    if st.button('Submit', type='primary') and sentence:
        processed_sentence = remove_number(sentence.lower())
        processed_sentence = remove_stop_words(processed_sentence, 'Data/vietnamese_stop_words.txt')
        vectorized_sentence = tfidf_vectorizer.transform([processed_sentence])
        category = model.predict(vectorized_sentence)[0]
        category_name = unconvert(category_dict, category)
        st.title(f'Với tiêu đề trên, thể loại của văn bản sẽ thuộc: {category_name}')

if __name__ == "__main__":
    run()
