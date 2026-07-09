ElasticSearch

1、概念
	1）、是一款分布式、高性能、高扩展，支持海量数据存储、分析、搜索、计算的搜索引擎
	2）、基于java语言编写，发起的请求是基于json格式符合Resful风格的DSL语句
	3）、前身-Lucene诞生于1999年，2004年变为了compass，2010年重构成了现在的ES
	4）、ELK：是一个围绕ElasticSearch的技术栈，包含：ElasticSearch、Logstatsh、Kibana，最新版本9.x
	5）、Solr: 是ES的一款竞品，2016年被ES吊打，主流成为ES
	
	
2、其中比较重要的概念
	1）、倒排索引 *****
		1、在文档【增删改】的时候对文档的某个字段进行【合理化的分词】，形成一个【不重复】的词条列表，其中每一个词条对应一个文档id集合
		2、形成一张根据词条查询id集合的 类似hash表结构
		3、形成一张根据id查询文档的 B+树结构
		将来搜索时先根据用户输入的条件进行【合理化的分词】，再根据词条找id，最后根据id找到相应的文档（涉及到两次查询）
	
	2）、索引-index：同一类型文档的集合，相当于mysql的表
	3）、映射-mapping：对索引结构的约束，相当于mysql的schema
		 type、analyzer、index、properties
	4）、文档-document：json格式的数据，相当于mysql的row
	5）、字段-field：一个个的字段，相当于mysql的列
	6）、DSL语句：json格式的符合resful风格的请求语句，相当于mysql的sql语句
	
3、DSL语句去操作索引、文档
	操作索引：
		- 创建索引库：
			 PUT /索引库名
			 {
				"mapping"：{
					"properties":{
						"fieldName":{
							"type": "",
							"analyzer": "",
							"index": ,
							"properties"
						}
					}
				}
			 }
		- 查询索引库：GET /索引库名
		- 删除索引库：DELETE /索引库名
		- 添加字段：
			PUT /索引库名/_mapping
			{
				"properties":{
				}
			}
	操作文档
		- 创建文档：POST /{索引库名}/_doc/文档id   { json文档 }
		- 查询文档：GET /{索引库名}/_doc/文档id
		- 删除文档：DELETE /{索引库名}/_doc/文档id
		- 修改文档：
		  - 全量修改：PUT /{索引库名}/_doc/文档id { json文档 }
		  - 增量修改：POST /{索引库名}/_update/文档id { "doc": {字段}}
	
4、用java api去操作索引、文档
	操作索引：
		- 初始化RestHighLevelClient
		- 创建XxxIndexRequest。XXX是Create、Get、Delete
		- 准备source（ Create时需要，其它是无参）
		- 发送请求。调用RestHighLevelClient#indices().xxx()方法，xxx是create、exists、delete
	
	操作文档
		- 初始化RestHighLevelClient
		- 创建XxxRequest。XXX是Index、Get、Update、Delete、Bulk
		- 准备参数（Index、Update、Bulk时需要）
		- 发送请求。调用RestHighLevelClient#.xxx()方法，xxx是index、get、update、delete、bulk
		- 解析结果（Get时需要）
	
