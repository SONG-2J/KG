import json
import jieba.posseg as jp


def get_spo(texts):
    # 分词和词性标注
    word_list = sent2word(texts)  # 分词
    # spo三元组
    spo_list = list(set([tuple(t) for t in word2SPO(word_list)]))  # 去重
    return spo_list
    # print(spo_list)


def sent2word(sentence):
    res_list = []
    pair_list = [list(e) for e in jp.lcut(sentence, HMM=True)]

    index = 0
    while index < len(pair_list)-1:
        tmp_str = ""
        # 对形容词和动词进行处理，产生一种新的词性质av
        if 'a' in pair_list[index][1] or 'v' in pair_list[index][1]:
            while 'a' in pair_list[index][1] or 'v' in pair_list[index][1]:
                tmp_str += pair_list[index][0]
                index += 1
            res_list.append([tmp_str, 'av'])
        elif 'f' in pair_list[index][1]:  # 对方位处理，nf
            tmp_index = index
            while tmp_index >= 0:
                if 'n' in pair_list[tmp_index][1]:
                    tmp_str += pair_list[tmp_index][0] + pair_list[index][0]
                    break
                tmp_index -= 1
            res_list.append(["方位关系", "av"])
            res_list.append([tmp_str, 'nf'])  # 添加方位
            index += 1
        else:
            if 'n' in pair_list[index][1] or 'v' in pair_list[index][1]:
                res_list.append(pair_list[index])
            index += 1

    return res_list


# 词性标注列表转换为SPO列表
def word2SPO(word_list):
    spo_list = []
    index = 0
    while index < len(word_list):
        if 'n' in word_list[index][1]:
            # if index + 1 < len(word_list) and 'av' in word_list[index + 1][1]:  # 跳过可能是主语的词
            #     index += 1
            #     continue
            fw1, fw1_index = preFindWord(word_list, index - 1, 'a')
            if fw1 == "UnFind":
                index += 1
                continue
            else:
                fw2, fw2_index = preFindWord(word_list, fw1_index - 1, 'n')
                if fw2 == "UnFind":
                    index += 1
                    continue
                else:
                    spo_list.append([fw2, fw1, word_list[index][0]])  # 添加三元关系组
        index += 1
    return spo_list


# 向前找到某一个词性 的 词
def preFindWord(word_list, index, word_p):
    while index >= 0:
        if word_p in word_list[index][1]:
            return word_list[index][0], index
        index -= 1
    return "UnFind", -1


if __name__ == '__main__':
    texts = "本实用新型涉及机械加工领域公开了一种方便使用的新型机械加工工作台，所述工作台的下侧固定旋转主轴，旋转主轴穿过第一轴承内壁，第一轴承外壁固定连接箱体上侧，箱体下端的内壁固定连接轴承固定块，轴承固定块上端开孔固定第二轴承外壁，第二轴承内壁固定旋转主轴下端，旋转主轴中部固定连接从动齿轮，从动齿轮啮合连接驱动齿轮，驱动齿轮固定连接驱动轴，驱动轴上端固定连接减速电机，设置旋转主轴。"
    get_spo(texts)
