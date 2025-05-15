export type Timespan =
  | 'minute'
  | 'hour'
  | 'day'
  | 'week'
  | 'month'
  | 'quarter'
  | 'year';

export interface TraderState {
    id: string;
    type: string;
    name: string;
    cash_basis: number;
    cash: number;
    profit: number;
    bought_price: number;
    current_price: number;
    holdings: number;
    holding: boolean;
    awaiting_trade_confirmation: boolean;
    order_id?: string | null;
    paper: boolean;
  
    // Shared
    ticker?: string;
  
    // SimpleThresholdTrader specific
    buy_threshold?: number;
    sell_threshold?: number;
  
    // VPA Trader specific
    timespan?: Timespan;
    window?: number;
    volume_sensitivity?: number;
    selloff_percentage?: number;
    stoploss_percentage?: number;
}
  