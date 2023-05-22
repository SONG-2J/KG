# 实体关系的类
from py2neo import Graph, Node, Relationship

# 根据本机实际情况修改
URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "123456")


class GraphERE:
    def __init__(self, uri=URI, auth=AUTH):
        self.graph = Graph(uri, auth=auth)
        # ===== 测试需要清空时放开 =====
        # self.graph.delete_all()  # 清空
        self.nodes_dict = dict()

    # 创建实体
    def createEntity(self, entityName):
        self.graph.create(Node("Entity", name=entityName))

    # 创建关系
    def createRelation(self, node1, node2, relationName):
        self.graph.create(Relationship(node1, "Rel", node2, name=relationName))

    # 根据传入的SPO三元组创建关系图，spo格式为 实体1-关系-实体2
    def graphBySPO(self, spo_list):
        for spo in spo_list:
            # 先创建实体结点
            if spo[0] not in self.nodes_dict:
                self.nodes_dict[spo[0]] = Node("Entity", name=spo[0])
            if spo[2] not in self.nodes_dict:
                self.nodes_dict[spo[2]] = Node("Entity", name=spo[2])
            # 构建二者的关系
            self.createRelation(self.nodes_dict[spo[0]], self.nodes_dict[spo[2]], spo[1])

    # 根据CSV文件创建关系图
    def graphByCsv(self, csv_file):
        f = open(csv_file, 'r')
        for line in f:
            spo = line.replace('\n', '').split(',')
            # 先创建实体结点
            if spo[0] not in self.nodes_dict:
                self.nodes_dict[spo[0]] = Node("Entity", name=spo[0])
            if spo[2] not in self.nodes_dict:
                self.nodes_dict[spo[2]] = Node("Entity", name=spo[2])
            # 构建二者的关系
            self.createRelation(self.nodes_dict[spo[0]], self.nodes_dict[spo[2]], spo[1])
        f.close()

    # 查找ERE
    def findERE(self, nodeName='', relationName=''):
        find_ere = "MATCH (e1:Entity)-[r:Rel]->(e2:Entity) " \
                   f"WHERE e1.name = '{nodeName}' OR e2.name = '{nodeName}' AND r.name CONTAINS '{relationName}'" \
                   "RETURN e1.name, r.name, e2.name"  # 查询出所有实体关系
        if '' == nodeName or "关键词-" in nodeName:
            nodeName = nodeName.replace("关键词-", '')
            find_ere = "MATCH (e1:Entity)-[r:Rel]->(e2:Entity) " \
                       f"WHERE e1.name CONTAINS '{nodeName}' OR e2.name CONTAINS '{nodeName}' AND r.name CONTAINS '{relationName}'" \
                       "RETURN e1.name, r.name, e2.name"  # 查询出所有实体关系
        result = self.graph.run(find_ere)
        res = []
        print("=====================")
        for record in result:
            e1 = record['e1.name']
            rel = record['r.name']
            e2 = record['e2.name']
            print(e1, rel, e2)
            res.append([e1, rel, e2])
        print("=====================")
        return res  # 返回SPO列表

    # 查找释义（此函数仅针对于A61L的关系）
    def findExplain(self, node_name):
        # 获得释义
        find_explain = "MATCH (e1:Entity)-[r:Rel]->(e2:Entity) " \
                       f"WHERE e1.name = '{node_name}' AND r.name = '释义'" \
                       "RETURN e2.name"
        explain_list = []
        for t in self.graph.run(find_explain):
            explain_list += t['e2.name'].split('；')
        return explain_list

    def findChildAndParent(self, node_name):
        # 获得子结点
        find_kids = "MATCH (e1:Entity)-[r:Rel]->(e2:Entity) " \
                    f"WHERE e1.name = '{node_name}' AND r.name <> '释义'" \
                    "RETURN e2.name"
        kids_list = [t['e2.name'] for t in self.graph.run(find_kids)]
        kids_dict = dict()
        for kid in kids_list:
            kids_dict[kid] = self.findExplain(kid)
        # 获得父结点
        find_p = "MATCH (e1:Entity)-[r:Rel]->(e2:Entity) " \
                 f"WHERE e2.name = '{node_name}'" \
                 "RETURN e1.name"
        if "关键词-" in node_name:
            node_name = node_name.replace("关键词-", '')
            find_p = "MATCH (e1:Entity)-[r:Rel]->(e2:Entity) " \
                     f"WHERE e2.name CONTAINS '{node_name}'" \
                     "RETURN e1.name"

        p_list = [t['e1.name'] for t in self.graph.run(find_p)]
        p_dict = dict()
        for p in p_list:
            p_dict[p] = self.findExplain(p)

        print(kids_dict)
        print(p_dict)
        return kids_dict, p_dict


if __name__ == '__main__':
    # spo_list = [
    #     ["本实用新型", "涉及领域", "机械加工"],
    #     ["工作台", "固定连接", "旋转主轴"],
    #     ["旋转主轴", "穿过", "第一轴承"],
    #     ["第一轴承", "固定连接", "箱体"],
    #     ["箱体", "固定连接", "轴承固定块"],
    #     ["轴承固定块", "固定", "第二轴承"],
    #     ["第二轴承", "固定连接", "旋转主轴"],
    #     ["旋转主轴", "固定连接", "从动齿轮"],
    #     ["从动齿轮", "啮合连接", "驱动齿轮"],
    #     ["驱动齿轮", "固定连接", "驱动轴"],
    #     ["驱动轴", "固定连接", "减速电机"],
    #     ["工作台", "设置", "旋转主轴"]
    # ]
    ere = GraphERE()
    # ere.graphBySPO(spo_list)
    ere.graphByCsv('../ere/data/A61L_ALL.csv')
    # ere.findERE(nodeName='A61L', relationName='')
    # ere.findChildAndParent("A61L")
