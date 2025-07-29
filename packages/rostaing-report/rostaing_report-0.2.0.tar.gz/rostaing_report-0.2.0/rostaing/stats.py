# rostaing/stats.py : V4 (International Version with Plotly Visualization)

import pandas as pd
import numpy as np
from scipy import stats
from tabulate import tabulate

# --- STATISTICAL & UTILITY IMPORTS ---
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.inter_rater import fleiss_kappa
import pingouin as pg
from lifelines import KaplanMeierFitter, CoxPHFitter
from lifelines.statistics import logrank_test
from sklearn.metrics import cohen_kappa_score
import matplotlib.pyplot as plt

# --- NEW VISUALIZATION IMPORT ---
import plotly.express as px
import plotly.graph_objects as go


class rostaing_report:
    """
    Main class for Exploratory Data Analysis (EDA), statistical tests,
    correlation analysis, survival analysis, and interactive data visualization.
    Takes a Pandas DataFrame as input and provides a comprehensive toolkit.
    """

    def __init__(self, df: pd.DataFrame):
        """
        Initializes the analyzer with a DataFrame.
        Args:
            df (pd.DataFrame): The DataFrame to be analyzed.
        """
        if not isinstance(df, pd.DataFrame):
            raise TypeError("Input must be a Pandas DataFrame.")
        self.df = df
        self.report = {}
        # Initial descriptive analysis is always performed
        self._analyze()

    # ==============================================================================
    # SECTION 1: AUTOMATED DESCRIPTIVE ANALYSIS (Unchanged)
    # ==============================================================================
    # This entire section remains the same as the previous version.
    # To save space, it's collapsed here but included in the full final block.
    def _analyze(self):
        self._overview_analysis()
        self._numerical_analysis()
        self._categorical_analysis()
        self._correlations_analysis()
    def _overview_analysis(self):
        self.report['overview'] = {"Number of Observations (Rows)": self.df.shape[0], "Number of Variables (Columns)": self.df.shape[1], "Total Missing Values (NA)": self.df.isna().sum().sum(), "Overall Missing Values Rate (%)": f"{(self.df.isna().sum().sum() / self.df.size) * 100:.2f}", "Duplicated Rows Count": self.df.duplicated().sum(), "Duplicated Rows Rate (%)": f"{(self.df.duplicated().sum() / len(self.df)) * 100:.2f}", "Memory Usage": f"{self.df.memory_usage(deep=True).sum() / 1024**2:.2f} MB"}
        variable_types_df = pd.DataFrame(self.df.dtypes.value_counts()); variable_types_df.columns = ['Count']; variable_types_df.index.name = 'Variable Type'; self.report['variable_types'] = variable_types_df
    @staticmethod
    def _detect_outliers(series: pd.Series) -> str:
        if not pd.api.types.is_numeric_dtype(series): return "N/A"
        q1 = series.quantile(0.25); q3 = series.quantile(0.75); iqr = q3 - q1
        if iqr == 0: return "No"
        lower_bound = q1 - 1.5 * iqr; upper_bound = q3 + 1.5 * iqr
        return "Yes" if any((series < lower_bound) | (series > upper_bound)) else "No"
    def _numerical_analysis(self):
        num_df = self.df.select_dtypes(include=np.number)
        if num_df.empty: self.report['numerical'] = None; return
        desc = num_df.describe().T
        desc['variance'] = num_df.var(); desc['skewness'] = num_df.skew(); desc['kurtosis'] = num_df.kurtosis(); desc['sem'] = num_df.sem(); desc['mad'] = num_df.apply(lambda x: (x - x.mean()).abs().mean()); desc['missing_count'] = num_df.isna().sum(); desc['missing_percent'] = (desc['missing_count'] / len(num_df)) * 100; desc['unique_count'] = num_df.nunique(); desc['duplicated_count'] = num_df.apply(lambda x: x.duplicated().sum()); desc['has_outliers'] = num_df.apply(self._detect_outliers)
        self.report['numerical'] = desc[['count', 'missing_count', 'missing_percent', 'unique_count', 'duplicated_count', 'has_outliers', 'mean', 'std', 'sem', 'mad', 'min', '25%', '50%', '75%', 'max', 'variance', 'skewness', 'kurtosis']].rename(columns={'std': 'std_dev', '25%': 'Q1', '50%': 'median', '75%': 'Q3'})
    def _categorical_analysis(self):
        cat_df = self.df.select_dtypes(include=['object', 'category', 'bool'])
        if cat_df.empty: self.report['categorical'] = None; return
        desc = cat_df.describe(include=['object', 'category', 'bool']).T
        desc['missing_count'] = cat_df.isna().sum(); desc['missing_percent'] = (desc['missing_count'] / len(cat_df)) * 100; desc['duplicated_count'] = cat_df.apply(lambda x: x.duplicated().sum())
        self.report['categorical'] = desc[['count', 'missing_count', 'missing_percent', 'unique', 'duplicated_count', 'top', 'freq']]
    @staticmethod
    def _interpret_correlation(r: float) -> str:
        r_abs = abs(r)
        if r_abs >= 0.9: strength = "Very Strong"
        elif r_abs >= 0.7: strength = "Strong"
        elif r_abs >= 0.5: strength = "Moderate"
        elif r_abs >= 0.3: strength = "Weak"
        else: return "Negligible"
        direction = "Positive" if r > 0 else "Negative"
        return f"{strength} {direction}"
    def _correlations_analysis(self, top_n=10):
        num_df = self.df.select_dtypes(include=np.number)
        if num_df.shape[1] < 2: self.report['correlations'] = None; return
        corr_matrix = num_df.corr(); corr_pairs = corr_matrix.unstack().reset_index(); corr_pairs.columns = ['var1', 'var2', 'correlation']; corr_pairs = corr_pairs[corr_pairs['var1'] != corr_pairs['var2']]; corr_pairs['pair_key'] = corr_pairs.apply(lambda row: tuple(sorted((row['var1'], row['var2']))), axis=1); corr_pairs = corr_pairs.drop_duplicates(subset=['pair_key']); corr_pairs['abs_correlation'] = corr_pairs['correlation'].abs(); corr_pairs = corr_pairs.sort_values('abs_correlation', ascending=False).drop(columns=['pair_key', 'abs_correlation']); corr_pairs['interpretation'] = corr_pairs['correlation'].apply(self._interpret_correlation)
        self.report['correlations'] = corr_pairs.head(top_n)
    def _format_html(self):
        html = "<h1>Rostaing Report</h1>"; html += "<h2>Overview Statistics</h2>"; html += tabulate(self.report['overview'].items(), headers=['Statistic', 'Value'], tablefmt='html')
        if self.report.get('variable_types') is not None: html += "<h2>Variable Types</h2>"; html += self.report['variable_types'].to_html(classes='table table-striped')
        if self.report.get('numerical') is not None: html += "<h2>Numerical Variables Analysis</h2>"; html += self.report['numerical'].to_html(classes='table table-striped', float_format='{:.3f}'.format)
        if self.report.get('categorical') is not None: html += "<h2>Categorical Variables Analysis</h2>"; html += self.report['categorical'].to_html(classes='table table-striped')
        if self.report.get('correlations') is not None and not self.report['correlations'].empty: html += "<h2>Top Correlations</h2>"; html += self.report['correlations'].to_html(classes='table table-striped', float_format='{:.3f}'.format, index=False)
        style = "<style> table { width: auto; border-collapse: collapse; margin-bottom: 20px; font-family: sans-serif; } th, td { padding: 8px; text-align: left; border-bottom: 1px solid #ddd; } tr:hover { background-color: #f5f5f5; } th { background-color: #007BFF; color: white; } h1, h2 { color: #333; border-bottom: 2px solid #007BFF; padding-bottom: 5px; } </style>"; return f"{style}{html}"
    def _format_str(self):
        output = "--- Rostaing Report ---\n\n"; output += "=== Overview Statistics ===\n"; output += tabulate(self.report['overview'].items(), headers=['Statistic', 'Value'], tablefmt='grid') + "\n\n"
        if self.report.get('variable_types') is not None: output += "=== Variable Types ===\n"; output += tabulate(self.report['variable_types'], headers='keys', tablefmt='grid') + "\n\n"
        if self.report.get('numerical') is not None: output += "=== Numerical Variables Analysis ===\n"; output += tabulate(self.report['numerical'], headers='keys', tablefmt='grid', floatfmt=".3f") + "\n\n"
        if self.report.get('categorical') is not None: output += "=== Categorical Variables Analysis ===\n"; output += tabulate(self.report['categorical'], headers='keys', tablefmt='grid') + "\n\n"
        if self.report.get('correlations') is not None and not self.report['correlations'].empty: output += "=== Top Correlations ===\n"; output += tabulate(self.report['correlations'], headers='keys', tablefmt='grid', floatfmt=".3f", showindex=False) + "\n"
        return output
    def __repr__(self): return self._format_str()
    def _repr_html_(self): return self._format_html()

    # ==============================================================================
    # SECTIONS 2-5: STATISTICAL ANALYSIS (Unchanged)
    # ==============================================================================
    # These sections (Inferential Stats, Correlation, Survival, Other Metrics)
    # remain the same as the previous version. They are also collapsed for brevity
    # but included in the full final block.
    def normality_test(self, col: str, test: str = 'shapiro', alpha: float = 0.05):
        data = self.df[col].dropna()
        if test.lower() == 'shapiro': stat, p_value = stats.shapiro(data); test_name = "Shapiro-Wilk"
        elif test.lower() == 'jarque_bera': stat, p_value = stats.jarque_bera(data); test_name = "Jarque-Bera"
        elif test.lower() == 'normaltest': stat, p_value = stats.normaltest(data); test_name = "D'Agostino & Pearson"
        else: raise ValueError("Unsupported test. Choose 'shapiro', 'jarque_bera', or 'normaltest'.")
        conclusion = f"The null hypothesis (normality) is rejected (p < {alpha})." if p_value < alpha else f"The null hypothesis (normality) cannot be rejected (p >= {alpha})."
        return {"test": test_name, "column": col, "statistic": stat, "p_value": p_value, f"conclusion (alpha={alpha})": conclusion}
    def ks_test(self, col: str, dist: str = 'norm', alpha: float = 0.05):
        data = self.df[col].dropna(); stat, p_value = stats.kstest(data, dist)
        conclusion = f"The data does not follow a '{dist}' distribution (p < {alpha})." if p_value < alpha else f"The data may follow a '{dist}' distribution (p >= {alpha})."
        return {"test": "Kolmogorov-Smirnov", "column": col, "distribution_tested": dist, "statistic": stat, "p_value": p_value, f"conclusion (alpha={alpha})": conclusion}
    def ttest_1samp(self, col: str, popmean: float, alpha: float = 0.05):
        data = self.df[col].dropna(); stat, p_value = stats.ttest_1samp(data, popmean)
        conclusion = f"Statistically significant difference from the population mean (p < {alpha})." if p_value < alpha else f"No statistically significant difference from the population mean (p >= {alpha})."
        return {"test": "T-test (one-sample)", "column": col, "population_mean": popmean, "t_statistic": stat, "p_value": p_value, f"conclusion (alpha={alpha})": conclusion}
    def ttest_ind(self, col1: str, col2: str, equal_var: bool = True, alpha: float = 0.05):
        data1 = self.df[col1].dropna(); data2 = self.df[col2].dropna(); stat, p_value = stats.ttest_ind(data1, data2, equal_var=equal_var)
        conclusion = f"Statistically significant difference in means (p < {alpha})." if p_value < alpha else f"No statistically significant difference in means (p >= {alpha})."
        return {"test": "T-test (independent)", "columns": f"{col1} vs {col2}", "t_statistic": stat, "p_value": p_value, f"conclusion (alpha={alpha})": conclusion}
    def ttest_paired(self, col1: str, col2: str, alpha: float = 0.05):
        data1 = self.df[col1].dropna(); data2 = self.df[col2].dropna(); common_index = data1.index.intersection(data2.index)
        if len(common_index) < len(data1) or len(common_index) < len(data2): print("Warning: NA values were dropped, which may affect pairing.")
        stat, p_value = stats.ttest_rel(data1.loc[common_index], data2.loc[common_index])
        conclusion = f"Statistically significant difference between pairs (p < {alpha})." if p_value < alpha else f"No statistically significant difference between pairs (p >= {alpha})."
        return {"test": "T-test (paired)", "columns": f"{col1} vs {col2}", "t_statistic": stat, "p_value": p_value, f"conclusion (alpha={alpha})": conclusion}
    def anova_oneway(self, dv: str, between: str, alpha: float = 0.05):
        groups = self.df[between].unique(); samples = [self.df[dv][self.df[between] == group].dropna() for group in groups]; f_stat, p_value = stats.f_oneway(*samples)
        conclusion = f"At least one group mean is significantly different (p < {alpha})." if p_value < alpha else f"No significant difference between group means (p >= {alpha})."
        return {"test": "One-way ANOVA", "dependent_var": dv, "group_var": between, "F_statistic": f_stat, "p_value": p_value, f"conclusion (alpha={alpha})": conclusion}
    def anova_twoway(self, dv: str, between: list, alpha: float = 0.05):
        if len(between) != 2: raise ValueError("Please provide exactly two factors in the 'between' list.")
        formula = f"{dv} ~ C({between[0]}) * C({between[1]})"; model = ols(formula, data=self.df).fit(); anova_table = sm.stats.anova_lm(model, typ=2); return anova_table
    def anova_rm(self, dv: str, within: str, subject: str, aggregate_func='mean'):
        return pg.rm_anova(data=self.df, dv=dv, within=within, subject=subject, detailed=True)
    def chi2_test(self, col1: str, col2: str, alpha: float = 0.05):
        contingency_table = pd.crosstab(self.df[col1], self.df[col2]); chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
        conclusion = f"The variables are dependent (p < {alpha})." if p_value < alpha else f"The variables are independent (p >= {alpha})."
        return {"test": "Chi-squared Test of Independence", "variables": f"{col1} and {col2}", "chi2_statistic": chi2, "p_value": p_value, "degrees_of_freedom": dof, f"conclusion (alpha={alpha})": conclusion, "contingency_table": contingency_table}
    def binomial_test(self, col: str, success_value, p: float = 0.5, alpha: float = 0.05):
        data = self.df[col].dropna(); k = (data == success_value).sum(); n = len(data); result = stats.binomtest(k, n, p); p_value = result.pvalue
        conclusion = f"The proportion of success ({k/n:.2f}) is significantly different from {p} (p < {alpha})." if p_value < alpha else f"The proportion of success ({k/n:.2f}) is not significantly different from {p} (p >= {alpha})."
        return {"test": "Binomial Test", "column": col, "success_count (k)": k, "total_count (n)": n, "p_value": p_value, f"conclusion (alpha={alpha})": conclusion}
    def wilcoxon_test(self, col1: str, col2: str, alpha: float = 0.05):
        data1 = self.df[col1].dropna(); data2 = self.df[col2].dropna(); common_index = data1.index.intersection(data2.index); stat, p_value = stats.wilcoxon(data1.loc[common_index], data2.loc[common_index])
        conclusion = f"Significant difference between paired distributions (p < {alpha})." if p_value < alpha else f"No significant difference between paired distributions (p >= {alpha})."
        return {"test": "Wilcoxon Signed-Rank Test", "columns": f"{col1} vs {col2}", "W_statistic": stat, "p_value": p_value, f"conclusion (alpha={alpha})": conclusion}
    def mann_whitney_u_test(self, dv: str, group_col: str, alpha: float = 0.05):
        groups = self.df[group_col].unique()
        if len(groups) != 2: raise ValueError(f"The grouping column '{group_col}' must have exactly 2 unique groups.")
        group1_data = self.df[self.df[group_col] == groups[0]][dv].dropna(); group2_data = self.df[self.df[group_col] == groups[1]][dv].dropna(); stat, p_value = stats.mannwhitneyu(group1_data, group2_data)
        conclusion = f"The distributions are significantly different (p < {alpha})." if p_value < alpha else f"No significant difference between distributions (p >= {alpha})."
        return {"test": "Mann-Whitney U", "dependent_var": dv, "groups": f"{groups[0]} vs {groups[1]}", "U_statistic": stat, "p_value": p_value, f"conclusion (alpha={alpha})": conclusion}
    def kruskal_wallis_test(self, dv: str, group_col: str, alpha: float = 0.05):
        groups_data = [self.df[self.df[group_col] == g][dv].dropna() for g in self.df[group_col].unique()]; stat, p_value = stats.kruskal(*groups_data)
        conclusion = f"At least one group median is significantly different (p < {alpha})." if p_value < alpha else f"No significant difference between group medians (p >= {alpha})."
        return {"test": "Kruskal-Wallis H", "dependent_var": dv, "group_column": group_col, "H_statistic": stat, "p_value": p_value, f"conclusion (alpha={alpha})": conclusion}
    def friedman_test(self, *cols, alpha: float = 0.05):
        samples = [self.df[col].dropna() for col in cols]; stat, p_value = stats.friedmanchisquare(*samples)
        conclusion = f"At least one condition has a significantly different distribution (p < {alpha})." if p_value < alpha else f"No significant difference between condition distributions (p >= {alpha})."
        return {"test": "Friedman Test", "conditions": list(cols), "statistic": stat, "p_value": p_value, f"conclusion (alpha={alpha})": conclusion}
    def correlation_matrix(self, method: str = 'pearson'):
        return self.df.select_dtypes(include=np.number).corr(method=method)
    def point_biserial_corr(self, binary_col: str, continuous_col: str, alpha: float = 0.05):
        binary_data = self.df[binary_col].dropna(); continuous_data = self.df[continuous_col].dropna(); common_index = binary_data.index.intersection(continuous_data.index)
        stat, p_value = stats.pointbiserialr(binary_data.loc[common_index], continuous_data.loc[common_index])
        conclusion = f"Significant correlation (p < {alpha})." if p_value < alpha else f"No significant correlation (p >= {alpha})."; interpretation = self._interpret_correlation(stat)
        return {"test": "Point-Biserial Correlation", "variables": f"{binary_col} & {continuous_col}", "r_statistic": stat, "p_value": p_value, "interpretation": interpretation, f"conclusion (alpha={alpha})": conclusion}
    def partial_corr(self, x: str, y: str, covar: list, method: str = 'pearson'):
        return pg.partial_corr(data=self.df, x=x, y=y, covar=covar, method=method).round(3)
    def kaplan_meier_curve(self, duration_col: str, event_col: str, group_col: str = None, ax=None):
        kmf = KaplanMeierFitter(); ax = ax or plt.gca()
        if group_col:
            for name, grouped_df in self.df.groupby(group_col): kmf.fit(grouped_df[duration_col], grouped_df[event_col], label=name); kmf.plot_survival_function(ax=ax)
            ax.set_title('Kaplan-Meier Survival Curve by Group')
        else: kmf.fit(self.df[duration_col], self.df[event_col]); kmf.plot_survival_function(ax=ax); ax.set_title('Kaplan-Meier Survival Curve')
        ax.set_xlabel('Time'); ax.set_ylabel('Survival Probability'); return ax
    def logrank_test(self, duration_col: str, event_col: str, group_col: str, alpha: float = 0.05):
        if len(self.df[group_col].unique()) < 2: raise ValueError("Log-rank test requires at least two groups.")
        results = pg.logrank(durations=self.df[duration_col], event=self.df[event_col], group=self.df[group_col]); p_value = results['p-val'].iloc[0]
        conclusion = f"Significant difference between group survival curves (p < {alpha})." if p_value < alpha else f"No significant difference between group survival curves (p >= {alpha})."
        results[f"conclusion (alpha={alpha})"] = conclusion; return results
    def cox_ph_regression(self, duration_col: str, event_col: str, *covariate_cols):
        cph = CoxPHFitter(); df_cox = self.df[[duration_col, event_col, *covariate_cols]].dropna()
        cph.fit(df_cox, duration_col=duration_col, event_col=event_col); return cph.summary
    def test_levene(self, dv: str, group_col: str, alpha: float = 0.05):
        groups = self.df[group_col].unique(); samples = [self.df[dv][self.df[group_col] == g].dropna() for g in groups]; stat, p_value = stats.levene(*samples)
        conclusion = f"The variances are unequal (heteroscedasticity) (p < {alpha})." if p_value < alpha else f"The variances are equal (homoscedasticity) (p >= {alpha})."
        return {"test": "Levene's Test", "dependent_var": dv, "group_var": group_col, "W_statistic": stat, "p_value": p_value, f"conclusion (alpha={alpha})": conclusion}
    def effect_size_cohen_d(self, dv: str, group_col: str):
        if len(self.df[group_col].unique()) != 2: raise ValueError(f"The grouping column '{group_col}' must have exactly 2 unique groups.")
        group1 = self.df[dv][self.df[group_col] == self.df[group_col].unique()[0]].dropna(); group2 = self.df[dv][self.df[group_col] == self.df[group_col].unique()[1]].dropna()
        d = pg.compute_effsize(group1, group2, eftype='cohen'); return {"test": "Effect Size (Cohen's d)", "d": d, "magnitude": pg.effsize.interpret_cohen_d(d)}
    def cronbachs_alpha(self, *items):
        data = self.df[list(items)].dropna(); alpha_results = pg.cronbach_alpha(data=data)
        return {"test": "Cronbach's Alpha", "items": list(items), "alpha": alpha_results[0], "confidence_interval_95%": alpha_results[1]}
    def cohens_kappa(self, col1: str, col2: str, weights: str = None):
        y1 = self.df[col1].dropna(); y2 = self.df[col2].dropna(); common_index = y1.index.intersection(y2.index)
        kappa = cohen_kappa_score(y1.loc[common_index], y2.loc[common_index], weights=weights)
        test_type = "Weighted Cohen's Kappa" if weights else "Cohen's Kappa"; return {"test": test_type, "kappa_score": kappa}
    def fleiss_kappa(self, *rater_cols):
        data = self.df[list(rater_cols)].dropna(); table = data.apply(pd.value_counts, axis=0).T.fillna(0)
        kappa, _ = fleiss_kappa(table, method='fleiss'); return {"test": "Fleiss' Kappa", "raters": list(rater_cols), "kappa_score": kappa}


    # ==============================================================================
    # SECTION 6: DATA VISUALIZATION (PLOTLY EXPRESS)
    # ==============================================================================

    def _plot(self, plot_function, **kwargs) -> go.Figure:
        """
        Internal helper method to call Plotly Express functions.
        Automatically passes the instance's DataFrame.
        """
        # For matrix/image inputs, the data is passed directly, not as a dataframe.
        if plot_function in [px.imshow]:
             return plot_function(**kwargs)
        return plot_function(self.df, **kwargs)
    
    # --- Basic Plots ---
    def scatter(self, **kwargs) -> go.Figure:
        """Wrapper for plotly.express.scatter. See Plotly docs for all available kwargs."""
        return self._plot(px.scatter, **kwargs)

    def line(self, **kwargs) -> go.Figure:
        """Wrapper for plotly.express.line. See Plotly docs for all available kwargs."""
        return self._plot(px.line, **kwargs)

    def bar(self, **kwargs) -> go.Figure:
        """Wrapper for plotly.express.bar. See Plotly docs for all available kwargs."""
        return self._plot(px.bar, **kwargs)

    def area(self, **kwargs) -> go.Figure:
        """Wrapper for plotly.express.area. See Plotly docs for all available kwargs."""
        return self._plot(px.area, **kwargs)

    def funnel(self, **kwargs) -> go.Figure:
        """Wrapper for plotly.express.funnel. See Plotly docs for all available kwargs."""
        return self._plot(px.funnel, **kwargs)

    def timeline(self, **kwargs) -> go.Figure:
        """Wrapper for plotly.express.timeline. See Plotly docs for all available kwargs."""
        return self._plot(px.timeline, **kwargs)

    # --- Part-of-Whole Plots ---
    def pie(self, **kwargs) -> go.Figure:
        """Wrapper for plotly.express.pie. See Plotly docs for all available kwargs."""
        return self._plot(px.pie, **kwargs)

    def sunburst(self, **kwargs) -> go.Figure:
        """Wrapper for plotly.express.sunburst. See Plotly docs for all available kwargs."""
        return self._plot(px.sunburst, **kwargs)

    def treemap(self, **kwargs) -> go.Figure:
        """Wrapper for plotly.express.treemap. See Plotly docs for all available kwargs."""
        return self._plot(px.treemap, **kwargs)

    def icicle(self, **kwargs) -> go.Figure:
        """Wrapper for plotly.express.icicle. See Plotly docs for all available kwargs."""
        return self._plot(px.icicle, **kwargs)

    def funnel_area(self, **kwargs) -> go.Figure:
        """Wrapper for plotly.express.funnel_area. See Plotly docs for all available kwargs."""
        return self._plot(px.funnel_area, **kwargs)

    # --- 1D Distribution Plots ---
    def histogram(self, **kwargs) -> go.Figure:
        """Wrapper for plotly.express.histogram. See Plotly docs for all available kwargs."""
        return self._plot(px.histogram, **kwargs)

    def box(self, **kwargs) -> go.Figure:
        """Wrapper for plotly.express.box. See Plotly docs for all available kwargs."""
        return self._plot(px.box, **kwargs)

    def violin(self, **kwargs) -> go.Figure:
        """Wrapper for plotly.express.violin. See Plotly docs for all available kwargs."""
        return self._plot(px.violin, **kwargs)

    def strip(self, **kwargs) -> go.Figure:
        """Wrapper for plotly.express.strip. See Plotly docs for all available kwargs."""
        return self._plot(px.strip, **kwargs)

    def ecdf(self, **kwargs) -> go.Figure:
        """Wrapper for plotly.express.ecdf. See Plotly docs for all available kwargs."""
        return self._plot(px.ecdf, **kwargs)

    # --- 2D Distribution Plots ---
    def density_heatmap(self, **kwargs) -> go.Figure:
        """Wrapper for plotly.express.density_heatmap. See Plotly docs for all available kwargs."""
        return self._plot(px.density_heatmap, **kwargs)
        
    def density_contour(self, **kwargs) -> go.Figure:
        """Wrapper for plotly.express.density_contour. See Plotly docs for all available kwargs."""
        return self._plot(px.density_contour, **kwargs)

    # --- Matrix/Image Input ---
    def imshow(self, **kwargs) -> go.Figure:
        """Wrapper for plotly.express.imshow. Note: Data is passed directly in kwargs (e.g., img=...)."""
        return self._plot(px.imshow, **kwargs)

    # --- 3D Plots ---
    def scatter_3d(self, **kwargs) -> go.Figure:
        """Wrapper for plotly.express.scatter_3d. See Plotly docs for all available kwargs."""
        return self._plot(px.scatter_3d, **kwargs)

    def line_3d(self, **kwargs) -> go.Figure:
        """Wrapper for plotly.express.line_3d. See Plotly docs for all available kwargs."""
        return self._plot(px.line_3d, **kwargs)

    # --- Multidimensional Plots ---
    def scatter_matrix(self, **kwargs) -> go.Figure:
        """Wrapper for plotly.express.scatter_matrix. See Plotly docs for all available kwargs."""
        return self._plot(px.scatter_matrix, **kwargs)
        
    def parallel_coordinates(self, **kwargs) -> go.Figure:
        """Wrapper for plotly.express.parallel_coordinates. See Plotly docs for all available kwargs."""
        return self._plot(px.parallel_coordinates, **kwargs)
        
    def parallel_categories(self, **kwargs) -> go.Figure:
        """Wrapper for plotly.express.parallel_categories. See Plotly docs for all available kwargs."""
        return self._plot(px.parallel_categories, **kwargs)

    # --- Map Plots ---
    def scatter_geo(self, **kwargs) -> go.Figure:
        """Wrapper for plotly.express.scatter_geo. See Plotly docs for all available kwargs."""
        return self._plot(px.scatter_geo, **kwargs)

    def line_geo(self, **kwargs) -> go.Figure:
        """Wrapper for plotly.express.line_geo. See Plotly docs for all available kwargs."""
        return self._plot(px.line_geo, **kwargs)
        
    def choropleth(self, **kwargs) -> go.Figure:
        """Wrapper for plotly.express.choropleth. See Plotly docs for all available kwargs."""
        return self._plot(px.choropleth, **kwargs)
        
    # --- Tile Map Plots (Mapbox) ---
    def scatter_mapbox(self, **kwargs) -> go.Figure:
        """Wrapper for plotly.express.scatter_mapbox. Requires a Mapbox token."""
        return self._plot(px.scatter_mapbox, **kwargs)
        
    def line_mapbox(self, **kwargs) -> go.Figure:
        """Wrapper for plotly.express.line_mapbox. Requires a Mapbox token."""
        return self._plot(px.line_mapbox, **kwargs)
        
    def choropleth_mapbox(self, **kwargs) -> go.Figure:
        """Wrapper for plotly.express.choropleth_mapbox. Requires a Mapbox token."""
        return self._plot(px.choropleth_mapbox, **kwargs)
        
    def density_mapbox(self, **kwargs) -> go.Figure:
        """Wrapper for plotly.express.density_mapbox. Requires a Mapbox token."""
        return self._plot(px.density_mapbox, **kwargs)
        
    # --- Polar Plots ---
    def scatter_polar(self, **kwargs) -> go.Figure:
        """Wrapper for plotly.express.scatter_polar. See Plotly docs for all available kwargs."""
        return self._plot(px.scatter_polar, **kwargs)
        
    def line_polar(self, **kwargs) -> go.Figure:
        """Wrapper for plotly.express.line_polar. See Plotly docs for all available kwargs."""
        return self._plot(px.line_polar, **kwargs)
        
    def bar_polar(self, **kwargs) -> go.Figure:
        """Wrapper for plotly.express.bar_polar. See Plotly docs for all available kwargs."""
        return self._plot(px.bar_polar, **kwargs)

    # --- Ternary Plots ---
    def scatter_ternary(self, **kwargs) -> go.Figure:
        """Wrapper for plotly.express.scatter_ternary. See Plotly docs for all available kwargs."""
        return self._plot(px.scatter_ternary, **kwargs)
        
    def line_ternary(self, **kwargs) -> go.Figure:
        """Wrapper for plotly.express.line_ternary. See Plotly docs for all available kwargs."""
        return self._plot(px.line_ternary, **kwargs)


# # rostaing/stats.py : V2

# import pandas as pd
# import numpy as np
# from scipy import stats
# from tabulate import tabulate

# # ### CORRIGÉ : Nom de la classe pour correspondre à l'importation de l'utilisateur ###
# class rostaing_report:
#     """
#     Main class for Exploratory Data Analysis (EDA) and statistical tests.
#     Takes a Pandas DataFrame as input and generates a comprehensive report.
#     """

#     def __init__(self, df: pd.DataFrame):
#         """
#         Initializes the analyzer with a DataFrame.
#         Args:
#             df (pd.DataFrame): The DataFrame to be analyzed.
#         """
#         if not isinstance(df, pd.DataFrame):
#             raise TypeError("Input must be a Pandas DataFrame.")
#         self.df = df
#         self.report = {}
#         self._analyze()

#     def _analyze(self):
#         """Runs all descriptive analysis methods."""
#         self._overview_analysis()
#         self._numerical_analysis()
#         self._categorical_analysis()
#         self._correlations_analysis()

#     def _overview_analysis(self):
#         """General analysis of the DataFrame and its composition."""
#         self.report['overview'] = {
#             "Number of Observations (Rows)": self.df.shape[0],
#             "Number of Variables (Columns)": self.df.shape[1],
#             "Total Missing Values (NA)": self.df.isna().sum().sum(),
#             "Overall Missing Values Rate (%)": f"{(self.df.isna().sum().sum() / self.df.size) * 100:.2f}",
#             "Duplicated Rows Count": self.df.duplicated().sum(),
#             "Duplicated Rows Rate (%)": f"{(self.df.duplicated().sum() / len(self.df)) * 100:.2f}",
#             # ### RÉINTÉGRÉ : Taille mémoire du DataFrame ###
#             "Memory Usage": f"{self.df.memory_usage(deep=True).sum() / 1024**2:.2f} MB"
#         }

#         variable_types_df = pd.DataFrame(self.df.dtypes.value_counts())
#         variable_types_df.columns = ['Count']
#         variable_types_df.index.name = 'Variable Type'
#         self.report['variable_types'] = variable_types_df

#     @staticmethod
#     def _detect_outliers(series: pd.Series) -> str:
#         """Detects outliers in a numerical series using the IQR method."""
#         if not pd.api.types.is_numeric_dtype(series):
#             return "N/A"
#         q1 = series.quantile(0.25)
#         q3 = series.quantile(0.75)
#         iqr = q3 - q1
#         if iqr == 0:
#             return "No" # Cannot determine outliers if IQR is zero
#         lower_bound = q1 - 1.5 * iqr
#         upper_bound = q3 + 1.5 * iqr
#         return "Yes" if any((series < lower_bound) | (series > upper_bound)) else "No"

#     def _numerical_analysis(self):
#         """Descriptive analysis of numerical variables."""
#         num_df = self.df.select_dtypes(include=np.number)
#         if num_df.empty:
#             self.report['numerical'] = None
#             return

#         desc = num_df.describe().T
#         desc['variance'] = num_df.var()
#         desc['skewness'] = num_df.skew()
#         desc['kurtosis'] = num_df.kurtosis()
#         desc['sem'] = num_df.sem()
#         desc['mad'] = num_df.apply(lambda x: (x - x.mean()).abs().mean())
#         desc['missing_count'] = num_df.isna().sum()
#         desc['missing_percent'] = (desc['missing_count'] / len(num_df)) * 100
#         desc['unique_count'] = num_df.nunique()
#         desc['duplicated_count'] = num_df.apply(lambda x: x.duplicated().sum())
#         desc['has_outliers'] = num_df.apply(self._detect_outliers)

#         self.report['numerical'] = desc[[
#             'count', 'missing_count', 'missing_percent', 'unique_count', 'duplicated_count', 'has_outliers',
#             'mean', 'std', 'sem', 'mad', 'min', '25%', '50%', '75%', 'max', 'variance', 'skewness', 'kurtosis'
#         ]].rename(columns={'std': 'std_dev', '25%': 'Q1', '50%': 'median', '75%': 'Q3'})

#     def _categorical_analysis(self):
#         """Descriptive analysis of categorical variables."""
#         cat_df = self.df.select_dtypes(include=['object', 'category', 'bool'])
#         if cat_df.empty:
#             self.report['categorical'] = None
#             return

#         desc = cat_df.describe(include=['object', 'category', 'bool']).T
#         desc['missing_count'] = cat_df.isna().sum()
#         desc['missing_percent'] = (desc['missing_count'] / len(cat_df)) * 100
#         desc['duplicated_count'] = cat_df.apply(lambda x: x.duplicated().sum())

#         self.report['categorical'] = desc[['count', 'missing_count', 'missing_percent', 'unique', 'duplicated_count', 'top', 'freq']]
        
#     @staticmethod
#     def _interpret_correlation(r: float) -> str:
#         """Provides a textual interpretation of a correlation coefficient."""
#         r_abs = abs(r)
#         if r_abs >= 0.9:
#             strength = "Very Strong"
#         elif r_abs >= 0.7:
#             strength = "Strong"
#         elif r_abs >= 0.5:
#             strength = "Moderate"
#         elif r_abs >= 0.3:
#             strength = "Weak"
#         else:
#             return "Negligible"
            
#         direction = "Positive" if r > 0 else "Negative"
#         return f"{strength} {direction}"

#     def _correlations_analysis(self, top_n=10):
#         """Calculates and reports the most correlated variable pairs with interpretation."""
#         num_df = self.df.select_dtypes(include=np.number)
#         if num_df.shape[1] < 2:
#             self.report['correlations'] = None
#             return
            
#         corr_matrix = num_df.corr()
#         corr_pairs = corr_matrix.unstack().reset_index()
#         corr_pairs.columns = ['var1', 'var2', 'correlation']
#         corr_pairs = corr_pairs[corr_pairs['var1'] != corr_pairs['var2']]
#         corr_pairs['pair_key'] = corr_pairs.apply(lambda row: tuple(sorted((row['var1'], row['var2']))), axis=1)
#         corr_pairs = corr_pairs.drop_duplicates(subset=['pair_key'])
#         corr_pairs['abs_correlation'] = corr_pairs['correlation'].abs()
#         corr_pairs = corr_pairs.sort_values('abs_correlation', ascending=False).drop(columns=['pair_key', 'abs_correlation'])
#         corr_pairs['interpretation'] = corr_pairs['correlation'].apply(self._interpret_correlation)

#         self.report['correlations'] = corr_pairs.head(top_n)

#     def _format_html(self):
#         """Generates the report in HTML format for Jupyter/notebooks."""
#         html = "<h1>Rostaing Report</h1>"

#         html += "<h2>Overview Statistics</h2>"
#         html += tabulate(self.report['overview'].items(), headers=['Statistic', 'Value'], tablefmt='html')

#         if self.report.get('variable_types') is not None:
#             html += "<h2>Variable Types</h2>"
#             html += self.report['variable_types'].to_html(classes='table table-striped')

#         if self.report.get('numerical') is not None:
#             html += "<h2>Numerical Variables Analysis</h2>"
#             html += self.report['numerical'].to_html(classes='table table-striped', float_format='{:.3f}'.format)
        
#         if self.report.get('categorical') is not None:
#             html += "<h2>Categorical Variables Analysis</h2>"
#             html += self.report['categorical'].to_html(classes='table table-striped')
            
#         if self.report.get('correlations') is not None and not self.report['correlations'].empty:
#             html += "<h2>Top Correlations</h2>"
#             html += self.report['correlations'].to_html(classes='table table-striped', float_format='{:.3f}'.format, index=False)

#         style = "<style> table { width: auto; border-collapse: collapse; margin-bottom: 20px; font-family: sans-serif; } th, td { padding: 8px; text-align: left; border-bottom: 1px solid #ddd; } tr:hover { background-color: #f5f5f5; } th { background-color: #007BFF; color: white; } h1, h2 { color: #333; border-bottom: 2px solid #007BFF; padding-bottom: 5px; } </style>"
#         return f"{style}{html}"

#     def _format_str(self):
#         """Generates the report in plain text format for the console."""
#         output = "--- Rostaing Report ---\n\n"

#         output += "=== Overview Statistics ===\n"
#         output += tabulate(self.report['overview'].items(), headers=['Statistic', 'Value'], tablefmt='grid')
#         output += "\n\n"
        
#         if self.report.get('variable_types') is not None:
#             output += "=== Variable Types ===\n"
#             output += tabulate(self.report['variable_types'], headers='keys', tablefmt='grid')
#             output += "\n\n"

#         if self.report.get('numerical') is not None:
#             output += "=== Numerical Variables Analysis ===\n"
#             output += tabulate(self.report['numerical'], headers='keys', tablefmt='grid', floatfmt=".3f")
#             output += "\n\n"

#         if self.report.get('categorical') is not None:
#             output += "=== Categorical Variables Analysis ===\n"
#             output += tabulate(self.report['categorical'], headers='keys', tablefmt='grid')
#             output += "\n\n"
            
#         if self.report.get('correlations') is not None and not self.report['correlations'].empty:
#             output += "=== Top Correlations ===\n"
#             output += tabulate(self.report['correlations'], headers='keys', tablefmt='grid', floatfmt=".3f", showindex=False)
#             output += "\n"

#         return output

#     def __repr__(self):
#         return self._format_str()

#     def _repr_html_(self):
#         return self._format_html()

#     # --- INFERENTIAL STATISTICS METHODS ---

#     def normality_test(self, col: str, test: str = 'shapiro', alpha: float = 0.05):
#         """
#         Performs a normality test on a column. H0: The sample comes from a normal distribution.
        
#         Args:
#             col (str): The column to test.
#             test (str): The test to use. One of 'shapiro', 'jarque_bera', or 'normaltest'.
#             alpha (float): The significance level.
#         """
#         data = self.df[col].dropna()
#         if test.lower() == 'shapiro':
#             stat, p_value = stats.shapiro(data)
#             test_name = "Shapiro-Wilk"
#         elif test.lower() == 'jarque_bera':
#             stat, p_value = stats.jarque_bera(data)
#             test_name = "Jarque-Bera"
#         ### MODIFIÉ : Ajout du test de D'Agostino et Pearson comme option ###
#         elif test.lower() == 'normaltest':
#             stat, p_value = stats.normaltest(data)
#             test_name = "D'Agostino & Pearson's test"
#         else:
#             ### MODIFIÉ : Mise à jour du message d'erreur pour inclure la nouvelle option ###
#             raise ValueError("Unsupported test. Choose 'shapiro', 'jarque_bera', or 'normaltest'.")
        
#         conclusion = f"The null hypothesis (normality) is rejected (p < {alpha})." if p_value < alpha else f"The null hypothesis (normality) cannot be rejected (p >= {alpha})."
#         return {"test": test_name, "column": col, "statistic": stat, "p_value": p_value, f"conclusion (alpha={alpha})": conclusion}

#     ### AJOUT : Nouvelle méthode pour le test de Kolmogorov-Smirnov ###
#     def ks_test(self, col: str, dist: str = 'norm', alpha: float = 0.05):
#         """
#         Performs the Kolmogorov-Smirnov test for goodness of fit.
#         H0: The data comes from the specified distribution.
        
#         Interpretation: This test checks if the distribution of data in a column is
#         significantly different from a theoretical distribution (e.g., 'norm' for normal).
#         A low p-value suggests the data does not follow that distribution.
        
#         Args:
#             col (str): The column of data to test.
#             dist (str or callable): The name of the distribution to test against (e.g., 'norm', 'expon').
#             alpha (float): The significance level for the conclusion.
#         """
#         data = self.df[col].dropna()
#         stat, p_value = stats.kstest(data, dist)
        
#         conclusion = f"The data does not follow a '{dist}' distribution (p < {alpha})." if p_value < alpha else f"The data may follow a '{dist}' distribution (p >= {alpha})."
#         return {"test": "Kolmogorov-Smirnov Test", "column": col, "distribution_tested": dist, "statistic": stat, "p_value": p_value, f"conclusion (alpha={alpha})": conclusion}


#     def ttest_ind(self, col1: str, col2: str, equal_var: bool = True, alpha: float = 0.05):
#         """
#         Performs an independent two-sample T-test. H0: The means of the two samples are equal.
        
#         Interpretation: Used to determine if there is a significant difference between the
#         means of two independent groups. A low p-value indicates the means are likely different.
#         """
#         data1 = self.df[col1].dropna()
#         data2 = self.df[col2].dropna()
#         stat, p_value = stats.ttest_ind(data1, data2, equal_var=equal_var)
#         conclusion = f"Statistically significant difference in means (p < {alpha})." if p_value < alpha else f"No statistically significant difference in means (p >= {alpha})."
#         return {"test": "T-test (independent)", "columns": f"{col1} vs {col2}", "t_statistic": stat, "p_value": p_value, f"conclusion (alpha={alpha})": conclusion}

#     def chi2_test(self, col1: str, col2: str, alpha: float = 0.05):
#         """
#         Performs a Chi-squared test of independence. H0: The two variables are independent.
#         """
#         contingency_table = pd.crosstab(self.df[col1], self.df[col2])
#         chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
#         conclusion = f"The variables are dependent (p < {alpha})." if p_value < alpha else f"The variables are independent (p >= {alpha})."
#         return {"test": "Chi-squared Test of Independence", "variables": f"{col1} and {col2}", "chi2_statistic": chi2, "p_value": p_value, "degrees_of_freedom": dof, f"conclusion (alpha={alpha})": conclusion, "contingency_table": contingency_table}

#     def mann_whitney_u_test(self, col: str, group_col: str, alpha: float = 0.05):
#         """
#         Performs the Mann-Whitney U test for two independent distributions. H0: The distributions are equal.
#         """
#         groups = self.df[group_col].unique()
#         if len(groups) != 2:
#             raise ValueError(f"The grouping column '{group_col}' must have exactly 2 unique groups.")
        
#         group1_data = self.df[self.df[group_col] == groups[0]][col].dropna()
#         group2_data = self.df[self.df[group_col] == groups[1]][col].dropna()
        
#         stat, p_value = stats.mannwhitneyu(group1_data, group2_data)
#         conclusion = f"The distributions are significantly different (p < {alpha})." if p_value < alpha else f"No significant difference between distributions (p >= {alpha})."
#         return {"test": "Mann-Whitney U", "compared_variable": col, "groups": f"{groups[0]} vs {groups[1]}", "U_statistic": stat, "p_value": p_value, f"conclusion (alpha={alpha})": conclusion}

#     def kruskal_wallis_test(self, col: str, group_col: str, alpha: float = 0.05):
#         """
#         Performs the Kruskal-Wallis test for k independent distributions. H0: The medians of all groups are equal.
#         """
#         groups_data = [self.df[self.df[group_col] == g][col].dropna() for g in self.df[group_col].unique()]
        
#         stat, p_value = stats.kruskal(*groups_data)
#         conclusion = f"At least one group median is significantly different (p < {alpha})." if p_value < alpha else f"No significant difference between group medians (p >= {alpha})."
#         return {"test": "Kruskal-Wallis H", "compared_variable": col, "group_column": group_col, "H_statistic": stat, "p_value": p_value, f"conclusion (alpha={alpha})": conclusion}

#     def correlation_matrix(self, method: str = 'pearson'):
#         """
#         Calculates the full correlation matrix for numerical variables.
#         """
#         num_df = self.df.select_dtypes(include=np.number)
#         return num_df.corr(method=method)