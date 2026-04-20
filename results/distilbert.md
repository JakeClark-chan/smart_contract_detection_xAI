============================================================
ENVIRONMENT CHECK
============================================================
Python: 3.12.12 (main, Oct 10 2025, 08:52:57) [GCC 11.4.0]
PyTorch: 2.8.0+cu126
CUDA available: True
GPU: Tesla P100-PCIE-16GB

============================================================
STEP 4: Run All Experiments
============================================================

============================================================
Training with column: before_optimized
============================================================
Train: 8444, Test: 2111
Some weights of DistilBertForSequenceClassification were not initialized from the model checkpoint at distilbert-base-uncased and are newly initialized: ['classifier.bias', 'classifier.weight', 'pre_classifier.bias', 'pre_classifier.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Training...
 [4230/4230 30:05, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.433900	0.406395	0.857984	0.777679	0.809229	0.737320	0.183777	13.495400	125.154000	3.927000
2	0.386700	0.395792	0.890716	0.763065	0.814123	0.746694	0.170634	13.422500	125.833000	3.949000
3	0.358700	0.348773	0.864998	0.831045	0.845032	0.779416	0.155240	13.480600	125.291000	3.932000
4	0.334200	0.348752	0.886139	0.805580	0.838910	0.778301	0.153819	13.491700	125.188000	3.928000
5	0.318600	0.329582	0.878105	0.826838	0.849170	0.790112	0.149438	13.531300	124.821000	3.917000
6	0.308800	0.322893	0.875988	0.843224	0.857642	0.797928	0.143754	13.510000	125.018000	3.923000
7	0.295200	0.318778	0.882502	0.848760	0.863299	0.804983	0.137715	13.526000	124.871000	3.918000
8	0.275000	0.313303	0.872955	0.871568	0.871695	0.811812	0.134044	13.555300	124.601000	3.910000
9	0.258400	0.313218	0.879006	0.868911	0.872228	0.814575	0.131083	13.453700	125.541000	3.939000
10	0.261600	0.310075	0.881000	0.869796	0.874121	0.816815	0.129544	13.518300	124.941000	3.921000
Evaluating on eval set...
Evaluating on test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.96      0.98      0.97      1952
Unchecked Return Values For Low Level Calls       0.86      0.88      0.87      1180
                          Denial of Service       0.86      0.82      0.84       985
                          Time manipulation       0.76      0.61      0.67       668
                                 Reentrancy       0.82      0.81      0.82       826

                                  micro avg       0.88      0.86      0.87      5611
                                  macro avg       0.85      0.82      0.84      5611
                               weighted avg       0.88      0.86      0.87      5611
                                samples avg       0.87      0.86      0.84      5611


Results for before_optimized:
  Train Samples: 8444, Test Samples: 2111
  Train Time: 30.1 min
  Train Inference Time: 16.83s
  Test Inference Time: 13.44s
  Precision: 0.8810
  Recall: 0.8698
  F1: 0.8741
  Hamming Score: 0.8168
  Hamming Loss: 0.1295

============================================================
Training with column: optimized_80p
============================================================
Train: 8444, Test: 2111
Some weights of DistilBertForSequenceClassification were not initialized from the model checkpoint at distilbert-base-uncased and are newly initialized: ['classifier.bias', 'classifier.weight', 'pre_classifier.bias', 'pre_classifier.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Training...
 [4230/4230 30:11, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.427400	0.410414	0.824917	0.817876	0.820340	0.745194	0.183304	13.510700	125.012000	3.923000
2	0.386600	0.353279	0.850449	0.838760	0.843339	0.780935	0.159029	13.484100	125.259000	3.931000
3	0.358400	0.336758	0.885757	0.809342	0.840818	0.786955	0.150977	13.530900	124.826000	3.917000
4	0.322900	0.322976	0.873192	0.841231	0.855344	0.797651	0.144701	13.545300	124.693000	3.913000
5	0.322600	0.311762	0.876731	0.849764	0.862405	0.803789	0.139964	13.518200	124.943000	3.921000
6	0.309000	0.311972	0.879911	0.847968	0.861703	0.807401	0.138070	13.498800	125.122000	3.926000
7	0.277500	0.310880	0.896663	0.833595	0.860567	0.807608	0.134636	13.515800	124.965000	3.921000
8	0.270400	0.305786	0.895354	0.843476	0.867374	0.813627	0.131676	13.527000	124.861000	3.918000
9	0.265700	0.297968	0.893815	0.862565	0.877329	0.824107	0.124452	13.547400	124.673000	3.912000
10	0.263100	0.298707	0.891277	0.866158	0.877758	0.826830	0.124097	13.513900	124.982000	3.922000
Evaluating on eval set...
Evaluating on test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.96      0.98      0.97      1952
Unchecked Return Values For Low Level Calls       0.89      0.86      0.88      1180
                          Denial of Service       0.89      0.78      0.83       985
                          Time manipulation       0.75      0.62      0.68       668
                                 Reentrancy       0.87      0.82      0.84       826

                                  micro avg       0.90      0.85      0.88      5611
                                  macro avg       0.87      0.81      0.84      5611
                               weighted avg       0.89      0.85      0.87      5611
                                samples avg       0.89      0.84      0.85      5611


Results for optimized_80p:
  Train Samples: 8444, Test Samples: 2111
  Train Time: 30.2 min
  Train Inference Time: 16.85s
  Test Inference Time: 13.39s
  Precision: 0.8913
  Recall: 0.8662
  F1: 0.8778
  Hamming Score: 0.8268
  Hamming Loss: 0.1241

============================================================
Training with column: optimized_50p
============================================================
Train: 8444, Test: 2111
Some weights of DistilBertForSequenceClassification were not initialized from the model checkpoint at distilbert-base-uncased and are newly initialized: ['classifier.bias', 'classifier.weight', 'pre_classifier.bias', 'pre_classifier.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Training...
 [4230/4230 30:15, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.409300	0.397800	0.853924	0.793622	0.819293	0.748628	0.175607	13.524200	124.887000	3.919000
2	0.373800	0.347576	0.848232	0.855154	0.850851	0.789343	0.154648	13.556100	124.594000	3.910000
3	0.344100	0.329412	0.859960	0.856052	0.857607	0.796892	0.147898	13.481700	125.281000	3.931000
4	0.307700	0.333456	0.855862	0.854031	0.854270	0.792323	0.151332	13.583400	124.343000	3.902000
5	0.301900	0.318211	0.879194	0.844824	0.859165	0.802033	0.140438	13.492500	125.181000	3.928000
6	0.296500	0.302172	0.868446	0.884348	0.875701	0.821749	0.130847	13.513200	124.989000	3.922000
7	0.251700	0.294286	0.885963	0.862115	0.872731	0.818433	0.128597	13.513500	124.986000	3.922000
8	0.255300	0.307658	0.890439	0.856501	0.872413	0.818246	0.128952	13.529600	124.838000	3.917000
9	0.243200	0.294260	0.885230	0.877386	0.881126	0.825775	0.123505	13.536600	124.773000	3.915000
10	0.242700	0.296367	0.889913	0.874916	0.881847	0.828814	0.121255	13.479300	125.303000	3.932000
Evaluating on eval set...
Evaluating on test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.96      0.98      0.97      1952
Unchecked Return Values For Low Level Calls       0.89      0.89      0.89      1180
                          Denial of Service       0.88      0.83      0.85       985
                          Time manipulation       0.75      0.66      0.70       668
                                 Reentrancy       0.85      0.86      0.86       826

                                  micro avg       0.89      0.88      0.89      5611
                                  macro avg       0.87      0.84      0.85      5611
                               weighted avg       0.89      0.88      0.88      5611
                                samples avg       0.88      0.86      0.85      5611


Results for optimized_50p:
  Train Samples: 8444, Test Samples: 2111
  Train Time: 30.3 min
  Train Inference Time: 16.89s
  Test Inference Time: 13.43s
  Precision: 0.8899
  Recall: 0.8749
  F1: 0.8818
  Hamming Score: 0.8288
  Hamming Loss: 0.1213

============================================================
Training with column: optimized_20p
============================================================
Train: 8444, Test: 2111
Some weights of DistilBertForSequenceClassification were not initialized from the model checkpoint at distilbert-base-uncased and are newly initialized: ['classifier.bias', 'classifier.weight', 'pre_classifier.bias', 'pre_classifier.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Training...
 [4230/4230 24:17, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.424300	0.395146	0.827050	0.837862	0.831638	0.756473	0.177146	10.806800	156.290000	4.904000
2	0.395200	0.363731	0.833021	0.862789	0.847223	0.780521	0.162226	10.764000	156.912000	4.924000
3	0.367200	0.349321	0.846462	0.846620	0.845255	0.784596	0.160332	10.779000	156.693000	4.917000
4	0.338500	0.340061	0.849258	0.855603	0.851849	0.792629	0.153819	10.807600	156.279000	4.904000
5	0.320500	0.319705	0.845653	0.877386	0.860794	0.803700	0.148490	10.814100	156.185000	4.901000
6	0.317200	0.319985	0.856190	0.868179	0.861575	0.806138	0.144109	10.852700	155.630000	4.884000
7	0.283400	0.313217	0.861533	0.878060	0.869580	0.812947	0.137715	10.813800	156.190000	4.901000
8	0.276000	0.311949	0.880937	0.842129	0.859897	0.810539	0.140083	10.805600	156.308000	4.905000
9	0.270000	0.307083	0.867186	0.879183	0.872955	0.818877	0.134281	10.792300	156.500000	4.911000
10	0.264600	0.307315	0.875098	0.875589	0.874789	0.824008	0.129781	10.750800	157.105000	4.930000
Evaluating on eval set...
Evaluating on test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.96      0.99      0.97      1952
Unchecked Return Values For Low Level Calls       0.85      0.90      0.88      1180
                          Denial of Service       0.88      0.81      0.84       985
                          Time manipulation       0.71      0.65      0.68       668
                                 Reentrancy       0.80      0.85      0.82       826

                                  micro avg       0.87      0.88      0.87      5611
                                  macro avg       0.84      0.84      0.84      5611
                               weighted avg       0.87      0.88      0.87      5611
                                samples avg       0.87      0.86      0.85      5611


Results for optimized_20p:
  Train Samples: 8444, Test Samples: 2111
  Train Time: 24.3 min
  Train Inference Time: 11.75s
  Test Inference Time: 10.75s
  Precision: 0.8751
  Recall: 0.8756
  F1: 0.8748
  Hamming Score: 0.8240
  Hamming Loss: 0.1298

Total training time: 118.9 minutes
