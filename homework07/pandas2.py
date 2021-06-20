# %matplotlib inline
import matplotlib.pyplot as plt  # type: ignore

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd  # type: ignore
import seaborn as sns  # type: ignore

"""## Загрузка и знакомство с данными

Для работы вам понадобятся предобработанные данные нашего учебного конкурса на kaggle [«Прогноз популярности статьи на Хабре»](https://www.kaggle.com/c/howpop-habrahabr-favs). Скачайте [данные](https://drive.google.com/file/d/1nV2qV9otN3LnVSDqy95hvpJdb6aWtATk/view?usp=sharing) соревнования (данные были удалены с Kaggle ради организации последующего идентичного соревнования, так что тут ссылка на Google Drive).
"""

import io
import os

import matplotlib.pyplot as plt #type: ignore

# %matplotlib inline
import numpy as np #type: ignore

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd #type: ignore

df = pd.read_csv("howpop_train.csv")
# delimiter=",", names = ["url", "domain", "post_id", "published", "author", "flow", "polling", "content_len", "title", "comments", "favs", "views", "votes_plus", "votes_minus", "views_lognorm", "favs_lognorm", "comments_lognorm"])

df.shape

df.head(3).T

"""Избавимся сразу от переменных, названия которых заканчиваются на `_lognorm` (нужны для соревнования на Kaggle). Выберем их с помощью `filter()` и удалим `drop`-ом:"""

df.drop(filter(lambda c: c.endswith("_lognorm"), df.columns), axis=1, inplace=True)
# избавляет от необходимости сохранять датасет

df.describe().T

df.describe(include=["object", "bool"]).T  # бинарные и категориальные переменные

# настройка внешнего вида графиков в seaborn
sns.set_style("dark")
sns.set_palette("RdBu")
sns.set_context("notebook", font_scale=1.5, rc={"figure.figsize": (15, 5), "axes.titlesize": 18})

"""Столбец **`published`** (время публикации) содержит строки. Чтобы мы могли работать с этими данными как с датой/временем публикации, приведём их к типу `datetime`:"""

print(df.published.dtype)
df["published"] = pd.to_datetime(df.published, yearfirst=True)
print(df.published.dtype)

"""Создадим несколько столбцов на основе данных о времени публикации:"""

df["year"] = [d.year for d in df.published]
df["month"] = [d.month for d in df.published]

df["dayofweek"] = [d.isoweekday() for d in df.published]
df["hour"] = [d.hour for d in df.published]

"""-----
Теперь Ваша очередь. В каждом пункте предлагается построить картинку и с ее помощью ответить на вопрос в [форме](https://docs.google.com/forms/d/e/1FAIpQLSf3b5OG8zX_nLQBQ-t20c6M5Auz-VUL-yxj8Fm9_o_XWDBTrg/viewform?c=0&w=1). Конечно, можно попытаться ответить на все вопросы только с Pandas, без картинок, но мы советуем Вам потренироваться строить (красивые) визуализации.

## 1\. В каком месяце (и какого года) было больше всего публикаций?

* март 2016
* март 2015
* апрель 2015
* апрель 2016
"""

march_2015 = df.query("year == 2015 & month == 3").shape[0]
march_2015

march_2016 = df.query("year == 2016 & month == 3").shape[0]
march_2016

april_2015 = df.query("year == 2015 & month == 4").shape[0]
april_2015

april_2016 = df.query("year == 2016 & month == 4").shape[0]
april_2016

df.drop(filter(lambda c: c.endswith("_lognorm"), df.columns), axis=1, inplace=True)

sns.set_style("white")
sns.set_palette("RdBu")
sns.set_context("notebook", font_scale=0.75, rc={"figure.figsize": (30, 15), "axes.titlesize": 12})

march_or_april = pd.DataFrame(
    {"2015": [march_2015, april_2015], "2016": [march_2016, april_2016]}, index=["March", "April"]
)
march_or_april.plot.bar(color=["deepskyblue", "dimgrey"], rot=0)

"""## 2\. Проанализируйте публикации в месяце из предыдущего вопроса

Выберите один или несколько вариантов:

* Один или несколько дней сильно выделяются из общей картины
* На хабре _всегда_ больше статей, чем на гиктаймсе
* По субботам на гиктаймс и на хабрахабр публикуют примерно одинаковое число статей

Подсказки: постройте график зависимости числа публикаций от дня; используйте параметр `hue`; не заморачивайтесь сильно с ответами и не ищите скрытого смысла :)
"""

df["dates"] = [str(p)[:7] for p in df.published]
list = df.dates.value_counts().index[0]
df_popmonth = df[df.dates == list]
df_popmonth["day"] = [p.day for p in df_popmonth.published]
sns.countplot(x="day", data=df_popmonth)

"""## 3\. Когда лучше всего публиковать статью?

* Больше всего просмотров набирают статьи, опубликованные в 12 часов дня
* У опубликованных в 10 утра постов больше всего комментариев
* Больше всего просмотров набирают статьи, опубликованные в 6 часов утра
* Максимальное число комментариев на гиктаймсе набрала статья, опубликованная в 9 часов вечера
* На хабре дневные статьи комментируют чаще, чем вечерние
"""

print(df.groupby("hour")["views"].mean().sort_values(ascending=False)[:5])

print(df.groupby("hour")["comments"].mean().sort_values(ascending=False)[:5])

print(
    df[df.domain == "habrahabr.ru"]
    .groupby("hour")["comments"]
    .mean()
    .sort_values(ascending=False)[:5]
)

df[df.domain == "habrahabr.ru"].groupby("hour")[["comments"]].mean().plot()

"""## 4\. Кого из топ-20 авторов чаще всего минусуют?

* @Mordatyj
* @Mithgol
* @alizar
* @ilya42
"""

df[df.author.isin(["@Mordatyj", "@Mithgol", "@alizar", "@ilya42"])].groupby("author")[
    ["votes_minus"]
].mean().sort_values("votes_minus", ascending=False)

who = pd.DataFrame(
    {"votes_minus": [20.481081, 7.928191, 7.471455, 6.216797]},
    index=["@Mithgol", "@alizar", "@Mordatyj", "@ilya42"],
)
who.plot.bar(color=["deepskyblue", "dimgrey", "mediumspringgreen", "orange"], rot=0)

"""## 5\. Сравните субботы и понедельники

Правда ли, что по субботам авторы пишут в основном днём, а по понедельникам — в основном вечером?
"""

fig = plt.figure(figsize=(20, 20))
fig.add_subplot(1, 1, 1)
pl = sns.countplot(y="hour", hue="dayofweek", data=df[df.dayofweek.isin([1, 6])], palette="Set2")
pl.set_title("Количество публикаций за час", fontweight="bold")
