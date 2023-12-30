import json
import os

import jieba
import pandas as pd

from ast import literal_eval

from aliyunsdkalinlp.request.v20200629 import GetWsChGeneralRequest, GetSaChGeneralRequest
from aliyunsdkcore.client import AcsClient

# 阿里云账号信息
access_key_id = os.environ['NLP_AK_ENV']
access_key_secret = os.environ['NLP_SK_ENV']

# 创建AcsClient实例
client = AcsClient(
    access_key_id,
    access_key_secret,
    "cn-hangzhou"
)

# 停用词
with open('../data/stop_words.txt', 'r', encoding='utf-8') as f:
    stop_words = f.readlines()
    stop_words = [word.strip() for word in stop_words]

stop_words.append(' ')
stop_words.append('\n')


def cut_words_by_ali_nlp(text: str) -> list:
    """
    通过阿里云NLP进行分词

    :param text: 待处理文本
    :return: 去除停用词后的分词结果
    """
    # 获取原始分词结果
    request = GetWsChGeneralRequest.GetWsChGeneralRequest()
    request.set_Text(text)
    request.set_OutType("0")
    request.set_ServiceCode("alinlp")
    request.set_TokenizerId("GENERAL_CHN")
    response = client.do_action_with_exception(request)
    resp_obj = json.loads(response)
    data_obj = json.loads(resp_obj['Data'])

    word_list = [word['word'] for word in data_obj['result']]

    # 去除停用词
    word_list_without_stop_words = []
    for word in word_list:
        if word not in stop_words:
            word_list_without_stop_words.append(word)

    return word_list_without_stop_words


def cut_words_by_jieba(text: str) -> list:
    """
    通过jieba进行分词

    :param text: 待处理文本
    :return: 去除停用词后的分词结果
    """
    word_list = list(jieba.cut(text))

    # 去除停用词
    word_list_without_stop_words = []
    for word in word_list:
        if word not in stop_words:
            word_list_without_stop_words.append(word)

    return word_list_without_stop_words


# 情感倾向分析
def get_sentiment_by_ali_nlp(text: str) -> dict:
    """
    通过阿里云NLP进行情感倾向分析

    :param text: 待处理文本
    :return: 文本情感倾向
    """
    # 获取情感倾向
    request = GetSaChGeneralRequest.GetSaChGeneralRequest()
    request.set_Text(text)
    request.set_ServiceCode("alinlp")
    response = client.do_action_with_exception(request)
    resp_obj = json.loads(response)
    data_obj = json.loads(resp_obj['Data'])

    return data_obj


def get_vote_result(moments: pd.DataFrame) -> pd.DataFrame:
    """
    获取投票结果

    :param moments: 投票数据
    :return: 投票结果
    """
    moments_vote_result = pd.DataFrame()
    for moment_id in moments['moment_id']:
        moment = moments[moments['moment_id'] == moment_id]
        options = pd.DataFrame(literal_eval(moment['options'].tolist()[0])).rename(columns={'id': 'option_id'})
        vote_result = pd.DataFrame(literal_eval(moment['vote_result'].tolist()[0]))
        vote_result = pd.merge(options, vote_result, on='option_id', how='left')
        vote_result['moment_id'] = moment_id
        moments_vote_result = pd.concat([moments_vote_result, vote_result])

    return moments_vote_result
