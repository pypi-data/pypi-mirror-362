"""
CONSTANTS
:NOTE DO NOT MODFIY UNLESS YOU ARE AWARE OF WHAT NEEDS TO BE DONE
"""

## MONGO CLIENT SETTINGS
MONGO_FILTER_FIELDS = {
    "alpha_code":1,
    "financial_results":1,
    "balance_sheet":1,
}


## PRIORIRY DEFINED IN CONSTANTS
#PRIORITY_ORDER = ['screener_consolidated', 'tijori_consolidated', 'screener_standalone', 'tijori_standalone']
PRIORITY_ORDER = ['tijori_consolidated', 'screener_consolidated', 'tijori_standalone', 'screener_standalone']
DOCUMENT_KEYS =  ['financial_results', 'balance_sheet']
ROLL_RATIO_KEYS = {
            "roll_pat":       "p_to_e",
            "roll_adj_pat":   "adj_p_to_e",
            "roll_ebitda":    "pebitda",
            "roll_pbt":       "pricepbt",
            "roll_netprofit": "pricepat",
            "roll_sales":     "pricesales",
            "book_value":     "pbook",
            "enterprise_value": "ev_ebitda"
        }