# BERT

============================================================
STEP 4: Run All Experiments
============================================================

============================================================
Training with column: before_optimized
============================================================
[START] No checkpoint found — training from scratch.
Train: 8444, Test: 2111
Some weights of BertForSequenceClassification were not initialized from the model checkpoint at bert-base-uncased and are newly initialized: ['classifier.bias', 'classifier.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Training...
 [4230/4230 59:23, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.432100	0.419368	0.823866	0.806975	0.809471	0.725903	0.192303	25.283500	66.802000	2.096000
2	0.385000	0.386715	0.830404	0.842729	0.834332	0.755960	0.176554	25.274600	66.826000	2.097000
3	0.359500	0.361287	0.849024	0.844703	0.845686	0.771630	0.161634	25.305700	66.744000	2.094000
4	0.342600	0.347653	0.846294	0.868392	0.856745	0.783057	0.156069	25.321300	66.703000	2.093000
5	0.316800	0.347940	0.866807	0.838342	0.851826	0.780116	0.155003	25.309000	66.735000	2.094000
6	0.296500	0.344255	0.855443	0.850844	0.852117	0.777867	0.155950	25.322100	66.701000	2.093000
7	0.276600	0.343245	0.858501	0.856109	0.856797	0.787951	0.151687	25.299700	66.760000	2.095000
8	0.267600	0.349490	0.870259	0.851064	0.860133	0.789392	0.146951	25.328300	66.684000	2.093000
9	0.242000	0.348995	0.862050	0.858960	0.859851	0.793172	0.148609	25.330600	66.678000	2.092000
10	0.232200	0.352184	0.865841	0.850844	0.857758	0.790349	0.149674	25.322000	66.701000	2.093000
Evaluating on eval split...
Evaluating on held-out test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.96      0.97      0.97      1952
Unchecked Return Values For Low Level Calls       0.86      0.85      0.86      1180
                          Denial of Service       0.88      0.78      0.83       985
                          Time manipulation       0.68      0.62      0.65       668
                                 Reentrancy       0.80      0.81      0.81       826

                                  micro avg       0.87      0.85      0.86      5611
                                  macro avg       0.84      0.81      0.82      5611
                               weighted avg       0.87      0.85      0.86      5611
                                samples avg       0.87      0.84      0.84      5611

Model saved to: /kaggle/working/output/before_optimized

Results for before_optimized:
  Train Samples      : 8444
  Test Samples       : 2111
  Train Time         : 59.4 min
  Train Infer. Time  : 31.63s
  Test Infer. Time   : 25.32s
  Precision          : 0.8658
  Recall             : 0.8508
  F1                 : 0.8578
  Hamming Score      : 0.7903
  Hamming Loss       : 0.1497

============================================================
Training with column: optimized_80p
============================================================
[START] No checkpoint found — training from scratch.
Train: 8444, Test: 2111
Some weights of BertForSequenceClassification were not initialized from the model checkpoint at bert-base-uncased and are newly initialized: ['classifier.bias', 'classifier.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Training...
 [4230/4230 59:48, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.450600	0.431056	0.813949	0.812569	0.809018	0.728715	0.191948	25.358600	66.605000	2.090000
2	0.403700	0.417057	0.847822	0.771264	0.802713	0.729278	0.187922	25.368500	66.579000	2.089000
3	0.380900	0.380283	0.848469	0.798357	0.818126	0.747967	0.178330	25.367800	66.580000	2.089000
4	0.348700	0.363849	0.844619	0.829447	0.835559	0.765946	0.167792	25.380600	66.547000	2.088000
5	0.343200	0.346688	0.861676	0.812347	0.831576	0.764664	0.163766	25.364500	66.589000	2.090000
6	0.314700	0.364510	0.865661	0.804797	0.830196	0.763677	0.164831	25.367200	66.582000	2.089000
7	0.298600	0.352440	0.855893	0.848990	0.851796	0.778242	0.155477	25.349300	66.629000	2.091000
8	0.274000	0.355307	0.866149	0.836553	0.850227	0.775163	0.154411	25.358400	66.605000	2.090000
9	0.265000	0.355044	0.857878	0.853209	0.855369	0.782110	0.152872	25.391900	66.517000	2.087000
10	0.247000	0.357259	0.862471	0.842549	0.852135	0.779347	0.153937	25.371700	66.570000	2.089000
Evaluating on eval split...
Evaluating on held-out test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.96      0.97      0.97      1952
Unchecked Return Values For Low Level Calls       0.84      0.86      0.85      1180
                          Denial of Service       0.87      0.79      0.83       985
                          Time manipulation       0.67      0.58      0.62       668
                                 Reentrancy       0.80      0.79      0.80       826

                                  micro avg       0.87      0.84      0.85      5611
                                  macro avg       0.83      0.80      0.81      5611
                               weighted avg       0.86      0.84      0.85      5611
                                samples avg       0.86      0.84      0.83      5611

Model saved to: /kaggle/working/output/optimized_80p

Results for optimized_80p:
  Train Samples      : 8444
  Test Samples       : 2111
  Train Time         : 59.8 min
  Train Infer. Time  : 31.68s
  Test Infer. Time   : 25.38s
  Precision          : 0.8625
  Recall             : 0.8425
  F1                 : 0.8521
  Hamming Score      : 0.7793
  Hamming Loss       : 0.1539

============================================================
Training with column: optimized_50p
============================================================
[START] No checkpoint found — training from scratch.
Train: 8444, Test: 2111
Some weights of BertForSequenceClassification were not initialized from the model checkpoint at bert-base-uncased and are newly initialized: ['classifier.bias', 'classifier.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Training...
 [4230/4230 1:00:02, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.433400	0.415447	0.813684	0.806351	0.808271	0.720831	0.196092	25.379000	66.551000	2.088000
2	0.392700	0.382264	0.828048	0.846325	0.836036	0.757766	0.173120	25.399100	66.498000	2.087000
3	0.372900	0.360511	0.846507	0.828337	0.835782	0.763292	0.167318	25.415100	66.456000	2.085000
4	0.336000	0.348240	0.836830	0.869198	0.852157	0.776416	0.159858	25.384800	66.536000	2.088000
5	0.327600	0.343173	0.860207	0.825894	0.839141	0.774097	0.159858	25.388400	66.526000	2.088000
6	0.302700	0.347718	0.863927	0.833222	0.847356	0.778863	0.156187	25.419500	66.445000	2.085000
7	0.289500	0.345754	0.878030	0.818121	0.844901	0.777196	0.153819	25.401400	66.492000	2.087000
8	0.263600	0.346653	0.871277	0.833222	0.850944	0.782129	0.152279	25.405500	66.482000	2.086000
9	0.254900	0.346013	0.861319	0.852099	0.856508	0.785563	0.152398	25.404500	66.484000	2.086000
10	0.238000	0.346861	0.863056	0.850100	0.856461	0.786817	0.151095	25.402300	66.490000	2.086000
Evaluating on eval split...
Evaluating on held-out test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.96      0.97      0.97      1952
Unchecked Return Values For Low Level Calls       0.85      0.86      0.85      1180
                          Denial of Service       0.85      0.79      0.82       985
                          Time manipulation       0.70      0.62      0.66       668
                                 Reentrancy       0.80      0.81      0.80       826

                                  micro avg       0.87      0.85      0.86      5611
                                  macro avg       0.83      0.81      0.82      5611
                               weighted avg       0.86      0.85      0.86      5611
                                samples avg       0.86      0.84      0.83      5611

Model saved to: /kaggle/working/output/optimized_50p

Results for optimized_50p:
  Train Samples      : 8444
  Test Samples       : 2111
  Train Time         : 60.1 min
  Train Infer. Time  : 31.74s
  Test Infer. Time   : 25.41s
  Precision          : 0.8631
  Recall             : 0.8501
  F1                 : 0.8565
  Hamming Score      : 0.7868
  Hamming Loss       : 0.1511

============================================================
Training with column: optimized_20p
============================================================
[START] No checkpoint found — training from scratch.
Train: 8444, Test: 2111
Some weights of BertForSequenceClassification were not initialized from the model checkpoint at bert-base-uncased and are newly initialized: ['classifier.bias', 'classifier.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Training...
 [4230/4230 48:27, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.422200	0.426295	0.832768	0.741062	0.772636	0.689017	0.211960	20.437100	82.644000	2.593000
2	0.391900	0.387197	0.827740	0.839662	0.833181	0.748530	0.176199	20.387600	82.845000	2.600000
3	0.374700	0.370653	0.836918	0.825006	0.829621	0.746783	0.174778	20.483900	82.455000	2.587000
4	0.338700	0.366317	0.835541	0.852765	0.843992	0.761220	0.166844	20.464800	82.532000	2.590000
5	0.336400	0.360779	0.849368	0.831002	0.838070	0.762877	0.164239	20.460800	82.548000	2.590000
6	0.307500	0.365950	0.825733	0.871419	0.847885	0.767190	0.166963	20.472600	82.501000	2.589000
7	0.294700	0.372333	0.854439	0.828559	0.840460	0.764141	0.163410	20.494100	82.414000	2.586000
8	0.266500	0.379609	0.852135	0.832778	0.841241	0.766598	0.163292	20.458000	82.559000	2.591000
9	0.262900	0.383337	0.836100	0.863202	0.849327	0.770564	0.163529	20.458400	82.558000	2.591000
10	0.235800	0.384449	0.845166	0.852987	0.848934	0.772064	0.160568	20.475800	82.488000	2.588000
Evaluating on eval split...
Evaluating on held-out test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.95      0.98      0.96      1952
Unchecked Return Values For Low Level Calls       0.83      0.87      0.85      1180
                          Denial of Service       0.83      0.77      0.80       985
                          Time manipulation       0.71      0.65      0.68       668
                                 Reentrancy       0.78      0.81      0.80       826

                                  micro avg       0.85      0.86      0.86      5611
                                  macro avg       0.82      0.82      0.82      5611
                               weighted avg       0.85      0.86      0.85      5611
                                samples avg       0.85      0.85      0.82      5611

Model saved to: /kaggle/working/output/optimized_20p

Results for optimized_20p:
  Train Samples      : 8444
  Test Samples       : 2111
  Train Time         : 48.5 min
  Train Infer. Time  : 26.36s
  Test Infer. Time   : 20.47s
  Precision          : 0.8452
  Recall             : 0.8530
  F1                 : 0.8489
  Hamming Score      : 0.7721
  Hamming Loss       : 0.1606

Total training time: 234.6 minutes

# DistilBERT

============================================================
STEP 4: Run All Experiments
============================================================

============================================================
Training with column: before_optimized
============================================================
[START] No checkpoint found — training from scratch.
Train: 8444, Test: 2111
Some weights of DistilBertForSequenceClassification were not initialized from the model checkpoint at distilbert-base-uncased and are newly initialized: ['classifier.bias', 'classifier.weight', 'pre_classifier.bias', 'pre_classifier.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Training...
 [4230/4230 29:53, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.422200	0.396990	0.832016	0.817840	0.820527	0.746892	0.180462	12.908000	130.850000	4.106000
2	0.379400	0.383979	0.848548	0.815184	0.828207	0.762098	0.170752	12.913500	130.793000	4.104000
3	0.371400	0.358247	0.854722	0.826693	0.837963	0.771048	0.164002	12.892700	131.005000	4.111000
4	0.348300	0.359428	0.867770	0.802346	0.830967	0.763440	0.166015	12.869200	131.243000	4.118000
5	0.322600	0.355761	0.828008	0.880035	0.851673	0.775863	0.165660	12.894500	130.986000	4.110000
6	0.313100	0.345266	0.860109	0.835547	0.846933	0.778626	0.157726	12.871200	131.224000	4.118000
7	0.293000	0.339757	0.864461	0.831563	0.846242	0.780304	0.156424	12.907900	130.850000	4.106000
8	0.286500	0.343004	0.849770	0.858566	0.853504	0.785248	0.156069	12.903100	130.899000	4.108000
9	0.280400	0.343629	0.851308	0.856352	0.853374	0.784271	0.155950	12.908600	130.843000	4.106000
10	0.264500	0.344686	0.855981	0.847942	0.851607	0.784054	0.156306	12.882700	131.106000	4.114000
Evaluating on eval split...
Evaluating on held-out test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.96      0.98      0.97      1952
Unchecked Return Values For Low Level Calls       0.86      0.87      0.86      1180
                          Denial of Service       0.86      0.77      0.81       985
                          Time manipulation       0.70      0.63      0.67       668
                                 Reentrancy       0.81      0.81      0.81       826

                                  micro avg       0.87      0.85      0.86      5611
                                  macro avg       0.84      0.81      0.82      5611
                               weighted avg       0.87      0.85      0.86      5611
                                samples avg       0.87      0.85      0.84      5611

Model saved to: /kaggle/working/output/before_optimized

Results for before_optimized:
  Train Samples      : 8444
  Test Samples       : 2111
  Train Time         : 29.9 min
  Train Infer. Time  : 16.13s
  Test Infer. Time   : 12.89s
  Precision          : 0.8560
  Recall             : 0.8479
  F1                 : 0.8516
  Hamming Score      : 0.7841
  Hamming Loss       : 0.1563

============================================================
Training with column: optimized_80p
============================================================
[START] No checkpoint found — training from scratch.
Train: 8444, Test: 2111
Some weights of DistilBertForSequenceClassification were not initialized from the model checkpoint at distilbert-base-uncased and are newly initialized: ['classifier.bias', 'classifier.weight', 'pre_classifier.bias', 'pre_classifier.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Training...
 [4230/4230 30:00, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.449700	0.432124	0.828680	0.767932	0.790360	0.709424	0.201658	12.920500	130.722000	4.102000
2	0.398400	0.390102	0.830459	0.827893	0.827002	0.752743	0.176791	12.905600	130.874000	4.107000
3	0.377100	0.365286	0.838258	0.839662	0.837070	0.769509	0.168147	12.924600	130.681000	4.101000
4	0.344600	0.364240	0.847827	0.829891	0.836702	0.769193	0.165305	12.936400	130.562000	4.097000
5	0.340600	0.344904	0.842401	0.851654	0.842649	0.779445	0.161160	12.922400	130.703000	4.101000
6	0.311700	0.346984	0.864747	0.827226	0.842407	0.778774	0.155832	12.944800	130.477000	4.094000
7	0.304500	0.336922	0.851307	0.859427	0.854410	0.786521	0.153464	12.940000	130.525000	4.096000
8	0.277400	0.342993	0.848489	0.858761	0.852363	0.787932	0.155240	12.935200	130.574000	4.097000
9	0.273900	0.341801	0.839735	0.879192	0.858648	0.788534	0.155358	12.914200	130.786000	4.104000
10	0.260000	0.342406	0.849104	0.867866	0.857739	0.791356	0.151687	12.929500	130.632000	4.099000
Evaluating on eval split...
Evaluating on held-out test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.96      0.98      0.97      1952
Unchecked Return Values For Low Level Calls       0.83      0.89      0.86      1180
                          Denial of Service       0.87      0.77      0.82       985
                          Time manipulation       0.69      0.59      0.64       668
                                 Reentrancy       0.78      0.83      0.81       826

                                  micro avg       0.86      0.86      0.86      5611
                                  macro avg       0.83      0.81      0.82      5611
                               weighted avg       0.86      0.86      0.86      5611
                                samples avg       0.86      0.85      0.83      5611

Model saved to: /kaggle/working/output/optimized_80p

Results for optimized_80p:
  Train Samples      : 8444
  Test Samples       : 2111
  Train Time         : 30.0 min
  Train Infer. Time  : 16.18s
  Test Infer. Time   : 12.94s
  Precision          : 0.8491
  Recall             : 0.8679
  F1                 : 0.8577
  Hamming Score      : 0.7914
  Hamming Loss       : 0.1517

============================================================
Training with column: optimized_50p
============================================================
[START] No checkpoint found — training from scratch.
Train: 8444, Test: 2111
Some weights of DistilBertForSequenceClassification were not initialized from the model checkpoint at distilbert-base-uncased and are newly initialized: ['classifier.bias', 'classifier.weight', 'pre_classifier.bias', 'pre_classifier.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Training...
 [4230/4230 30:07, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.435100	0.410503	0.819542	0.814568	0.814649	0.733037	0.192066	12.952000	130.405000	4.092000
2	0.384200	0.372475	0.840664	0.828115	0.832498	0.760124	0.170397	12.949500	130.430000	4.093000
3	0.361900	0.353796	0.838962	0.857650	0.847955	0.773722	0.162581	12.946100	130.464000	4.094000
4	0.325100	0.349813	0.840901	0.866755	0.853456	0.781251	0.157608	12.953500	130.390000	4.092000
5	0.321700	0.342266	0.851410	0.842771	0.845701	0.774077	0.159503	12.966700	130.257000	4.087000
6	0.300000	0.346306	0.867369	0.833222	0.848296	0.780896	0.152872	12.954200	130.382000	4.091000
7	0.286200	0.348991	0.862879	0.839440	0.849762	0.780422	0.153582	12.968600	130.238000	4.087000
8	0.269500	0.347027	0.855329	0.862980	0.858581	0.786955	0.150385	12.952500	130.400000	4.092000
9	0.264900	0.355465	0.843040	0.882745	0.861759	0.789836	0.152516	12.948200	130.443000	4.093000
10	0.242900	0.351721	0.852013	0.864757	0.858090	0.786896	0.151451	12.950800	130.417000	4.092000
Evaluating on eval split...
Evaluating on held-out test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.95      0.98      0.97      1952
Unchecked Return Values For Low Level Calls       0.84      0.88      0.86      1180
                          Denial of Service       0.86      0.77      0.82       985
                          Time manipulation       0.71      0.63      0.67       668
                                 Reentrancy       0.78      0.81      0.79       826

                                  micro avg       0.86      0.86      0.86      5611
                                  macro avg       0.83      0.81      0.82      5611
                               weighted avg       0.86      0.86      0.86      5611
                                samples avg       0.86      0.85      0.83      5611

Model saved to: /kaggle/working/output/optimized_50p

Results for optimized_50p:
  Train Samples      : 8444
  Test Samples       : 2111
  Train Time         : 30.1 min
  Train Infer. Time  : 16.17s
  Test Infer. Time   : 12.94s
  Precision          : 0.8520
  Recall             : 0.8648
  F1                 : 0.8581
  Hamming Score      : 0.7869
  Hamming Loss       : 0.1515

============================================================
Training with column: optimized_20p
============================================================
[START] No checkpoint found — training from scratch.
Train: 8444, Test: 2111
Some weights of DistilBertForSequenceClassification were not initialized from the model checkpoint at distilbert-base-uncased and are newly initialized: ['classifier.bias', 'classifier.weight', 'pre_classifier.bias', 'pre_classifier.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Training...
 [4230/4230 24:21, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.428900	0.458421	0.846140	0.722407	0.763679	0.680166	0.214920	10.401400	162.383000	5.095000
2	0.390100	0.381595	0.823377	0.848767	0.835423	0.751135	0.175133	10.417900	162.125000	5.087000
3	0.367200	0.368052	0.849327	0.813902	0.829657	0.747425	0.171936	10.407500	162.286000	5.092000
4	0.345400	0.362668	0.853842	0.828781	0.840063	0.760874	0.163292	10.435100	161.858000	5.079000
5	0.341500	0.358416	0.845732	0.837442	0.840048	0.763953	0.164594	10.418100	162.121000	5.087000
6	0.311200	0.361619	0.850198	0.838774	0.843438	0.764407	0.161634	10.415000	162.170000	5.089000
7	0.309900	0.368482	0.851659	0.830557	0.839475	0.761012	0.163884	10.425100	162.014000	5.084000
8	0.280800	0.369545	0.855052	0.833222	0.842747	0.764792	0.161042	10.421200	162.074000	5.086000
9	0.278200	0.368188	0.843727	0.859871	0.851427	0.770969	0.159029	10.424500	162.021000	5.084000
10	0.254300	0.372936	0.849070	0.843882	0.845637	0.767634	0.160568	10.433000	161.890000	5.080000
Evaluating on eval split...
Evaluating on held-out test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.95      0.99      0.97      1952
Unchecked Return Values For Low Level Calls       0.83      0.87      0.85      1180
                          Denial of Service       0.83      0.75      0.79       985
                          Time manipulation       0.71      0.63      0.67       668
                                 Reentrancy       0.79      0.81      0.80       826

                                  micro avg       0.85      0.85      0.85      5611
                                  macro avg       0.82      0.81      0.81      5611
                               weighted avg       0.85      0.85      0.85      5611
                                samples avg       0.85      0.84      0.82      5611

Model saved to: /kaggle/working/output/optimized_20p

Results for optimized_20p:
  Train Samples      : 8444
  Test Samples       : 2111
  Train Time         : 24.4 min
  Train Infer. Time  : 13.43s
  Test Infer. Time   : 10.41s
  Precision          : 0.8491
  Recall             : 0.8439
  F1                 : 0.8456
  Hamming Score      : 0.7676
  Hamming Loss       : 0.1606

Total training time: 118.4 minutes

# CodeBERT

============================================================
STEP 4: Run All Experiments
============================================================

============================================================
Training with column: before_optimized
============================================================
[START] No checkpoint found — training from scratch.
Train: 8444, Test: 2111
Some weights of RobertaForSequenceClassification were not initialized from the model checkpoint at microsoft/codebert-base and are newly initialized: ['classifier.dense.bias', 'classifier.dense.weight', 'classifier.out_proj.bias', 'classifier.out_proj.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Training...
 [4230/4230 59:40, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.397200	0.366292	0.829983	0.858520	0.843650	0.770722	0.165779	25.611000	65.948000	2.069000
2	0.339100	0.330679	0.839035	0.878027	0.857630	0.783679	0.153582	25.581900	66.023000	2.072000
3	0.312300	0.324343	0.872293	0.850448	0.859487	0.793033	0.142570	25.589600	66.003000	2.071000
4	0.275100	0.325123	0.826340	0.925785	0.872200	0.804283	0.147188	25.600500	65.975000	2.070000
5	0.260300	0.340556	0.842585	0.914798	0.874217	0.806424	0.142451	25.606400	65.960000	2.070000
6	0.214500	0.323657	0.886163	0.834753	0.856554	0.797444	0.140438	25.613300	65.942000	2.069000
7	0.204300	0.321967	0.870140	0.881390	0.875509	0.815512	0.131912	25.606900	65.959000	2.070000
8	0.179300	0.330046	0.880971	0.872646	0.876424	0.815098	0.128242	25.614500	65.939000	2.069000
9	0.166600	0.329311	0.874273	0.881614	0.877865	0.816973	0.129307	25.506200	66.219000	2.078000
10	0.149200	0.336995	0.882497	0.870852	0.876493	0.816292	0.128597	25.611300	65.947000	2.069000
Evaluating on eval split...
Evaluating on held-out test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.97      0.97      0.97      1952
Unchecked Return Values For Low Level Calls       0.87      0.86      0.87      1180
                          Denial of Service       0.88      0.86      0.87       985
                          Time manipulation       0.77      0.71      0.74       668
                                 Reentrancy       0.85      0.80      0.82       826

                                  micro avg       0.89      0.87      0.88      5611
                                  macro avg       0.87      0.84      0.85      5611
                               weighted avg       0.89      0.87      0.88      5611
                                samples avg       0.89      0.86      0.86      5611

Model saved to: /kaggle/working/output/before_optimized

Results for before_optimized:
  Train Samples      : 8444
  Test Samples       : 2111
  Train Time         : 59.7 min
  Train Infer. Time  : 31.89s
  Test Infer. Time   : 25.50s
  Precision          : 0.8825
  Recall             : 0.8709
  F1                 : 0.8765
  Hamming Score      : 0.8163
  Hamming Loss       : 0.1286

============================================================
Training with column: optimized_80p
============================================================
[START] No checkpoint found — training from scratch.
Train: 8444, Test: 2111
Some weights of RobertaForSequenceClassification were not initialized from the model checkpoint at microsoft/codebert-base and are newly initialized: ['classifier.dense.bias', 'classifier.dense.weight', 'classifier.out_proj.bias', 'classifier.out_proj.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Training...
 [4230/4230 1:00:05, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.382700	0.400695	0.862100	0.785476	0.816479	0.746152	0.178449	25.633200	65.891000	2.068000
2	0.353700	0.357503	0.867875	0.819676	0.840353	0.770485	0.158319	25.644700	65.862000	2.067000
3	0.325200	0.321447	0.849582	0.877193	0.862655	0.793862	0.146832	25.633500	65.890000	2.068000
4	0.298600	0.316562	0.877599	0.858539	0.867046	0.798135	0.136412	25.654300	65.837000	2.066000
5	0.293200	0.307711	0.888965	0.850544	0.865858	0.803562	0.132978	25.560400	66.079000	2.074000
6	0.260200	0.319645	0.896048	0.839885	0.862200	0.799447	0.134517	25.551700	66.101000	2.074000
7	0.244200	0.326244	0.890045	0.837664	0.860568	0.797454	0.138070	25.590400	66.001000	2.071000
8	0.216400	0.331796	0.899896	0.825450	0.858013	0.792599	0.138662	25.582000	66.023000	2.072000
9	0.198700	0.320131	0.873160	0.875194	0.873971	0.807865	0.133570	25.563400	66.071000	2.073000
10	0.181700	0.325383	0.883020	0.869865	0.875726	0.812345	0.128715	25.596600	65.985000	2.071000
Evaluating on eval split...
Evaluating on held-out test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.96      0.98      0.97      1952
Unchecked Return Values For Low Level Calls       0.88      0.86      0.87      1180
                          Denial of Service       0.88      0.80      0.84       985
                          Time manipulation       0.76      0.61      0.68       668
                                 Reentrancy       0.84      0.78      0.81       826

                                  micro avg       0.89      0.85      0.87      5611
                                  macro avg       0.87      0.81      0.83      5611
                               weighted avg       0.89      0.85      0.87      5611
                                samples avg       0.89      0.85      0.84      5611

Model saved to: /kaggle/working/output/optimized_80p

Results for optimized_80p:
  Train Samples      : 8444
  Test Samples       : 2111
  Train Time         : 60.1 min
  Train Infer. Time  : 31.95s
  Test Infer. Time   : 25.56s
  Precision          : 0.8830
  Recall             : 0.8699
  F1                 : 0.8757
  Hamming Score      : 0.8123
  Hamming Loss       : 0.1287

============================================================
Training with column: optimized_50p
============================================================
[START] No checkpoint found — training from scratch.
Train: 8444, Test: 2111
Some weights of RobertaForSequenceClassification were not initialized from the model checkpoint at microsoft/codebert-base and are newly initialized: ['classifier.dense.bias', 'classifier.dense.weight', 'classifier.out_proj.bias', 'classifier.out_proj.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Training...
 [4230/4230 1:00:19, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.390400	0.387193	0.853696	0.795470	0.813607	0.734656	0.182238	25.573300	66.046000	2.072000
2	0.349200	0.354266	0.885776	0.803020	0.839707	0.764249	0.156661	25.551600	66.102000	2.074000
3	0.324300	0.308717	0.865807	0.878748	0.871850	0.799803	0.138307	25.570900	66.052000	2.073000
4	0.290100	0.307205	0.888252	0.848101	0.866690	0.801569	0.135820	25.572300	66.048000	2.073000
5	0.277700	0.309740	0.889050	0.849878	0.868111	0.801263	0.134399	25.567200	66.061000	2.073000
6	0.239700	0.300675	0.886410	0.869865	0.877654	0.813993	0.127294	25.574500	66.042000	2.072000
7	0.231000	0.303706	0.900138	0.858983	0.878091	0.815700	0.124334	25.569600	66.055000	2.073000
8	0.211600	0.325857	0.905245	0.841883	0.871080	0.807608	0.129189	25.566400	66.063000	2.073000
9	0.196500	0.311694	0.880242	0.888519	0.884078	0.820259	0.124097	25.592000	65.997000	2.071000
10	0.170300	0.316580	0.885693	0.881190	0.883144	0.819726	0.123268	25.569600	66.055000	2.073000
Evaluating on eval split...
Evaluating on held-out test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.96      0.97      0.97      1952
Unchecked Return Values For Low Level Calls       0.89      0.90      0.89      1180
                          Denial of Service       0.89      0.80      0.84       985
                          Time manipulation       0.74      0.71      0.72       668
                                 Reentrancy       0.83      0.85      0.84       826

                                  micro avg       0.89      0.88      0.88      5611
                                  macro avg       0.86      0.85      0.85      5611
                               weighted avg       0.89      0.88      0.88      5611
                                samples avg       0.88      0.86      0.85      5611

Model saved to: /kaggle/working/output/optimized_50p

Results for optimized_50p:
  Train Samples      : 8444
  Test Samples       : 2111
  Train Time         : 60.3 min
  Train Infer. Time  : 31.93s
  Test Infer. Time   : 25.55s
  Precision          : 0.8857
  Recall             : 0.8812
  F1                 : 0.8831
  Hamming Score      : 0.8197
  Hamming Loss       : 0.1233

============================================================
Training with column: optimized_20p
============================================================
[START] No checkpoint found — training from scratch.
Train: 8444, Test: 2111
Some weights of RobertaForSequenceClassification were not initialized from the model checkpoint at microsoft/codebert-base and are newly initialized: ['classifier.dense.bias', 'classifier.dense.weight', 'classifier.out_proj.bias', 'classifier.out_proj.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Training...
 [4230/4230 29:37, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.424900	0.489368	0.820266	0.718410	0.747882	0.645520	0.231972	12.657800	133.436000	4.187000
2	0.382600	0.395468	0.844153	0.821897	0.831696	0.743882	0.172883	12.658100	133.432000	4.187000
3	0.363800	0.359066	0.839085	0.843216	0.840564	0.763657	0.167555	12.680300	133.198000	4.180000
4	0.329900	0.353054	0.858072	0.833000	0.844163	0.770614	0.159147	12.666400	133.344000	4.184000
5	0.320700	0.359602	0.850968	0.847435	0.848325	0.771887	0.157845	12.679300	133.209000	4.180000
6	0.290100	0.350960	0.848569	0.865423	0.856393	0.780975	0.152398	12.662700	133.384000	4.186000
7	0.276100	0.353561	0.854221	0.858539	0.855997	0.780817	0.151806	12.672400	133.282000	4.182000
8	0.255400	0.369317	0.873523	0.831002	0.850604	0.777965	0.151451	12.663300	133.377000	4.185000
9	0.244900	0.373094	0.852792	0.856762	0.854309	0.777452	0.155121	12.677500	133.228000	4.181000
10	0.218600	0.378125	0.857109	0.853875	0.855255	0.779297	0.152872	12.673700	133.269000	4.182000
Evaluating on eval split...
Evaluating on held-out test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.96      0.98      0.97      1952
Unchecked Return Values For Low Level Calls       0.84      0.87      0.85      1180
                          Denial of Service       0.82      0.77      0.79       985
                          Time manipulation       0.71      0.68      0.69       668
                                 Reentrancy       0.80      0.81      0.80       826

                                  micro avg       0.86      0.86      0.86      5611
                                  macro avg       0.82      0.82      0.82      5611
                               weighted avg       0.85      0.86      0.86      5611
                                samples avg       0.85      0.84      0.82      5611

Model saved to: /kaggle/working/output/optimized_20p

Results for optimized_20p:
  Train Samples      : 8444
  Test Samples       : 2111
  Train Time         : 29.6 min
  Train Infer. Time  : 15.16s
  Test Infer. Time   : 12.62s
  Precision          : 0.8571
  Recall             : 0.8539
  F1                 : 0.8553
  Hamming Score      : 0.7793
  Hamming Loss       : 0.1529

Total training time: 215.9 minutes

# GPT-2

============================================================
STEP 4: Run All Experiments
============================================================

============================================================
Training with column: before_optimized
============================================================
[START] No checkpoint found — training from scratch.
Train: 8444, Test: 2111
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
GPT2ForSequenceClassification LOAD REPORT from: gpt2
Key          | Status  | 
-------------+---------+-
score.weight | MISSING | 

Notes:
- MISSING:	those params were newly initialized because missing from the checkpoint. Consider training on your downstream task.
Training...
 [4230/4230 24:17, Epoch 10/10]
Epoch	Training Loss	Validation Loss
1	0.748002	0.337464
2	0.632331	0.312934
3	0.602393	0.320658
4	0.555423	0.292715
5	0.524659	0.301622
6	0.494947	0.272048
7	0.467113	0.275506
8	0.435053	0.272489
9	0.425234	0.272734
10	0.417194	0.275091
Generating predictions...
Starting inference on 2111 samples...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.96      0.98      0.97      1952
Unchecked Return Values For Low Level Calls       0.89      0.93      0.91      1180
                          Denial of Service       0.86      0.86      0.86       985
                          Time manipulation       0.77      0.76      0.76       668
                                 Reentrancy       0.85      0.88      0.86       826

                                  micro avg       0.89      0.91      0.90      5611
                                  macro avg       0.86      0.88      0.87      5611
                               weighted avg       0.89      0.91      0.90      5611
                                samples avg       0.89      0.89      0.88      5611

Model saved to: /working/data/before_optimized

Results for before_optimized:
  Train Samples: 8444, Test Samples: 2111
  Train Time: 24.3 min
  Test Inference Time: 15.47s
  Precision: 0.8871
  Recall: 0.9059
  F1: 0.8963
  Hamming Score: 0.8408
  Hamming Loss: 0.1110

============================================================
Training with column: optimized_80p
============================================================
[START] No checkpoint found — training from scratch.
Train: 8444, Test: 2111
GPT2ForSequenceClassification LOAD REPORT from: gpt2
Key          | Status  | 
-------------+---------+-
score.weight | MISSING | 

Notes:
- MISSING:	those params were newly initialized because missing from the checkpoint. Consider training on your downstream task.
Training...
 [4230/4230 23:50, Epoch 10/10]
Epoch	Training Loss	Validation Loss
1	0.783075	0.377666
2	0.701683	0.334379
3	0.617700	0.301236
4	0.572747	0.310701
5	0.544417	0.292749
6	0.522806	0.288380
7	0.503885	0.290771
8	0.486659	0.294290
9	0.452759	0.284682
10	0.425936	0.284116
Generating predictions...
Starting inference on 2111 samples...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.96      0.98      0.97      1952
Unchecked Return Values For Low Level Calls       0.89      0.92      0.91      1180
                          Denial of Service       0.85      0.84      0.84       985
                          Time manipulation       0.73      0.79      0.76       668
                                 Reentrancy       0.83      0.92      0.87       826

                                  micro avg       0.88      0.91      0.89      5611
                                  macro avg       0.85      0.89      0.87      5611
                               weighted avg       0.88      0.91      0.89      5611
                                samples avg       0.87      0.89      0.87      5611

Model saved to: /working/data/optimized_80p

Results for optimized_80p:
  Train Samples: 8444, Test Samples: 2111
  Train Time: 23.8 min
  Test Inference Time: 14.73s
  Precision: 0.8768
  Recall: 0.9134
  F1: 0.8945
  Hamming Score: 0.8353
  Hamming Loss: 0.1152

============================================================
Training with column: optimized_50p
============================================================
[START] No checkpoint found — training from scratch.
Train: 8444, Test: 2111
GPT2ForSequenceClassification LOAD REPORT from: gpt2
Key          | Status  | 
-------------+---------+-
score.weight | MISSING | 

Notes:
- MISSING:	those params were newly initialized because missing from the checkpoint. Consider training on your downstream task.
Training...
 [4230/4230 23:15, Epoch 10/10]
Epoch	Training Loss	Validation Loss
1	0.826677	0.391177
2	0.746643	0.356050
3	0.675646	0.341563
4	0.646979	0.329268
5	0.613819	0.330079
6	0.583536	0.328542
7	0.556680	0.325857
8	0.551027	0.324809
9	0.513808	0.328455
10	0.496481	0.330011
Generating predictions...
Starting inference on 2111 samples...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.95      0.98      0.97      1952
Unchecked Return Values For Low Level Calls       0.86      0.93      0.89      1180
                          Denial of Service       0.83      0.83      0.83       985
                          Time manipulation       0.75      0.68      0.71       668
                                 Reentrancy       0.80      0.90      0.85       826

                                  micro avg       0.87      0.90      0.88      5611
                                  macro avg       0.84      0.86      0.85      5611
                               weighted avg       0.87      0.90      0.88      5611
                                samples avg       0.86      0.88      0.85      5611

Model saved to: /working/data/optimized_50p

Results for optimized_50p:
  Train Samples: 8444, Test Samples: 2111
  Train Time: 23.3 min
  Test Inference Time: 14.03s
  Precision: 0.8658
  Recall: 0.8961
  F1: 0.8800
  Hamming Score: 0.8163
  Hamming Loss: 0.1284

============================================================
Training with column: optimized_20p
============================================================
[START] No checkpoint found — training from scratch.
Train: 8444, Test: 2111
GPT2ForSequenceClassification LOAD REPORT from: gpt2
Key          | Status  | 
-------------+---------+-
score.weight | MISSING | 

Notes:
- MISSING:	those params were newly initialized because missing from the checkpoint. Consider training on your downstream task.
Training...
 [4230/4230 22:34, Epoch 10/10]
Epoch	Training Loss	Validation Loss
1	0.971650	0.451087
2	0.842093	0.418496
3	0.776067	0.384398
4	0.755149	0.368043
5	0.727917	0.362036
6	0.702682	0.362041
7	0.675313	0.360176
8	0.673705	0.358816
9	0.629608	0.352835
10	0.624774	0.352322
Generating predictions...
Starting inference on 2111 samples...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.94      0.99      0.96      1952
Unchecked Return Values For Low Level Calls       0.84      0.86      0.85      1180
                          Denial of Service       0.78      0.81      0.80       985
                          Time manipulation       0.69      0.66      0.68       668
                                 Reentrancy       0.78      0.83      0.80       826

                                  micro avg       0.84      0.87      0.85      5611
                                  macro avg       0.81      0.83      0.82      5611
                               weighted avg       0.84      0.87      0.85      5611
                                samples avg       0.84      0.86      0.82      5611

Model saved to: /working/data/optimized_20p

Results for optimized_20p:
  Train Samples: 8444, Test Samples: 2111
  Train Time: 22.6 min
  Test Inference Time: 13.22s
  Precision: 0.8381
  Recall: 0.8683
  F1: 0.8528
  Hamming Score: 0.7707
  Hamming Loss: 0.1582

Total training time: 95.4 minutes