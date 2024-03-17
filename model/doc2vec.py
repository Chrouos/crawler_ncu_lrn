import gensim
import numpy as np
import jieba
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

stop_text = open('stop_list.txt', 'r')
stop_word = []
for line in stop_text:
    stop_word.append(line.strip())
    
TaggededDocument = gensim.models.doc2vec.TaggedDocument

def get_corpus():
    with open("stop_list.txt", 'r') as doc:
        docs = doc.readlines()
    train_docs = []
    for i, text in enumerate(docs):
        word_list = text.split(' ')
        length = len(word_list)
        word_list[length - 1] = word_list[length - 1].strip()
        document = TaggedDocument(word_list, tags=[i])
        train_docs.append(document)
    return train_docs

def train(x_train, vector_size=200, epoch_num=1):
    model_dm = Doc2Vec(x_train, min_count=1, window=3, vector_size=vector_size, sample=1e-3, negative=5, workers=4)
    model_dm.train(x_train, total_examples=model_dm.corpus_count, epochs=70)
    model_dm.save('model_doc2vec')
    return model_dm

def test():
    model_dm = Doc2Vec.load("model_doc2vec")
    text_test = u'武漢東湖新技術開發區人民檢察院指控： 2013年4月27日21時許，被告人王某、連某經預謀後，竄至本區流芳高新四路聯想工地內，竊取該處扣件若干 欲離開時，被此處工地值班人員劉某發現並制止。 被告王某、連某遂共同用拳頭、安全帽及啤酒瓶毆打劉某的頭部、背部等處，致受害人劉某輕微傷，後共同逃離現場。 2013年11月1日，被告國王被公安機關逮捕。 同年11月25日，被告王某依照公安機關的安排，以打電話的方式聯絡被告連某投案。 到案後，上述二被告共同賠償被害人劉某人民幣1．5萬元，並獲得諒解。 針對上述指控的事實，公訴機關當庭出示及宣讀的證據有：1、抓獲及破案經過；2、調解協議、諒解書、病歷等書證；3、涉案物品照片；4、鑑定意見書；5、 證人證詞；6、被害人陳述；7、被告的供述及辯解、訊問同步錄音錄影等。 公訴機關認為，被告人王某、連某以非法佔有為目的，在實施竊盜行為時，為抗拒抓捕，當場使用暴力，致一人輕微傷，其行為均觸犯了《中華人民共和國刑法》第二 百六十九條、第二百六十三條的規定，應以搶劫罪追究其刑事責任。 案發後，被告人王某協助公安機關抓捕同案犯，具有《中華人民共和國刑法》第六十八條規定的情節；被告人連某主動投案，並如實供述自己的犯罪事實，具有《中華人民 共和國刑法》第六十七條第一款規定的劇情。'
    text_cut = jieba.cut(text_test)
    text_raw = []
    for i in list(text_cut):
        text_raw.append(i)
    inferred_vector_dm = model_dm.infer_vector(text_raw)
    sims = model_dm.docvecs.most_similar([inferred_vector_dm], topn=10)

    return sims

if __name__ == '__main__':
    x_train = get_corpus()
    # model_dm = train(x_train)
    sims = test()
    for count, sim in sims:
        sentence = x_train[count]
        words = ''
        for word in sentence[0]:
            words = words + word + ' '
        print(words, sim, len(sentence[0]))