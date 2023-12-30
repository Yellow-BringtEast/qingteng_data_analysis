import json
import os
import re

import pandas as pd

null = 'null'
false = 'false'
true = 'true'


class GetCommentData:
    def __init__(self):
        # 评论请求地址
        self.url_list = ['https://api-love.qingteng-inc.com/moment/get_moment_detail',
                         'https://api-love.qingteng-inc.com/moment/get_comments_list']

    def response(self, flow):
        # 拦截请求，如果为评论请求，则获取评论内容
        if flow.request.url in self.url_list:

            moment_info_lst = []
            comment_info_lst = []

            # 获取投票id
            res_body = flow.request.get_text()
            moment_id = re.findall('moment_id=([0-9]+)', res_body)[0]

            # 获取评论内容
            res = flow.response.content
            res_json = json.loads(res)

            moment_info, comment_list = self.extract_data(res_json, moment_id)

            if moment_info is not None:
                moment_info_lst.append(moment_info)

            comment_info_lst.append(comment_list)

            # 保存数据
            self.sava_data(moment_info_lst, comment_info_lst)

    @staticmethod
    def sava_data(moment_info_lst, comment_info_lst):
        try:
            df_moment_info = pd.read_csv('../data/moment_info.csv')
        except FileNotFoundError:
            df_moment_info = pd.DataFrame()

        try:
            df_comment_info = pd.read_csv('../data/comment_info.csv')
        except FileNotFoundError:
            df_comment_info = pd.DataFrame()

        df_moment = pd.DataFrame(moment_info_lst).drop_duplicates(subset=['moment_id'])

        df_comment = pd.DataFrame()
        for comment_info in comment_info_lst:
            df_temp = pd.DataFrame(comment_info)
            df_comment = pd.concat([df_comment, df_temp])

        df_moment_info = pd.concat([df_moment_info, df_moment])
        df_moment_info.drop_duplicates(subset=['moment_id'], inplace=True)
        df_moment_info.to_csv('../data/moment_info.csv', index=False)

        df_comment_info = pd.concat([df_comment_info, df_comment])
        df_comment_info.drop_duplicates(inplace=True)
        df_comment_info.to_csv('../data/comment_info.csv', index=False)

    @staticmethod
    def extract_data(moment_data, moment_id):
        moment_data = moment_data['data']

        if moment_data is None:
            moment_info_data = None
            comment_info_data = None

        elif 'moment_info' in moment_data.keys():
            moment_info_data = {
                'moment_id': moment_data['vote_detail']['vote_info']['id'],
                'content': moment_data['vote_detail']['vote_info']['content'],
                'options': moment_data['vote_detail']['vote_info']['options'],
                'vote_result': moment_data['vote_detail']['vote_result'],
            }

            comment_info_data = [
                {
                    'moment_id': moment_id,
                    'comment_id': comment_data['comment_id'],
                    'gender': comment_data['comment_user_info']['gender'],
                    'age': comment_data['comment_user_info']['age'],
                    'city': comment_data['comment_user_info']['city'],
                    'province': comment_data['comment_user_info']['province'],
                    'profession': comment_data['comment_user_info']['profession'],
                    'education': comment_data['comment_user_info']['education'],
                    'content': comment_data['content'],
                    'reply_num': comment_data['reply_num'],
                    'thumbs_up_num': comment_data['thumbs_up_num'],
                    'vote_option_id': comment_data['vote_option_id'],
                }
                for comment_data in moment_data['comment_list']
            ]

        else:
            moment_info_data = None
            comment_info_data = [
                {
                    'moment_id': moment_id,
                    'comment_id': comment_data['comment_id'],
                    'gender': comment_data['comment_user_info']['gender'],
                    'age': comment_data['comment_user_info']['age'],
                    'city': comment_data['comment_user_info']['city'],
                    'province': comment_data['comment_user_info']['province'],
                    'profession': comment_data['comment_user_info']['profession'],
                    'education': comment_data['comment_user_info']['education'],
                    'content': comment_data['content'],
                    'reply_num': comment_data['reply_num'],
                    'thumbs_up_num': comment_data['thumbs_up_num'],
                    'vote_option_id': comment_data['vote_option_id'],
                }
                for comment_data in moment_data['comments_list']
            ]

        return moment_info_data, comment_info_data


addons = [GetCommentData()]

if __name__ == '__main__':
    os.system('mitmdump -s get_data.py -q')
