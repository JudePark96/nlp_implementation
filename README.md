# NLP paper implementation with PyTorch
The papers were implemented in using korean corpus 

### Classification
+ Using the [Naver sentiment movie corpus v1.0](https://github.com/e9t/nsmc)
+ Hyper-parameter was arbitrarily selected. (defined by `experiments/base_model/config.json`)

| Model \ Accuracy | Train (120,000) | Validation (30,000) | Test (50,000) | Date |
| :--------------- | :-------: | :------------: | :------: | :--------------: |
| SenCNN           |  90.80%  |     86.48%     |  85.90%  | 191027 |
| CharCNN          | 86.20% | 82.21% | 81.60% | 191027 |
| ConvRec          | 86.48% | 82.81% | 82.45% | 191027 |
| VDCNN            | 87.32% | 84.46% | 84.35% | 191027 |
| SAN | 90.86% | 86.76% | 86.47% | 191027 |
| ETRIBERT | 91.13% | 89.18% | 88.88% | 191027 |
| SKTBERT | 92.39% | 88.98% | 88.98% | 191110 |

* [x] [Convolutional Neural Networks for Sentence Classification](https://github.com/aisolab/nlp_implementation/tree/master/Convolutional_Neural_Networks_for_Sentence_Classification) (as SenCNN)
  + https://arxiv.org/abs/1408.5882
* [x] [Character-level Convolutional Networks for Text Classification](https://github.com/aisolab/nlp_implementation/tree/master/Character-level_Convolutional_Networks_for_Text_Classification) (as CharCNN)
  + https://arxiv.org/abs/1509.01626
* [x] [Efficient Character-level Document Classification by Combining Convolution and Recurrent Layers](https://github.com/aisolab/nlp_implementation/tree/master/Efficient_Character-level_Document_Classification_by_Combining_Convolution_and_Recurrent_Layers) (as ConvRec)
  + https://arxiv.org/abs/1602.00367
* [x] [Very Deep Convolutional Networks for Text Classification](https://github.com/aisolab/nlp_implementation/tree/master/Very_Deep_Convolutional_Networks_for_Text_Classification) (as VDCNN)
  + https://arxiv.org/abs/1606.01781
* [x] [A Structured Self-attentive Sentence Embedding](https://github.com/aisolab/nlp_implementation/tree/master/A_Structured_Self-attentive_Sentence_Embedding_cls) (as SAN)
  + https://arxiv.org/abs/1703.03130
* [x] [BERT_single_sentence_classification](https://github.com/aisolab/nlp_implementation/tree/master/BERT_single_sentence_classification) (as ETRIBERT, SKTBERT)
  + https://arxiv.org/abs/1810.04805

### Paraphrase detection
+ Creating dataset from https://github.com/songys/Question_pair 
+ Hyper-parameter was arbitrarily selected. (epoch: 5, mini_batch: 64)

| Model \ Accuracy | Train (6,136) | Validation (682) | Test (758) | Date |
| :--------------- | :-------: | :------------: | :------------: | -------------- |
| Siam     |  93.30%  |     83.57%     |     84.16%     | 191028       |
| SAN | 94.86% | 83.13% | 84.96% | 191028 |
| Stochastic | 88.70% | 81.67% | 81.92% | 191106 |
| ETRIBERT | 95.04% | 93.69% | 93.93% | 191004 |


* [x] [A Structured Self-attentive Sentence Embedding](https://github.com/aisolab/nlp_implementation/tree/master/A_Structured_Self-attentive_Sentence_Embedding_ptc) (as SAN)
  + https://arxiv.org/abs/1703.03130
* [x] [Siamese recurrent architectures for learning sentence similarity](https://github.com/aisolab/nlp_implementation/tree/master/Siamese_recurrent_architectures_for_learning_sentence_similarity) (as Siam)
  + https://www.aaai.org/ocs/index.php/AAAI/AAAI16/paper/viewPaper/12195
* [x] [Stochastic Answer Networks for Natural Language Inference](https://github.com/aisolab/nlp_implementation/tree/master/Stochastic_Answer_Networks_for_Natural_Language_Inference) (as Stochastic)
  + https://arxiv.org/abs/1804.07888
* [x] [BERT_pairwise_text_classification](https://github.com/aisolab/nlp_implementation/tree/master/BERT_pairwise_text_classification) (as ETRIBERT)
  + https://arxiv.org/abs/1810.04805

### Language model
* [ ] Character-Aware Neural Language Models
  + https://arxiv.org/abs/1508.06615


### Named entity recognition
| Model \ f1 | Train (81,000) | Validation (9,000) | Date |
| :--------------- | :-------: | :------------: | -------------- |
| BiLSTM-CRF |  79.88%  |     76.45%     | 191004         |
+ Using the [Naver nlp-challange corpus for NER](https://github.com/naver/nlp-challenge/tree/master/missions/ner)
+ Hyper-parameter was arbitrarily selected.
* [x] [Bidirectional LSTM-CRF Models for Sequence Tagging](https://github.com/aisolab/nlp_implementation/tree/master/Bidirectional_LSTM-CRF_Models_for_Sequence_Tagging) (BiLSTM-CRF)
	+ https://arxiv.org/abs/1508.01991
* [ ] End-to-end Sequence Labeling via Bi-directional LSTM-CNNs-CRF
	+ https://arxiv.org/abs/1603.01354
* [ ] Neural Architectures for Named Entity Recognition
	+ https://arxiv.org/abs/1603.01360
* [ ] BERT_single_sentence_tagging
	+ https://arxiv.org/abs/1810.04805


### Neural machine translation

| Model \ Perplexity | Train () | Validation  () | Test () | Date |
| ------------------ | -------- | -------------- | ------- | ---- |
| LuongAttn          |          |                |         |      |
| Transformer        |          |                |         |      |

* [x] Effective Approaches to Attention-based Neural Machine Translation (as LuongAttn)
	+ https://arxiv.org/abs/1608.07905
* [ ] Attention Is All You Need (as Transformer)
	+ https://arxiv.org/abs/1706.03762


### Machine reading comprension
* [ ] Machine Comprehension Using Match-LSTM and Answer Pointer
	+ https://arxiv.org/abs/1611.01603
* [ ] Bi-directional attention flow for machine comprehension
	+ https://arxiv.org/abs/1611.01603
* [ ] BERT_question_answering
	+ https://arxiv.org/abs/1810.04805
