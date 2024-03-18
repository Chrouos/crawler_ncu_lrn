from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F

def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]  # 取得所有token的嵌入向量
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

def compute_sentence_embeddings(sentences):
    # 載入模型和分詞器
    tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
    model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

    # 對句子進行分詞
    encoded_input = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')

    # 計算token嵌入向量
    with torch.no_grad():
        model_output = model(**encoded_input)

    # 執行池化操作
    sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])

    # 正規化嵌入向量
    sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)

    return sentence_embeddings


if __name__ == "__main__":
    sentences = ['This is an example sentence', 'Each sentence is converted']
    sentence_embeddings = compute_sentence_embeddings(sentences)
    print("Sentence embeddings:")
    print(sentence_embeddings[0].tolist())
