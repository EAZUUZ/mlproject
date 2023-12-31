#import dependencies for logging and custom exception
import os
import sys

### added to fix src load issue, then use python -m src.components.data_ingestion
#### because following code did not work: python src/components/data_ingestion.py
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
###

from exception import CustomException
from logger import logging


#import dependencies for data ingestion
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass #Used for class variables

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig
from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer

#decorater
@dataclass
class DataIngestionConfig:
    # inputs for data ingestion config test, train, raw
    train_data_path: str = os.path.join('artifacts', 'train.csv')
    test_data_path: str = os.path.join('artifacts', 'test.csv')
    raw_data_path: str = os.path.join('artifacts', 'data.csv')

    
class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()
        
    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            df=pd.read_csv("notebook\data\stud.csv")
            logging.info('Read data as a dataframe')
            #create directory for train // combine directory path name
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            #save raw data path
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            logging.info("Raw data has been saved")
            #Train test start
            logging.info("Train test split initiated")
            test_data, train_set= train_test_split(df, test_size=0.2, random_state=42)
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_data.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            logging.info('Data ingestion complete')
            
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
            )
        except Exception as e:
            raise CustomException(e,sys)

#initiate data ingestion
## use python -m src.components.data_ingestion
if __name__=="__main__":
    obj = DataIngestion()

    train_data, test_data = obj.initiate_data_ingestion()
    data_transformation=DataTransformation()
    train_arr,test_arr,_=data_transformation.initiate_data_transformation(train_data,test_data)

    modeltrainer=ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr,test_arr))
