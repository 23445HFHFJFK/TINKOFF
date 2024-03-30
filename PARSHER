import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from random import randint


def parse_reviews(url):
    session = requests.Session()
    import random
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
        # Добавьте больше строк User-Agent для разнообразия
    ]

    headers = {'User-Agent': random.choice(user_agents)}

    session.headers.update(headers)

    try:
        response = session.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Проверяем наличие элемента капчи по уникальному классу или id
            if soup.find('div', id='captcha') or "Please prove you are not a robot" in response.text:
                print("Обнаружена капча!")
            else:
                print("Капча не обнаружена.")

            reviews_data = []

            # Вместо отдельного поиска кратких и полных отзывов, ищем контейнеры отзывов
            review_containers = soup.find_all('div', class_='item-right')  # Примерный класс, проверьте точный

            for container in review_containers:
                # Используем метод .find() для поиска внутри контейнера
                date = container.find('div', class_='review-postdate').text.strip() if container.find('div',
                                                                                                      class_='review-postdate') else "Дата не указана"
                pros = container.find('div', class_='review-plus').text.strip() if container.find('div',
                                                                                                  class_='review-plus') else "Достоинства не указаны"
                cons = container.find('div', class_='review-minus').text.strip() if container.find('div',
                                                                                                   class_='review-minus') else "Недостатки не указаны"

                # Для краткого содержания и полного отзыва, предположим, что они также внутри контейнера
                teaser = container.find(class_='review-teaser').text.strip() if container.find(
                    class_='review-teaser') else "Краткое содержание не найдено"
                full_review_text = "Не найдено"
                full_review = container.find('h3')
                if full_review:
                    next_siblings = list(full_review.next_siblings)
                    for sibling in next_siblings:
                        if sibling.name and sibling.name in ['p', 'div']:
                            full_review_text = sibling.text.strip()
                            break

                reviews_data.append({
                    "Дата": date,
                    "Достоинства": pros,
                    "Недостатки": cons,
                    "Краткое содержание": teaser,
                    "Полный отзыв": full_review_text
                })

            reviews_df = pd.DataFrame(reviews_data)
            reviews_df.to_csv('reviews.csv', index=False, encoding='cp1251')
            print("Отзывы сохранены в файл 'reviews.csv'.")
        else:
            print(f"Ошибка доступа к странице: HTTP {response.status_code}")
    except requests.RequestException as e:
        print(f"Ошибка при запросе к {url}: {e}")

    # Пауза, чтобы минимизировать риск блокировки
    time.sleep(randint(100, 500))


# Подставьте свой URL
url = 'https://otzovik.com/reviews/bank_tinkoff_kreditnie_sistemi/'  # Замените это на реальный URL страницы с отзывами
parse_reviews(url)
