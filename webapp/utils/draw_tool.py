import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Graph


# spo_list绘图
def list2graph(spo_list, html_file, graph_title="spo_kg", width="1200px", height="750px"):
    nodes = set()
    nodes_data = list()  # 结点数据
    links_data = list()  # 关系数据
    for spo in spo_list:
        if spo[0] not in nodes:
            nodes.add(spo[0])
            nodes_data.append(opts.GraphNode(name=spo[0], symbol_size=60))
        if spo[2] not in nodes:
            nodes.add(spo[2])
            nodes_data.append(opts.GraphNode(name=spo[2], symbol_size=60))
        links_data.append(opts.GraphLink(source=spo[0], value=spo[1], target=spo[2]))
    # 绘图
    print(nodes_data)
    print(links_data)
    c = (
        Graph(init_opts=opts.InitOpts(
            width=width,
            height=height
        ))
            .add(
            "",
            nodes_data,
            links_data,
            repulsion=4000,
            edge_label=opts.LabelOpts(
                is_show=True, position="middle", formatter="{c}"
            ),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title=graph_title)
        )
            .render(html_file)
    )


# csv文件转变为关系图：读csv写html
# csv文件的行头为：subject,predicate,object
def csv2graph(csv_file, html_file, graph_title="关系图", width="1200px", height="600px"):
    # 先从csv文件获得节点数目
    df = pd.read_csv(csv_file)
    nodes = list(set(list(df['subject']) + list(df['object'])))  # 结点：subject列和object列合并然后去重复
    # print(nodes)
    links = [[getattr(row, "subject"), getattr(row, "predicate"), getattr(row, "object")] for row in
             df.itertuples()]  # 关系
    # print(links)
    nodes_data = [opts.GraphNode(name=node, symbol_size=60) for node in nodes]
    links_data = [
        opts.GraphLink(source=l[0], target=l[2], value=l[1]) for l in links
    ]
    c = (
        Graph(init_opts=opts.InitOpts(
            width=width,
            height=height
        ))
            .add(
            "",
            nodes_data,
            links_data,
            repulsion=4000,
            edge_label=opts.LabelOpts(
                is_show=True, position="middle", formatter="{c}"
            ),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title=graph_title)
        )
            .render(html_file)
    )


# 写csv文件
def list2csv(file_path, data_list, header):
    f = open(file_path, 'w')
    f.write(','.join(header) + '\n')
    for data in data_list:
        f.write(','.join(data) + '\n')
    f.close()
