## 环境部署
```shell
# 操作系统：Ubuntu 18.04 64位
# 1 * NVIDIA V100
# CUDA 10.1.130
# Driver 450.80.2
# CUDNN 7.6.5
# tensorflow-gpu 1.15.0
# python版本：3.6.9
# python环境
pip3 install --upgrade pip
pip3 install -r requirements.txt
```
对于没有GPU的伙伴可以像我一样去租用一台云服务器，我使用的是aliyun的ECS容器服务，配置按照以上给出的进行选择即可

## Docker部署

```shell
# docker环境
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 卸载docker（一般用不到）
sudo apt-get purge docker-ce
sudo rm -rf /var/lib/docker
```

### Docker部署neo4j

```shell
# docker部署neo4j
# 用户：neo4j
# 密码：123456
docker run -d --name neo4j -p 7474:7474 -p 7687:7687 \
-v /root/neo4j_v/data:/data \
-v /root/neo4j_v/logs:/logs \
-v /root/neo4j_v/conf:/var/lib/neo4j/conf \
-v /root/neo4j_v/import:/var/lib/neo4j/import \
--env NEO4J_AUTH=neo4j/123456 \
neo4j
```
- 运行 **store/er_graph.py** 文件，初始化neo4j数据
- 如果你不想使用docker来部署neo4j数据库，当然可以在本机或远端的服务器中部署
- ⚠️但需要注意的是，如果你选择远端部署，不要忘了修改neo4j的配置文件，以保证你的neo4j是能被远程访问到的
- 页面：http://127.0.0.1:7474

## 运行项目

```shell
cd KG/webapp
python3 app.py
```
## 另外的方法

我可太喜欢dokcer了，所以我将项目移植到了Ubuntu，方便大家使用。

```shell
docker run -id --name KG  \
	-p 15000:5000 -p 17474:7474 -p 17687:7687 \
	song2j/kg:1.0
```
- web页面：127.0.0.1:15000
- neo4j管理页面：localhost:17474
    - 连接端口：17867
    - 用户：neo4j
    - 密码：123456



## 项目结构介绍

```shell
.
├── README.md    # README文件
├── ere          # 实体-关系-实体三元组抽取模块
│   ├── checkpoint
│   │   └── rel                          # 存放训练好的权重文件
│   │       ├── casrel_a61l.weights      # CasRel模型在小类A61L的权重文件
│   │       └── gp_a61l.weights          # GlobalPointer在小类A61L的权重文件
│   ├── chinese_L-12_H-768_A-12          # bert模型文件
│   │   ├── bert_config.json
│   │   ├── bert_model.ckpt.data-00000-of-00001
│   │   ├── bert_model.ckpt.index
│   │   ├── bert_model.ckpt.meta
│   │   └── vocab.txt
│   ├── data                             # 文件存放位置
│   │   ├── A61L                         # A61L专利数据集（该数据集没有原作者的授权，不予提供）
│   │   │   ├── dev.json                 # 验证集
│   │   │   ├── schemas.json             # 关系种类
│   │   │   ├── test.json                # 测试集
│   │   │   └── train.json               # 训练集
│   │   ├── A61L_ALL.csv                 # A61L小类下的各种专利分类之间的树关系
│   │   └── tmp                          # 文件上传的临时存放地点
│   └── rel                              # 训练模型的py文件（使用苏剑林大神的代码）
│       ├── casrel_re.py
│       └── globalpointer_re.py
├── requirements.txt                     # 环境配置文件
├── store        # 数据存放模块
│   └── er_graph.py                      # neo4j中实体关系的类
└── webapp       # web模块
    ├── app.py   # 启动文件
    ├── static
    │   └── bootstrap-5.3.0-alpha1-dist  # 使用bootstrap5
    ├── templates
    │   ├── body.html            # 主界面的body部分
    │   ├── file_page            # 文件上传部分html
    │   │   ├── result.html      # 文件上传结果
    │   │   └── upload.html      # 文件上传过程
    │   ├── footer.html          # 页脚
    │   ├── header.html          # 头部导航栏
    │   ├── index.html           # 主界面（header+body+footer）
    │   ├── kg_big.html          # kg_big模块：小类的完整知识图谱
    │   ├── kg_file.html         # kg_file模块：上传文件的方式抽取三元组形成知识图谱
    │   ├── kg_others.html       # 其它
    │   ├── other_page           # 其它功能页面补充
    │   │   ├── line.html        # 两个模型在20个epoch的对比
    │   │   ├── operation.html   # 设置（未实现）
    │   │   └── use.html         # 知识图谱实际应用（总结）
    │   └── show_page    # 存放关系图
    │       ├── spo_all.html
    │       ├── spo_file.html
    │       └── spo_tmp.html
    ├── utils
    │   ├── draw_tool.py # 将列表、csv文件转换为关系图
    │   └── getSPO.py    # 利用规则的方式抽取三元组（已淘汰）
    └── views.py         # 视图文件
```

项目基本功能完善，但也尚有不足，下面提供一些缺漏和发展建议：

- 如何使用自己的数据集？
	- 在路径 **ere/data** 中添加自己的数据集，格式要求可参考[百度DuIE数据集](http://ai.baidu.com/broad/download?dataset=sked)；schemas要求有 **"predicate"** 字段即可；
	- 更改 **ere/rel** 下两个模型py文件中数据集的路径
- 绘图不是Echarts接收后端数据实现，而是使用Pyecharts直接对图进行重新绘制得到的，emmm
- 项目没有什么用户之类的，没有实现隔离，只是提供一个大致的框架

- kg_other模块未完善

## 感谢
https://kexue.fm/archives/7161
https://kexue.fm/archives/8888