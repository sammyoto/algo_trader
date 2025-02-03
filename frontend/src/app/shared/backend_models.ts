export interface Trader_Metadata {
    type: string;
    ticker: string;
}

export interface Schwab_Trader_Data {
    trader_data:    {
                    ticker: string, 
                    market_price: string,
                    last_price: string,
                    current_holdings : string,
                    account_cash : string,
                    trend : string,
                    session_profit : string,
                    last_action_price : string,
                    last_action : string,
                    last_pivot : string
                    }
    ticker_data:    {
                    key: string,
                    delayed: boolean, 
                    assetMainType: string, 
                    assetSubType: string, 
                    cusip: string, 
                    1: any, 
                    2: any, 
                    3: any, 
                    4: any, 
                    5: any, 
                    6: any, 
                    7: any, 
                    8: any
                    }
}