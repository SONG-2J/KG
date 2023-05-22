from flask import render_template, request

from ere.rel.globalpointer_re import model, model_save_path, SPO, K, extract_spoes
from store.er_graph import GraphERE
from utils.draw_tool import list2csv, list2graph, csv2graph
from utils.getSPO import get_spo

# 数据初始化
ere_path = "/Users/soutsukyou/Desktop/KG/ere/"
tmp_path = ere_path + 'data/tmp/'  # 数据临时存储目录
file_list = list()  # 上传的文件列表
ere = GraphERE()  # neo4j实体关系对象
# globalpointer模型初始化
model.load_weights(model_save_path)


# 主页面
def index_page():
    if request.method == "POST":
        # 获取前端输入文本
        p_text = request.form.get("P_text")
        print(p_text)
        # ========== 使用深度学习的模型进行预测 ==========
        # 先用基于规则的方法模拟
        # 使用训练的模型需要加载训练模型
        # spo_list = get_spo(p_text)  # 规则提取
        spo_list = set([SPO(spo) for spo in extract_spoes(p_text)])  # 模型预测
        print(spo_list)
        # 列表转关系图
        list2graph(
            spo_list=spo_list,
            html_file='templates/show_page/spo_tmp.html',
            graph_title="spo_kg",
            width="80vw",
            height='80vh'
        )
        # ========== END ==========

    return render_template("index.html")


# 大知识图谱：待实现
def kg_big():
    spo_list = []
    # 与词相关
    word_around = dict()
    if request.method == "POST":
        f_word = request.form.get("F_word_big")
        if f_word:
            spo_list = ere.findERE(nodeName=f_word)  # neo4j查询
            word_around['word'] = f_word
            word_around['explain_list'] = ere.findExplain(f_word)
            word_around['kids_list'], word_around['p_list'] = ere.findChildAndParent(f_word)
    else:
        spo_list = ere.findERE()
    list2graph(
        spo_list=spo_list,
        html_file='templates/show_page/spo_all.html',
        graph_title="spo_big",
        width="58vw",
        height='80vh'
    )
    return render_template("kg_big.html", word_around=word_around)


# 文件方式
def kg_file():
    if request.method == "POST":
        file = request.files.get('file')
        f_word = request.form.get('F_word_file')  # 过滤词组
        # 上传文件
        if file:
            filename = file.filename
            # 是否是CSV文件
            if filename.endswith(".csv") or filename.endswith('.txt'):
                if filename not in file_list:
                    file_list.append(filename)  # 文件列表追加
                file.save(tmp_path + filename)  # 存储到指定的路径
                return render_template("kg_file.html", up_msg="上传成功！", file_list=file_list)
            else:
                return render_template("kg_file.html", up_msg="非指定格式文件！", file_list=file_list)
        # 查询知识图谱
        if f_word:
            if f_word == "all":
                f_word = ""
            sents_list = []  # 存放句子
            # 现将上传的csv文件都读出来
            for tmp_f in file_list:
                f = open(tmp_path + tmp_f, 'r')
                for line in f:
                    sents_list += line.split('。')  # 根据句号分隔
                f.close()
            # ========== 使用深度学习的模型进行预测（暂时未接入） ==========
            spo_list = []  # 存放三元组
            for sent in sents_list:
                print(sent)
                spo_list += set([SPO(spo) for spo in extract_spoes(sent)])  # 调用方法
            # 过滤出需要的字段
            final_spo_list = []
            for spo in spo_list:
                if f_word in spo[0] or f_word in spo[1] or f_word in spo[2]:
                    final_spo_list.append(spo)
            # ========== 绘图 ==========
            print(final_spo_list)
            list2graph(
                final_spo_list,
                html_file='templates/show_page/spo_file.html',
                graph_title='spo_file',
                width='58vw',
                height='67vh'
            )
            # ========== END ==========
            return render_template('kg_file.html', spo_list=final_spo_list, file_list=file_list)

        # 默认返回样式
        return render_template("kg_file.html", up_msg="无操作！", file_list=file_list)
    elif request.method == "GET":
        file_list.clear()  # 清空之前的列表
        return render_template("kg_file.html", file_list=file_list)


# 其它：待实现
def others():
    # 模型切换

    # 自定义模型

    # 折线图展示

    # 返回结果
    return render_template("kg_others.html")
