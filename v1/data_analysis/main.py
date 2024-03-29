import os
import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.schema import Base
from config import settings
from data_analysis.db import add_extracted_info_database
from data_analysis.token import average_token


if __name__ == "__main__":
    # Create a parser object
    parser = argparse.ArgumentParser(description="Create Training Files")
    # Add common command-line arguments
    parser.add_argument("command", help="The command to execute (extract or average)")
    parser.add_argument("-i", "--input_path", help="Method")
    # Parse the command-line arguments
    args = parser.parse_args()

    if args.command == "extract":
        # Base Path for Case Studies Directory
        base_folder_path = "E:/Freelancing/AXEOM/Axeom_EUTraining/CS docs for AI/Generic Case Studies"
        # Create Database Engine
        engine = create_engine(settings.DB_PATH, echo=True)
        # If database not present in file system, then make a new one
        if not os.path.isfile(settings.DB_PATH):
            Base.metadata.create_all(engine)
        # Create a session to interact with the database
        Session = sessionmaker(bind=engine)
        session = Session()
        # Function to execute the extraction and creation of records into DB
        add_extracted_info_database(base_folder_path, session)
        # Close the session after inserting data
        session.close()
    elif args.command == "average-tokens":
        path = args.input_path
        avg_cs_token = average_token(path)  # "./dataset/singleton/summary/overall_score_v2_sample.jsonl"
