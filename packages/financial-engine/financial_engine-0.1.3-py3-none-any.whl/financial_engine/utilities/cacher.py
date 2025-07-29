import logging
from financial_engine.calculations.ratios import FinancialRatios

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)



class RatioCacher:
    """
    A caching utility that efficiently iterates over quarters and balance sheets using a pointer-based mechanism.

    This system is designed to generate and store keys efficiently across a date range, minimizing redundant computation.

    **Key Structure:**
        AI_<alpha_code>_<quarter>_<balancesheet>

    **Performance Example:**

    Without caching:
        n operations → O(n) time
        Example: O(365) = 365 seconds

    With caching (generalized case):
        O(365) = 4 * (full computations: roll + ratio) + 361 * ( ratio calculations)
            ≈ 4 * (0.3 - 0.8 sec) + 361 * (8 * 0.001 sec)
            ≈ 6.088 seconds

    :note: Timing and performance are approximate and based on typical usage patterns.
    """

    def __init__(self, raw_company_data:dict):
        self.alpha_code = raw_company_data.get("alpha_code", None)
        self.dates = raw_company_data.get("dates", None)
        self.balancesheet = raw_company_data.get("balancesheet", None)
        self.quarter = raw_company_data.get("quarter", None)
        self.balancesheet_dates = raw_company_data.get("balancesheet_dates", None)
        self.quarter_dates = raw_company_data.get("quarter_dates", None)
        self.trading_view = raw_company_data.get("trading_view", None)

        ## Results and Cache
        self.key_cache = {}
        self.final_result = []

        ## INDEXS
        self.balancesheet_index = 0
        self.quarter_index = 0

        # Setup -> O(n log n) Lookup -> O(log n)
        self.trading_view.set_index('datetime', inplace=True)
        self.trading_view.sort_index(inplace=True)

        self.balancesheet.set_index('report_date', inplace=True)
        self.balancesheet.sort_index(inplace=True)

        self.quarter.set_index('report_date', inplace=True)
        self.quarter.sort_index(inplace=True)



    def iterate(self):
        """
        Iterate through the dates and calculating financial ratios
        """
        try:
            logging.info(f"Managing ratios for alpha_code: {self.alpha_code}...")
            for date in self.dates:
                result_key = f"AI_{self.alpha_code}_{self.quarter_dates[self.quarter_index]}_{self.balancesheet_dates[self.balancesheet_index]}"
                valid_tv = self.trading_view.loc[date]
                market_cap = valid_tv['market_cap']

                if result_key not in self.key_cache:
                    logging.debug("CACHE MISS %s", result_key)
                    company_document = {
                        "alpha_code":self.alpha_code,
                        "financial_results": self.quarter.loc[:self.quarter_dates[self.quarter_index]],
                        "balance_sheet": self.balancesheet.loc[:self.balancesheet_dates[self.balancesheet_index]],
                        "alpha_code":self.alpha_code,
                        "market_cap":market_cap
                    }
                    calculator = FinancialRatios(company_document=company_document)
                    roll_values = calculator.extract_rolling_values()
                    
                    ratio_values = FinancialRatios.calculate_ratios(market_cap=market_cap, roll_values_dict={"roll_values":roll_values})
                    financial_ratios = {
                        "alpha_code":self.alpha_code, 
                        "calculation_date":date,
                        "market_cap":market_cap, 
                        "roll_values":roll_values, 
                        "ratio_values": ratio_values
                    }
                    
                    ## Caching Key
                    self.key_cache[result_key] = {
                        "alpha_code":self.alpha_code,
                        "roll_values":financial_ratios["roll_values"]
                    }
                    self.final_result.append(financial_ratios)

                else:
                    logging.debug("CACHE HIT %s", result_key)
                    company_dict = self.key_cache.get(result_key, {})
                    roll_values = company_dict.get("roll_values", {})
                    compute_ratios = FinancialRatios.calculate_ratios(market_cap=market_cap, roll_values_dict={"roll_values":roll_values})
                    financial_ratios = {
                        "alpha_code":self.alpha_code,
                        "calculation_date":date,
                        "market_cap":market_cap, 
                        "roll_values":roll_values,
                        "ratio_values":compute_ratios
                    }
                    self.final_result.append(financial_ratios)


                ## Quarter Handling
                if self.quarter_index + 1 < len(self.quarter_dates) and date >= self.quarter_dates[self.quarter_index+1]:
                    #print(f"QD: date: {date} >> report_date: {self.quarter_dates[self.quarter_index]}")
                    self.quarter_index += 1
                
                ## BalacneSheet Handling
                if self.balancesheet_index + 1 < len(self.balancesheet_dates) and date >= self.balancesheet_dates[self.balancesheet_index+1]:
                    #print(f"BD: date: {date} >> report_date: {self.quarter_dates[self.balancesheet_index]}")
                    self.balancesheet_index += 1

            return self.final_result

        except Exception as e:
            logging.error(f"ERROR RatiosCacher -> (iterate): {e}")
            return None