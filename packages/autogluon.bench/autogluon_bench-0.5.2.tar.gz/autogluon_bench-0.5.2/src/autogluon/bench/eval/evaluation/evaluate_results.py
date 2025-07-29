import copy
import logging
import os
from collections import Counter
from typing import Tuple

import pandas as pd

from autogluon.common.savers import save_pd

from . import evaluate_utils
from .constants import *
from .preprocess import preprocess_utils

logger = logging.getLogger(__name__)

WINRATE = "Winrate"


def compute_vs_diff(
    results_ranked_by_dataset: pd.DataFrame, framework_1: str, framework_2: str
) -> Tuple[float, float]:
    """
    Compare two frameworks across a suite of datasets and calculate mean_diff and median_diff.

    Parameters
    ----------
    results_ranked_by_dataset: pd.DataFrame
        The ranked results by dataset containing only the two frameworks.
    framework_1: str
        The name of the first framework to compare.
    framework_2: str
        The name of the second framework to compare.

    Returns
    -------
    A tuple of (mean_diff, median_diff).

    mean_diff: float
        The proportional mean difference in the metric error of framework_1 to framework_2, normalized per dataset.
        As an example, if the value is 0.05, then the metric error is on average 5% lower on framework_1 compared to framework_2.
            Example: framework_2 has a metric_error of 0.1, then framework_1 would have a metric_error of 0.095.
        Conversely, if the value is -0.05, then the metric error is on average 5% lower on framework_2 compared to framework_1.
        The maximum and minimum possible value is 1.0 and -1.0.
    median_diff: float
        The proportional median difference in the metric error of framework_1 to framework_2, normalized per dataset.
        The maximum and minimum possible value is 1.0 and -1.0.
    """
    assert framework_1 != framework_2
    assert set(results_ranked_by_dataset[FRAMEWORK].unique()) == {framework_1, framework_2}

    results_ranked_by_dataset = copy.deepcopy(results_ranked_by_dataset)

    results_ranked_by_dataset.loc[results_ranked_by_dataset[FRAMEWORK] == framework_1, "sign"] = -1
    results_ranked_by_dataset.loc[results_ranked_by_dataset[FRAMEWORK] == framework_2, "sign"] = 1

    results_ranked_by_dataset = results_ranked_by_dataset.sort_values(by=[BESTDIFF], ascending=False)
    results_ranked_by_dataset = results_ranked_by_dataset.drop_duplicates(subset=[DATASET], keep="first")
    results_ranked_by_dataset[BESTDIFF] = results_ranked_by_dataset[BESTDIFF] * results_ranked_by_dataset["sign"]

    mean_diff = results_ranked_by_dataset[BESTDIFF].mean()
    median_diff = results_ranked_by_dataset[BESTDIFF].median()

    return mean_diff, median_diff


def evaluate(
    results_raw,
    frameworks=None,
    banned_datasets=None,
    folds_to_keep=None,
    columns_to_agg_extra=None,
    frameworks_compare_vs_all=None,
    output_dir=None,
    verbose=True,
):
    if len(results_raw) == 0:
        raise AssertionError("results_raw cannot be empty")

    if columns_to_agg_extra is None:
        columns_to_agg_extra = []

    valid_columns = [
        FRAMEWORK,
        DATASET,
        FOLD,
        PROBLEM_TYPE,
        METRIC_ERROR,
        TIME_TRAIN_S,
    ] + columns_to_agg_extra

    og_columns = list(results_raw.columns)
    og_columns_set = set(og_columns)
    valid_columns_set = set(valid_columns)
    invalid_columns = [col for col in og_columns if col not in valid_columns_set]

    print(f"FOUND {len(invalid_columns)} unused columns, dropping... Unused columns: {invalid_columns}")
    print(f"Filtering to only valid columns: {valid_columns}")

    missing_columns = [col for col in valid_columns if col not in og_columns_set]
    if missing_columns:
        raise AssertionError(f"Missing {len(missing_columns)} required columns: {missing_columns}")

    results_raw = results_raw[valid_columns]

    if frameworks is None:
        frameworks = sorted(list(results_raw[FRAMEWORK].unique()))
    elif len(set(frameworks)) != len(frameworks):
        d = Counter(frameworks)
        d = {k: v for k, v in d.items() if v > 1}
        raise AssertionError("Framework duplicate detected. Frameworks must be unique.\n" "Framework counts:\n" f"{d}")
    results_raw = results_raw[results_raw[FRAMEWORK].isin(set(frameworks))]
    print(f"Filtered to only valid frameworks: {len(frameworks)} frameworks")
    if len(results_raw) == 0:
        raise AssertionError("results_raw cannot be empty")
    if frameworks_compare_vs_all is None:
        frameworks_compare_vs_all = []
    if folds_to_keep is None:
        folds_to_keep = sorted(list(results_raw[FOLD].unique()))
    if banned_datasets is not None:
        results_raw = results_raw[~results_raw[DATASET].isin(banned_datasets)]

    total_datasets = sorted(results_raw[DATASET].unique())
    results_raw = preprocess_utils.clean_result(
        result_df=results_raw, folds_to_keep=folds_to_keep, remove_invalid=True
    )

    # Calculate each frameworks errored datasets
    total_frameworks = results_raw[FRAMEWORK].unique()
    total_folds = results_raw[FOLD].unique()
    num_frameworks = len(total_frameworks)
    num_datasets = len(total_datasets)
    num_folds = len(total_folds)
    ideal_rows = num_folds * num_datasets * num_frameworks
    actual_rows = len(results_raw)
    errors = ideal_rows - actual_rows
    if verbose:
        print("num_datasets:", num_datasets)
        print("num_folds:", num_folds)
        print("errors:", errors)
        print("################################################")

    missing_frameworks = [f for f in frameworks_compare_vs_all if f not in total_frameworks]
    if missing_frameworks:
        raise AssertionError(
            f"Missing specified comparison frameworks: {missing_frameworks}\n"
            f"\tValid frameworks: {list(total_frameworks)}"
        )
    for framework in total_frameworks:
        results_framework = results_raw[results_raw[FRAMEWORK] == framework]
        num_rows_framework = len(results_framework)
        datasets_framework = results_framework[DATASET].unique()
        datasets_framework_errors = [dataset for dataset in total_datasets if dataset not in datasets_framework]
        datasets_framework_errors_count = len(datasets_framework_errors)
        framework_fold_errors = num_datasets * num_folds - num_rows_framework
        if verbose:
            print("framework:", framework)
            print(
                f"\tdatasets_errors: {datasets_framework_errors_count}"
                f"\tfold_errors: {framework_fold_errors}"
                f"\tdatasets_framework_errors: {datasets_framework_errors}"
            )
    if verbose:
        print("################################################")
        print("%s VS %s" % ("all", "all"))
        print("\tAll datasets regardless of failures")
    results_ranked_all, results_ranked_by_dataset_all = evaluate_utils.compare_frameworks(
        results_raw=results_raw,
        banned_datasets=banned_datasets,
        folds_to_keep=folds_to_keep,
        filter_errors=False,
        columns_to_agg_extra=columns_to_agg_extra,
        datasets=total_datasets,
        verbose=verbose,
    )

    if output_dir:
        path_ranked_all = os.path.join(output_dir, "results_ranked_all.csv")
        save_pd.save(path=path_ranked_all, df=results_ranked_all)
        logger.info(f"{path_ranked_all} saved.")

        path_ranked_by_dataset_all = os.path.join(output_dir, "results_ranked_by_dataset_all.csv")
        save_pd.save(path=path_ranked_by_dataset_all, df=results_ranked_by_dataset_all)
        logger.info(f"{path_ranked_by_dataset_all} saved.")

    if verbose:
        print("################################################")
        print("%s VS %s" % ("all", "all"))
        print("\tOnly datasets where all frameworks succeeded")
    results_ranked_valid, results_ranked_by_dataset_valid = evaluate_utils.compare_frameworks(
        results_raw=results_raw,
        frameworks=frameworks,
        banned_datasets=banned_datasets,
        folds_to_keep=folds_to_keep,
        columns_to_agg_extra=columns_to_agg_extra,
        datasets=total_datasets,
        verbose=verbose,
    )

    if output_dir:
        path_ranked_valid = os.path.join(output_dir, "results_ranked_valid.csv")
        save_pd.save(path=path_ranked_valid, df=results_ranked_valid)
        logger.info(f"{path_ranked_valid} saved.")

        path_ranked_by_dataset_valid = os.path.join(output_dir, "results_ranked_by_dataset_valid.csv")
        save_pd.save(path=path_ranked_by_dataset_valid, df=results_ranked_by_dataset_valid)
        logger.info(f"{path_ranked_by_dataset_valid} saved.")

    calc_inf_diff = TIME_INFER_S in columns_to_agg_extra
    time_train_s_rescaled = TIME_TRAIN_S + "_rescaled"
    time_infer_s_rescaled = TIME_INFER_S + "_rescaled"

    all_results_pairs = {}
    for framework_1 in frameworks_compare_vs_all:
        print(f"Computing comparison vs '{framework_1}'")
        results_list = []

        for framework_2 in total_frameworks:
            if framework_2 == framework_1:
                results_ranked, results_ranked_by_dataset = evaluate_utils.compare_frameworks(
                    results_raw=results_raw,
                    frameworks=[framework_1],
                    banned_datasets=banned_datasets,
                    folds_to_keep=folds_to_keep,
                    columns_to_agg_extra=columns_to_agg_extra,
                    datasets=total_datasets,
                    verbose=False,
                )
                ties = len(results_ranked_by_dataset)
                out = [framework_1, 0.5, 0, 0, ties, 0, 0, 0]
                if calc_inf_diff:
                    out.append(0)
                results_list.append(out)
                continue

            results_ranked, results_ranked_by_dataset = evaluate_utils.compare_frameworks(
                results_raw=results_raw,
                frameworks=[framework_2, framework_1],
                banned_datasets=banned_datasets,
                folds_to_keep=folds_to_keep,
                columns_to_agg_extra=columns_to_agg_extra,
                datasets=total_datasets,
                verbose=False,
            )

            mean_diff, median_diff = compute_vs_diff(
                results_ranked_by_dataset=results_ranked_by_dataset, framework_1=framework_1, framework_2=framework_2
            )

            # Convert proportion to percentile
            mean_diff *= 100
            median_diff *= 100

            datasets_pair = results_ranked_by_dataset[DATASET].unique()
            framework_1_wins = 0
            framework_2_wins = 0
            ties = 0
            avg_fit_diffs = 0
            avg_inf_diffs = 0
            for dataset in datasets_pair:
                results_isolated = results_ranked_by_dataset[results_ranked_by_dataset[DATASET] == dataset]

                if len(results_isolated) != 2:
                    print(f"Found invalid results_isolated! Printing:")
                    with pd.option_context("display.max_columns", None, "display.width", 1000):
                        print(results_isolated)
                    raise AssertionError(
                        "results_isolated is not of expected length 2! "
                        f"Actual len: {len(results_isolated)} | dataset={dataset} | "
                        f"framework_1={framework_1} | framework_2={framework_2}"
                    )

                fit_2 = results_isolated[results_isolated[FRAMEWORK] == framework_2][time_train_s_rescaled].iloc[0]
                fit_1 = results_isolated[results_isolated[FRAMEWORK] == framework_1][time_train_s_rescaled].iloc[0]

                if fit_2 > fit_1:
                    avg_fit_diff = -(fit_2 - 1)
                else:
                    avg_fit_diff = fit_1 - 1
                avg_fit_diffs += avg_fit_diff

                if calc_inf_diff:
                    inf_2 = results_isolated[results_isolated[FRAMEWORK] == framework_2][time_infer_s_rescaled].iloc[0]
                    inf_1 = results_isolated[results_isolated[FRAMEWORK] == framework_1][time_infer_s_rescaled].iloc[0]

                    if inf_2 > inf_1:
                        avg_inf_diff = -(inf_2 - 1)
                    else:
                        avg_inf_diff = inf_1 - 1
                    avg_inf_diffs += avg_inf_diff

                results_isolated = results_isolated[results_isolated[FRAMEWORK] == framework_1]
                results_isolated_rank = results_isolated[RANK].iloc[0]
                if results_isolated_rank == 1:
                    framework_1_wins += 1
                elif results_isolated_rank == 2:
                    framework_2_wins += 1
                elif results_isolated_rank == 1.5:
                    ties += 1
                else:
                    raise AssertionError("Rank not valid: %s" % results_isolated_rank)
            winrate = (framework_1_wins + 0.5 * ties) / (framework_1_wins + framework_2_wins + ties)

            avg_fit_diffs = avg_fit_diffs / len(datasets_pair)
            out = [
                framework_2,
                winrate,
                framework_1_wins,
                framework_2_wins,
                ties,
                mean_diff,
                median_diff,
                avg_fit_diffs,
            ]
            if calc_inf_diff:
                avg_inf_diffs = avg_inf_diffs / len(datasets_pair)
                out.append(avg_inf_diffs)
            results_list.append(out)
        out_col_names = [
            FRAMEWORK,
            WINRATE,
            ">",
            "<",
            "=",
            "% Loss Reduction",
            "% Loss Reduction (median)",
            "Avg Fit Speed Diff",
        ]
        if calc_inf_diff:
            out_col_names.append("Avg Inf Speed Diff")
        results_pairs = pd.DataFrame(data=results_list, columns=out_col_names)
        all_results_pairs[framework_1] = results_pairs

    results_pairs_merged_dict = {}
    for framework in frameworks_compare_vs_all:
        columns_to_get_from_all = [RANK_1, "rank=2_count", "rank=3_count", "rank>3_count", ERROR_COUNT]
        results_pairs = all_results_pairs[framework]
        results_pairs_merged = pd.merge(results_pairs, results_ranked_valid, on=FRAMEWORK, how="left")
        results_pairs_merged = results_pairs_merged.drop(columns_to_get_from_all, axis=1)
        results_pairs_merged = pd.merge(
            results_pairs_merged, results_ranked_all[[FRAMEWORK] + columns_to_get_from_all], on=FRAMEWORK, how="left"
        )
        results_pairs_merged = results_pairs_merged.sort_values(by=RANK)
        if verbose:
            print_champion(results_pairs_merged=results_pairs_merged, framework=framework, num_datasets=num_datasets)
        if output_dir:
            path_pairwise = os.path.join(output_dir, "pairwise", framework + ".csv")
            save_pd.save(path=path_pairwise, df=results_pairs_merged)
            logger.info(f"{path_pairwise} saved.")
        results_pairs_merged_dict[framework] = results_pairs_merged

    return (
        results_ranked_valid,
        results_ranked_by_dataset_valid,
        results_ranked_all,
        results_ranked_by_dataset_all,
        results_pairs_merged_dict,
    )


def print_champion(results_pairs_merged, framework, num_datasets):
    print("################################################")
    print("%s VS %s" % (framework, "all"))
    with pd.option_context("display.max_rows", None, "display.max_columns", None, "display.width", 1000):
        results_pairs_merged_print = results_pairs_merged.drop(["bestdiff", "metric_error"], axis=1)
        results_pairs_merged_print = results_pairs_merged_print.reset_index(drop=True)
        print(results_pairs_merged_print)
