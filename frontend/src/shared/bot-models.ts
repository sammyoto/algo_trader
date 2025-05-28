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
    timestamp: Date;
    type: string;
    name: string;
    market: MarketType;
    status: TraderStatus;
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

export enum TraderType {
  SIMPLE_THRESHOLD = "simple_threshold",
  VOLUME_PRICE_ANALYSIS = "vpa",
}

export enum MarketType {
  STOCKS = "stocks",
  CRYPTO = "crypto"
}

export enum TraderStatus {
  ACTIVE = "active",
  RETIRED = "retired"
}

export interface DataFrequency {
  days: number;
  hours: number;
  minutes: number;
  seconds: number;
}

export interface TraderCreationRequest {
  trader_type: TraderType;
  name: string;
  cash: string;
  market: MarketType;
  paper?: boolean; // optional with default true
  init_data?: Record<string, any>; // optional dict equivalent
  data_frequency: DataFrequency;
  ticker?: string;
  buy_threshold?: string;
  sell_threshold?: string;
  timespan?: Timespan;
  window?: number;
  volume_sensitivity?: number;
  selloff_percentage?: number;
  stoploss_percentage?: number;
}