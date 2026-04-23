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
 [4230/4230 59:35, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.420500	0.435599	0.807455	0.799956	0.799804	0.706059	0.204381	25.502900	66.228000	2.078000
2	0.371300	0.376011	0.820495	0.854674	0.835721	0.758595	0.175252	25.500400	66.234000	2.078000
3	0.340600	0.355961	0.853943	0.823660	0.832226	0.761230	0.166371	25.468800	66.316000	2.081000
4	0.327900	0.345564	0.860788	0.841604	0.844800	0.783748	0.154056	25.505700	66.220000	2.078000
5	0.304100	0.327124	0.870117	0.844927	0.854877	0.789313	0.146714	25.525200	66.170000	2.076000
6	0.264000	0.334404	0.887378	0.831635	0.851030	0.791691	0.143754	25.517500	66.190000	2.077000
7	0.253200	0.326567	0.872197	0.864865	0.865581	0.800730	0.138899	25.540400	66.130000	2.075000
8	0.234200	0.319541	0.872087	0.873726	0.871463	0.810243	0.134873	25.532200	66.152000	2.076000
9	0.229100	0.320594	0.872317	0.870182	0.869973	0.808555	0.135465	25.557700	66.086000	2.074000
10	0.206300	0.321420	0.878671	0.870182	0.873038	0.812473	0.132031	25.527000	66.165000	2.076000
Evaluating on eval split...
Evaluating on held-out test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.96      0.98      0.97      1952
Unchecked Return Values For Low Level Calls       0.88      0.90      0.89      1180
                          Denial of Service       0.89      0.80      0.84       985
                          Time manipulation       0.76      0.63      0.69       668
                                 Reentrancy       0.83      0.87      0.85       826

                                  micro avg       0.89      0.87      0.88      5611
                                  macro avg       0.86      0.84      0.85      5611
                               weighted avg       0.89      0.87      0.88      5611
                                samples avg       0.89      0.87      0.86      5611

Model saved to: /kaggle/working/output/before_optimized

Results for before_optimized:
  Train Samples      : 8444
  Test Samples       : 2111
  Train Time         : 59.6 min
  Train Infer. Time  : 31.88s
  Test Infer. Time   : 25.54s
  Precision          : 0.8787
  Recall             : 0.8702
  F1                 : 0.8730
  Hamming Score      : 0.8125
  Hamming Loss       : 0.1320

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
1	0.413200	0.417516	0.852588	0.752387	0.788909	0.717249	0.197513	25.492700	66.254000	2.079000
2	0.372600	0.354285	0.857419	0.847213	0.851609	0.779337	0.153819	25.571800	66.049000	2.073000
3	0.343000	0.333960	0.840578	0.885188	0.860803	0.794444	0.150148	25.558700	66.083000	2.074000
4	0.318200	0.322386	0.868474	0.857873	0.862031	0.795125	0.142570	25.540300	66.131000	2.075000
5	0.301300	0.306458	0.877828	0.861426	0.866596	0.805121	0.134754	25.555800	66.091000	2.074000
6	0.274600	0.311146	0.880991	0.864313	0.870259	0.805664	0.132386	25.520600	66.182000	2.077000
7	0.257700	0.299790	0.877816	0.879636	0.878560	0.814022	0.128478	25.625200	65.912000	2.068000
8	0.237200	0.295404	0.885420	0.889407	0.887025	0.826998	0.119716	25.601300	65.973000	2.070000
9	0.227000	0.301871	0.874534	0.912503	0.892618	0.831794	0.119361	25.594100	65.992000	2.071000
10	0.205100	0.299302	0.885832	0.888519	0.887087	0.823712	0.119953	25.573300	66.045000	2.072000
Evaluating on eval split...
Evaluating on held-out test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.96      0.98      0.97      1952
Unchecked Return Values For Low Level Calls       0.88      0.90      0.89      1180
                          Denial of Service       0.89      0.84      0.87       985
                          Time manipulation       0.74      0.72      0.73       668
                                 Reentrancy       0.83      0.87      0.85       826

                                  micro avg       0.89      0.89      0.89      5611
                                  macro avg       0.86      0.86      0.86      5611
                               weighted avg       0.89      0.89      0.89      5611
                                samples avg       0.88      0.87      0.86      5611

Model saved to: /kaggle/working/output/optimized_80p

Results for optimized_80p:
  Train Samples      : 8444
  Test Samples       : 2111
  Train Time         : 59.9 min
  Train Infer. Time  : 31.98s
  Test Infer. Time   : 25.57s
  Precision          : 0.8858
  Recall             : 0.8885
  F1                 : 0.8871
  Hamming Score      : 0.8237
  Hamming Loss       : 0.1200

============================================================
Training with column: optimized_50p
============================================================
[START] No checkpoint found — training from scratch.
Train: 8444, Test: 2111
Some weights of BertForSequenceClassification were not initialized from the model checkpoint at bert-base-uncased and are newly initialized: ['classifier.bias', 'classifier.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Training...
 [4230/4230 1:00:06, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.379700	0.380004	0.846238	0.813458	0.826563	0.756157	0.175725	25.594100	65.992000	2.071000
2	0.352000	0.337141	0.854548	0.861204	0.857193	0.786274	0.151095	25.590100	66.002000	2.071000
3	0.330300	0.318386	0.847494	0.900511	0.872774	0.804963	0.141385	25.591900	65.997000	2.071000
4	0.294800	0.295928	0.867815	0.906951	0.886128	0.822499	0.126939	25.626700	65.908000	2.068000
5	0.287200	0.280969	0.880224	0.900511	0.889868	0.831143	0.117703	25.631400	65.896000	2.068000
6	0.251900	0.280387	0.876630	0.904508	0.889994	0.831192	0.118532	25.642300	65.868000	2.067000
7	0.237800	0.272985	0.887814	0.899622	0.893605	0.835810	0.114269	25.637200	65.881000	2.067000
8	0.209300	0.272604	0.892504	0.893404	0.892582	0.839303	0.113085	25.609000	65.953000	2.070000
9	0.204200	0.272466	0.888360	0.914279	0.901031	0.847434	0.107756	25.637900	65.879000	2.067000
10	0.182400	0.270136	0.891438	0.913169	0.902146	0.850030	0.105743	25.638600	65.877000	2.067000
Evaluating on eval split...
Evaluating on held-out test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.97      0.99      0.98      1952
Unchecked Return Values For Low Level Calls       0.89      0.91      0.90      1180
                          Denial of Service       0.89      0.87      0.88       985
                          Time manipulation       0.79      0.80      0.79       668
                                 Reentrancy       0.86      0.88      0.87       826

                                  micro avg       0.90      0.91      0.91      5611
                                  macro avg       0.88      0.89      0.88      5611
                               weighted avg       0.90      0.91      0.91      5611
                                samples avg       0.90      0.89      0.88      5611

Model saved to: /kaggle/working/output/optimized_50p

Results for optimized_50p:
  Train Samples      : 8444
  Test Samples       : 2111
  Train Time         : 60.1 min
  Train Infer. Time  : 31.93s
  Test Infer. Time   : 25.62s
  Precision          : 0.8914
  Recall             : 0.9132
  F1                 : 0.9021
  Hamming Score      : 0.8500
  Hamming Loss       : 0.1057

============================================================
Training with column: optimized_20p
============================================================
[START] No checkpoint found — training from scratch.
Train: 8444, Test: 2111
Some weights of BertForSequenceClassification were not initialized from the model checkpoint at bert-base-uncased and are newly initialized: ['classifier.bias', 'classifier.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Training...
 [4230/4230 47:47, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.365600	0.349321	0.849581	0.851877	0.849549	0.775972	0.160095	20.466300	82.526000	2.590000
2	0.325600	0.321807	0.855585	0.894071	0.874193	0.802220	0.138780	20.396700	82.808000	2.598000
3	0.301800	0.293701	0.868800	0.888963	0.878617	0.811121	0.130965	20.428000	82.680000	2.594000
4	0.271100	0.279786	0.873997	0.912059	0.891101	0.829781	0.121137	20.415400	82.732000	2.596000
5	0.261400	0.266027	0.894479	0.896291	0.895190	0.834883	0.110835	20.427100	82.684000	2.595000
6	0.230400	0.267805	0.888943	0.914057	0.900979	0.843981	0.106690	20.416700	82.727000	2.596000
7	0.211900	0.257894	0.904175	0.903842	0.903883	0.850484	0.102191	20.415500	82.731000	2.596000
8	0.184700	0.260476	0.919584	0.881412	0.899287	0.846467	0.103138	20.433200	82.660000	2.594000
9	0.170900	0.259373	0.905138	0.907173	0.905890	0.851500	0.100888	20.420000	82.713000	2.595000
10	0.155600	0.257952	0.910219	0.904730	0.907400	0.854825	0.097928	20.419300	82.716000	2.596000
Evaluating on eval split...
Evaluating on held-out test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.97      0.98      0.98      1952
Unchecked Return Values For Low Level Calls       0.91      0.93      0.92      1180
                          Denial of Service       0.91      0.85      0.88       985
                          Time manipulation       0.79      0.76      0.78       668
                                 Reentrancy       0.87      0.89      0.88       826

                                  micro avg       0.91      0.91      0.91      5611
                                  macro avg       0.89      0.88      0.89      5611
                               weighted avg       0.91      0.91      0.91      5611
                                samples avg       0.90      0.89      0.88      5611

Model saved to: /kaggle/working/output/optimized_20p

Results for optimized_20p:
  Train Samples      : 8444
  Test Samples       : 2111
  Train Time         : 47.8 min
  Train Infer. Time  : 25.25s
  Test Infer. Time   : 20.39s
  Precision          : 0.9102
  Recall             : 0.9047
  F1                 : 0.9074
  Hamming Score      : 0.8548
  Hamming Loss       : 0.0979

Total training time: 234.5 minutes


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
 [4230/4230 29:55, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.423100	0.404391	0.841683	0.802546	0.819035	0.742451	0.179988	12.897600	130.955000	4.109000
2	0.394500	0.375414	0.857535	0.826670	0.838604	0.772202	0.160450	12.886900	131.064000	4.113000
3	0.345900	0.353114	0.846068	0.848559	0.845179	0.780412	0.158082	12.890600	131.026000	4.112000
4	0.326600	0.328429	0.877891	0.834487	0.852310	0.788445	0.145175	12.886700	131.066000	4.113000
5	0.297300	0.324269	0.859051	0.869109	0.863450	0.800898	0.142806	12.892900	131.003000	4.111000
6	0.293200	0.314790	0.865816	0.869556	0.866094	0.803858	0.139491	12.905900	130.870000	4.107000
7	0.280700	0.313853	0.888979	0.846772	0.866197	0.804312	0.134754	12.883200	131.101000	4.114000
8	0.271700	0.311445	0.873726	0.869779	0.871369	0.809147	0.134162	12.897900	130.951000	4.109000
9	0.264500	0.309529	0.878876	0.867769	0.872660	0.812670	0.131794	12.892700	131.004000	4.111000
10	0.243500	0.309902	0.874635	0.876927	0.875534	0.815256	0.130965	12.909600	130.832000	4.105000
Evaluating on eval split...
Evaluating on held-out test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.96      0.98      0.97      1952
Unchecked Return Values For Low Level Calls       0.90      0.88      0.89      1180
                          Denial of Service       0.89      0.82      0.86       985
                          Time manipulation       0.75      0.68      0.71       668
                                 Reentrancy       0.84      0.83      0.84       826

                                  micro avg       0.89      0.87      0.88      5611
                                  macro avg       0.87      0.84      0.85      5611
                               weighted avg       0.89      0.87      0.88      5611
                                samples avg       0.88      0.86      0.85      5611

Model saved to: /kaggle/working/output/before_optimized

Results for before_optimized:
  Train Samples      : 8444
  Test Samples       : 2111
  Train Time         : 30.0 min
  Train Infer. Time  : 16.13s
  Test Infer. Time   : 12.90s
  Precision          : 0.8746
  Recall             : 0.8769
  F1                 : 0.8755
  Hamming Score      : 0.8153
  Hamming Loss       : 0.1310

============================================================
Training with column: optimized_80p
============================================================
[START] No checkpoint found — training from scratch.
Train: 8444, Test: 2111
Some weights of DistilBertForSequenceClassification were not initialized from the model checkpoint at distilbert-base-uncased and are newly initialized: ['classifier.bias', 'classifier.weight', 'pre_classifier.bias', 'pre_classifier.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Training...
 [4230/4230 30:02, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.415800	0.407486	0.867189	0.757939	0.802741	0.721354	0.185790	12.914700	130.781000	4.104000
2	0.371900	0.349784	0.861017	0.834555	0.846377	0.773525	0.156542	12.915200	130.776000	4.104000
3	0.350000	0.335904	0.843880	0.886520	0.863834	0.789540	0.149438	12.922000	130.707000	4.102000
4	0.317000	0.326535	0.874934	0.846103	0.856123	0.790063	0.144346	12.918800	130.740000	4.103000
5	0.305400	0.308448	0.887396	0.841883	0.861592	0.797089	0.137478	12.908300	130.846000	4.106000
6	0.279200	0.306491	0.888243	0.855208	0.869861	0.803927	0.131557	12.910000	130.828000	4.105000
7	0.264700	0.294356	0.888602	0.873418	0.879973	0.817130	0.124216	12.898100	130.949000	4.109000
8	0.249400	0.296005	0.897448	0.870309	0.882339	0.820456	0.120545	12.917900	130.749000	4.103000
9	0.240600	0.287654	0.886418	0.895847	0.890596	0.826653	0.117111	12.933000	130.596000	4.098000
10	0.228100	0.288119	0.893285	0.881412	0.886777	0.823604	0.118176	12.936900	130.557000	4.097000
Evaluating on eval split...
Evaluating on held-out test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.96      0.98      0.97      1952
Unchecked Return Values For Low Level Calls       0.90      0.91      0.90      1180
                          Denial of Service       0.91      0.80      0.85       985
                          Time manipulation       0.77      0.66      0.71       668
                                 Reentrancy       0.85      0.85      0.85       826

                                  micro avg       0.90      0.88      0.89      5611
                                  macro avg       0.88      0.84      0.86      5611
                               weighted avg       0.90      0.88      0.89      5611
                                samples avg       0.89      0.86      0.86      5611

Model saved to: /kaggle/working/output/optimized_80p

Results for optimized_80p:
  Train Samples      : 8444
  Test Samples       : 2111
  Train Time         : 30.1 min
  Train Infer. Time  : 16.13s
  Test Infer. Time   : 12.92s
  Precision          : 0.8933
  Recall             : 0.8814
  F1                 : 0.8868
  Hamming Score      : 0.8236
  Hamming Loss       : 0.1182

============================================================
Training with column: optimized_50p
============================================================
[START] No checkpoint found — training from scratch.
Train: 8444, Test: 2111
Some weights of DistilBertForSequenceClassification were not initialized from the model checkpoint at distilbert-base-uncased and are newly initialized: ['classifier.bias', 'classifier.weight', 'pre_classifier.bias', 'pre_classifier.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Training...
 [4230/4230 30:11, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.380600	0.367823	0.853164	0.827670	0.838367	0.763489	0.163884	12.932600	130.601000	4.098000
2	0.344100	0.330389	0.867840	0.848545	0.856889	0.786412	0.146477	12.935600	130.569000	4.097000
3	0.321900	0.306313	0.855820	0.900289	0.877441	0.812680	0.134517	12.932100	130.605000	4.098000
4	0.286000	0.289904	0.875084	0.898068	0.886061	0.827334	0.122676	12.936700	130.559000	4.097000
5	0.280300	0.276448	0.887827	0.895847	0.891497	0.830126	0.115690	12.939200	130.534000	4.096000
6	0.257100	0.270555	0.895121	0.893182	0.893160	0.835534	0.111190	12.939600	130.529000	4.096000
7	0.241200	0.268364	0.903938	0.878081	0.890205	0.831606	0.113203	12.940100	130.524000	4.096000
8	0.212900	0.266359	0.904878	0.887853	0.895830	0.839086	0.108230	12.947400	130.451000	4.093000
9	0.208000	0.259245	0.895415	0.909172	0.902003	0.845481	0.105151	12.925700	130.670000	4.100000
10	0.192900	0.259629	0.896734	0.907173	0.901808	0.845698	0.104914	12.924500	130.682000	4.101000
Evaluating on eval split...
Evaluating on held-out test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.97      0.99      0.98      1952
Unchecked Return Values For Low Level Calls       0.89      0.92      0.90      1180
                          Denial of Service       0.90      0.85      0.87       985
                          Time manipulation       0.82      0.76      0.79       668
                                 Reentrancy       0.85      0.88      0.86       826

                                  micro avg       0.91      0.91      0.91      5611
                                  macro avg       0.89      0.88      0.88      5611
                               weighted avg       0.90      0.91      0.90      5611
                                samples avg       0.89      0.88      0.87      5611

Model saved to: /kaggle/working/output/optimized_50p

Results for optimized_50p:
  Train Samples      : 8444
  Test Samples       : 2111
  Train Time         : 30.2 min
  Train Infer. Time  : 16.16s
  Test Infer. Time   : 12.93s
  Precision          : 0.8967
  Recall             : 0.9072
  F1                 : 0.9018
  Hamming Score      : 0.8457
  Hamming Loss       : 0.1049

============================================================
Training with column: optimized_20p
============================================================
[START] No checkpoint found — training from scratch.
Train: 8444, Test: 2111
Some weights of DistilBertForSequenceClassification were not initialized from the model checkpoint at distilbert-base-uncased and are newly initialized: ['classifier.bias', 'classifier.weight', 'pre_classifier.bias', 'pre_classifier.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Training...
 [4230/4230 24:05, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.371800	0.351318	0.841230	0.870753	0.855128	0.778192	0.156069	10.303000	163.934000	5.144000
2	0.331100	0.326068	0.855863	0.883633	0.869313	0.798540	0.141385	10.309600	163.828000	5.141000
3	0.305700	0.298938	0.866327	0.903398	0.884260	0.820032	0.125636	10.303900	163.919000	5.144000
4	0.275100	0.283565	0.864656	0.900067	0.881244	0.815532	0.129899	10.306200	163.882000	5.143000
5	0.271800	0.283880	0.879333	0.899178	0.889041	0.823584	0.119005	10.302700	163.938000	5.144000
6	0.241000	0.262368	0.885742	0.908061	0.896400	0.835149	0.111072	10.310400	163.815000	5.140000
7	0.231600	0.261541	0.896840	0.892738	0.894339	0.836077	0.110953	10.326500	163.560000	5.132000
8	0.216300	0.265626	0.905712	0.892516	0.898469	0.839738	0.105506	10.305300	163.897000	5.143000
9	0.198900	0.254257	0.893166	0.910948	0.901829	0.842254	0.106098	10.312600	163.781000	5.139000
10	0.184200	0.255630	0.899491	0.905396	0.902365	0.843793	0.104085	10.322300	163.626000	5.134000
Evaluating on eval split...
Evaluating on held-out test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.96      0.98      0.97      1952
Unchecked Return Values For Low Level Calls       0.90      0.94      0.92      1180
                          Denial of Service       0.90      0.84      0.87       985
                          Time manipulation       0.79      0.77      0.78       668
                                 Reentrancy       0.86      0.91      0.88       826

                                  micro avg       0.90      0.91      0.91      5611
                                  macro avg       0.88      0.89      0.88      5611
                               weighted avg       0.90      0.91      0.91      5611
                                samples avg       0.89      0.89      0.87      5611

Model saved to: /kaggle/working/output/optimized_20p

Results for optimized_20p:
  Train Samples      : 8444
  Test Samples       : 2111
  Train Time         : 24.1 min
  Train Infer. Time  : 12.75s
  Test Infer. Time   : 10.31s
  Precision          : 0.8995
  Recall             : 0.9054
  F1                 : 0.9024
  Hamming Score      : 0.8438
  Hamming Loss       : 0.1041

Total training time: 118.3 minutes

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
 [4230/4230 59:38, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.399000	0.368634	0.850035	0.828903	0.832380	0.765048	0.165423	25.522300	66.177000	2.077000
2	0.350800	0.339411	0.846236	0.866652	0.851246	0.791869	0.151332	25.577700	66.034000	2.072000
3	0.306000	0.324768	0.855057	0.893455	0.871450	0.807825	0.137833	25.575700	66.039000	2.072000
4	0.268900	0.307037	0.880019	0.880054	0.877247	0.819232	0.126584	25.610100	65.951000	2.069000
5	0.243400	0.294606	0.881740	0.898369	0.889680	0.831814	0.117584	25.615200	65.937000	2.069000
6	0.221100	0.298308	0.891476	0.869779	0.879975	0.819716	0.123505	25.613700	65.941000	2.069000
7	0.190500	0.306579	0.897162	0.874023	0.883891	0.826623	0.118295	25.621900	65.920000	2.069000
8	0.176400	0.298739	0.901204	0.880947	0.888769	0.836984	0.112374	25.652300	65.842000	2.066000
9	0.154200	0.301321	0.887702	0.903507	0.895378	0.842362	0.111072	25.626700	65.908000	2.068000
10	0.127300	0.304360	0.897006	0.892785	0.894342	0.842915	0.110006	25.639700	65.875000	2.067000
Evaluating on eval split...
Evaluating on held-out test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.97      0.98      0.98      1952
Unchecked Return Values For Low Level Calls       0.89      0.91      0.90      1180
                          Denial of Service       0.91      0.86      0.89       985
                          Time manipulation       0.86      0.71      0.77       668
                                 Reentrancy       0.86      0.87      0.87       826

                                  micro avg       0.91      0.90      0.91      5611
                                  macro avg       0.90      0.87      0.88      5611
                               weighted avg       0.91      0.90      0.90      5611
                                samples avg       0.90      0.88      0.88      5611

Model saved to: /kaggle/working/output/before_optimized

Results for before_optimized:
  Train Samples      : 8444
  Test Samples       : 2111
  Train Time         : 59.7 min
  Train Infer. Time  : 32.03s
  Test Infer. Time   : 25.61s
  Precision          : 0.8970
  Recall             : 0.8928
  F1                 : 0.8943
  Hamming Score      : 0.8429
  Hamming Loss       : 0.1100

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
1	0.364200	0.347289	0.844252	0.883411	0.863187	0.790941	0.149201	25.564100	66.069000	2.073000
2	0.325300	0.305737	0.885508	0.864091	0.873884	0.812345	0.129544	25.664300	65.811000	2.065000
3	0.301900	0.297540	0.853100	0.916944	0.883350	0.823130	0.131320	25.650300	65.847000	2.066000
4	0.265100	0.278062	0.887321	0.892294	0.889552	0.829889	0.117229	25.693700	65.736000	2.063000
5	0.244700	0.270893	0.901380	0.877415	0.888537	0.834873	0.114742	25.703600	65.711000	2.062000
6	0.207700	0.283342	0.916820	0.868754	0.890163	0.835573	0.110124	25.674200	65.786000	2.064000
7	0.193600	0.284176	0.915215	0.874972	0.893832	0.839057	0.108467	25.683200	65.763000	2.064000
8	0.178300	0.272253	0.901791	0.900733	0.901095	0.848658	0.104440	25.692500	65.739000	2.063000
9	0.159700	0.272924	0.898960	0.918055	0.908073	0.854687	0.100296	25.691100	65.743000	2.063000
10	0.143700	0.272647	0.906080	0.903176	0.904553	0.849526	0.101599	25.687000	65.753000	2.063000
Evaluating on eval split...
Evaluating on held-out test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.97      0.98      0.97      1952
Unchecked Return Values For Low Level Calls       0.91      0.91      0.91      1180
                          Denial of Service       0.89      0.86      0.88       985
                          Time manipulation       0.79      0.78      0.78       668
                                 Reentrancy       0.89      0.87      0.88       826

                                  micro avg       0.91      0.91      0.91      5611
                                  macro avg       0.89      0.88      0.89      5611
                               weighted avg       0.91      0.91      0.91      5611
                                samples avg       0.90      0.88      0.88      5611

Model saved to: /kaggle/working/output/optimized_80p

Results for optimized_80p:
  Train Samples      : 8444
  Test Samples       : 2111
  Train Time         : 60.1 min
  Train Infer. Time  : 32.06s
  Test Infer. Time   : 25.66s
  Precision          : 0.9061
  Recall             : 0.9032
  F1                 : 0.9046
  Hamming Score      : 0.8495
  Hamming Loss       : 0.1016

============================================================
Training with column: optimized_50p
============================================================
[START] No checkpoint found — training from scratch.
Train: 8444, Test: 2111
Some weights of RobertaForSequenceClassification were not initialized from the model checkpoint at microsoft/codebert-base and are newly initialized: ['classifier.dense.bias', 'classifier.dense.weight', 'classifier.out_proj.bias', 'classifier.out_proj.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Training...
 [4230/4230 1:00:20, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.334100	0.326284	0.864055	0.867866	0.864485	0.790497	0.140557	25.732400	65.637000	2.060000
2	0.298100	0.283433	0.890068	0.885188	0.887065	0.822785	0.118650	25.679100	65.773000	2.064000
3	0.266000	0.262326	0.883993	0.921830	0.902270	0.842323	0.106927	25.699400	65.721000	2.062000
4	0.234400	0.249633	0.905616	0.903398	0.903316	0.847247	0.102783	25.667700	65.802000	2.065000
5	0.213200	0.241269	0.913629	0.907617	0.910379	0.857401	0.094375	25.673900	65.787000	2.064000
6	0.177100	0.238213	0.913341	0.920942	0.915694	0.869844	0.087981	25.703000	65.712000	2.062000
7	0.155000	0.236608	0.909179	0.928714	0.918757	0.873564	0.087034	25.680000	65.771000	2.064000
8	0.139200	0.235738	0.919446	0.917833	0.918087	0.874235	0.086323	25.708800	65.697000	2.062000
9	0.119100	0.235203	0.918853	0.927160	0.922871	0.877600	0.082652	25.663300	65.814000	2.065000
10	0.105300	0.234838	0.922816	0.926271	0.924444	0.880472	0.080403	25.676900	65.779000	2.064000
Evaluating on eval split...
Evaluating on held-out test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.97      0.98      0.98      1952
Unchecked Return Values For Low Level Calls       0.92      0.95      0.93      1180
                          Denial of Service       0.93      0.85      0.89       985
                          Time manipulation       0.84      0.81      0.82       668
                                 Reentrancy       0.89      0.91      0.90       826

                                  micro avg       0.93      0.92      0.92      5611
                                  macro avg       0.91      0.90      0.90      5611
                               weighted avg       0.93      0.92      0.92      5611
                                samples avg       0.91      0.90      0.89      5611

Model saved to: /kaggle/working/output/optimized_50p

Results for optimized_50p:
  Train Samples      : 8444
  Test Samples       : 2111
  Train Time         : 60.4 min
  Train Infer. Time  : 32.05s
  Test Infer. Time   : 25.62s
  Precision          : 0.9228
  Recall             : 0.9263
  F1                 : 0.9244
  Hamming Score      : 0.8805
  Hamming Loss       : 0.0804

============================================================
Training with column: optimized_20p
============================================================
[START] No checkpoint found — training from scratch.
Train: 8444, Test: 2111
Some weights of RobertaForSequenceClassification were not initialized from the model checkpoint at microsoft/codebert-base and are newly initialized: ['classifier.dense.bias', 'classifier.dense.weight', 'classifier.out_proj.bias', 'classifier.out_proj.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Training...
 [4230/4230 26:26, Epoch 10/10]
Epoch	Training Loss	Validation Loss	Precision	Recall	F1	Hamming Score	Hamming Loss	Runtime	Samples Per Second	Steps Per Second
1	0.357800	0.326796	0.853933	0.875416	0.864002	0.796053	0.144227	11.406300	148.076000	4.647000
2	0.312300	0.314836	0.870218	0.879414	0.874635	0.805121	0.133689	11.398800	148.173000	4.650000
3	0.287800	0.281635	0.872053	0.922274	0.896005	0.835514	0.115808	11.407500	148.061000	4.646000
4	0.244200	0.274323	0.892553	0.892294	0.890875	0.830679	0.116282	11.414100	147.974000	4.643000
5	0.240400	0.264365	0.890468	0.911170	0.900667	0.841938	0.107401	11.424300	147.843000	4.639000
6	0.210000	0.259729	0.900695	0.909616	0.904129	0.853010	0.101125	11.433700	147.722000	4.635000
7	0.195800	0.250857	0.905581	0.909394	0.907215	0.853118	0.098401	11.424700	147.837000	4.639000
8	0.178100	0.269220	0.922279	0.874528	0.895294	0.839807	0.105151	11.426200	147.818000	4.638000
9	0.157300	0.247351	0.909798	0.917610	0.913416	0.862611	0.093073	11.426500	147.814000	4.638000
10	0.142000	0.247936	0.912517	0.913169	0.912720	0.861654	0.092836	11.426900	147.810000	4.638000
Evaluating on eval split...
Evaluating on held-out test set...
Generating classification report...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.97      0.98      0.97      1952
Unchecked Return Values For Low Level Calls       0.90      0.94      0.92      1180
                          Denial of Service       0.93      0.84      0.88       985
                          Time manipulation       0.80      0.77      0.79       668
                                 Reentrancy       0.86      0.90      0.88       826

                                  micro avg       0.91      0.91      0.91      5611
                                  macro avg       0.89      0.88      0.89      5611
                               weighted avg       0.91      0.91      0.91      5611
                                samples avg       0.90      0.89      0.88      5611

Model saved to: /kaggle/working/output/optimized_20p

Results for optimized_20p:
  Train Samples      : 8444
  Test Samples       : 2111
  Train Time         : 26.5 min
  Train Infer. Time  : 14.27s
  Test Infer. Time   : 11.36s
  Precision          : 0.9125
  Recall             : 0.9132
  F1                 : 0.9127
  Hamming Score      : 0.8617
  Hamming Loss       : 0.0928

Total training time: 212.6 minutes

# GPT-2

============================================================
STEP 4: Run All Experiments
============================================================

============================================================
Training with column: before_optimized
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
 [4230/4230 23:14, Epoch 10/10]
Epoch	Training Loss	Validation Loss
1	0.694247	0.326075
2	0.588594	0.292670
3	0.568882	0.274196
4	0.502621	0.267204
5	0.457880	0.264255
6	0.430608	0.246094
7	0.398989	0.242712
8	0.357222	0.242125
9	0.343966	0.241635
10	0.341531	0.240817
Generating predictions...
Starting inference on 2111 samples...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.97      0.98      0.97      1952
Unchecked Return Values For Low Level Calls       0.90      0.94      0.92      1180
                          Denial of Service       0.87      0.87      0.87       985
                          Time manipulation       0.80      0.83      0.82       668
                                 Reentrancy       0.86      0.91      0.89       826

                                  micro avg       0.90      0.93      0.91      5611
                                  macro avg       0.88      0.91      0.89      5611
                               weighted avg       0.90      0.93      0.91      5611
                                samples avg       0.89      0.91      0.89      5611

Model saved to: /working/data/before_optimized

Results for before_optimized:
  Train Samples: 8444, Test Samples: 2111
  Train Time: 23.3 min
  Test Inference Time: 14.76s
  Precision: 0.9024
  Recall: 0.9253
  F1: 0.9136
  Hamming Score: 0.8623
  Hamming Loss: 0.0932

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
 [4230/4230 22:43, Epoch 10/10]
Epoch	Training Loss	Validation Loss
1	0.750045	0.351534
2	0.654672	0.304340
3	0.595812	0.287022
4	0.524733	0.272521
5	0.481129	0.261760
6	0.468013	0.251703
7	0.432810	0.252389
8	0.419394	0.251921
9	0.377135	0.246022
10	0.371800	0.242539
Generating predictions...
Starting inference on 2111 samples...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.96      0.99      0.97      1952
Unchecked Return Values For Low Level Calls       0.91      0.95      0.93      1180
                          Denial of Service       0.84      0.89      0.87       985
                          Time manipulation       0.79      0.80      0.79       668
                                 Reentrancy       0.86      0.93      0.89       826

                                  micro avg       0.89      0.93      0.91      5611
                                  macro avg       0.87      0.91      0.89      5611
                               weighted avg       0.89      0.93      0.91      5611
                                samples avg       0.89      0.91      0.89      5611

Model saved to: /working/data/optimized_80p

Results for optimized_80p:
  Train Samples: 8444, Test Samples: 2111
  Train Time: 22.7 min
  Test Inference Time: 14.12s
  Precision: 0.8928
  Recall: 0.9312
  F1: 0.9115
  Hamming Score: 0.8604
  Hamming Loss: 0.0962

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
 [4230/4230 22:12, Epoch 10/10]
Epoch	Training Loss	Validation Loss
1	0.747543	0.352576
2	0.656460	0.314659
3	0.591833	0.296742
4	0.550480	0.289270
5	0.511573	0.283346
6	0.503083	0.265468
7	0.462315	0.260442
8	0.446940	0.262841
9	0.410056	0.256712
10	0.390359	0.258728
Generating predictions...
Starting inference on 2111 samples...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.96      0.98      0.97      1952
Unchecked Return Values For Low Level Calls       0.90      0.95      0.92      1180
                          Denial of Service       0.86      0.89      0.87       985
                          Time manipulation       0.77      0.86      0.81       668
                                 Reentrancy       0.84      0.93      0.88       826

                                  micro avg       0.89      0.94      0.91      5611
                                  macro avg       0.86      0.92      0.89      5611
                               weighted avg       0.89      0.94      0.91      5611
                                samples avg       0.89      0.91      0.89      5611

Model saved to: /working/data/optimized_50p

Results for optimized_50p:
  Train Samples: 8444, Test Samples: 2111
  Train Time: 22.2 min
  Test Inference Time: 13.44s
  Precision: 0.8887
  Recall: 0.9371
  F1: 0.9120
  Hamming Score: 0.8616
  Hamming Loss: 0.0971

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
 [4230/4230 21:42, Epoch 10/10]
Epoch	Training Loss	Validation Loss
1	0.790605	0.364276
2	0.714548	0.328530
3	0.621314	0.316575
4	0.582052	0.308109
5	0.552520	0.302085
6	0.544904	0.306179
7	0.511654	0.299684
8	0.496089	0.290090
9	0.468530	0.292120
10	0.451200	0.288621
Generating predictions...
Starting inference on 2111 samples...

Classification Report by Label:
                                             precision    recall  f1-score   support

                                 Arithmetic       0.95      0.98      0.97      1952
Unchecked Return Values For Low Level Calls       0.90      0.92      0.91      1180
                          Denial of Service       0.82      0.86      0.84       985
                          Time manipulation       0.76      0.79      0.78       668
                                 Reentrancy       0.85      0.89      0.87       826

                                  micro avg       0.88      0.91      0.89      5611
                                  macro avg       0.86      0.89      0.87      5611
                               weighted avg       0.88      0.91      0.89      5611
                                samples avg       0.87      0.89      0.87      5611

Model saved to: /working/data/optimized_20p

Results for optimized_20p:
  Train Samples: 8444, Test Samples: 2111
  Train Time: 21.7 min
  Test Inference Time: 12.67s
  Precision: 0.8783
  Recall: 0.9120
  F1: 0.8948
  Hamming Score: 0.8378
  Hamming Loss: 0.1141

Total training time: 93.8 minutes