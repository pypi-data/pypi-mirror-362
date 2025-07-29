import logging
from datetime import date
from financial_engine.constants.constants import ROLL_RATIO_KEYS

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class FinancialRatios:
    """
    Class Responsible for calculating Financial Ratios 
    """
    def __init__(self, company_document:dict):
        self.company_document = company_document
        self.alpha_code = self.company_document.get("alpha_code", None)
        self.quarter = self.company_document.get("financial_results", None)
        self.balancesheet = self.company_document.get("balance_sheet", None)
        self.market_cap = self.company_document.get("market_cap", None)

    @staticmethod
    def __safe_division(market_cap:float=None, last_roll:float=None) -> float | None:
        """
        Handles division of numbers
        """
        if last_roll == 0:
            logging.error("Division by Zero Not possible")
            return None
        return market_cap / last_roll
    

    @staticmethod
    def extract_closest_quarter(data_list:list=None, date:date=None) -> int | None:
        """
        Binary Search algorithm that returns closest quarter 
        quar
        EX : date : 2022 - 01 - 01 -> Return 2021-12-31
        T/C : O (log n)
        """
        if data_list is None or date is None:
            logging.error("Date or date_list wasnt passed.")
            return None
        

        start = mid = 0
        end = len(data_list)-1
        valid_index = -1 

        while start <= end:
            mid = (start + end)//2
            
            if data_list[mid] <= date:
                valid_index = mid
                start = mid + 1

            elif data_list[mid] > date:
                end = mid - 1
        
        return valid_index
    
    
    ## MAJOR FUNCTION -> Ratios Calculations
    @staticmethod
    def calculate_ratios(market_cap:float=None, roll_values_dict:dict=None) -> dict | None:
        """
        Computes financial ratios on basis of company_dict's roll_values
        T/C : Fixed Number of Roll values and ratios thus  O(1) * 8
        """
        try:
            ratios = {}

            if roll_values_dict is None:
                logging.error("No data")
                return None
            
            ## Extracting market cap
            if market_cap is None:
                logging.error("No market cap found~")
                return None
            
            for key in ROLL_RATIO_KEYS:
                roll_values = roll_values_dict.get('roll_values', {}).get(key, [])
                if roll_values is None:
                    logging.error(f"{ROLL_RATIO_KEYS[key]} key is not aviailable")
                    continue
                latest_value = roll_values[-1] if isinstance(roll_values, list) else roll_values
                ratios[ROLL_RATIO_KEYS[key]] = FinancialRatios.__safe_division(market_cap=market_cap, last_roll=latest_value)
            
            return ratios
        
        except Exception as e:
            logging.error(f"ERROR FinancialRatios (calculate_ratios) -> {e}")
            return None


    ## BASE FUNCTION : calculating roll
    def __calculate_roll(self, column_name:str=None, window=4) -> list | None:
        """
        Calculates rolling value for a defined column and defined window size
        """
        if column_name is None:
            logging.error("Rolling Calculation requires column name")
            return None
        
        try:
            ## P1 Preprcoessing
            temp_sorted = self.quarter.copy()
            values = temp_sorted[column_name].fillna(0)
            
            ## Not enough values
            if len(values) < window:
                message = f"Not enough quarters to process for rolling for {column_name} : {None}"
                logging.warning(message)
                return None
            
            ## calc rolling num
            rolled_values = values.rolling(window=window).sum().dropna()
            return rolled_values.tolist()

        except Exception as e:
            logging.error(f"ERROR FinancialRatios (calculate_roll) -> {e}")
            return None

    
    
    def roll_pat(self, window=4) -> list | None:
        """
        Calculates rolling PAT of the data
        """
        try:
            ## P1 Preprcoessing
            temp_sorted = self.quarter.copy()
            columns = temp_sorted.columns.tolist()

            if 'net_profit' in columns:
                logging.info("using net_profit ... ")
                temp_sorted['pat'] = temp_sorted['net_profit']
            else:
                logging.error("No suitable PAT-related column found.")
                return None
                
            ## Rolling
            temp_sorted['pat'] = temp_sorted['pat'].fillna(0)

            if len(temp_sorted) < window:
                message = f"Not enough quarters to process for rolling for PAT : {None}"
                logging.warning(message)
                return None

            rolled_values = temp_sorted['pat'].rolling(window=window).sum().dropna()
            return rolled_values.tolist()
        
        except Exception as e:
            logging.error(f"ERROR FinancialRatios (roll_pat) -> {e}")
            return None

    

    def roll_adj_pat(self, window=4) -> list | None:
        """
        Calculates adjusted rolling PAT of the data
        """
        try:
            ## P1 Preprcoessing
            temp_sorted = self.quarter.copy()
            columns = temp_sorted.columns.tolist()
            
            if 'net_profit' in columns:
                logging.info("using net_profit ... ")
                temp_sorted['pat'] = temp_sorted['net_profit']
            else:
                logging.error("No suitable PAT-related column found.")
                return None

            temp_sorted['pat'] = temp_sorted['pat'].fillna(0)
            temp_sorted['tax'] = temp_sorted['tax'].fillna(0)
            temp_sorted['exceptional_items'] = temp_sorted['exceptional_items'].fillna(0)
            temp_sorted['profit_before_tax'] = temp_sorted['profit_before_tax'].fillna(0)

            ## Calc adjusted pat
            temp_sorted['adj_pat'] = temp_sorted['pat'] + temp_sorted['exceptional_items'] * (
                1 - (temp_sorted['tax'] / temp_sorted['profit_before_tax'])
            ).fillna(0)

            if len(temp_sorted) < 4:
                message = f"Not enough quarters to process for rolling for PAT: {self.alpha_code}"
                logging.warning(message)
                return None
            
            rolled_values = temp_sorted['adj_pat'].rolling(window=window).sum().dropna()
            return rolled_values.tolist()
        
        except Exception as e:
            logging.error(f"ERROR FinancialRatios (roll_adj_pat) -> {e}")
            return None


    def calculate_book(self) -> float | None:
        """
        Calculates book value
        """
        try:
            temp_sorted = self.balancesheet.copy()
            temp_sorted['reserves'] = temp_sorted['reserves'].fillna(0)
            temp_sorted['equity_share_capital'] = temp_sorted['equity_share_capital'].fillna(0)

            temp_sorted['book_value'] = temp_sorted['reserves'] + temp_sorted['equity_share_capital']
            latest_book_value = temp_sorted['book_value'].iloc[-1]
            return latest_book_value
        
        except Exception as e:
            logging.error(f"ERROR FinancialRatios (calculate_book) -> {e}")
            return None


    def calculate_enterprise_value(self) -> float | None:
        """
        Calculates Enterprise value
        """
        try:
            temp_sorted = self.balancesheet.copy()
            temp_sorted['borrowings'] = temp_sorted['borrowings'].fillna(0)
            temp_sorted['cash_and_bank'] = temp_sorted['cash_and_bank'].fillna(0)

            latest_debt = temp_sorted['borrowings'].iloc[-1]
            latest_cash = temp_sorted['cash_and_bank'].iloc[-1]
            latest_market_cap = self.market_cap

            return latest_market_cap + latest_debt - latest_cash
        
        except Exception as e:
            logging.error(f"ERROR FinancialRatios (calculate_enterprise_value) -> {e}")
            return None

    

    def extract_rolling_values(self) -> dict:
        """
        Hanlder function for managing rolling values
        """
        return {
            "roll_pat":self.roll_pat(),
            "roll_adj_pat":self.roll_adj_pat(),
            "book_value":self.calculate_book(),
            "enterprise_value":self.calculate_enterprise_value(),
            "roll_ebitda":self.__calculate_roll('operating_profit'),
            "roll_pbt":self.__calculate_roll("profit_before_tax"),
            "roll_netprofit":self.__calculate_roll("net_profit"),
            "roll_sales":self.__calculate_roll("sales"),
        }