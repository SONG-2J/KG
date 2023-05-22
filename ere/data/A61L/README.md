这是个人手动标注的A61L小类专利数据集，由于该数据集作者并未同意将其公布到网络，这里我简单描述一下数据集的结构：
## schemas.json
该文件包含该数据的所有关系类别，每一行是一条JSON数据，参考百度DuIE数据集，但是并不需要实体的类别，所以格式可如下：
```json
{"predicate": "关系1"}
{"predicate": "关系2"}
{"predicate": "关系3"}
```
对于不同样式的schemas文件可以通过简单修改至相同样式或修改代码中读取文件这一部分来实现。
## train.json & test.json & dev.json
三者样式一致，每一行是一条json数据，参考百度DuIE数据集。
包含两个元素：
1. 文本：text
2. spo三元组列表：spo_list
例如：
   
```json
{"text": "A由B和C组成，需要和D连接", "spo_list": [{"subject": "A", "predicate": "组件", "object": "B"}, {"subject": "A", "predicate": "组件", "object": "C"}, {"subject": "A", "predicate": "连接", "object": "D"}]}
{"text": "...", "spo_list": [...]}
```