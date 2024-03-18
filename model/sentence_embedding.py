from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F

# 載入模型和分詞器
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/paraphrase-mpnet-base-v2')
model = AutoModel.from_pretrained('sentence-transformers/paraphrase-mpnet-base-v2')

def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]  # 取得所有token的嵌入向量
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

def compute_sentence_embeddings(sentences):

    # 對句子進行分詞
    encoded_input = tokenizer(sentences, max_length=768, padding=True, truncation=True, return_tensors='pt')

    # 計算token嵌入向量
    with torch.no_grad():
        model_output = model(**encoded_input)

    # 執行池化操作
    sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])

    # 正規化嵌入向量
    sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)

    return sentence_embeddings

def get_sentence_embedding(sentence):
    # 分詞並準備模型輸入
    encoded_input = tokenizer(sentence, return_tensors='pt', truncation=True) # , max_length=768

    # 計算嵌入向量
    with torch.no_grad():
        model_output = model(**encoded_input)

    # 取平均池化作為句子向量
    attention_mask = encoded_input['attention_mask']
    sentence_embedding = mean_pooling(model_output, attention_mask)

    # 正規化
    sentence_embedding = F.normalize(sentence_embedding, p=2, dim=1)

    return sentence_embedding.squeeze()


def cosine_similarity(a, b):
    dot_product = torch.dot(a, b)
    
    norm_a = torch.norm(a, p=2)
    norm_b = torch.norm(b, p=2)
    
    similarity = dot_product / (norm_a * norm_b)
    return similarity


if __name__ == "__main__":
    word1 = '張立杰教授'
    word2 = '理財能力 | 均一教育平台 <![endif]--> x'
    word2 = '立杰 教授 LI-CHIEH CHANG, PROFESSOR (03) 4227151 ext 33870 bchang.tw@gmail.comx'

    # 獲得詞嵌入
    word_embedding1 = get_sentence_embedding(word1)
    word_embedding2 = get_sentence_embedding(word2)
    print(len(word_embedding1), len(word_embedding2))

    # 計算相似度
    similarity = cosine_similarity(word_embedding1, word_embedding2)
    print(f"Similarity between '{word1}' and '{word2}':", similarity.item())
