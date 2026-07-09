查询的DSL是一个大的JSON对象，包含下列属性：
	- query：查询条件
	- from和size：分页条件
	- sort：排序条件
	
	- highlight：高亮条件
	- aggs : 聚合

ES查询语句的统一模板：
	GET /indexName/_search
	{
	  "query":{...},
	  
	  "sort": [...],
	  
	  "from": 0,
	  "size": 30,
	  
	  "highlight": {...},
	  
	  "aggs":{},
	  "suggest":{}
	}

一、query查询部分：
	- 查询所有：查询出所有数据，一般测试用。例如：match_all

	- 全文检索（full text）查询：利用分词器对用户输入内容分词，然后去倒排索引库中匹配。例如：
	  - match_query   单字段全文检索查询（一般是text类型字段）
	  - multi_match_query  多字段全文检索查询（一般是text类型字段）
	  - simple_query_string  多字段全文检索查询（一般是text类型字段）
	  
	- 精确查询：根据精确词条值查找数据，一般是查找keyword、数值、日期、boolean等类型字段。例如：
	  - ids  根据id集合进行查询
	  - range 范围查询（数值、日期类型的字段）
	  - term 词条精准匹配查询（一般是keyword类型字段）
	  
	- 模糊查询：根据词条进行相应规则的匹配查询
	  - wildcard  模糊匹配查询，类似于like
	  - prefix  前缀匹配查询
	  
	- 复合（compound）查询：复合查询可以将上述各种查询条件组合起来，合并查询条件。例如：
	  - bool  对于各种简单查询进行组合，形成一个复合查询，其中组合的条件包含：
			- must：必须成立（类似and，参与算分）
			- must not：必须不成立（类似 not，不参与算分）
			- should：可以成立（类似 or，参与算分）
			- filter：必须成立（类似and，不参与算分）
	  - function_score 对指定的文档进行算分加分
			query部分：原始查询条件，基于这个条件搜索文档，并且基于BM25算法给文档打分，得出原始算分（query score)
			另外关键三要素包括：
			- 算分过滤条件：filter部分，符合该条件的文档才会重新算分
			- 算分函数：符合filter条件的文档要根据这个函数做运算，得到的函数算分（function score），有四种函数
				- weight：函数结果是常量
				- field_value_factor：以文档中的某个字段值作为函数结果
				- random_score：以随机数作为函数结果
				- script_score：自定义算分函数算法
			- 加权模式：算分函数的结果、原始查询的相关性算分，两者之间的运算方式，包括：
				- multiply：相乘
				- replace：用function score替换query score
				- 其它，例如：sum、avg、max、min
				
				GET /indexName/_search
				{
				 "query":{
				   "function_score":{
					 "query": {                        
					   "match":{"all":"外滩"}
					 },
					 "functions":[
					  {
					   "filter":{"term":{"id":"60487"}},
					   "weight":10                      
					  }
					 ],
					 "boost_mode":"multiply"            
				   }
				  }
				}
			
二、sort排序部分
	1、普通排序：keyword、数值、日期类型排序
		  "sort": [
			{
			  "FIELD": "desc"  // 排序字段、排序方式ASC、DESC
			}
		  ]
		  
三、from、size分页部分  
	from：指定开始角标位置
	size：指定搜索的文档条数
	深度分页问题
		- search after
		- scroll
		---- 物理分页、逻辑分页
	
四、highlight高亮部分
	- 高亮是对关键字高亮，因此搜索条件必须带有关键字，而不能是范围这样的查询。
	- 默认情况下，高亮的字段，必须与搜索指定的字段一致，否则无法高亮
	- 如果要对非搜索字段高亮，则需要添加一个属性：required_field_match=false
	"highlight": {
		"fields": { // 指定要高亮的字段名称
		  "FIELD": {  //需要高亮的字段名称
			"pre_tags": "<em>",  // 用来标记高亮字段的前置标签
			"post_tags": "</em>", // 用来标记高亮字段的后置标签
			"required_field_match": "false"  //用来标记对非搜索字段高亮
		  }
		}
	}
	
五、聚合（三要素：聚合名字、聚合类型、聚合字段）
	桶聚合：Terms
	度量聚合：Stats
	GET /items/_search
	 {
	   "query": {
		 "term": {
		   "category": "手机"
		 }
	   },
	   "size": 0,
	   "aggs": {
		 "brandAgg": {
		   "terms": {
			 "field": "brand",
			 "size": 20
		   },
		   "aggs": {
			 "priceAgg": {
			   "stats": {
				 "field": "price"
			   }
			 }
		   }
		 }
	   }
	 }
