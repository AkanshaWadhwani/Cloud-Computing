# Dataset and Provenance

## Source used for the Member 1 model

The model was trained from the eight CoAID News CSV parts supplied by the project team. The original research repository was also supplied and inspected.

The original repository's notebook defaults to a synthetic 100-sentence corpus. That synthetic corpus was **not** used for this production model.

## Preprocessing

1. Concatenate the eight supplied CSV parts.
2. Assign label 0 to `NewsRealCOVID-19` and label 1 to `NewsFakeCOVID-19`.
3. Build text from `title`, `abstract`, and `content`.
4. Remove rows with no usable text.
5. Remove exact duplicate normalized text records before splitting.
6. Exclude three clearly non-COVID pre-2020 anomaly records.
7. Stratified 80/10/10 train/validation/test split with random seed 42.
8. Fit TF-IDF + Logistic Regression on train, evaluate during validation, then fit the production artifact on train + validation while keeping the test set held out.

## Date coverage

Publication-date metadata is sparse. Only 181 usable records have a parseable date. The recorded dates span 2020-01-06 through 2020-11-03 UTC after excluding the three pre-2020 anomalies.
