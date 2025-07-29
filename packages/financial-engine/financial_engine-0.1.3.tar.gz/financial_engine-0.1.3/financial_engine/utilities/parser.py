import logging
import pandas as pd
from datetime import datetime
from financial_engine.constants.constants import DOCUMENT_KEYS, PRIORITY_ORDER

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)



class DocumentParser:
    """
    Class Responsible for Parsing Company documents as per priorities
    Extract Proper line items with report_date as factor 
    Current Line items handled -> Quarter, Balancesheet
    # Priority
    1. Screener - Consolidated
    2. Tijori - Consolidated
    3. Screener - Stanalone
    4. Tijori - Standalone
    """
    
    def __process_document(self, document:dict, date:datetime):
        """
        Process quarter document
        """
        merged_dates = set()
        merged_results = []

        if document is None:
            logging.warning("Document provided was None")
            return pd.DataFrame()
        
        ## Phase 2. Traversal
        try:
            for key, records in document.items():
                if key not in PRIORITY_ORDER:
                    logging.warning(f"Key: {key} not in collection")
                    continue

                ## Handlign records
                for record in records:
                    report_date = record.get('report_date', None)
                    if report_date is None:
                        continue

                    if report_date in merged_dates:
                        continue

                    record['source'] = key
                    merged_dates.add(report_date)
                    merged_results.append(record)

            merged_df = pd.DataFrame(merged_results)
            merged_df['report_date'] = pd.to_datetime(merged_df['report_date'], errors='coerce')

            ## TEST ZONE ##
            if date is not None:
                merged_df = merged_df[merged_df['report_date'] <= pd.to_datetime(date)]
            return merged_df.sort_values(by='report_date', ascending=True)
        
        except Exception as e:
            logging.error(f"ERROR (DocumentParser) -> process_document: {key} -> {e}")
            return None
        

    def traverse_all_documents(self, company_document:dict, date:datetime):
        """
        Traverses through financial documents such as financial_results(quarterly), balancesheet and cashflow
        T/C : O(k * (m * n)) -> k is the key( quarter, bs, cf)
        """
        result = {}
        for fin_key in DOCUMENT_KEYS:
            document = company_document.get(fin_key, None)
            if document is None:
                result[fin_key] = None
                continue

            if fin_key == 'financial_results':
                quarterly = document.get("quarterly", None)
                result[fin_key] = self.__process_document(document=quarterly, date=date)
            else:
                result[fin_key] = self.__process_document(document=document, date=date)

        return result
    

    def parse(self, company_document:dict=None, date:datetime=None):
        """
        Handles Parsing of mond
        """
        if company_document is None:
            logging.error("mongo_output must not be None")
            return None

        result_dict = self.traverse_all_documents(company_document=company_document, date=date)
        return result_dict