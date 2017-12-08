# QA 中文问答

## QA1.0 
参见 [QA1.0/SearchEngine.ipynb](https://github.com/githubxiaowei/QA/blob/master/QA1.0/SearchEngine.ipynb)

* 直接将xml文档分成平均大小约100k的49125块part,存到parts/目录下
* 建立基于jieba词典的倒排索引，由词语索引到part
* 根据查询语句query中的分词，索引到包含分词的part
* 取出部分part，分析这些part中每一句话，找到包含不同分词最多的语句


## QA2.0 
参见[QA2.0/SearchEngine.ipynb](https://github.com/githubxiaowei/QA/blob/master/QA2.0/SearchEngine.ipynb)

* 使用xmlReader流式读取xml文件，解析出每一个page,存到pages/[0-46]/[0-255]/目录下，最后一个文件 pages/46/59/180，故页面总数为46*256*256+59*256+181=3029941
* 由于维基百科每一个页面page的标题title基本互不相同，所以建立title到index的映射
* 根据查询语句query中的分词，如果有分词恰好对应到相关百科页面，返回页面的index
* 取出相关page，分析这些page中每一句话，找到包含不同分词最多的语句


## QA1.0 
参见[QA3.0/SearchEngine.ipynb](https://github.com/githubxiaowei/QA/blob/master/QA3.0/SearchEngine.ipynb)

* 使用xmlReader流式读取xml文件，解析出每一个page,存到pages/[0-46]/[0-255]/目录下（同QA2.0）
* 建立基于jieba词典的倒排索引，由词语索引到page
* 根据查询语句query中的分词，索引到包含分词的page
* 取出部分page，分析这些page中每一句话，找到包含不同分词最多的语句	


