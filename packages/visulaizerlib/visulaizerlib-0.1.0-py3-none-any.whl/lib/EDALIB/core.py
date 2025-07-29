import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from typing import Tuple, Literal, List, Optional
import math
warnings.filterwarnings("ignore")



def inspect_dataframe(data: pd.DataFrame) -> pd.DataFrame:

    try:
        print(f"Data Frame Info :")

        print("-" * 40)

        data.info()

        print("-" * 40)

        count_duplicated = data.duplicated().sum()

        print(f"Duplicated Sum Of Count : {int(count_duplicated)}")

        print("-" * 40)

        print(f"Missing Values Per Columns:")

        print("-" * 40)

        print(data.isnull().sum())

        print("-" * 40)

        missing_columns_values = data.columns[data.isnull().any()]
        print(f"Missing value Colums : {missing_columns_values}")

        print("-" * 40)

        summary_statistics = data.describe()

        return summary_statistics

    except Exception as e:
        print(f"Error Occured In : {e}")
        raise



def split_numeric_and_categorical_columns(data: pd.DataFrame) -> Tuple[list, list]:

    try:
        print(f"Shape of Data : {data.shape}")

        print("-----------------------------------------------")

        numerical_columns = data.select_dtypes(include=np.number).columns.tolist()
        print(f"The lenght of Numerical Data Are : {len(numerical_columns)}")

        print("------------------------------------------------")

        print(f"Numerical column list : {numerical_columns}")

        print("------------------------------------------------")

        categorical_columns = data.select_dtypes(include=np.object_).columns.tolist()
        print(f"The lenght of Categorical Data Are : {len(categorical_columns)}")

        print("------------------------------------------------")

        print(f"Categorical columns list : {categorical_columns}")

        return (
            numerical_columns,
            categorical_columns
        )
    except Exception as e:
        print(f"Error Occured In: {e}")    



def univariant_analysis_of_all_numeric_columns_plot(
    numerical_columns: list,
    n: int,
    data: pd.DataFrame,
    plot_name: Literal["hist", "box", "violin", "kde"] = None
) -> plt.Figure:

    try:
        ncols = 2
        nrows = math.ceil(n / ncols)

        fig, ax = plt.subplots(ncols=ncols, nrows=nrows, figsize=(6 * ncols, 4 * nrows))
        fig.suptitle(f"Univariate Analysis of Numeric Columns ({plot_name})", fontsize=16)
        ax = ax.flatten()

        for i, col in enumerate(numerical_columns):
            if plot_name == "hist":
                ax[i].hist(data[col].dropna(), bins=25, color="orange", edgecolor="black")
                ax[i].set_title(f"{col} Histogram")
                ax[i].set_xlabel(col)
                ax[i].set_ylabel("Frequency")

            elif plot_name == "box":
                ax[i].boxplot(data[col].dropna(), patch_artist=True,
                              boxprops=dict(facecolor="black", color="black"),
                              medianprops=dict(color="red"))
                ax[i].set_title(f"{col} Boxplot")
                ax[i].set_ylabel(col)
            elif plot_name == "violin":
                sns.violinplot(y=data[col], ax=ax[i], color="Violet")
                ax[i].set_title(f"{col} violin plot")
                ax[i].set_xlabel(col)
            elif plot_name == "kde":
                series = data[col].dropna()
                if len(series.unique()) > 1:
                   sns.kdeplot(series, ax=ax[i], fill=True, color="orange")
                   ax[i].set_title(f"{col} KDE Plot")
                   ax[i].set_xlabel(col)
                   ax[i].set_ylabel("Density")

                   mean_val = series.mean()
                   std_val = series.std()
                   skew_val = series.skew()

                   stats_text = f"Mean: {mean_val:.2f}\nStd: {std_val:.2f}\nSkew: {skew_val:.2f}"
                   ax[i].text(0.95, 0.95, stats_text, ha='right', va='top', fontsize=9,
                              transform=ax[i].transAxes, bbox=dict(facecolor='white', alpha=0.5))
                else:
                    ax[i].set_title(f"{col} - Skipped (No variation)")
                    ax[i].text(0.5, 0.5, 'Flat or empty data', ha='center', va='center')
                    print(f"Skipped KDE for '{col}' — Not enough variation.")
            else:
                raise ValueError("Invalid plot_name. Use 'hist', 'box', violin or kde.")


        for j in range(i + 1, len(ax)):
            fig.delaxes(ax[j])

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()

        if plot_name == "hist":
            # Print skewness
            print("-" * 40)
            print("📉 Skewness of All Numeric Columns:")
            print(data[numerical_columns].skew())



    except Exception as e:
        print(f"Error occurred in plot function: {e}")
        return None
    


def bivariate_analysis_of_all_numeric_categorical_plots(
    data: pd.DataFrame,
    plot_name: Literal[
        "ScatterPlot", "LinePlot", "BoxPlot", "ViolinPlot",
        "CorrHeatmap", "JointPlot", "RegressionPlot",
        "BarPlot", "SwarmPlot", "HexbinPlot"
    ],
    column_pairs: List[Tuple[str, str]] = None,
    hue_scatter: str = None,
    fig_size: Tuple[int, int] = (6, 4)
) -> plt.Figure:

    import seaborn as sns
    import matplotlib.pyplot as plt
    import math

    try:
        plot_type = plot_name.lower()

        if plot_type == "corrheatmap" and not column_pairs:
            corr = data.select_dtypes(include=["number"]).corr()
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
            ax.set_title("Full Correlation Matrix (All Numeric Columns)")
            plt.tight_layout()
            plt.show()
            return fig

        if not column_pairs:
            raise ValueError("'column_pairs' must be provided for this plot type.")

        n = len(column_pairs)
        ncols = 2
        nrows = math.ceil(n / ncols)

        fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(fig_size[0]*ncols, fig_size[1]*nrows))
        axs = axs.flatten()

        for i, (x, y) in enumerate(column_pairs):
            ax = axs[i]

            if plot_type == "scatterplot":
                sns.scatterplot(data=data, x=x, y=y, hue=hue_scatter, ax=ax)
                ax.set_title(f"{x} vs {y} (Scatter)")

            elif plot_type == "lineplot":
                sns.lineplot(data=data, x=x, y=y, ax=ax)
                ax.set_title(f"{y} over {x} (Line)")

            elif plot_type == "boxplot":
                sns.boxplot(data=data, x=x, y=y, ax=ax)
                ax.set_title(f"{y} by {x} (Box)")

            elif plot_type == "violinplot":
                sns.violinplot(data=data, x=x, y=y, ax=ax)
                ax.set_title(f"{y} by {x} (Violin)")

            elif plot_type == "regressionplot":
                sns.regplot(data=data, x=x, y=y, ax=ax, scatter=True, line_kws={"color": "red"})
                ax.set_title(f"{x} vs {y} (Regression)")

            elif plot_type == "barplot":
                sns.barplot(data=data, x=x, y=y, ax=ax, estimator="mean", ci=None)
                ax.set_title(f"{y} by {x} (Bar)")

            elif plot_type == "swarmplot":
                sns.swarmplot(data=data, x=x, y=y, ax=ax)
                ax.set_title(f"{y} by {x} (Swarm)")

            elif plot_type == "hexbinplot":
                # Must use matplotlib's hexbin for 2D numeric
                ax.hexbin(data[x], data[y], gridsize=30, cmap="Blues", mincnt=1)
                ax.set_title(f"{x} vs {y} (Hexbin)")
                ax.set_xlabel(x)
                ax.set_ylabel(y)

            elif plot_type == "corrheatmap":
                corr = data[[x, y]].corr()
                sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
                ax.set_title(f"Correlation: {x} & {y}")

            elif plot_type == "jointplot":
                sns.jointplot(data=data, x=x, y=y, kind="scatter", hue=hue_scatter)
                plt.subplots_adjust(top=0.9, bottom=0.1)
                plt.figure(figsize=(1, 1))  # spacing trick
                fig.delaxes(ax)
                continue

            else:
                ax.set_title("Unsupported plot type")
                ax.text(0.5, 0.5, "Invalid plot", ha='center')
                print("! support only ScatterPlot, LinePlot, BoxPlot, ViolinPlot,\
                      CorrHeatmap, JointPlot, RegressionPlot,\
                      BarPlot, SwarmPlot, HexbinPlot")

        for j in range(i + 1, len(axs)):
            fig.delaxes(axs[j])

        plt.tight_layout()
        plt.subplots_adjust(wspace=0.3, hspace=0.4)
        plt.show()

    except Exception as e:
        print(f"Error Occurred In: {e}")
        raise



def multivariate_analysis_all_numeric_and_categorical_plots(
    data: pd.DataFrame,
    plot_name: Literal[
        "PairPlot", "CorrHeatmap", "FacetGrid",
        "3DScatter", "BubblePlot", "MissingHeatmap"
    ],
    hue: Optional[str] = None,
    x: Optional[str] = None,
    y: Optional[str] = None,
    z: Optional[str] = None,
    size: Optional[str] = None,
    facet_col: Optional[str] = None
) -> Optional[plt.Figure]:

    try:
        plot_type = plot_name.lower()

        if plot_type == "pairplot":
            fig = sns.pairplot(data.select_dtypes(include="number"), hue=hue)
            plt.suptitle("Pair Plot", y=1.02)
            return fig

        elif plot_type == "corrheatmap":
            fig, ax = plt.subplots(figsize=(10, 8))
            corr = data.select_dtypes(include="number").corr()
            sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
            ax.set_title("🔗 Correlation Heatmap")
            #plt.tight_layout()
            plt.close(fig)
            return fig

        elif plot_type == "missingheatmap":
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(data.isnull(), cbar=False, cmap="viridis", ax=ax)
            ax.set_title("Missing Value Heatmap")
            #plt.tight_layout()
            plt.close(fig)
            return fig

        elif plot_type == "facetgrid":
            if not all([facet_col, x, y]):
                raise ValueError("facet_col, x, and y must be provided for FacetGrid.")
            g = sns.FacetGrid(data, col=facet_col, height=4, aspect=1.2)
            g.map_dataframe(sns.lineplot, x=x, y=y)
            g.set_titles("{col_name}")
            g.fig.suptitle("Facet Grid Line Plot", y=1.02)
            return g.fig

        elif plot_type == "3dscatter":
            if not all([x, y, z]):
                raise ValueError("x, y, and z must be provided for 3DScatter.")
            fig = plt.figure(figsize=(8, 6))
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(data[x], data[y], data[z], color="skyblue", edgecolor="black")
            ax.set_xlabel(x)
            ax.set_ylabel(y)
            ax.set_zlabel(z)
            ax.set_title("3D Scatter Plot")
            plt.tight_layout()
            plt.close(fig)
            return fig

        elif plot_type == "bubbleplot":
            if not all([x, y, size]):
                raise ValueError("x, y, and size must be provided for BubblePlot.")
            fig, ax = plt.subplots(figsize=(8, 6))

            size_values = data[size] / data[size].max() * 1000

            ax.scatter(data[x], data[y], s=size_values, alpha=0.6, color="coral", edgecolor="black")
            ax.set_xlabel(x)
            ax.set_ylabel(y)
            ax.set_title(f"Bubble Plot: {x} vs {y} (Size: {size})")

            plt.tight_layout()
            #display(fig)
            plt.close(fig)
            return fig

        else:
            raise ValueError(f"Unsupported plot type: {plot_name}")

    except Exception as e:
        print(f"Error occurred: {e}")
        return None    
    


def categorical_visualization_plot(
    data: pd.DataFrame,
    cat_cols: List[str],
    num_cols: Optional[List[str]] = None,
    plot_type: Literal["countplot", "barplot", "piechart"] = "countplot",
    x: Optional[str] = None,
    ncols: int = 2,
    fig_size: Tuple[int, int] = (6, 4)
) -> plt.Figure:

    try:
        if plot_type == "countplot":
            n = len(cat_cols)
            nrows = math.ceil(n / ncols)
            fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(fig_size[0]*ncols, fig_size[1]*nrows))
            axs = axs.flatten()

            for i, col in enumerate(cat_cols):
                sns.countplot(data=data, x=col, ax=axs[i], palette="Set2")
                axs[i].set_title(f"Count of {col}")
                axs[i].tick_params(axis='x', rotation=45)

            for j in range(i + 1, len(axs)):
                fig.delaxes(axs[j])

            plt.tight_layout()
            return fig

        elif plot_type == "barplot":
            if num_cols is None:
                raise ValueError("❌ 'num_cols' must be provided for barplot.")

            n = len(cat_cols) * len(num_cols)
            nrows = math.ceil(n / ncols)
            fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(fig_size[0]*ncols, fig_size[1]*nrows))
            axs = axs.flatten()

            idx = 0
            for cat in cat_cols:
                for num in num_cols:
                    sns.barplot(data=data, x=cat, y=num, ax=axs[idx], estimator="mean", palette="coolwarm")
                    axs[idx].set_title(f"Avg {num} by {cat}")
                    axs[idx].tick_params(axis='x', rotation=45)
                    idx += 1

            for j in range(idx, len(axs)):
                fig.delaxes(axs[j])

            plt.tight_layout()
            return fig

        elif plot_type == "piechart":
            if not x:
                raise ValueError("❌ 'x' must be provided for PieChart.")
            counts = data[x].value_counts()
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90)
            ax.set_title(f"Distribution of {x}")
            ax.axis('equal')
            plt.tight_layout()
            return fig

        else:
            raise ValueError("❌ Unsupported plot type. Use: 'countplot', 'barplot', or 'piechart'.")

    except Exception as e:
        print(f"❌ Error occurred: {e}")
        return None    

