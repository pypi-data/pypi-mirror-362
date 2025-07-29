import os
import time
import logging
import asyncio
import pandas as pd
from typing import List
from datetime import datetime
from datetime import date
from dotenv import load_dotenv
from financial_engine.database.s3 import S3
from financial_engine.database.mongo import ASyncMongoClient
from financial_engine.utilities.parser import DocumentParser
from financial_engine.utilities.cacher import RatioCacher
from financial_engine.calculations.ratios import FinancialRatios
from financial_engine.constants.constants import MONGO_FILTER_FIELDS

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

semaphore = asyncio.Semaphore(20)

class FinancialEngine:
    """
    An Engine class that allows calculting Financial Ratios in 2 flavours 
    1. Single Alpha_code(company) and Single Date
    2. Single Alpha_code(company) and Range of dates (start_date, end_date)
    View README for detailed Documentation
    """
    def __init__(self):
        mongo_uri = os.getenv("MONGO_URI")
        db_name = os.getenv("MONGO_DATABASE")
        collection_name = os.getenv("MONGO_COLLECTION")
        bucket_name = os.getenv("BUCKET_NAME")

        if not all([mongo_uri, db_name, collection_name, bucket_name]):
            raise EnvironmentError("Missing one or more required environment variables: MONGO_URI, MONGO_DATABASE, MONGO_COLLECTION, BUCKET_NAME")
 
        self.mongo_client = ASyncMongoClient(mongo_uri=mongo_uri)
        self.db_name = db_name
        self.collection_name = collection_name
        self.bucket_name = bucket_name


    async def get_ratio(self, alpha_code:str=None, date:datetime=None) -> dict | None:
        """
        Calculates financial ratio for a single company (using alphacode) and date
        """
        if alpha_code is None or date is None:
            logging.error("Required variables alpha_code and date were not passed.")
            return None

        ## TIMING the total wait
        logging.info(f"Processing alpha_code: {alpha_code} for date: {date}...")
        start = time.time()

        try:
            ## 1. Extract Company Document
            extract_mongo_start = time.time()
            company_document = await self.__extract_mongo_data(alpha_code=alpha_code)
            if company_document is None:
                logging.error(f"Document for alpha_code: {alpha_code} does not exist.")
                return None
            logging.info(f"Extraction time Mongo: {time.time()-extract_mongo_start}")
                    

            ## 2. Extract Trading View data
            extract_tv_start = time.time()
            s3_client = S3(bucket_name=self.bucket_name)
            trading_view_df = await s3_client.extract_trading_view_data(alpha_code, date)
            if trading_view_df is None:
                return None
            market_cap = trading_view_df['market_cap'].iloc[0]
            logging.info(f"Extraction time TV: {time.time()-extract_tv_start}")

            ## 3. Parse The Company Document
            extract_parse_start = time.time()
            parsed_company_document = await FinancialEngine.__extract_parsed_document(alpha_code=alpha_code, 
                                                                                    date=date, 
                                                                                    company_document=company_document)
            
            if parsed_company_document is None:
                return None
            parsed_company_document['alpha_code'] = alpha_code
            parsed_company_document['market_cap'] = market_cap
            logging.info(f"Exttaction time Parser: {time.time()-extract_parse_start}")

            ## 4. Calculating Ratios
            extract_calc_start = time.time()
            calculator = FinancialRatios(company_document=parsed_company_document)
            roll_values = calculator.extract_rolling_values()
            ratio_values = FinancialRatios.calculate_ratios(market_cap=market_cap, roll_values_dict={"roll_values":roll_values})
            final_result = {
                "alpha_code":alpha_code,
                "calculation_date":date, 
                "market_cap":market_cap ,
                "roll_values": roll_values,
                "ratio_values":ratio_values
            }
            logging.info(f"Extraction time calculation: {time.time()-extract_calc_start}")

            end = time.time()
            return {
                "time":(end-start),
                "today_date":datetime.today().date(), 
                "results":final_result
            }
        
        except Exception as e:
            logging.error(f"ERROR FinancialEngine -> (get_ratio): {e}")
            return None
        


    async def get_ratio_range(self, alpha_code:str=None, start_date:datetime=None, end_date:datetime=None) -> dict | None:
        """
        Calculate financial ratios for a single company (using alpha_code) , start and end date
        """
        if alpha_code is None:
            logging.error("Required parameter alpha_code was not passed.")
            return None


        if start_date and end_date and end_date < start_date:
            logging.error(f"End date cannot be smaller than start date")
            return None


        logging.info(f"Processing alpha_code: {alpha_code} --> date range: {start_date} :: {end_date}")
        start = time.time()

        try:
            # 1. Extract TV data for all the dates for alpha_code
            extract_tv_start = time.time()
            s3_client = S3(bucket_name=self.bucket_name)
            trading_view_df = await s3_client.extract_trading_view_data(alpha_code, start_date, end_date)
            if trading_view_df is None:
                return None
            dates = pd.to_datetime(trading_view_df['datetime']).dt.date.tolist()
            logging.info(f"Exttaction time TV: {time.time()-extract_tv_start}")

            # 2. Extract Mongo document for the alpha_code
            extract_mongo_start = time.time()
            company_document = await self.__extract_mongo_data(alpha_code=alpha_code)
            if company_document is None:
                logging.error(f"Document for alpha_code: {alpha_code} does not exist.")
                return None
            logging.info(f"Exttaction time Mongo: {time.time()-extract_mongo_start}")

            extract_parse_start = time.time()
            parsed_company_document = await self.__extract_parsed_document(alpha_code=alpha_code, company_document=company_document, date=end_date)
            if parsed_company_document is None:
                return None

            ## Handling Quarter and Balancesheet -> Extract document , dates
            quarters = parsed_company_document.get("financial_results", None)
            balancesheet = parsed_company_document.get("balance_sheet", None)
            quarter_dates = [date.date() for date in quarters['report_date']]
            balancesheet_dates = [date.date() for date in balancesheet['report_date']]

            ## Extracting closest quarters to work with inital dates (provided start_dates)
            quarter_start = FinancialRatios.extract_closest_quarter(data_list=quarter_dates, date=start_date.date() if start_date else dates[0])
            balancesheet_start = FinancialRatios.extract_closest_quarter(data_list=balancesheet_dates, date=start_date.date() if start_date else dates[0])
            quarter_dates = quarter_dates[quarter_start:]
            balancesheet_dates = balancesheet_dates[balancesheet_start:]
            logging.info(f"Exttaction time Parser: {time.time()-extract_parse_start}")

            raw_data = {
                "dates":dates,
                "alpha_code":alpha_code,
                "balancesheet":balancesheet,
                "balancesheet_dates":balancesheet_dates,
                "quarter":quarters,
                "quarter_dates":quarter_dates,
                "trading_view":trading_view_df
            }

            # 3. Caching Mechanism
            extract_calc_start = time.time()
            cacher = RatioCacher(raw_company_data=raw_data)
            final_result_dict = cacher.iterate()
            if final_result_dict is None:
                return None
            logging.info(f"Exttaction time Calc: {time.time()-extract_calc_start}")
            
            end = time.time()
            return {
                "time":(end-start),
                "today_date":datetime.today().date(), 
                "results":final_result_dict
            }
        
        except Exception as e:
            logging.error(f"ERROR FinancialEngine -> (get_ratio_range): {e}")
            return None
        

    async def get_ratios_range_multiple(self, alpha_codes:List[str]=None, start_date:datetime=None, end_date:datetime=None) -> dict | None:
        """
        Calculates financial ratios for multiple alpha_codes over range of dates
        :NOTE -> BETA
        - if dates not provided -> calculations would be for all the dates for all alpha_codes in the list
        - start_date and end_date is None -> calculations from earliest till latest date in trading view
        - Start date is None : calculation from earliest date till end_date in trading view
        - end_date is None: calculations from the start_date till latest date in trading view
        """
        if alpha_codes is None:
            logging.error("Alpha codes were not passed in...")
            return None
        
        
        if start_date and end_date and end_date < start_date:
            logging.error(f"End date cannot be smaller than start date")
            return None
        
        try:
            start = time.time()
            final_results = {}

            async def worker(alpha_code:str):
                key = f"AI_{alpha_code}_{start_date}_{end_date}"
                async with semaphore:
                    result = await self.get_ratio_range(
                        alpha_code=alpha_code,
                        start_date=start_date,
                        end_date=end_date
                    )
                    final_results[key] = result

            ## Setting up the tasjss
            tasks = [asyncio.create_task(worker(code)) for code in alpha_codes]
            await asyncio.gather(*tasks)

            end = time.time()
            final_results = {"time":(end-start), "today_date": datetime.today().date(), **final_results}
            return final_results
        
        except Exception as e:
            logging.error(f"ERROR FinancialEngine -> (get_ratios_range_multiple): {e}")
            return None



    ########## HELPER FUNCTIONS ##########
    async def __extract_mongo_data(self, alpha_code:str=None) -> dict | None:
        """
        Helper function to extract the mongo data
        """
        if alpha_code is None:
            logging.error("Alpha_code to extract mongo document was not provided")
            return None

        try:
            filter_query = {"alpha_code":alpha_code}
            company_document = await self.mongo_client.find_one_record(
                filter_query=filter_query,
                database_name=self.db_name,
                collection_name=self.collection_name,
                filter_fields=MONGO_FILTER_FIELDS
            )
            return company_document
        except Exception as e:
            logging.error(f"ERROR FinancialEngine -> (extract_mongo_data): {e}")
            return None
        

    @staticmethod
    async def __extract_parsed_document(alpha_code:str=None, company_document:dict=None, date:datetime=None) -> pd.DataFrame | None:
        """
        Helper Function for parsing the company document extracted from mongo db
        """
        try:
            parser = DocumentParser()
            parsed_company_document = parser.parse(company_document=company_document, date=date)
            if parsed_company_document is None:
                logging.warning(f"Document for alpha_code: {alpha_code} was not parsed")
                return None

            # For dates Lower than quarter
            quarterly = parsed_company_document['financial_results']
            if quarterly.empty or quarterly is None:
                logging.warning(f"No Quarters available for processing alpha_code: {alpha_code} at date: {date.date()}")
                return None    
            return parsed_company_document
        
        except Exception as e:
            logging.error(f"ERROR FinancialEngine -> (extract_parsed_document): {e}")
            return None

    