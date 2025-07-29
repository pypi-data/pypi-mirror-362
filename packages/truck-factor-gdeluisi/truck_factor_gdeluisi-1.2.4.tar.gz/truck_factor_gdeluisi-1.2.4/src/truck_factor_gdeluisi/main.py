
from tempfile import gettempdir
from .helper import *
import pandas as pd
from math import log1p

def _filter_dead_files(df:pd.DataFrame,current_files:Iterable[str])->pd.DataFrame:
    new_df=df.loc[df["fname"].isin(current_files)]
    return new_df

def filter_files_of_interest(df:pd.DataFrame):
    files=df["fname"].unique()
    exts=infer_programming_language(files)
    # print(exts)
    exts=resolve_programming_languages(exts)
    # print(exts)
    tmp_df=df.copy()
    tmp_df["ext"]=df["fname"].apply(lambda f: "."+f.rsplit(".",1)[1] if len(f.rsplit(".",1))>1 else "")
    tmp_df=tmp_df.loc[tmp_df["ext"].isin(exts)]
    tmp_df.reset_index(drop=True,inplace=True)
    return tmp_df

def create_contribution_dataframe(repo:str,only_of_files=True)->pd.DataFrame:
    with ThreadPoolExecutor(max_workers=max_worker) as executor:
        logs=executor.submit(write_logs,repo)
        alias_map=executor.submit(get_aliases,repo)
        current_files=set(subprocess.check_output(f"git -C \"{repo}\" ls-files",shell=True).decode()[:-1].split('\n'))
    contributions=parse_logs(logs.result())
    df=pd.DataFrame(contributions)
    df["date"]=pd.to_datetime(df["date"])
    df.replace(alias_map.result(),inplace=True)
    df=_filter_dead_files(df,current_files)
    if only_of_files:
        df=filter_files_of_interest(df)
    return df

def _compute_DOA(row:pd.Series):
    DL=row["tot_contributions"]
    FA=1 if row["author"] == row["author_FA"] else 0
    AC=row["tot_contributions_TOT"] - DL
    DOA=3.293 + 1.098 *  FA + 0.164* DL - 0.321 *  log1p(AC)
    return DOA

def compute_DOA(contributions:pd.DataFrame)->pd.DataFrame:
    """Computes the Degree Of Authorship of each author for each file

    Args:
        contributions (pd.DataFrame): contributions dataframe (Obtained from create_contribution_dataframe function)

    Returns:
        pd.DataFrame: Dataframe representing the the DOA distribution
    """
    if contributions.empty:
        return contributions
    #DOA=3.293 + 1.098 × FA(md, fp) + 0.164×DL(md, fp) − 0.321 × ln(1 + AC (md, fp))
    df=contributions.sort_values("date")
    df=df.groupby(["fname","author","date"]).sum().reset_index(drop=False)
    #drop all 0 contributions
    df=df.loc[df["tot_contributions"]!=0]
    df["DOA"]=0
    tracked_files=df["fname"].unique()
    per_author_df=df.groupby(["fname","author"]).sum(True).reset_index(drop=False)
    per_file_df=per_author_df.groupby(["fname"]).sum(True)
    first_authors=df.groupby("fname").first()
    per_author_df_tmp=per_author_df.set_index("fname").join(first_authors,rsuffix="_FA",on="fname")
    per_author_df_tmp=per_author_df_tmp.join(per_file_df,rsuffix="_TOT",on="fname").reset_index(inplace=False)
    per_author_df["DOA"]=per_author_df_tmp.apply(_compute_DOA,axis=1)
    per_author_df["DOA"]=per_author_df.groupby("fname",as_index=False)["DOA"].transform(lambda x: x/x.max())
    return per_author_df

def compute_truck_factor(repo:str,orphan_files_threashold:float=0.5,authorship_threshold:float=0.7)->int:
    """Compute the truck factor from a git repository

    Args:
        repo (str): The path to the repository
        orphan_files_threashold (float, optional): Value between 0 and 1 which determines when to stop calculating the truck factor. 1 means all files must be orphans, 0 no file must be orphan. Defaults to 0.5.
        authorship_threshold (float, optional):  Value between 0 and 1 which determines the value from which an author with a normalized DOA over a file can be considered a major file contributor. Defaults to 0.7.

    Raises:
        ValueError: Whether the thresholds are not in the range limit or the repository is not suited for truck factor calculation
        Exception: If git CLI is not on PATH
        ValueError: If submitted repo does not point to a git repository

    Returns:
        int: The integer representing the truck factor for the repository
    """
    if not( (orphan_files_threashold >0 and orphan_files_threashold <=1 ) and (authorship_threshold >0 and authorship_threshold <=1 )):
        raise ValueError("All threshold values must have a value between 0 and 1")
    #https://arxiv.org/abs/1604.06766
    if not is_git_available():
        raise Exception("No git CLI found on PATH")
    if not is_dir_a_repo(repo):
        raise ValueError(f"Path {repo} is not a git directory")
    df=create_contribution_dataframe(repo)
    if not( (orphan_files_threashold >0 and orphan_files_threashold <=1 ) and (authorship_threshold >0 and authorship_threshold <=1 )):
        raise ValueError("All threshold values must have a value between 0 and 1")
    #https://arxiv.org/abs/1604.06766
    if df.empty:
        raise ValueError("Repository not suited for truck factor calculation, no source code found")
    df=compute_DOA(df)
    return compute_truck_factor_from_contributions(df)
    
def compute_truck_factor_from_contributions(df:pd.DataFrame,orphan_files_threashold:float=0.5,authorship_threshold:float=0.7)->int:
    """Compute the truck factor from a contribution dataframe (Look at compute_DOA function)

    Args:
        df (pd.DataFrame): contribution dataframe
        orphan_files_threashold (float, optional): Value between 0 and 1 which determines when to stop calculating the truck factor. 1 means all files must be orphans, 0 no file must be orphan. Defaults to 0.5.
        authorship_threshold (float, optional):  Value between 0 and 1 which determines the value from which an author with a normalized DOA over a file can be considered a major file contributor. Defaults to 0.7.

    Raises:
        ValueError: Whether the thresholds are not in the range limit or the repository is not suited for truck factor calculation

    Returns:
        int: The integer representing the truck factor for the repository
    """
    df=df.loc[df["DOA"]>=authorship_threshold]
    orig_size=len(df["fname"].unique())
    quorum=orig_size*orphan_files_threashold
    per_author_files=pd.DataFrame()
    tmp_df=df.groupby("author").count().reset_index(drop=False)
    per_author_files["author"]=tmp_df["author"]
    per_author_files["fname"]=tmp_df["fname"]
    per_author_files.sort_values("fname",ascending=False,inplace=True)
    tf=0
    for row in per_author_files.itertuples(index=False,name="Author"):
        author=row.author
        df=df.loc[df["author"]!=author]
        tf+=1
        if len(df["fname"].unique())<=quorum:
            break
    return tf