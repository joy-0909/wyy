import json
import time
import requests

headers = {
        'Host': 'music.163.com',
}


def get_comments(page):

    url = 'http://music.163.com/api/v1/resource/comments/R_SO_4_446557635?limit=20&offset=' + str(page)
    response = requests.get(url=url, headers=headers)
    # 将字符串转为json格式
    result = json.loads(response.text)
    items = result['comments']
    for item in items:

        user_name = item['user']['nickname'].replace(',', '，')
        user_id = str(item['user']['userId'])
        user_message = get_user(user_id)
        user_age = str(user_message['age'])
        user_gender = str(user_message['gender'])
        user_city = str(user_message['city'])
        user_introduce = user_message['sign'].strip().replace('\n', '').replace(',', '，')
        comment = item['content'].strip().replace('\n', '').replace(',', '，')
        comment_id = str(item['commentId'])
        praise = str(item['likedCount'])
        date = time.localtime(int(str(item['time'])[:10]))
        date = time.strftime("%Y-%m-%d %H:%M:%S", date)
        print(user_name, user_id, user_age, user_gender, user_city, user_introduce, comment, comment_id, praise, date)

        with open('music_comments.csv', 'a', encoding='utf-8-sig') as f:
            f.write(user_name + ',' + user_id + ',' + user_age + ',' + user_gender + ',' + user_city + ',' + user_introduce + ',' + comment + ',' + comment_id + ',' + praise + ',' + date + '\n')
        f.close()


def get_user(user_id):
    data = {}
    url = 'https://music.163.com/api/v1/user/detail/' + str(user_id)
    response = requests.get(url=url, headers=headers)
    # 将字符串转为json格式
    js = json.loads(response.text)
    if js['code'] == 200:
        data['gender'] = js['profile']['gender']
        if int(js['profile']['birthday']) < 0:
            data['age'] = 0
        else:
            data['age'] = (2018 - 1970) - (int(js['profile']['birthday']) // (1000 * 365 * 24 * 3600))
        if int(data['age']) < 0:
            data['age'] = 0
        data['city'] = js['profile']['city']
        data['sign'] = js['profile']['signature']
    else:
        data['gender'] = '无'
        data['age'] = '无'
        data['city'] = '无'
        data['sign'] = '无'
    return data


def main():
    for i in range(0, 25000, 20):
        print('\n---------------第 ' + str(i // 20 + 1) + ' 页---------------')
        get_comments(i)


if __name__ == '__main__':
    main()