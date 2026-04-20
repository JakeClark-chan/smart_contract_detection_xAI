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
