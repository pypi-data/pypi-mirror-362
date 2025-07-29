from cca import CCA
from finqual import Finqual
import time

if __name__ == '__main__':

    # --- Comparable company analysis

    start = time.time()

    test = CCA("MSFT")
    df_p = test.profitability_ratios(2024)
    df_l = test.liquidity_ratios(2024)
    df_v = test.valuation_ratios(2024)

    end = time.time()
    print(end - start)

    # ---

    year_1 = 2024
    quarter_1 = None
    ticker_1 = "ORCL"

    ticker_1 = Finqual(ticker_1)

    df_inc = ticker_1.income_stmt(year_1, quarter_1)
    df_inc1 = ticker_1.income_stmt_period(2023,2025, True)

    df_bsh = ticker_1.balance_sheet(year_1, quarter_1)
    df_bsh1 = ticker_1.balance_sheet_period(2020, 2021, True)

    df_cfs = ticker_1.cash_flow(year_1, quarter_1)
    df_cfs1 = ticker_1.cash_flow_period(2020, 2026, True)

    df_pr = ticker_1.profitability_ratios(2024, 3)
    df_lr = ticker_1.liquidity_ratios(2024, 3)

    a = ticker_1.profitability_ratios_period(2022, 2024, True)
    b = ticker_1.liquidity_ratios_period(2022, 2024, False)
    c = ticker_1.valuation_ratios(2024)
