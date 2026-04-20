============================================================
ENVIRONMENT CHECK
============================================================
Python: 3.12.13 | packaged by conda-forge | (main, Mar  5 2026, 16:50:00) [GCC 14.3.0]
PyTorch: 2.11.0+cu128
CUDA available: True
GPU: NVIDIA GeForce RTX 4090

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
