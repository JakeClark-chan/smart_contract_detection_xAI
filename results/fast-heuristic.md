# BERT
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
Some weights of BertForSequenceClassification were not initialized from the model checkpoint at bert-base-uncased and are newly initialized: ['classifier.bias', 'classifier.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Training...
 [4230/4230 59:25, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.425300	0.401083	0.839257	0.810587	0.821671	0.743645	0.177383	25.477400	66.294000	2.080000
2	0.384100	0.372001	0.826407	0.856377	0.839946	0.761151	0.169213	25.487400	66.268000	2.079000
3	0.347900	0.364571	0.851898	0.834934	0.841520	0.772804	0.160213	25.497800	66.241000	2.079000
4	0.324200	0.357648	0.865926	0.832254	0.846377	0.776100	0.153700	25.503400	66.226000	2.078000
5	0.318200	0.352246	0.835070	0.890328	0.860968	0.790872	0.156069	25.504100	66.225000	2.078000
6	0.293200	0.336707	0.857899	0.860174	0.856967	0.791247	0.148727	25.489000	66.264000	2.079000
7	0.273600	0.331239	0.870597	0.846102	0.855134	0.793685	0.144819	25.520600	66.182000	2.077000
8	0.248100	0.331005	0.872781	0.847219	0.858609	0.794662	0.143635	25.523200	66.175000	2.077000
9	0.253200	0.333219	0.866310	0.858164	0.861697	0.794415	0.143635	25.527600	66.164000	2.076000
10	0.237300	0.334363	0.869902	0.861068	0.865270	0.797168	0.140912	25.525300	66.170000	2.076000
Evaluating on eval set...
Evaluating on test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.96      0.98      0.97      1952
Unchecked Return Values For Low Level Calls       0.88      0.86      0.87      1180
                          Denial of Service       0.88      0.83      0.85       985
                          Time manipulation       0.71      0.69      0.70       668
                                 Reentrancy       0.83      0.81      0.82       826

                                  micro avg       0.88      0.87      0.88      5611
                                  macro avg       0.85      0.83      0.84      5611
                               weighted avg       0.88      0.87      0.87      5611
                                samples avg       0.87      0.86      0.84      5611


Results for before_optimized:
  Train Samples: 8444, Test Samples: 2111
  Train Time: 59.5 min
  Train Inference Time: 31.87s
  Test Inference Time: 25.51s
  Precision: 0.8699
  Recall: 0.8611
  F1: 0.8653
  Hamming Score: 0.7972
  Hamming Loss: 0.1409

============================================================
Training with column: optimized_80p
============================================================
Train: 8444, Test: 2111
Some weights of BertForSequenceClassification were not initialized from the model checkpoint at bert-base-uncased and are newly initialized: ['classifier.bias', 'classifier.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Training...
 [4230/4230 59:46, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.429300	0.425813	0.801585	0.847488	0.820477	0.730264	0.191593	25.535000	66.144000	2.076000
2	0.381300	0.360833	0.867020	0.810138	0.833436	0.763371	0.162345	25.542900	66.124000	2.075000
3	0.351500	0.344614	0.877004	0.820142	0.844440	0.776426	0.152872	25.536500	66.141000	2.075000
4	0.322800	0.345625	0.839694	0.903290	0.869674	0.799901	0.146714	25.550000	66.106000	2.074000
5	0.298600	0.330473	0.861582	0.858826	0.858481	0.789964	0.147188	25.544600	66.120000	2.075000
6	0.287100	0.324164	0.875990	0.849711	0.859607	0.794237	0.141385	25.540900	66.129000	2.075000
7	0.266200	0.321512	0.877883	0.852157	0.862107	0.797780	0.139728	25.531200	66.154000	2.076000
8	0.268600	0.312964	0.875187	0.877279	0.875987	0.809335	0.131676	25.538000	66.137000	2.075000
9	0.224400	0.314209	0.876262	0.872165	0.873813	0.807075	0.132860	25.538600	66.135000	2.075000
10	0.216900	0.311405	0.876235	0.870387	0.872494	0.806355	0.133333	25.531000	66.155000	2.076000
Evaluating on eval set...
Evaluating on test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.97      0.97      0.97      1952
Unchecked Return Values For Low Level Calls       0.88      0.89      0.89      1180
                          Denial of Service       0.87      0.85      0.86       985
                          Time manipulation       0.77      0.67      0.72       668
                                 Reentrancy       0.83      0.84      0.83       826

                                  micro avg       0.89      0.88      0.88      5611
                                  macro avg       0.86      0.85      0.85      5611
                               weighted avg       0.89      0.88      0.88      5611
                                samples avg       0.88      0.87      0.85      5611


Results for optimized_80p:
  Train Samples: 8444, Test Samples: 2111
  Train Time: 59.8 min
  Train Inference Time: 31.89s
  Test Inference Time: 25.55s
  Precision: 0.8762
  Recall: 0.8704
  F1: 0.8725
  Hamming Score: 0.8064
  Hamming Loss: 0.1333

============================================================
Training with column: optimized_50p
============================================================
Train: 8444, Test: 2111
Some weights of BertForSequenceClassification were not initialized from the model checkpoint at bert-base-uncased and are newly initialized: ['classifier.bias', 'classifier.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Training...
 [4230/4230 59:59, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.408000	0.392879	0.847048	0.805469	0.816517	0.733491	0.178922	25.559300	66.082000	2.074000
2	0.359600	0.359503	0.866397	0.801912	0.827294	0.761141	0.166134	25.569400	66.056000	2.073000
3	0.332400	0.325612	0.871259	0.841263	0.852994	0.785001	0.147780	25.568100	66.059000	2.073000
4	0.300800	0.325513	0.855906	0.887728	0.870959	0.797918	0.141741	25.559100	66.082000	2.074000
5	0.271700	0.308702	0.872559	0.879057	0.875192	0.811437	0.131557	25.570200	66.053000	2.073000
6	0.269000	0.312895	0.883070	0.849266	0.860897	0.798244	0.138780	25.584200	66.017000	2.072000
7	0.244500	0.303987	0.889094	0.853935	0.870344	0.805033	0.133097	25.560400	66.079000	2.074000
8	0.233000	0.298053	0.894081	0.865273	0.879076	0.816104	0.125163	25.568400	66.058000	2.073000
9	0.191600	0.298704	0.890993	0.879502	0.884976	0.821275	0.121018	25.572100	66.049000	2.073000
10	0.191000	0.302641	0.892808	0.872832	0.882015	0.821285	0.122321	25.563500	66.071000	2.073000
Evaluating on eval set...
Evaluating on test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.97      0.97      0.97      1952
Unchecked Return Values For Low Level Calls       0.89      0.91      0.90      1180
                          Denial of Service       0.88      0.83      0.86       985
                          Time manipulation       0.77      0.67      0.72       668
                                 Reentrancy       0.84      0.86      0.85       826

                                  micro avg       0.90      0.88      0.89      5611
                                  macro avg       0.87      0.85      0.86      5611
                               weighted avg       0.89      0.88      0.89      5611
                                samples avg       0.88      0.87      0.86      5611


Results for optimized_50p:
  Train Samples: 8444, Test Samples: 2111
  Train Time: 60.0 min
  Train Inference Time: 31.94s
  Test Inference Time: 25.56s
  Precision: 0.8928
  Recall: 0.8728
  F1: 0.8820
  Hamming Score: 0.8213
  Hamming Loss: 0.1223

============================================================
Training with column: optimized_20p
============================================================
Train: 8444, Test: 2111
Some weights of BertForSequenceClassification were not initialized from the model checkpoint at bert-base-uncased and are newly initialized: ['classifier.bias', 'classifier.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Training...
 [4230/4230 48:16, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.431100	0.411112	0.814112	0.835482	0.823105	0.735554	0.186264	20.521700	82.303000	2.583000
2	0.394700	0.390282	0.839576	0.812139	0.823818	0.749467	0.177857	20.531600	82.264000	2.581000
3	0.358100	0.358467	0.851601	0.843931	0.847285	0.775202	0.159266	20.536000	82.246000	2.581000
4	0.327000	0.351036	0.846309	0.873499	0.859360	0.786846	0.153582	20.546000	82.206000	2.580000
5	0.302600	0.345026	0.841823	0.890396	0.864041	0.791346	0.149556	20.533700	82.255000	2.581000
6	0.307800	0.325413	0.869373	0.864606	0.866186	0.801036	0.139372	20.551700	82.183000	2.579000
7	0.281200	0.328187	0.872917	0.859271	0.865183	0.801164	0.139491	20.558100	82.158000	2.578000
8	0.262400	0.323234	0.874694	0.871054	0.872278	0.808999	0.133807	20.548400	82.196000	2.579000
9	0.226100	0.320333	0.873923	0.877946	0.875418	0.813677	0.131912	20.565700	82.127000	2.577000
10	0.225700	0.320103	0.879253	0.870165	0.873927	0.810973	0.131202	20.552000	82.182000	2.579000
Evaluating on eval set...
Evaluating on test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.96      0.98      0.97      1952
Unchecked Return Values For Low Level Calls       0.86      0.89      0.88      1180
                          Denial of Service       0.90      0.82      0.86       985
                          Time manipulation       0.73      0.67      0.70       668
                                 Reentrancy       0.82      0.85      0.83       826

                                  micro avg       0.88      0.88      0.88      5611
                                  macro avg       0.85      0.84      0.85      5611
                               weighted avg       0.88      0.88      0.88      5611
                                samples avg       0.87      0.86      0.85      5611


Results for optimized_20p:
  Train Samples: 8444, Test Samples: 2111
  Train Time: 48.3 min
  Train Inference Time: 22.23s
  Test Inference Time: 20.55s
  Precision: 0.8793
  Recall: 0.8702
  F1: 0.8739
  Hamming Score: 0.8110
  Hamming Loss: 0.1312

Total training time: 234.3 minutes

# DistilBERT

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

# CodeBERT

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
Some weights of RobertaForSequenceClassification were not initialized from the model checkpoint at microsoft/codebert-base and are newly initialized: ['classifier.dense.bias', 'classifier.dense.weight', 'classifier.out_proj.bias', 'classifier.out_proj.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Training...
 [4230/4230 59:39, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.388100	0.372179	0.833920	0.860506	0.846362	0.771403	0.163410	25.367600	66.581000	2.089000
2	0.343100	0.331781	0.846416	0.875389	0.859764	0.788317	0.150148	25.344400	66.642000	2.091000
3	0.316900	0.311083	0.864073	0.888938	0.875608	0.809443	0.134162	25.380700	66.547000	2.088000
4	0.282700	0.301030	0.871767	0.893381	0.881929	0.818482	0.126821	25.365600	66.586000	2.089000
5	0.255200	0.301737	0.884845	0.861617	0.872520	0.810746	0.133925	25.383300	66.540000	2.088000
6	0.222500	0.287522	0.897366	0.891159	0.893988	0.835050	0.111782	25.378500	66.552000	2.088000
7	0.210400	0.297358	0.879124	0.906264	0.892266	0.831735	0.117703	25.373000	66.567000	2.089000
8	0.194900	0.299970	0.899624	0.892048	0.895355	0.836797	0.112256	25.392500	66.516000	2.087000
9	0.177700	0.296092	0.896001	0.898712	0.897290	0.840586	0.109532	25.392400	66.516000	2.087000
10	0.163700	0.299557	0.896174	0.900044	0.897988	0.843428	0.109414	25.383500	66.539000	2.088000
Evaluating on eval set...
Evaluating on test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.97      0.98      0.97      1952
Unchecked Return Values For Low Level Calls       0.89      0.91      0.90      1180
                          Denial of Service       0.91      0.85      0.88       985
                          Time manipulation       0.75      0.78      0.76       668
                                 Reentrancy       0.85      0.89      0.87       826

                                  micro avg       0.90      0.91      0.90      5611
                                  macro avg       0.87      0.88      0.88      5611
                               weighted avg       0.90      0.91      0.90      5611
                                samples avg       0.89      0.89      0.87      5611


Results for before_optimized:
  Train Samples: 8444, Test Samples: 2111
  Train Time: 59.7 min
  Train Inference Time: 31.70s
  Test Inference Time: 25.39s
  Precision: 0.8962
  Recall: 0.9000
  F1: 0.8980
  Hamming Score: 0.8434
  Hamming Loss: 0.1094

============================================================
Training with column: optimized_80p
============================================================
Train: 8444, Test: 2111
Some weights of RobertaForSequenceClassification were not initialized from the model checkpoint at microsoft/codebert-base and are newly initialized: ['classifier.dense.bias', 'classifier.dense.weight', 'classifier.out_proj.bias', 'classifier.out_proj.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Training...
 [4230/4230 59:59, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.386200	0.367356	0.842194	0.853357	0.847516	0.778054	0.160332	25.362300	66.595000	2.090000
2	0.346900	0.327318	0.878442	0.844375	0.859407	0.807065	0.139964	25.363700	66.591000	2.090000
3	0.313500	0.304355	0.877223	0.868628	0.872188	0.818769	0.132149	25.370000	66.575000	2.089000
4	0.270800	0.294851	0.875043	0.887492	0.880121	0.827442	0.125992	25.385500	66.534000	2.088000
5	0.262400	0.285312	0.890477	0.892432	0.891351	0.842560	0.114150	25.391400	66.519000	2.087000
6	0.232700	0.284601	0.881410	0.896025	0.887610	0.838030	0.117940	25.388200	66.527000	2.088000
7	0.191400	0.285079	0.883298	0.900741	0.890999	0.845402	0.114742	25.376200	66.559000	2.089000
8	0.184800	0.296402	0.902981	0.880530	0.891103	0.842333	0.112256	25.388100	66.527000	2.088000
9	0.182500	0.284473	0.888578	0.916685	0.902297	0.857253	0.105151	25.391700	66.518000	2.087000
10	0.172600	0.287195	0.894933	0.904783	0.899739	0.854125	0.106098	25.425500	66.429000	2.085000
Evaluating on eval set...
Evaluating on test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.97      0.98      0.97      1952
Unchecked Return Values For Low Level Calls       0.91      0.91      0.91      1180
                          Denial of Service       0.87      0.89      0.88       985
                          Time manipulation       0.77      0.78      0.77       668
                                 Reentrancy       0.86      0.87      0.87       826

                                  micro avg       0.90      0.91      0.91      5611
                                  macro avg       0.88      0.89      0.88      5611
                               weighted avg       0.90      0.91      0.91      5611
                                samples avg       0.89      0.89      0.88      5611


Results for optimized_80p:
  Train Samples: 8444, Test Samples: 2111
  Train Time: 60.0 min
  Train Inference Time: 31.76s
  Test Inference Time: 25.41s
  Precision: 0.8949
  Recall: 0.9048
  F1: 0.8997
  Hamming Score: 0.8541
  Hamming Loss: 0.1061

============================================================
Training with column: optimized_50p
============================================================
Train: 8444, Test: 2111
Some weights of RobertaForSequenceClassification were not initialized from the model checkpoint at microsoft/codebert-base and are newly initialized: ['classifier.dense.bias', 'classifier.dense.weight', 'classifier.out_proj.bias', 'classifier.out_proj.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Training...
 [4230/4230 1:00:11, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.392700	0.389838	0.864415	0.809117	0.834457	0.763993	0.164121	25.407800	66.476000	2.086000
2	0.346100	0.313856	0.857927	0.874467	0.865744	0.802427	0.142214	25.415600	66.455000	2.085000
3	0.309300	0.292792	0.865646	0.898495	0.881586	0.827156	0.127886	25.422600	66.437000	2.085000
4	0.268700	0.306633	0.865191	0.893106	0.877453	0.817900	0.132860	25.404800	66.484000	2.086000
5	0.249400	0.281166	0.879394	0.910173	0.894348	0.845934	0.114506	25.403400	66.487000	2.086000
6	0.231400	0.273086	0.875295	0.919605	0.896666	0.848796	0.111545	25.395100	66.509000	2.087000
7	0.195800	0.281353	0.899175	0.889737	0.893530	0.849388	0.109651	25.399200	66.498000	2.087000
8	0.176900	0.279974	0.908375	0.885021	0.896352	0.851569	0.106809	25.422300	66.438000	2.085000
9	0.175900	0.273797	0.898091	0.910173	0.904080	0.859286	0.101954	25.422000	66.438000	2.085000
10	0.158000	0.274042	0.901139	0.907703	0.904304	0.861072	0.100651	25.410500	66.469000	2.086000
Evaluating on eval set...
Evaluating on test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.97      0.98      0.97      1952
Unchecked Return Values For Low Level Calls       0.90      0.91      0.90      1180
                          Denial of Service       0.89      0.87      0.88       985
                          Time manipulation       0.77      0.76      0.77       668
                                 Reentrancy       0.86      0.87      0.87       826

                                  micro avg       0.90      0.90      0.90      5611
                                  macro avg       0.88      0.88      0.88      5611
                               weighted avg       0.90      0.90      0.90      5611
                                samples avg       0.89      0.89      0.87      5611


Results for optimized_50p:
  Train Samples: 8444, Test Samples: 2111
  Train Time: 60.2 min
  Train Inference Time: 31.75s
  Test Inference Time: 25.41s
  Precision: 0.9011
  Recall: 0.9077
  F1: 0.9043
  Hamming Score: 0.8611
  Hamming Loss: 0.1007

============================================================
Training with column: optimized_20p
============================================================
Train: 8444, Test: 2111
Some weights of RobertaForSequenceClassification were not initialized from the model checkpoint at microsoft/codebert-base and are newly initialized: ['classifier.dense.bias', 'classifier.dense.weight', 'classifier.out_proj.bias', 'classifier.out_proj.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Training...
 [4230/4230 39:30, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.409200	0.388025	0.846574	0.815854	0.829570	0.761062	0.171462	16.743100	100.877000	3.165000
2	0.375300	0.340466	0.825660	0.896025	0.858436	0.793231	0.157608	16.735900	100.921000	3.167000
3	0.339700	0.329976	0.864058	0.856277	0.859795	0.803799	0.145293	16.750900	100.830000	3.164000
4	0.306800	0.324839	0.862242	0.878060	0.869852	0.810785	0.138544	16.735500	100.923000	3.167000
5	0.278500	0.300712	0.871203	0.881204	0.875929	0.823574	0.131557	16.744700	100.868000	3.165000
6	0.258500	0.307333	0.878377	0.866158	0.871054	0.819074	0.131557	16.724600	100.989000	3.169000
7	0.229300	0.297016	0.892477	0.867954	0.879088	0.827955	0.122795	16.733900	100.933000	3.167000
8	0.209100	0.307829	0.892304	0.866158	0.878832	0.829436	0.124926	16.750100	100.835000	3.164000
9	0.198800	0.298996	0.884769	0.889737	0.887124	0.835070	0.119953	16.724000	100.993000	3.169000
10	0.192400	0.300407	0.888504	0.887492	0.887889	0.838692	0.117229	16.734400	100.930000	3.167000
Evaluating on eval set...
Evaluating on test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.96      0.98      0.97      1952
Unchecked Return Values For Low Level Calls       0.87      0.89      0.88      1180
                          Denial of Service       0.91      0.85      0.88       985
                          Time manipulation       0.74      0.73      0.73       668
                                 Reentrancy       0.83      0.85      0.84       826

                                  micro avg       0.89      0.89      0.89      5611
                                  macro avg       0.86      0.86      0.86      5611
                               weighted avg       0.89      0.89      0.89      5611
                                samples avg       0.88      0.87      0.86      5611


Results for optimized_20p:
  Train Samples: 8444, Test Samples: 2111
  Train Time: 39.5 min
  Train Inference Time: 19.84s
  Test Inference Time: 16.72s
  Precision: 0.8885
  Recall: 0.8875
  F1: 0.8879
  Hamming Score: 0.8387
  Hamming Loss: 0.1172

Total training time: 225.7 minutes

# GPT-2

============================================================
STEP 4: Run All Experiments
============================================================

============================================================
Training with column: before_optimized
============================================================
Train: 8444, Test: 2111
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
GPT2ForSequenceClassification LOAD REPORT from: gpt2
Key          | Status  | 
-------------+---------+-
score.weight | MISSING | 

Notes:
- MISSING:	those params were newly initialized because missing from the checkpoint. Consider training on your downstream task.
Training...
 [4230/4230 24:34, Epoch 10/10]
Epoch	Training Loss	Validation Loss
1	0.696421	0.335121
2	0.646020	0.305431
3	0.588352	0.289899
4	0.555712	0.272489
5	0.529050	0.275614
6	0.477198	0.262662
7	0.472562	0.260902
8	0.428397	0.251857
9	0.427706	0.250064
10	0.394769	0.251826
Generating predictions...
Starting inference on 2111 samples...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.96      0.98      0.97      1952
Unchecked Return Values For Low Level Calls       0.88      0.95      0.91      1180
                          Denial of Service       0.86      0.88      0.87       985
                          Time manipulation       0.77      0.81      0.79       668
                                 Reentrancy       0.83      0.91      0.87       826

                                  micro avg       0.88      0.93      0.90      5611
                                  macro avg       0.86      0.91      0.88      5611
                               weighted avg       0.88      0.93      0.90      5611
                                samples avg       0.88      0.90      0.88      5611

Results for before_optimized:
  Train Samples: 8444, Test Samples: 2111
  Train Time: 24.6 min
  Train Inference Time: 0.00s
  Test Inference Time: 16.06s
  Precision: 0.8834
  Recall: 0.9251
  F1: 0.9036
  Hamming Score: 0.8474
  Hamming Loss: 0.1054

============================================================
Training with column: optimized_80p
============================================================
Train: 8444, Test: 2111
GPT2ForSequenceClassification LOAD REPORT from: gpt2
Key          | Status  | 
-------------+---------+-
score.weight | MISSING | 

Notes:
- MISSING:	those params were newly initialized because missing from the checkpoint. Consider training on your downstream task.
Training...
 [4230/4230 24:06, Epoch 10/10]
Epoch	Training Loss	Validation Loss
1	0.782258	0.372598
2	0.694496	0.327428
3	0.617530	0.311203
4	0.564328	0.304183
5	0.532458	0.287743
6	0.517854	0.282604
7	0.481048	0.284591
8	0.467530	0.270248
9	0.438551	0.272004
10	0.403803	0.271590
Generating predictions...
Starting inference on 2111 samples...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.95      0.98      0.97      1952
Unchecked Return Values For Low Level Calls       0.89      0.94      0.91      1180
                          Denial of Service       0.87      0.85      0.86       985
                          Time manipulation       0.76      0.81      0.78       668
                                 Reentrancy       0.84      0.90      0.87       826

                                  micro avg       0.88      0.92      0.90      5611
                                  macro avg       0.86      0.90      0.88      5611
                               weighted avg       0.89      0.92      0.90      5611
                                samples avg       0.88      0.90      0.87      5611

Results for optimized_80p:
  Train Samples: 8444, Test Samples: 2111
  Train Time: 24.1 min
  Train Inference Time: 0.00s
  Test Inference Time: 14.80s
  Precision: 0.8852
  Recall: 0.9162
  F1: 0.9002
  Hamming Score: 0.8430
  Hamming Loss: 0.1082

============================================================
Training with column: optimized_50p
============================================================
Train: 8444, Test: 2111
GPT2ForSequenceClassification LOAD REPORT from: gpt2
Key          | Status  | 
-------------+---------+-
score.weight | MISSING | 

Notes:
- MISSING:	those params were newly initialized because missing from the checkpoint. Consider training on your downstream task.
Training...
 [4230/4230 23:26, Epoch 10/10]
Epoch	Training Loss	Validation Loss
1	0.799791	0.397959
2	0.739177	0.346550
3	0.659573	0.328950
4	0.610344	0.344907
5	0.587060	0.328537
6	0.580124	0.304334
7	0.543393	0.312251
8	0.526311	0.306871
9	0.516708	0.302070
10	0.476708	0.304146
Generating predictions...
Starting inference on 2111 samples...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.96      0.97      0.96      1952
Unchecked Return Values For Low Level Calls       0.89      0.91      0.90      1180
                          Denial of Service       0.88      0.82      0.85       985
                          Time manipulation       0.77      0.73      0.75       668
                                 Reentrancy       0.85      0.88      0.87       826

                                  micro avg       0.89      0.89      0.89      5611
                                  macro avg       0.87      0.86      0.86      5611
                               weighted avg       0.89      0.89      0.89      5611
                                samples avg       0.88      0.87      0.86      5611

Results for optimized_50p:
  Train Samples: 8444, Test Samples: 2111
  Train Time: 23.4 min
  Train Inference Time: 0.00s
  Test Inference Time: 14.06s
  Precision: 0.8900
  Recall: 0.8897
  F1: 0.8895
  Hamming Score: 0.8323
  Hamming Loss: 0.1165

============================================================
Training with column: optimized_20p
============================================================
Train: 8444, Test: 2111
GPT2ForSequenceClassification LOAD REPORT from: gpt2
Key          | Status  | 
-------------+---------+-
score.weight | MISSING | 

Notes:
- MISSING:	those params were newly initialized because missing from the checkpoint. Consider training on your downstream task.
Training...
 [4230/4230 22:44, Epoch 10/10]
Epoch	Training Loss	Validation Loss
1	0.908648	0.461804
2	0.810340	0.433736
3	0.738409	0.383285
4	0.700781	0.363508
5	0.673343	0.364920
6	0.680864	0.352013
7	0.628432	0.352441
8	0.619969	0.352997
9	0.593311	0.345672
10	0.591532	0.345497
Generating predictions...
Starting inference on 2111 samples...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.95      0.99      0.97      1952
Unchecked Return Values For Low Level Calls       0.84      0.87      0.86      1180
                          Denial of Service       0.87      0.81      0.84       985
                          Time manipulation       0.65      0.66      0.65       668
                                 Reentrancy       0.78      0.83      0.80       826

                                  micro avg       0.85      0.87      0.86      5611
                                  macro avg       0.82      0.83      0.82      5611
                               weighted avg       0.85      0.87      0.86      5611
                                samples avg       0.85      0.86      0.84      5611

Results for optimized_20p:
  Train Samples: 8444, Test Samples: 2111
  Train Time: 22.7 min
  Train Inference Time: 0.00s
  Test Inference Time: 13.37s
  Precision: 0.8509
  Recall: 0.8706
  F1: 0.8603
  Hamming Score: 0.7966
  Hamming Loss: 0.1500

Total training time: 96.1 minutes
