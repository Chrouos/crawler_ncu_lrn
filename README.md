# 學習與教學研究所 (session)
+ depth = 2
+ 總花費: 2189.4633433818817
+ 長度: 160

# 學習與教學研究所 (bs4)
+ depth = 2
+ 總花費: 1402.2504224777222秒
+ 長度: 223

# 學習與教學研究所 (bs4)
+ depth = 3
+ 總花費: 
+ 長度: 846

# Embedding Model
分別比較三個句子，預計是 word_1 和 word_3 應該要最接近
```
word_1 = '張立傑教授'
word_2 = '理財能力 | 均一教育平台 <![endif]--> x'
word_3 = '立杰 教授 LI-CHIEH CHANG, PROFESSOR (03) 4227151 ext 33870 bchang.tw@gmail.comx'
```
分別跑下面兩個 embedding model
+ sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
+ sentence-transformers/all-MiniLM-L6-v2
結果:
```
sentence-transformers/paraphrase-mpnet-base-v2
Similarity between word_1_2: 0.5558281540870667
Similarity between word_1_3: 0.694909930229187
Similarity between word_2_3 0.5728631019592285
768
sentence-transformers/multi-qa-mpnet-base-dot-v1
Similarity between word_1_2: 0.5421507358551025
Similarity between word_1_3: 0.6456298828125
Similarity between word_2_3 0.6729167699813843
768
sentence-transformers/multi-qa-MiniLM-L6-cos-v1
Similarity between word_1_2: 0.3625856637954712
Similarity between word_1_3: 0.5489000678062439
Similarity between word_2_3 0.5522013902664185
384
sentence-transformers/all-MiniLM-L12-v2
Similarity between word_1_2: 0.35926708579063416
Similarity between word_1_3: 0.3059222102165222
Similarity between word_2_3 0.3771684169769287
384
sentence-transformers/all-MiniLM-L6-v2
Similarity between word_1_2: 0.3682458698749542
Similarity between word_1_3: 0.42082086205482483
Similarity between word_2_3 0.5987534523010254
384
```

使用 Embedding 與未使用的結果:
```
搜尋語句: 張立杰教授 搜尋欄位: content
未使用 Embedding 搜尋結果:
URL: http://lrn.ncu.edu.tw/research_areas/
URL: http://lrn.ncu.edu.tw/?p=1761
@ 使用 Embedding 搜尋結果:
URL: http://lrn.ncu.edu.tw/lc-chang/
URL: http://lrn.ncu.edu.tw/zh/lc-chang/
```
使用 Embedding 模型的成效，可以讓搜尋結果更貼切



# 注意
1. 其他：參考 https://blog.csdn.net/qq_17375491/article/details/121116747 說明作業說明的 Elasticsearch 的版本是7.11.2，因此採用最新版本的 pip install elasticsearch 會無法成功連線，要降版本到7.13.1 才有辦法成功執行程式碼。

2. Elastic Kibana 使用最新版本的 Chrome 打不開，但使用 Edge 可以成功使用。

3. Kibana download file 如果有壓縮打不開的問題(zip)，建議使用 WinRAR 打開。除此之外要與 Elasticsearch 找到對應的版本下載 7.11.2

# Version
+ Elasticsearch: 7.11.1
+ Kibana 7.11.2
+ pip  install  elasticsearch==7.13.1
