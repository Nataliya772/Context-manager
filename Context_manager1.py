import time
import contextlib
import json
import sys
import datetime

def read_news(news_fail):
    with open(news_fail, 'r', encoding = 'utf8') as file_open:
        news_file = json.load(file_open)
    all_news = {}
    news_temp = [news_file['rss']['channel']['items']]
    for news_name in news_temp:
        for name in news_name:
            id_news = name['_id']
            title_news = name['title']
            all_news[id_news] = title_news
        break
    return all_news

def write_log(log_file, args_geted):
    log_file.write(f'{datetime.datetime.utcnow()} - {args_geted}\n')

def find_news_by_tow_words(all_news, word1, word2, log_file):
    word_news = {}
    word_news_id = []
    for new in all_news.items():
        id_new = new[0]
        title = new[1].split()
        if word1 in title or word2 in title:
            word_news[id_new] = new[1]
            word_news_id.append(id_new)
    write_log(log_file, word_news_id)
    return word_news

@contextlib.contextmanager
def news_search(news_fail, word1, word2, log_file):
    try:
        time_open = time.time()
        print(f'Время запуска кода {time_open}')
        log_file = open(log_file, 'a')
        all_news = read_news(news_fail)
        word_news = find_news_by_tow_words(all_news, word1, word2, log_file)
        yield log_file, word_news
    finally:
        exc_type, exc_val, exc_tb = sys.exc_info()
        if exc_val is not None:
            write_log(log_file, exc_val)
        log_file.close()
        time_close = time.time()
        print(f'Время окончания работы {time_close}')
        print(f'Время работы кода {time_close - time_open} секунд\n')

if __name__ == '__main__':
    with news_search('newsafr.json', 'ДТП', 'шенген', 'found_news1.log') as file:
        log_file, word_news = file
        print(f'Найденные по выбранным словам новости {word_news}\n')
