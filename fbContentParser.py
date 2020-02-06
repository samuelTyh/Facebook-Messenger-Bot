import os
import json
from tqdm import tqdm
import datetime


class FacebookContentParser(object):
    root = 'Dataset/facebook-yhtsamuel/'

    def extract_messages(self):
        chat_root = 'messages'
        writing_dir = 'data/facebook_chat'

        for root, dirs, files in tqdm(os.walk(os.path.join(self.root, chat_root))):
            for name in files:
                if not name == 'message_1.json':
                    continue
                data = json.load(open(os.path.join(root, name), 'r', encoding='utf-8'))

                for msg in data['messages']:
                    try:
                        if msg['sender_name'] == 'Yu Hsiang Tseng':
                            if msg['content'] != "You are now connected on Messenger.":
                                content = msg['content']
                                ts = datetime.datetime.fromtimestamp(msg['timestamp_ms'] / 1000)

                                filename = os.path.join(writing_dir,
                                                        str(ts.year) + '-' + str(ts.month) + '-' + str(ts.day) + '.txt')
                                if not os.path.exists(writing_dir):
                                    os.makedirs(writing_dir)

                                with open(filename, 'a+', encoding='utf8') as out_file:
                                    out_file.write(content + '\n')
                    except KeyError:
                        pass

    def extract_posts(self):

        in_data = 'posts/your_posts_1.json'
        writing_dir = 'data/facebook_posts'

        data = json.load(open(os.path.join(self.root, in_data), 'r'))

        for post in data['status_updates']:
            try:
                ts = datetime.datetime.fromtimestamp(post['timestamp'])
                post_text = post['data'][0]['post']

                filename = os.path.join(writing_dir, str(ts.year) + '-' + str(ts.month) + '-' + str(ts.day) + '.txt')
                if not os.path.exists(writing_dir):
                    os.makedirs(writing_dir)

                with open(filename, 'a+') as out_file:
                    out_file.write(post_text + '\n')
            except KeyError:
                print(post)

    def extract_comments(self):
        comment_path = 'comments/comments.json'
        writing_dir = 'data/facebook_comments'

        data = json.load(open(os.path.join(self.root, comment_path), 'r'))
        for comment in data['comments']:
            try:
                for d in comment['data']:
                    if d['comment']['author'] == "Yu Hsiang Tseng":
                        ts = datetime.datetime.fromtimestamp(d['comment']['timestamp'])
                        com = d['comment']['comment']

                        filename = os.path.join(
                            writing_dir, str(ts.year) + '-' + str(ts.month) + '-' + str(ts.day) + '.txt'
                        )
                        if not os.path.exists(writing_dir):
                            os.makedirs(writing_dir)

                        with open(filename, 'a+') as out_file:
                            out_file.write(com + '\n')
            except KeyError:
                print(comment)
