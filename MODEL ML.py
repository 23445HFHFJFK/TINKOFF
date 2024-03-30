
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import pandas as pd

# Предполагается, что df - это ваш DataFrame с колонками 'Отзыв' и 'Метка'
# Перед выполнением этого кода убедитесь, что у вас есть эти данные

# Разделение данных на обучающую и тестовую выборки
from MEM import df

X_train, X_test, y_train, y_test = train_test_split(df['Отзыв'], df['Метка'], test_size=0.3, random_state=42)

# Векторизация текста
vectorizer = CountVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Создание и обучение модели
model = MultinomialNB()
model.fit(X_train_vec, y_train)

# Предсказание на тестовых данных
y_pred = model.predict(X_test_vec)

# Расчет точности
accuracy = accuracy_score(y_test, y_pred)
print(f"Точность модели: {accuracy:.2f}")
