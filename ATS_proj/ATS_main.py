from util import get_stop_words, split_sentence, cut, token
from setting import summary_ratio, stopwords_path
import networkx as nx
import math
import os
os.chdir("E:\\！研三上\\00 讲座课ML\\")


def get_connect_graph_by_weight_text_rank(original_text, title):
    sentences_graph = nx.Graph()
    sentences = split_sentence(original_text)
    sentences_cut = [cut(''.join(token(n))) for n in sentences]
    sentences_cut_del_stopwords = []
    stop_words = get_stop_words(stopwords_path)

    for s in sentences_cut:
        words = s.split()
        sentence_cut_del_stopwords = list(set(words) - set(stop_words))
        if sentence_cut_del_stopwords != []:
            sentences_cut_del_stopwords.append(sentence_cut_del_stopwords)

    is_title = False
    # 处理标题
    if title:
        title_cut = [cut(''.join(token(title)))]
        words = title_cut[0].split()
        title_cut_del_stopwords = list(set(words) - set(stop_words))
        if title_cut_del_stopwords != []:
            is_title = True
            sentences_cut_del_stopwords.insert(0, title_cut_del_stopwords)
            sentences.insert(0, title)

    for i, sentence in enumerate(sentences_cut_del_stopwords):
        for connect_id in range(i + 1, len(sentences_cut_del_stopwords)):
            # 求两个句子的相同词
            length_same_words = len(set(sentence).intersection(set(sentences_cut_del_stopwords[connect_id])))

            if is_title and (i == 0 or i == 1):
                # 如果是第一句double权重
                similiar = 2 * length_same_words / (
                        math.log(len(sentence)) + math.log(len(sentences_cut_del_stopwords[connect_id])))

            elif (not is_title) and i == 0:
                similiar = 2 * length_same_words / (
                        math.log(len(sentence)) + math.log(len(sentences_cut_del_stopwords[connect_id])))

            else:
                similiar = length_same_words / (
                            math.log(len(sentence)) + math.log(len(sentences_cut_del_stopwords[connect_id])))
            sentences_graph.add_edges_from([(i, connect_id)], weight=similiar)

    return sentences, sentences_graph, is_title


def sentences_ranking(original_text, title):
    sentences, sentences_graph, is_title = get_connect_graph_by_weight_text_rank(original_text, title)
    ranking_sentences_id = nx.pagerank(sentences_graph)
    if is_title:
        ranking_sentences_id.pop(0)
    ranking_sentences_id = sorted(ranking_sentences_id.items(), key=lambda x: x[1], reverse=True)
    return ranking_sentences_id, sentences


def get_summarization_by_textrank(original_text=None, title=None, summary_ratio=summary_ratio):
    '''
    :param original_text: 正文
    :param title: 标题
    :param summary_ratio: 压缩比，原文与摘要句子数量的比例
    :return:
    '''
    # 正文不能为空
    if original_text == None:
        print('please input text')
        return None

    ranking_sentences_id, sentences = sentences_ranking(original_text, title)
    # if len(sentences) <= summary_ratio:
    #     return ''.join(sentences)
    candidate_sentences = [s[0] for s in ranking_sentences_id[:len(sentences) // summary_ratio + 1]]
    candidate_sentences = sorted(candidate_sentences)

    return ''.join([sentences[id] for id in candidate_sentences])

if __name__ == '__main__':
    text = '在美联储召开货币政策会议前夕，投资者担心货币政策或会有收紧信号，全球避险情绪高涨，恐慌指数本周初飙升至5月以来新高，风险资产也全线下挫，金价及美元指数等避险资产价格上涨。\n\n\u3000\u3000对于全球市场四季度表现，业内预期，经济下行风险或会令美股回调20%甚至更多。相对而言，欧洲股票估值具吸引力，其表现有望在短期内跑赢其他发达市场资产。中国的潜在增长和经济基本面没有改变，看好中国股市长期表现。\n\n\u3000\u3000天气变冷或导致变异病毒加速传播、货币政策或会收紧等一系列因素抑制了投资者的积极情绪，衡量市场波动性的“恐慌指数”周一飙升至28以上，为5月来最高水平。全球风险资产波动性加剧，截至上周五，道指已连跌三周，是2020年9月以来首次。\n\n\u3000\u3000美联储将在北京时间周四结束为期两天的会议并召开新闻发布会。美联储主席鲍威尔曾表示，今年年内或会缩债，目前投资者正在等待更多细节。摩根士丹利策略师表示，预计标普500指数将出现10%的回调，如果美国经济增长出现停滞迹象，则回调幅度可能会加大至20%。\n\n\u3000\u3000除美联储政策信号的不确定性外，美国提高债务上限的最后期限临近，美国两党谈判结果的不确定性也给金融市场带来压力。此前，美国财政部长耶伦再次敦促国会提高债务上限，以避免债务违约造成金融市场动荡。业内预计，美国国会或会像往常一样提高债务上限。\n\n\u3000\u3000本周，除美联储外，英国、日本、挪威等多国央行宣布货币决策，市场预计挪威将成十国集团（G10）中首个加息的国家。此外，英美央行或表态鹰派，叠加疫情复燃，投资者集体恐慌情绪被放大。\n\n\u3000\u3000对于全球市场四季度表现，景顺亚太区（日本除外）全球市场策略师赵耀庭表示，新冠病毒变异毒株德尔塔的蔓延可能会阻碍美国就业和消费者信心的恢复，随着美国经济增长和盈利放缓，市场可能会经历更多波动和短期的回调，投资者可能会转向美国以外股票投资。\n\n\u3000\u3000“宽松货币政策支撑地区经济增长，同时欧盟复苏基金的实施有利经济复苏。欧洲股票估值具有吸引力，其表现有望在短期内跑赢其他发达市场资产。”赵耀庭说。'
    title = None
    summarization = get_summarization_by_textrank(text, title)
    print(summarization)


# >>> 在美联储召开货币政策会议前夕，投资者担心货币政策或会有收紧信号，全球避险情绪高涨，恐慌指数本周初飙升至5月以来新高，风险资产也全线下挫，金价及美元指数等避险资产价格上涨。
# 　　对于全球市场四季度表现，景顺亚太区（日本除外）全球市场策略师赵耀庭表示，新冠病毒变异毒株德尔塔的蔓延可能会阻碍美国就业和消费者信心的恢复，随着美国经济增长和盈利放缓，市场可能会经历更多波动和短期的回调，投资者可能会转向美国以外股票投资。