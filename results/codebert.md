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
