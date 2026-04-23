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
 [4230/4230 59:29, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.426100	0.414919	0.818052	0.827510	0.815841	0.733156	0.197276	25.426600	66.427000	2.084000
2	0.360700	0.364601	0.823750	0.878269	0.849902	0.776821	0.166726	25.427900	66.423000	2.084000
3	0.342900	0.336151	0.834433	0.886399	0.859409	0.784527	0.157726	25.453100	66.357000	2.082000
4	0.310500	0.316458	0.862415	0.872336	0.866784	0.793556	0.143754	25.410900	66.468000	2.086000
5	0.286600	0.311797	0.882218	0.854757	0.866800	0.800138	0.136886	25.456700	66.348000	2.082000
6	0.276000	0.314567	0.853670	0.909470	0.880240	0.814673	0.134991	25.455100	66.352000	2.082000
7	0.252600	0.300224	0.874192	0.887717	0.880563	0.819814	0.128478	25.488300	66.266000	2.079000
8	0.225100	0.298888	0.874012	0.910569	0.891834	0.831981	0.119834	25.477100	66.295000	2.080000
9	0.221600	0.299797	0.880157	0.896067	0.887895	0.828508	0.122439	25.479900	66.287000	2.080000
10	0.205100	0.296011	0.882704	0.901121	0.891779	0.834458	0.117940	25.483800	66.277000	2.080000
Evaluating on eval split...
Evaluating on held-out test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.96      0.98      0.97      1952
Unchecked Return Values For Low Level Calls       0.87      0.91      0.89      1180
                          Denial of Service       0.88      0.87      0.87       985
                          Time manipulation       0.74      0.74      0.74       668
                                 Reentrancy       0.84      0.87      0.85       826

                                  micro avg       0.88      0.90      0.89      5611
                                  macro avg       0.86      0.87      0.86      5611
                               weighted avg       0.88      0.90      0.89      5611
                                samples avg       0.88      0.88      0.86      5611

Model saved to: /kaggle/working/output/before_optimized

Results for before_optimized:
  Train Samples      : 8444
  Test Samples       : 2111
  Train Time         : 59.5 min
  Train Infer. Time  : 31.83s
  Test Infer. Time   : 25.46s
  Precision          : 0.8827
  Recall             : 0.9011
  F1                 : 0.8918
  Hamming Score      : 0.8345
  Hamming Loss       : 0.1179

============================================================
Training with column: optimized_80p
============================================================
[START] No checkpoint found — training from scratch.
Train: 8444, Test: 2111
Some weights of BertForSequenceClassification were not initialized from the model checkpoint at bert-base-uncased and are newly initialized: ['classifier.bias', 'classifier.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Training...
 [4230/4230 59:52, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.407100	0.398789	0.877473	0.744837	0.797202	0.721107	0.186264	25.506200	66.219000	2.078000
2	0.359900	0.348014	0.862219	0.840773	0.850122	0.777482	0.152872	25.531700	66.153000	2.076000
3	0.336500	0.340129	0.859978	0.854097	0.856059	0.785327	0.150148	25.526900	66.165000	2.076000
4	0.301600	0.314992	0.869942	0.876083	0.872643	0.806444	0.135346	25.514100	66.199000	2.077000
5	0.292800	0.300863	0.885096	0.865423	0.873146	0.811230	0.129426	25.508500	66.213000	2.078000
6	0.253800	0.295994	0.890658	0.864979	0.875952	0.811614	0.126584	25.506400	66.219000	2.078000
7	0.249400	0.286377	0.889209	0.883633	0.886001	0.821906	0.120308	25.513100	66.201000	2.077000
8	0.219800	0.287300	0.892990	0.885188	0.888533	0.828380	0.116992	25.520900	66.181000	2.077000
9	0.216700	0.282660	0.886847	0.903842	0.895113	0.837123	0.113203	25.519300	66.185000	2.077000
10	0.192800	0.282644	0.891228	0.897846	0.894391	0.834212	0.112611	25.538400	66.136000	2.075000
Evaluating on eval split...
Evaluating on held-out test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.97      0.97      0.97      1952
Unchecked Return Values For Low Level Calls       0.89      0.91      0.90      1180
                          Denial of Service       0.90      0.83      0.87       985
                          Time manipulation       0.76      0.70      0.73       668
                                 Reentrancy       0.85      0.88      0.86       826

                                  micro avg       0.90      0.89      0.89      5611
                                  macro avg       0.87      0.86      0.87      5611
                               weighted avg       0.90      0.89      0.89      5611
                                samples avg       0.89      0.87      0.86      5611

Model saved to: /kaggle/working/output/optimized_80p

Results for optimized_80p:
  Train Samples      : 8444
  Test Samples       : 2111
  Train Time         : 59.9 min
  Train Infer. Time  : 31.87s
  Test Infer. Time   : 25.52s
  Precision          : 0.8912
  Recall             : 0.8978
  F1                 : 0.8944
  Hamming Score      : 0.8342
  Hamming Loss       : 0.1126

============================================================
Training with column: optimized_50p
============================================================
[START] No checkpoint found — training from scratch.
Train: 8444, Test: 2111
Some weights of BertForSequenceClassification were not initialized from the model checkpoint at bert-base-uncased and are newly initialized: ['classifier.bias', 'classifier.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Training...
 [4230/4230 1:00:04, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.378500	0.364214	0.823449	0.873862	0.847092	0.759651	0.165423	25.524400	66.172000	2.076000
2	0.351600	0.338247	0.874590	0.842771	0.856097	0.783314	0.145530	25.528400	66.162000	2.076000
3	0.318200	0.304034	0.859068	0.889851	0.873765	0.805042	0.136294	25.548400	66.110000	2.074000
4	0.286900	0.292697	0.878318	0.874528	0.876023	0.808901	0.130136	25.547800	66.111000	2.075000
5	0.273100	0.284482	0.895843	0.859871	0.876538	0.813361	0.126347	25.555300	66.092000	2.074000
6	0.242100	0.278357	0.899040	0.868976	0.882426	0.820170	0.119953	25.552100	66.100000	2.074000
7	0.228300	0.269402	0.903329	0.879858	0.891045	0.826840	0.113203	25.559200	66.082000	2.074000
8	0.204700	0.269844	0.902377	0.884299	0.892836	0.833748	0.111782	25.584800	66.016000	2.072000
9	0.192000	0.274632	0.891382	0.904508	0.897745	0.838928	0.110243	25.572100	66.048000	2.073000
10	0.177500	0.270181	0.902010	0.896736	0.899252	0.841573	0.106690	25.571000	66.052000	2.073000
Evaluating on eval split...
Evaluating on held-out test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.96      0.98      0.97      1952
Unchecked Return Values For Low Level Calls       0.91      0.90      0.91      1180
                          Denial of Service       0.88      0.86      0.87       985
                          Time manipulation       0.80      0.75      0.78       668
                                 Reentrancy       0.88      0.87      0.87       826

                                  micro avg       0.91      0.90      0.90      5611
                                  macro avg       0.89      0.87      0.88      5611
                               weighted avg       0.90      0.90      0.90      5611
                                samples avg       0.89      0.88      0.87      5611

Model saved to: /kaggle/working/output/optimized_50p

Results for optimized_50p:
  Train Samples      : 8444
  Test Samples       : 2111
  Train Time         : 60.1 min
  Train Infer. Time  : 31.94s
  Test Infer. Time   : 25.55s
  Precision          : 0.9020
  Recall             : 0.8967
  F1                 : 0.8993
  Hamming Score      : 0.8416
  Hamming Loss       : 0.1067

============================================================
Training with column: optimized_20p
============================================================
[START] No checkpoint found — training from scratch.
Train: 8444, Test: 2111
Some weights of BertForSequenceClassification were not initialized from the model checkpoint at bert-base-uncased and are newly initialized: ['classifier.bias', 'classifier.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Training...
 [4230/4230 57:43, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.382700	0.355183	0.842454	0.864757	0.852643	0.774294	0.156898	24.393600	69.239000	2.173000
2	0.338100	0.319307	0.862750	0.876305	0.868673	0.800780	0.138780	24.399100	69.224000	2.172000
3	0.318000	0.319924	0.887087	0.853875	0.869100	0.798017	0.134399	24.399500	69.223000	2.172000
4	0.279100	0.303181	0.892507	0.855874	0.872940	0.803059	0.131202	24.406600	69.203000	2.172000
5	0.268100	0.281401	0.899427	0.874972	0.886586	0.822795	0.118176	24.393500	69.240000	2.173000
6	0.236900	0.273988	0.897995	0.884077	0.890801	0.828261	0.114506	24.383100	69.269000	2.174000
7	0.222300	0.280598	0.905134	0.881190	0.891931	0.830008	0.113677	24.393000	69.241000	2.173000
8	0.197400	0.272874	0.908586	0.889851	0.898791	0.839392	0.106098	24.405900	69.205000	2.172000
9	0.183500	0.274906	0.901200	0.895847	0.898071	0.837211	0.109059	24.412700	69.185000	2.171000
10	0.168100	0.274698	0.905442	0.893182	0.898867	0.837369	0.107401	24.415200	69.178000	2.171000
Evaluating on eval split...
Evaluating on held-out test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.96      0.97      0.97      1952
Unchecked Return Values For Low Level Calls       0.91      0.88      0.89      1180
                          Denial of Service       0.91      0.84      0.87       985
                          Time manipulation       0.78      0.79      0.78       668
                                 Reentrancy       0.86      0.84      0.85       826

                                  micro avg       0.91      0.89      0.90      5611
                                  macro avg       0.88      0.87      0.87      5611
                               weighted avg       0.91      0.89      0.90      5611
                                samples avg       0.88      0.87      0.86      5611

Model saved to: /kaggle/working/output/optimized_20p

Results for optimized_20p:
  Train Samples      : 8444
  Test Samples       : 2111
  Train Time         : 57.7 min
  Train Infer. Time  : 29.19s
  Test Infer. Time   : 24.41s
  Precision          : 0.9054
  Recall             : 0.8932
  F1                 : 0.8989
  Hamming Score      : 0.8374
  Hamming Loss       : 0.1074

Total training time: 244.4 minutes


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
 [4230/4230 29:51, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.404700	0.418306	0.829976	0.788886	0.805060	0.722153	0.192066	12.833200	131.612000	4.130000
2	0.370300	0.363747	0.837063	0.842669	0.837336	0.761703	0.168502	12.859000	131.347000	4.122000
3	0.342200	0.343586	0.841993	0.868779	0.855014	0.781932	0.154766	12.851500	131.424000	4.124000
4	0.323000	0.334986	0.869415	0.837536	0.850024	0.776367	0.150622	12.863500	131.301000	4.120000
5	0.300300	0.326666	0.874278	0.839991	0.855035	0.789017	0.146240	12.872800	131.207000	4.117000
6	0.291600	0.317286	0.871771	0.865655	0.867305	0.797770	0.137241	12.878400	131.150000	4.115000
7	0.270100	0.308940	0.872235	0.876813	0.873342	0.806335	0.132386	12.874300	131.192000	4.117000
8	0.251300	0.301169	0.879594	0.868779	0.873725	0.803049	0.131557	12.863700	131.300000	4.120000
9	0.228500	0.305057	0.870765	0.886409	0.878176	0.812236	0.129307	12.867800	131.258000	4.119000
10	0.226900	0.303714	0.874573	0.880607	0.876883	0.808062	0.129781	12.878100	131.153000	4.116000
Evaluating on eval split...
Evaluating on held-out test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.96      0.98      0.97      1952
Unchecked Return Values For Low Level Calls       0.87      0.91      0.89      1180
                          Denial of Service       0.89      0.82      0.86       985
                          Time manipulation       0.78      0.70      0.73       668
                                 Reentrancy       0.82      0.87      0.84       826

                                  micro avg       0.89      0.89      0.89      5611
                                  macro avg       0.86      0.86      0.86      5611
                               weighted avg       0.89      0.89      0.89      5611
                                samples avg       0.88      0.87      0.86      5611

Model saved to: /kaggle/working/output/before_optimized

Results for before_optimized:
  Train Samples      : 8444
  Test Samples       : 2111
  Train Time         : 29.9 min
  Train Infer. Time  : 16.07s
  Test Infer. Time   : 12.86s
  Precision          : 0.8746
  Recall             : 0.8806
  F1                 : 0.8769
  Hamming Score      : 0.8081
  Hamming Loss       : 0.1298

============================================================
Training with column: optimized_80p
============================================================
[START] No checkpoint found — training from scratch.
Train: 8444, Test: 2111
Some weights of DistilBertForSequenceClassification were not initialized from the model checkpoint at distilbert-base-uncased and are newly initialized: ['classifier.bias', 'classifier.weight', 'pre_classifier.bias', 'pre_classifier.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Training...
 [4230/4230 29:59, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.406500	0.415882	0.884181	0.701310	0.768899	0.694622	0.202013	12.862500	131.312000	4.121000
2	0.353300	0.350441	0.869592	0.819232	0.840158	0.768591	0.156898	12.874400	131.190000	4.117000
3	0.339500	0.336864	0.867144	0.848767	0.857433	0.781962	0.148372	12.873300	131.201000	4.117000
4	0.306900	0.316706	0.862387	0.870975	0.865990	0.794819	0.142806	12.858100	131.357000	4.122000
5	0.295900	0.307567	0.885917	0.852765	0.866797	0.799290	0.134162	12.882100	131.112000	4.114000
6	0.266400	0.308960	0.888942	0.856540	0.870906	0.804253	0.131202	12.864600	131.291000	4.120000
7	0.266100	0.294337	0.887097	0.872085	0.878824	0.816341	0.125636	12.884000	131.093000	4.114000
8	0.244200	0.289277	0.880847	0.883189	0.880948	0.818009	0.124808	12.870700	131.228000	4.118000
9	0.242300	0.283340	0.876124	0.902065	0.888828	0.821749	0.120545	12.889900	131.033000	4.112000
10	0.217400	0.284868	0.885046	0.885632	0.885120	0.819607	0.121374	12.885800	131.075000	4.113000
Evaluating on eval split...
Evaluating on held-out test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.95      0.98      0.97      1952
Unchecked Return Values For Low Level Calls       0.88      0.90      0.89      1180
                          Denial of Service       0.90      0.83      0.86       985
                          Time manipulation       0.79      0.71      0.75       668
                                 Reentrancy       0.86      0.86      0.86       826

                                  micro avg       0.90      0.89      0.89      5611
                                  macro avg       0.88      0.86      0.87      5611
                               weighted avg       0.89      0.89      0.89      5611
                                samples avg       0.89      0.87      0.86      5611

Model saved to: /kaggle/working/output/optimized_80p

Results for optimized_80p:
  Train Samples      : 8444
  Test Samples       : 2111
  Train Time         : 30.0 min
  Train Infer. Time  : 16.08s
  Test Infer. Time   : 12.87s
  Precision          : 0.8850
  Recall             : 0.8856
  F1                 : 0.8851
  Hamming Score      : 0.8196
  Hamming Loss       : 0.1214

============================================================
Training with column: optimized_50p
============================================================
[START] No checkpoint found — training from scratch.
Train: 8444, Test: 2111
Some weights of DistilBertForSequenceClassification were not initialized from the model checkpoint at distilbert-base-uncased and are newly initialized: ['classifier.bias', 'classifier.weight', 'pre_classifier.bias', 'pre_classifier.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Training...
 [4230/4230 30:06, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.375100	0.364507	0.861545	0.816345	0.831824	0.762542	0.163173	12.888600	131.047000	4.112000
2	0.344700	0.336284	0.874533	0.832112	0.849060	0.780649	0.149793	12.857500	131.363000	4.122000
3	0.316700	0.307542	0.857572	0.896736	0.876458	0.809355	0.134636	12.876500	131.170000	4.116000
4	0.288200	0.287718	0.876326	0.880080	0.877684	0.809818	0.130373	12.884800	131.085000	4.113000
5	0.277100	0.276813	0.892725	0.869642	0.880276	0.814446	0.123505	12.898300	130.948000	4.109000
6	0.251200	0.276984	0.898543	0.869865	0.882252	0.818838	0.119479	12.893600	130.995000	4.111000
7	0.240700	0.266483	0.901925	0.883633	0.892223	0.829445	0.113203	12.899600	130.934000	4.109000
8	0.216900	0.264719	0.907422	0.882967	0.894345	0.831991	0.109295	12.888500	131.047000	4.112000
9	0.205300	0.261219	0.882416	0.915834	0.898553	0.837882	0.111190	12.898300	130.948000	4.109000
10	0.187900	0.258489	0.899029	0.900511	0.899685	0.839984	0.106809	12.888600	131.046000	4.112000
Evaluating on eval split...
Evaluating on held-out test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.96      0.98      0.97      1952
Unchecked Return Values For Low Level Calls       0.90      0.93      0.91      1180
                          Denial of Service       0.89      0.84      0.86       985
                          Time manipulation       0.78      0.73      0.75       668
                                 Reentrancy       0.87      0.89      0.88       826

                                  micro avg       0.90      0.90      0.90      5611
                                  macro avg       0.88      0.87      0.88      5611
                               weighted avg       0.90      0.90      0.90      5611
                                samples avg       0.89      0.88      0.87      5611

Model saved to: /kaggle/working/output/optimized_50p

Results for optimized_50p:
  Train Samples      : 8444
  Test Samples       : 2111
  Train Time         : 30.1 min
  Train Infer. Time  : 16.09s
  Test Infer. Time   : 12.88s
  Precision          : 0.8990
  Recall             : 0.9005
  F1                 : 0.8997
  Hamming Score      : 0.8400
  Hamming Loss       : 0.1068

============================================================
Training with column: optimized_20p
============================================================
[START] No checkpoint found — training from scratch.
Train: 8444, Test: 2111
Some weights of DistilBertForSequenceClassification were not initialized from the model checkpoint at distilbert-base-uncased and are newly initialized: ['classifier.bias', 'classifier.weight', 'pre_classifier.bias', 'pre_classifier.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Training...
 [4230/4230 28:58, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.392500	0.392216	0.860407	0.789252	0.819671	0.738405	0.177146	12.308000	137.228000	4.306000
2	0.346100	0.326770	0.856661	0.878303	0.866549	0.794425	0.142214	12.313800	137.163000	4.304000
3	0.321700	0.327121	0.884492	0.835221	0.857159	0.789303	0.143754	12.324300	137.047000	4.300000
4	0.286400	0.294513	0.875363	0.882079	0.878182	0.810933	0.130136	12.309700	137.209000	4.306000
5	0.280000	0.284566	0.884987	0.873196	0.878238	0.814664	0.126229	12.312900	137.174000	4.304000
6	0.260700	0.274993	0.891024	0.888963	0.889282	0.826041	0.115690	12.332800	136.951000	4.297000
7	0.245100	0.269250	0.892478	0.895181	0.893472	0.830087	0.113085	12.316300	137.135000	4.303000
8	0.226400	0.264429	0.900514	0.893626	0.896770	0.833333	0.108467	12.328900	136.995000	4.299000
9	0.207100	0.260812	0.892245	0.908283	0.900135	0.838889	0.107519	12.311000	137.195000	4.305000
10	0.199500	0.260691	0.897947	0.901399	0.899577	0.837971	0.106690	12.326600	137.021000	4.300000
Evaluating on eval split...
Evaluating on held-out test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.96      0.99      0.97      1952
Unchecked Return Values For Low Level Calls       0.90      0.88      0.89      1180
                          Denial of Service       0.87      0.86      0.87       985
                          Time manipulation       0.82      0.77      0.79       668
                                 Reentrancy       0.87      0.83      0.85       826

                                  micro avg       0.90      0.89      0.90      5611
                                  macro avg       0.88      0.87      0.87      5611
                               weighted avg       0.90      0.89      0.90      5611
                                samples avg       0.89      0.88      0.86      5611

Model saved to: /kaggle/working/output/optimized_20p

Results for optimized_20p:
  Train Samples      : 8444
  Test Samples       : 2111
  Train Time         : 29.0 min
  Train Infer. Time  : 14.76s
  Test Infer. Time   : 12.31s
  Precision          : 0.8979
  Recall             : 0.9014
  F1                 : 0.8996
  Hamming Score      : 0.8380
  Hamming Loss       : 0.1067

Total training time: 123.0 minutes

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
 [4230/4230 59:53, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.385300	0.364342	0.848122	0.846847	0.845574	0.773357	0.159858	25.542900	66.124000	2.075000
2	0.331100	0.320681	0.865482	0.871171	0.867763	0.799270	0.139136	25.547300	66.113000	2.075000
3	0.299900	0.299311	0.864450	0.896171	0.879701	0.815897	0.130136	25.570100	66.054000	2.073000
4	0.276100	0.295584	0.892487	0.868468	0.878867	0.815946	0.124216	25.562600	66.073000	2.073000
5	0.245600	0.290449	0.909461	0.860586	0.882952	0.823821	0.116637	25.571500	66.050000	2.073000
6	0.225000	0.276442	0.901032	0.890090	0.895234	0.835327	0.109295	25.612100	65.945000	2.069000
7	0.196600	0.278328	0.906603	0.881757	0.892690	0.837330	0.108230	25.613100	65.943000	2.069000
8	0.188300	0.277370	0.908332	0.886036	0.896625	0.843093	0.105980	25.610900	65.949000	2.069000
9	0.169800	0.279760	0.907249	0.890315	0.898125	0.843793	0.104440	25.615100	65.938000	2.069000
10	0.149000	0.278280	0.908083	0.893919	0.900699	0.846783	0.102427	25.585000	66.015000	2.072000
Evaluating on eval split...
Evaluating on held-out test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.97      0.98      0.98      1952
Unchecked Return Values For Low Level Calls       0.91      0.91      0.91      1180
                          Denial of Service       0.91      0.86      0.89       985
                          Time manipulation       0.79      0.74      0.76       668
                                 Reentrancy       0.88      0.88      0.88       826

                                  micro avg       0.91      0.90      0.91      5611
                                  macro avg       0.89      0.87      0.88      5611
                               weighted avg       0.91      0.90      0.91      5611
                                samples avg       0.90      0.88      0.88      5611

Model saved to: /kaggle/working/output/before_optimized

Results for before_optimized:
  Train Samples      : 8444
  Test Samples       : 2111
  Train Time         : 59.9 min
  Train Infer. Time  : 31.98s
  Test Infer. Time   : 25.65s
  Precision          : 0.9081
  Recall             : 0.8939
  F1                 : 0.9007
  Hamming Score      : 0.8468
  Hamming Loss       : 0.1024

============================================================
Training with column: optimized_80p
============================================================
[START] No checkpoint found — training from scratch.
Train: 8444, Test: 2111
Some weights of RobertaForSequenceClassification were not initialized from the model checkpoint at microsoft/codebert-base and are newly initialized: ['classifier.dense.bias', 'classifier.dense.weight', 'classifier.out_proj.bias', 'classifier.out_proj.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Training...
 [4230/4230 1:00:21, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.363500	0.341331	0.859013	0.852987	0.855279	0.777423	0.152753	25.617000	65.933000	2.069000
2	0.325000	0.315597	0.862369	0.868532	0.864914	0.795204	0.141978	25.614300	65.940000	2.069000
3	0.298400	0.296713	0.871464	0.893404	0.882144	0.817663	0.127531	25.629600	65.900000	2.068000
4	0.262500	0.285267	0.882374	0.890073	0.885974	0.824285	0.121255	25.634000	65.889000	2.068000
5	0.242600	0.280224	0.881308	0.898956	0.889282	0.833452	0.117466	25.625000	65.912000	2.068000
6	0.215400	0.285726	0.887045	0.903620	0.894184	0.836323	0.111901	25.615400	65.937000	2.069000
7	0.196900	0.278335	0.904574	0.892294	0.897658	0.842471	0.106572	25.619200	65.927000	2.069000
8	0.170100	0.277346	0.901603	0.908505	0.904483	0.851648	0.101243	25.637000	65.881000	2.067000
9	0.151500	0.299560	0.883667	0.930713	0.906216	0.852921	0.103256	25.636700	65.882000	2.067000
10	0.137600	0.285792	0.895799	0.921830	0.908526	0.858891	0.098875	25.637000	65.881000	2.067000
Evaluating on eval split...
Evaluating on held-out test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.97      0.98      0.98      1952
Unchecked Return Values For Low Level Calls       0.88      0.93      0.91      1180
                          Denial of Service       0.91      0.88      0.89       985
                          Time manipulation       0.80      0.78      0.79       668
                                 Reentrancy       0.86      0.91      0.88       826

                                  micro avg       0.90      0.92      0.91      5611
                                  macro avg       0.88      0.89      0.89      5611
                               weighted avg       0.90      0.92      0.91      5611
                                samples avg       0.90      0.90      0.88      5611

Model saved to: /kaggle/working/output/optimized_80p

Results for optimized_80p:
  Train Samples      : 8444
  Test Samples       : 2111
  Train Time         : 60.4 min
  Train Infer. Time  : 32.04s
  Test Infer. Time   : 25.63s
  Precision          : 0.8958
  Recall             : 0.9218
  F1                 : 0.9085
  Hamming Score      : 0.8589
  Hamming Loss       : 0.0989

============================================================
Training with column: optimized_50p
============================================================
[START] No checkpoint found — training from scratch.
Train: 8444, Test: 2111
Some weights of RobertaForSequenceClassification were not initialized from the model checkpoint at microsoft/codebert-base and are newly initialized: ['classifier.dense.bias', 'classifier.dense.weight', 'classifier.out_proj.bias', 'classifier.out_proj.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Training...
 [4230/4230 1:00:37, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.345900	0.341997	0.816891	0.931823	0.867669	0.794040	0.157608	25.626200	65.909000	2.068000
2	0.304800	0.286175	0.882792	0.888075	0.885080	0.818502	0.122084	25.633100	65.891000	2.068000
3	0.279400	0.292058	0.869800	0.918721	0.893333	0.829949	0.118295	25.684200	65.760000	2.064000
4	0.237600	0.267129	0.911300	0.879636	0.893913	0.833422	0.109295	25.648300	65.852000	2.066000
5	0.215100	0.271086	0.894158	0.904286	0.898776	0.845204	0.107282	25.640000	65.874000	2.067000
6	0.193200	0.263805	0.915105	0.896069	0.904618	0.849743	0.098638	25.652800	65.841000	2.066000
7	0.169300	0.272273	0.914748	0.899178	0.906647	0.855901	0.098165	25.655800	65.833000	2.066000
8	0.146300	0.271992	0.915633	0.903176	0.908958	0.859897	0.095086	25.669900	65.797000	2.065000
9	0.132900	0.268527	0.913754	0.913835	0.913623	0.863134	0.091533	25.663000	65.815000	2.065000
10	0.115200	0.268341	0.916452	0.911837	0.914043	0.864446	0.090823	25.685700	65.756000	2.063000
Evaluating on eval split...
Evaluating on held-out test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.97      0.98      0.97      1952
Unchecked Return Values For Low Level Calls       0.92      0.93      0.93      1180
                          Denial of Service       0.90      0.90      0.90       985
                          Time manipulation       0.82      0.76      0.79       668
                                 Reentrancy       0.89      0.91      0.90       826

                                  micro avg       0.92      0.92      0.92      5611
                                  macro avg       0.90      0.90      0.90      5611
                               weighted avg       0.92      0.92      0.92      5611
                                samples avg       0.91      0.90      0.89      5611

Model saved to: /kaggle/working/output/optimized_50p

Results for optimized_50p:
  Train Samples      : 8444
  Test Samples       : 2111
  Train Time         : 60.6 min
  Train Infer. Time  : 32.09s
  Test Infer. Time   : 25.71s
  Precision          : 0.9165
  Recall             : 0.9118
  F1                 : 0.9140
  Hamming Score      : 0.8644
  Hamming Loss       : 0.0908

============================================================
Training with column: optimized_20p
============================================================
[START] No checkpoint found — training from scratch.
Train: 8444, Test: 2111
Some weights of RobertaForSequenceClassification were not initialized from the model checkpoint at microsoft/codebert-base and are newly initialized: ['classifier.dense.bias', 'classifier.dense.weight', 'classifier.out_proj.bias', 'classifier.out_proj.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Training...
 [4230/4230 33:23, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.374600	0.346284	0.837221	0.895181	0.864970	0.788997	0.148964	14.315800	117.982000	3.702000
2	0.325600	0.316068	0.857614	0.894515	0.875115	0.808141	0.135346	14.317100	117.970000	3.702000
3	0.304200	0.301264	0.867059	0.893849	0.879970	0.813341	0.131083	14.339700	117.785000	3.696000
4	0.265400	0.281631	0.872475	0.904730	0.887433	0.820851	0.123623	14.331000	117.856000	3.698000
5	0.247700	0.276968	0.882453	0.893404	0.887660	0.822933	0.120189	14.336600	117.810000	3.697000
6	0.217200	0.276620	0.885235	0.902065	0.893116	0.833452	0.114269	14.335600	117.819000	3.697000
7	0.202400	0.275503	0.899123	0.894293	0.896257	0.835938	0.110243	14.341900	117.767000	3.695000
8	0.179500	0.274507	0.895317	0.909616	0.902334	0.845244	0.105033	14.333700	117.834000	3.698000
9	0.166600	0.278741	0.893057	0.911837	0.902128	0.844148	0.106098	14.354000	117.668000	3.692000
10	0.151800	0.278780	0.894120	0.906951	0.900409	0.841168	0.107164	14.346700	117.727000	3.694000
Evaluating on eval split...
Evaluating on held-out test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.97      0.97      0.97      1952
Unchecked Return Values For Low Level Calls       0.90      0.91      0.90      1180
                          Denial of Service       0.88      0.87      0.88       985
                          Time manipulation       0.78      0.82      0.80       668
                                 Reentrancy       0.87      0.89      0.88       826

                                  micro avg       0.90      0.91      0.91      5611
                                  macro avg       0.88      0.89      0.88      5611
                               weighted avg       0.90      0.91      0.91      5611
                                samples avg       0.88      0.89      0.87      5611

Model saved to: /kaggle/working/output/optimized_20p

Results for optimized_20p:
  Train Samples      : 8444
  Test Samples       : 2111
  Train Time         : 33.4 min
  Train Infer. Time  : 17.71s
  Test Infer. Time   : 14.35s
  Precision          : 0.8941
  Recall             : 0.9070
  F1                 : 0.9004
  Hamming Score      : 0.8412
  Hamming Loss       : 0.1072

Total training time: 220.6 minutes

# GPT-2

============================================================
STEP 4: Run All Experiments
============================================================

============================================================
Training with column: before_optimized
============================================================
[RESUME] Found checkpoint: /kaggle/working/output/before_optimized/checkpoint-4230
Train: 8444, Test: 2111
GPT2ForSequenceClassification LOAD REPORT from: gpt2
Key          | Status  | 
-------------+---------+-
score.weight | MISSING | 

Notes:
- MISSING:	those params were newly initialized because missing from the checkpoint. Consider training on your downstream task.
Training...
 [4230/4230 : < :, Epoch 10/10]
Epoch	Training Loss	Validation Loss
Generating predictions...
Starting inference on 2111 samples...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.96      0.99      0.97      1952
Unchecked Return Values For Low Level Calls       0.90      0.94      0.92      1180
                          Denial of Service       0.89      0.86      0.88       985
                          Time manipulation       0.76      0.78      0.77       668
                                 Reentrancy       0.85      0.92      0.89       826

                                  micro avg       0.89      0.92      0.91      5611
                                  macro avg       0.87      0.90      0.88      5611
                               weighted avg       0.90      0.92      0.91      5611
                                samples avg       0.90      0.90      0.88      5611

Model saved to: /kaggle/working/output/before_optimized

Results for before_optimized:
  Train Samples: 8444, Test Samples: 2111
  Train Time: 0.8 min
  Test Inference Time: 14.83s
  Precision: 0.8950
  Recall: 0.9203
  F1: 0.9073
  Hamming Score: 0.8569
  Hamming Loss: 0.0998

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
 [4230/4230 22:33, Epoch 10/10]
Epoch	Training Loss	Validation Loss
1	0.738711	0.345578
2	0.630591	0.314678
3	0.599389	0.282400
4	0.535378	0.269700
5	0.527659	0.258341
6	0.474285	0.265525
7	0.432423	0.259703
8	0.378979	0.259552
9	0.394970	0.250584
10	0.378773	0.257281
Generating predictions...
Starting inference on 2111 samples...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.96      0.98      0.97      1952
Unchecked Return Values For Low Level Calls       0.88      0.95      0.92      1180
                          Denial of Service       0.89      0.85      0.87       985
                          Time manipulation       0.79      0.83      0.81       668
                                 Reentrancy       0.83      0.93      0.88       826

                                  micro avg       0.89      0.92      0.91      5611
                                  macro avg       0.87      0.91      0.89      5611
                               weighted avg       0.89      0.92      0.91      5611
                                samples avg       0.89      0.90      0.88      5611

Model saved to: /kaggle/working/output/optimized_80p

Results for optimized_80p:
  Train Samples: 8444, Test Samples: 2111
  Train Time: 22.6 min
  Test Inference Time: 14.06s
  Precision: 0.8912
  Recall: 0.9241
  F1: 0.9067
  Hamming Score: 0.8516
  Hamming Loss: 0.1011

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
 [4230/4230 22:06, Epoch 10/10]
Epoch	Training Loss	Validation Loss
1	0.769335	0.372047
2	0.688934	0.310238
3	0.598216	0.304433
4	0.566169	0.280342
5	0.520723	0.275732
6	0.508039	0.276694
7	0.465783	0.274908
8	0.464200	0.263127
9	0.431542	0.256996
10	0.388553	0.258355
Generating predictions...
Starting inference on 2111 samples...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.94      0.99      0.96      1952
Unchecked Return Values For Low Level Calls       0.91      0.94      0.92      1180
                          Denial of Service       0.85      0.85      0.85       985
                          Time manipulation       0.79      0.78      0.79       668
                                 Reentrancy       0.87      0.92      0.89       826

                                  micro avg       0.89      0.92      0.90      5611
                                  macro avg       0.87      0.90      0.88      5611
                               weighted avg       0.89      0.92      0.90      5611
                                samples avg       0.89      0.90      0.88      5611

Model saved to: /kaggle/working/output/optimized_50p

Results for optimized_50p:
  Train Samples: 8444, Test Samples: 2111
  Train Time: 22.1 min
  Test Inference Time: 13.33s
  Precision: 0.8882
  Recall: 0.9191
  F1: 0.9032
  Hamming Score: 0.8489
  Hamming Loss: 0.1039

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
 [4230/4230 21:33, Epoch 10/10]
Epoch	Training Loss	Validation Loss
1	0.858209	0.385915
2	0.752393	0.356316
3	0.660483	0.349222
4	0.636829	0.328358
5	0.594740	0.339456
6	0.601837	0.326702
7	0.552338	0.312409
8	0.535281	0.307521
9	0.505882	0.307835
10	0.489779	0.305347
Generating predictions...
Starting inference on 2111 samples...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.94      0.99      0.97      1952
Unchecked Return Values For Low Level Calls       0.88      0.89      0.89      1180
                          Denial of Service       0.86      0.84      0.85       985
                          Time manipulation       0.76      0.76      0.76       668
                                 Reentrancy       0.82      0.84      0.83       826

                                  micro avg       0.88      0.89      0.88      5611
                                  macro avg       0.85      0.86      0.86      5611
                               weighted avg       0.87      0.89      0.88      5611
                                samples avg       0.87      0.87      0.85      5611

Model saved to: /kaggle/working/output/optimized_20p

Results for optimized_20p:
  Train Samples: 8444, Test Samples: 2111
  Train Time: 21.6 min
  Test Inference Time: 12.65s
  Precision: 0.8746
  Recall: 0.8936
  F1: 0.8839
  Hamming Score: 0.8222
  Hamming Loss: 0.1240

Total training time: 68.8 minutes