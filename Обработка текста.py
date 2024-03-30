import pandas as pd
import requests
from bs4 import BeautifulSoup
import openpyxl
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

# Функция для предобработки текста
def preprocess_text(text):
    # Удаление HTML-тегов
    text = BeautifulSoup(text, "html.parser").get_text()
    # Приведение к нижнему регистру
    text = text.lower()
    # Удаление знаков препинания
    text = re.sub(r'\W', ' ', text)
    # Удаление лишних пробелов
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Удаление стоп-слов и лемматизация
    stop_words = set(stopwords.words('english'))  # Используйте 'russian' для русского языка
    lemmatizer = WordNetLemmatizer()
    word_tokens = word_tokenize(text)
    filtered_text = [lemmatizer.lemmatize(word) for word in word_tokens if word not in stop_words]
    
    return ' '.join(filtered_text)

def parse_reviews(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    reviews_data = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        review_elements = soup.find_all('div', class_='item-right')

        for element in review_elements:
            date = element.find('div', class_='review-postdate').get_text(strip=True) if element.find('div', class_='review-postdate') else ""
            advantages = element.find('div', class_='review-plus').get_text(strip=True) if element.find('div', class_='review-plus') else ""
            disadvantages = element.find('div', class_='review-minus').get_text(strip=True) if element.find('div', class_='review-minus') else ""
            review_text = element.get_text(strip=True)
            
            # Применение предобработки к каждому текстовому полю
            date = preprocess_text(date)
            advantages = preprocess_text(advantages)
            disadvantages = preprocess_text(disadvantages)
            review_text = preprocess_text(review_text)

            reviews_data.append([date, advantages, disadvantages, review_text])

        df = pd.DataFrame(reviews_data, columns=['Дата', 'Достоинства', 'Недостатки', 'Отзыв'])

        # Удаление дубликатов
        df = df.drop_duplicates()

        dates_df = df[['Дата']]
        advantages_df = df[['Достоинства']]
        disadvantages_df = df[['Недостатки']]
        reviews_df = df[['Отзыв']]

        dates_df.to_excel('only_dates.xlsx', index=False, engine='openpyxl')
        advantages_df.to_excel('only_advantages.xlsx', index=False, engine='openpyxl')
        disadvantages_df.to_excel('only_disadvantages.xlsx', index=False, engine='openpyxl')
        reviews_df.to_excel('only_reviews.xlsx', index=False, engine='openpyxl')

        print("Данные успешно сохранены в отдельные файлы.")
        df.to_excel('reviews.xlsx', index=False, engine='openpyxl')
        print("Данные успешно сохранены в файл 'reviews.xlsx'.")
    else:
        print(f"Ошибка доступа к сайту, код ответа HTTP: {response.status_code}")

url = 'https://otzovik.com/reviews/bank_tinkoff_kreditnie_sistemi/'
parse_reviews(url)
