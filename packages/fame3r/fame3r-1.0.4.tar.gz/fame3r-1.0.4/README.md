FAME3R: a re-implementation of the FAME3 model.

FAME3R is a random forest model predicting the phase 1 and phase 2 sites of metabolism (SOMs) in small organic molecules.

### Installation

1. Create a conda environment with the required python version:

```sh
conda create --name fame3r-env python=3.10
```

2. Activate the environment:

```sh
conda activate fame3r-env
```

3. Install package:

```sh
pip install fame3r
```

### Usage

#### Input data

The input data must be provided in SD file format. Any number and type of molecular properties are accepted. For labeled data, the true sites of metabolism (SOMs) should be specified as a list of atom indices under the `soms` property. For example, if atoms 1 and 6 are SOMs, the `soms` property should be written as [1, 6]. For unlabeled data, the `soms` property can be omitted.

Each of the core scripts (`cv_hp_search.py`, `train.py`, `test.py`, and `infer.py`) automatically computes FAME descriptors for each atom in the input molecules. These descriptors are saved to `*_descriptors.csv` files in the output directory to ensure transparency and reproducibility.

For more information on FAME descriptors, we refer the reader to Šícho, Martin, et al. "FAME 3: predicting the sites of metabolism in synthetic compounds and natural products for phase 1 and phase 2 metabolic enzymes." *Journal of chemical information and modeling* 59.8 (2019): 3400-3412.

#### Determining the optimal hyperparameters via k-fold cross-validation

Different training datasets may require hyperparameters that differ from the provided defaults. To identify the optimal hyperparameters for your specific data, you can run K-fold cross-validation with a grid search using the `cv_hp_search.py` script.

The search space is defined in the param_grid dictionary within the script. After running, the script saves:

- The best hyperparameter set (based on validation performance) to a text file.

- The optimal binary decision threshold — chosen to maximize the Matthews Correlation Coefficient (MCC) on the validation set — based on the majority vote across folds.

- The mean and standard deviation of the model’s performance metrics across all folds.

Note:

- The atom environment radius is not part of the hyperparameter search but can be set via the `--radius` command-line argument (default: 5).

- The number of folds used in cross-validation can be set with the `--num_folds` command-line argument (default: 10).

```sh
fame3r-cv-hp-search -i INPUT_FILE -o OUTPUT_FOLDER -r RADIUS[OPTIONAL, DEFAULT=5] -n NUM_FOLDS[OPTIONAL, DEFAULT=10]
```

#### Training a model

Use the `train.py` to train a random forest classifier with pre-defined hyperparameters.

The trained model is saved as a .joblib file in the specified output folder.

Note:

- This script does not perform hyperparameter optimization or radius tuning. For that, see the section "Determining the optimal hyperparameters via K-fold cross-validation."

- You can manually adjust the model's hyperparameters in the `RandomForestClassifier` constructor within the script.

- The atom environment radius can be set via the `--radius` command-line argument (default: 5).

```sh
fame3r-train -i INPUT_FILE -o OUTPUT_FOLDER -r RADIUS[OPTIONAL, DEFAULT=5]
```

#### Testing a trained model on labeled test data

Use the `test.py` script to evaluate a trained model on labeled test data.

After execution, the script saves:

- Test performance metrics are saved to a text file. The metrics include the Area Under the Receiver Operating Characteristic curve (AUROC), the area under the precision-recall curve (average precision), the F1 score, the Matthews Correlation Coefficient (MCC), precision, recall, and the top-2 correctness rate. The top-2 correctness rate represents the percentage of molecules for which at least one true site of metabolism (SOM) is ranked among the top two atoms in the molecule based on predicted SOM probabilities.

- Per-atom predictions (including probabilities, binary classifications, and true labels) to a CSV file.

Note:

- This script performs bootstrapping to estimate the uncertainty in the metrics. The number of bootstraps can be set by changing the `NUM_BOOTSTRAPS` variable. Default is 1000.

- The radius of the atom environment is not part of the hyperparameter search, but can be set by changing the `--radius` command-line argument. Default is 5.

- The decision threshold can be changed by changing the `--threshold` command-line argument. Default is 0.3.

- The script also computes FAME scores if the `-fs` flag is set. FAME scores are an indication of the well-representedness of the inference data compared to the training data and is defined as the Tanimoto similarity to the three nearest neighbors in the training data, computed on FAME descriptors. The higher the score, the most trustworthy the predictions.

```sh
fame3r-test -i INPUT_FILE -m MODEL_FOLDER -o OUTPUT_FOLDER -r RADIUS[OPTIONAL, DEFAULT=5] -t THRESHOLD[OPTIONAL, DEFAULT=0.3] -fs[OPTIONAL]
```

#### Inference mode: computing the SOMs of unlabeled data

The `inference.py` script applies a trained model to unlabeled input data and saves the per-atom predictions to a CSV file. Each row contains the predicted SOM probability and its corresponding binary classification based on a decision threshold. If the `--compute_fame_scores` (-fs) flag is set, the script also computes FAME scores, which indicate how well each atom's environment is represented in the training data. These scores are calculated as the average Tanimoto similarity to the three nearest neighbors in the training set, based on FAME descriptors. The higher the score, the most trustworthy the predictions. The radius of the atom environment can be specified using the --radius argument (default: 5), and the decision threshold can be set via the --threshold argument (default: 0.3).

```sh
fame3r-infer -i INPUT_FILE -m MODEL_FOLDER -o OUTPUT_FOLDER -r RADIUS[OPTIONAL, DEFAULT=5] -t THRESHOLD[OPTIONAL, DEFAULT=0.3] -fs[OPTIONAL]
```
