import pandas as pd 
import get_data_from_web as get_data_from_web
import os

def main(run_mode, I_file, batch_size, f_keywords, f_question, l_column, n_column):
    """
    Processes a CSV file to enrich data with answers from a model.

    This function reads a CSV file, processes a batch of rows, and uses a model 
    to generate answers based on specified keywords and questions. The answers 
    are added to a new column in the DataFrame, and the updated DataFrame is 
    saved to a new CSV file.

    Args:
        run_mode (str): run_mode tell program to use 'R': Remote model or 'L': Local model
        I_file (str): Path to the input CSV file.
        batch_size (int): Number of rows to process from the input file.
        f_keywords (str): Keywords to be used to search on the web.
        f_question (str): Question to be asked to the model.
        l_column (str): Name of the column in the input file containing data 
                        to append to the keywords and questions.
        n_column (str): Name of the new column to store the model's answers.

    Returns:
        None
    """

    df = pd.read_csv(I_file)
    sub_df = df.head(batch_size)

    final_df = sub_df.copy()
    for index, row in sub_df.iterrows():
        anwer = get_data_from_web.main(run_mode, f_keywords + " " + row[l_column], f_question  + " " + row[l_column] + "?")
        #sub_df.at[index, n_column] = anwer
        final_df.loc[index, n_column] = anwer

    # Split the path
    head_tail = os.path.split(I_file)

    dest_file = str(head_tail[0]) + '/' + str(head_tail[1]).split('.')[0] + '_with_' + n_column + '.' + str(head_tail[1]).split('.')[1]

    final_df.to_csv(f'{dest_file}', index=False)
    print(f"File saved as {dest_file}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Gets anwer from get_data_from_web program, sends it to the model and finally our model answers to question asked")

    # Define positional argument
    parser.add_argument("run_mode", type=str, help="run_mode tell program to use 'R': Remote model or 'L': Local model")
    parser.add_argument("I_file", type=str, help="Input csv file with data")
    parser.add_argument("batch_size", type=int, help="Get the data from input csv file in batch of this size")
    parser.add_argument("f_keywords", type=str, help="Fillable keywords to search in web")
    parser.add_argument("f_question", type=str, help="question to ask")
    parser.add_argument("l_column", type=str, help="Lookup column which will be used to fill the f_keywords and f_question sentences")
    parser.add_argument("n_column", type=str, help="New column name to store the answer which will get added at the end of new csv file.")

    # Parse arguments from command line
    args = parser.parse_args()
    main(run_mode=args.run_mode, I_file=args.I_file, batch_size=args.batch_size, f_keywords=args.f_keywords, f_question=args.f_question, l_column=args.l_column, n_column=args.n_column)
