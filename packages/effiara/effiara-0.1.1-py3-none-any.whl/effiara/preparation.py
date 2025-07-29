"""Module to handle the preparation for anntotation.
This includes:
* calculating number of samples to annotate
* calculating the distribution of samples
"""

import re
import warnings
from typing import List, Optional

import pandas as pd
from sympy import Eq, solve, symbols
from sympy.core.symbol import Symbol


def sample_without_replacement(
    df: pd.DataFrame, n: int
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Sample a number of data points without replacement.

    Args:
        df (pd.DataFrame): DataFrame to sample from.
        n (int): number of data points to sample.

    Returns:
        pd.DataFrame: complete dataset with sampled data points
            removed.
        pd.DataFrame: sampled data points.
    """
    if not isinstance(n, int):
        raise TypeError("n must be an integer.")
    if n <= 0:
        raise ValueError("Should not attempt to sample 0 or less from DataFrame.")
    n = min([len(df), n])
    sampled_df = df.sample(n)
    return df.drop(sampled_df.index.to_list()), sampled_df


def get_missing_var(variables: dict) -> Symbol:
    """Find the missing variable given a dict of variables.
       Exactly one variable should be None.

    Args:
        variables (dict): dict of variables {var: value}.

    Returns:
        Symbol: symbol of the missing variable using sympy.

    Raises:
        ValueError: if there are no missing variables or more
            than one missing variable.
    """
    if not isinstance(variables, dict):
        raise TypeError("variables must be of type 'dict'.")
    missing_count = 0
    missing_variable = None

    for var, value in variables.items():
        if value is None:
            missing_variable = var
            missing_count += 1
        if missing_count > 1:
            raise ValueError("variables has more than one missing value.")

    if missing_variable is None:
        raise ValueError("variables does not have any missing values.")

    return missing_variable


class SampleDistributor:
    """
    Attributes:
        annotators (list)
        num_annotators (int)
        time_available (float)
        annotation_rate (float)
        num_samples (int)
        double_proportion (float)
        re_proportion (float)
    """

    def __init__(
        self,
        annotators: Optional[List[str]] = None,
        time_available: Optional[float] = None,
        annotation_rate: Optional[float] = None,
        num_samples: Optional[int] = None,
        double_proportion: Optional[float] = None,
        re_proportion: Optional[float] = None,
    ):
        """
        Args:
            annotators (list)
            num_annotators (int)
            time_available (float)
            annotation_rate (float)
            num_samples (int)
            double_proportion (float)
            re_proportion (float)
        """
        if annotators is None:
            num_annotators = None
        else:
            num_annotators = len(annotators)

        self.annotators = annotators

        self.get_variables(
            num_annotators,
            time_available,
            annotation_rate,
            num_samples,
            double_proportion,
            re_proportion,
        )

        # error raised if more than annotators is None
        if self.annotators is None:
            self.annotators = [f"user_{i}" for i in range(1, self.num_annotators + 1)]

    def _assign_variables(self, variables: dict):
        """Assign class level variables from dict of symbolised
           variables (as defined in 'get_variables').

        Args:
            variables (dict): dict of variables to assign.
        """
        n, t, rho, k, d, r = symbols("n t rho k d r")
        self.num_annotators = int(variables.get(n))
        self.time_available = float(variables.get(t))
        self.annotation_rate = float(variables.get(rho))
        self.num_samples = int(variables.get(k))
        self.double_proportion = float(variables.get(d))
        self.re_proportion = float(variables.get(r))

    def get_variables(self,
                      num_annotators: Optional[int] = None,
                      time_available: Optional[float] = None,
                      annotation_rate: Optional[float] = None,
                      num_samples: Optional[int] = None,
                      double_proportion: Optional[float] = None,
                      re_proportion: Optional[float] = None):
        """Solves the annotation framework equation to find the missing
        variable. Only one of the available arguments should be ommitted.

        Args:
            num_annotators (int): number of annotators available [n].
            time_available (float): time available for each annotator
                (assuming they all have the same time available) [t].
            annotation_rate (float): expected rate of annotation per
                unit time (same unit as time_available) [rho].
            num_samples (int): number of desired samples [k].
            double_proportion (float): proportion of the whole dataset that
                should be double-annotated samples (0 <= n <= 1) [d].
            re_proportion (float): proportion of single-annotated samples
                that should be re-annotated (0 <= n <= 1) [r].
        """
        # define variable symbols
        n, t, rho, k, d, r = symbols("n t rho k d r")

        # define distribution equation
        equation = Eq(k, ((2 * d) + ((1 + r) * (1 - d))) ** (-1) * rho * t * n)

        # set vars
        variables = {
            n: num_annotators,
            t: time_available,
            rho: annotation_rate,
            k: num_samples,
            d: double_proportion,
            r: re_proportion,
        }

        # find missing var to solve for
        missing_variable = get_missing_var(variables)

        solution = solve(equation, missing_variable)

        # substitute values into solution
        variables[missing_variable] = solution[0].subs(
            {k: v for k, v in variables.items() if v is not None}
        )

        self._assign_variables(variables)

    def set_project_distribution(self):
        """Set project distributions once all values have been defined."""
        assert self.num_annotators is not None, "num_annotators must be set"  # noqa
        assert self.num_samples is not None, "num_samples must be set"  # noqa
        assert (
            self.double_proportion is not None
        ), "double_proportion must be set"  # noqa
        assert self.re_proportion is not None, "re_proportion must be set"  # noqa

        self.double_annotation_project = round(
            (self.double_proportion * self.num_samples)
            / (2 * self.num_annotators)  # noqa
        )
        self.single_annotation_project = round(
            ((1 - self.double_proportion) * self.num_samples)
            / self.num_annotators  # noqa
        )
        self.re_annotation_project = round(
            self.re_proportion * self.single_annotation_project
        )

    def create_example_distribution_df(self):
        """Create a simple DataFrame to test sample distribution."""
        assert self.num_samples is not None, "num_samples must be set"

        data = {"sample_number": range(1, self.num_samples * 2 + 1)}
        df = pd.DataFrame(data)

        return df

    def distribute_samples(
        self,
        df: pd.DataFrame,
        save_path: Optional[str] = None,
        all_reannotation: bool = False,
    ):
        """Distribute samples based on sample distributor
           settings.

        Args:
            df (pd.DataFrame): dataframe containing samples with
                each row being a separate sample - using a copy
                is recommended.
            save_path (str): (Optional) If not None, dir path to save
                             all data to. If not supplied, a dict of
                             allocations is returned. Default None.
            all_reannotation (bool): whether re-annotations should be sampled
                from all the user's annotations rather than just single
                annotations. In this case, a double annotation project amount
                is sampled from all their annotations.

        Returns:
            dict: Mapping from usernames to assigned samples.
        """
        assert self.num_samples is not None, "num_samples must be set"
        assert self.annotators is not None, "annotators must be set"
        assert (
            self.double_annotation_project is not None
        ), "double_annotation_project must be set"
        assert (
            self.double_proportion is not None
        ), "double_proportion must be set"  # noqa
        assert (
            self.single_annotation_project is not None
        ), "single_annotation_project must be set"
        assert (
            self.re_annotation_project is not None
        ), "re_annotation_project must be set"

        if len(df) < self.num_samples:
            raise ValueError(
                f"DataFrame does not contain enough samples. len(df) [{len(df)}] < num_samples [{self.num_samples}]."  # noqa
            )

        # add sample_id to allow final dataset compilation
        df["sample_id"] = range(len(df))

        # create annotator dict
        annotations_dict = {user: [] for user in self.annotators}

        for i, current_annotator in enumerate(self.annotators):
            link_1_idx = (i + 1) % self.num_annotators
            link_2_idx = (i + 2) % self.num_annotators
            link_1_annotator = self.annotators[link_1_idx]
            link_2_annotator = self.annotators[link_2_idx]
            re_annotation_samples = None

            # single annotations
            if self.double_proportion < 1:
                df, single_samples = sample_without_replacement(
                    df, self.single_annotation_project
                )
                single_samples["is_reannotation"] = False

                annotations_dict[current_annotator].append(single_samples)

                if not all_reannotation:
                    re_annotation_samples = single_samples.sample(
                        self.re_annotation_project
                    )
                    re_annotation_samples["is_reannotation"] = True
                    annotations_dict[current_annotator].append(
                        re_annotation_samples
                    )  # noqa

            # double annotations
            if self.double_annotation_project > 0:
                df, first_double_samples = sample_without_replacement(
                    df, self.double_annotation_project
                )
                first_double_samples["is_reannotation"] = False

                annotations_dict[current_annotator].append(first_double_samples)  # noqa
                annotations_dict[link_1_annotator].append(first_double_samples)  # noqa

                df, second_double_samples = sample_without_replacement(
                    df, self.double_annotation_project
                )
                second_double_samples["is_reannotation"] = False

                annotations_dict[current_annotator].append(
                    second_double_samples
                )  # noqa
                annotations_dict[link_2_annotator].append(second_double_samples)  # noqa

        if len(df) > 0:
            annotations_dict["left_over"] = [df]

        for user, df_list in annotations_dict.items():
            # concat all user's dataframes
            user_df = pd.concat(df_list, ignore_index=True)
            # sample from all if not from singles
            if all_reannotation and user != "left_over":
                re_annotation_samples = user_df.sample(
                    self.re_annotation_project
                )  # noqa
                re_annotation_samples["is_reannotation"] = True
                user_df = pd.concat(
                    [user_df, re_annotation_samples], ignore_index=True
                )  # noqa
            # save df
            if save_path is not None:
                user_df.to_csv(f"{save_path}/{user}.csv", index=False)
            annotations_dict[user] = user_df

        return annotations_dict

    def __str__(self):
        """String representation of sample distribution."""
        return (
            f"Variables:\n"
            f"num_annotators (n): {self.num_annotators}\n"
            f"time_available (t): {self.time_available}\n"
            f"annotation_rate (rho): {self.annotation_rate}\n"
            f"num_samples (k): {self.num_samples}\n"
            f"double_proportion (d): {self.double_proportion}\n"
            f"re_proportion (r): {self.re_proportion}\n"
            f"double_annotation_project: {self.double_annotation_project}\n"
            f"single_annotation_project: {self.single_annotation_project}\n"
            f"re_annotation_project: {self.re_annotation_project}"
        )

    def output_variables(self):
        """Output all variables."""
        print(self)


class SampleRedistributor(SampleDistributor):

    @classmethod
    def from_sample_distributor(cls, sd: SampleDistributor):
        return cls(
            annotators=sd.annotators,
            #time_available=sd.time_available, # need one missing
            annotation_rate=sd.annotation_rate,
            num_samples=sd.num_samples,
            double_proportion=0.0,
            re_proportion=0.0,
        )

    def distribute_samples(
        self,
        df: pd.DataFrame,
        save_path: Optional[str] = None,
        all_reannotation: bool = False,
    ):
        """Distribute samples based on sample distributor
           settings, avoiding allocating samples to annotators
           that have already annotated it.

        Args:
            df (pd.DataFrame): dataframe containing samples with
                each row being a separate sample. Must contain existing
                annotations in columns of the format {user}_label.
            save_path (str): (Optional) If not None, dir path to save all data to.
                             If not supplied, a dict of allocations is returned.
                             Default None.

        Returns:
        annotations (dict): dict of annotator -> pd.DataFrame with allocations
        """
        assert self.double_proportion == 0.0, "Double annotation not yet supported"
        assert self.re_proportion == 0.0, "Reannotation not yet supported"
        assert self.num_samples is not None, "num_samples must be set"
        assert self.annotators is not None, "annotators must be set"
        assert (
            self.double_annotation_project is not None
        ), "double_annotation_project must be set"
        assert (
            self.double_proportion is not None
        ), "double_proportion must be set"  # noqa
        assert (
            self.single_annotation_project is not None
        ), "single_annotation_project must be set"
        assert (
            self.re_annotation_project is not None
        ), "re_annotation_project must be set"
        assert not all_reannotation, "Reannotation not yet supported"

        if len(df) < self.num_samples:
            raise ValueError(
                f"DataFrame does not contain enough samples. len(df) [{len(df)}] < num_samples [{self.num_samples}]."  # noqa
            )
        # Required by other functions
        if "is_reannotation" not in df.columns:
            df["is_reannotation"] = False

        # to hold allocations
        annotations_dict = {user: [] for user in self.annotators}

        user_re = re.compile(r"(re_)?([\w -_]+)_.+")
        label_cols = [c for c in df.columns if c.endswith("_label")]
        annotator_cols = []
        usernames = []
        for lc in label_cols:
            user_re_match = user_re.match(lc)
            assert user_re_match is not None, "Error initialising user_re_match"
            is_reanno = user_re_match.group(1) is not None
            username = user_re_match.group(2)
            if is_reanno is False and username in self.annotators:
                annotator_cols.append(lc)
                usernames.append(username)
        if len(annotator_cols) < 1:
            raise ValueError("No annotations found in dataframe!")

        # First collect the full sample pool for each annotator
        sample_pools = {}
        for ann_col, username in zip(annotator_cols, usernames):
            # nan examples haven't been annotated by this user
            sample_pools[username] = list(df.index[df[ann_col].isna()])

        # Allocate examples round-robin style, which ensures each
        # annotator gets approximately the same number of samples.
        idxs_to_drop = []
        num_failed = 0
        user_idx = 0
        for i, sample in df.iterrows():
            num_users_tried = 0
            while True:
                cur_idx = user_idx % len(annotator_cols)
                ann_col = annotator_cols[cur_idx]
                username = usernames[cur_idx]
                num_users_tried += 1
                user_idx += 1
                if i in sample_pools[username]:
                    annotations_dict[username].append(sample)
                    idxs_to_drop.append(i)
                    break
                if num_users_tried == len(usernames):
                    num_failed += 1
                    break

        for user, annos in annotations_dict.items():
            annotations_dict[user] = pd.DataFrame(annos)

        df.drop(idxs_to_drop, inplace=True)
        if len(df) > 0:
            warnings.warn(
                f"Not all examples were able to be allocated ({len(df)})! Try increasing the number of annotators."
            )  # noqa
            annotations_dict["left_over"] = df

        if save_path is not None:
            for user, user_df in annotations_dict.items():
                user_df.to_csv(f"{save_path}/{user}.csv", index=False)

        return annotations_dict
