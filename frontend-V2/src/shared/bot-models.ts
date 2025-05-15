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

export enum TraderType {
  SIMPLE_THRESHOLD = "SIMPLE_THRESHOLD",
  VOLUME_PRICE_ANALYSIS = "VOLUME_PRICE_ANALYSIS",
}

export interface DataFrequency {
  days: number;
  hours: number;
  minutes: number;
  seconds: number;
}

export interface BaseTraderCreationRequest {
  trader_type: TraderType;
  name: string;
  cash: number;
  paper?: boolean; // optional with default true
  init_data?: Record<string, any>; // optional dict equivalent
  data_frequency: DataFrequency;
}

export interface SimpleThresholdTraderCreationRequest extends BaseTraderCreationRequest {
  trader_type: TraderType.SIMPLE_THRESHOLD;
  ticker: string;
  buy_threshold: number;
  sell_threshold: number;
}

export interface VPATraderCreationRequest extends BaseTraderCreationRequest {
  trader_type: TraderType.VOLUME_PRICE_ANALYSIS;
  ticker: string;
  timespan: Timespan;
  window: number;
  volume_sensitivity: number;
  selloff_percentage: number;
  stoploss_percentage: number;
}

export const baseTraderFieldDescriptions: Record<keyof BaseTraderCreationRequest, string> = {
  trader_type: "The type of trader logic to use.",
  name: "The display name for this trader instance.",
  cash: "The initial capital allocated to the trader.",
  paper: "Whether this trader is in paper (simulated) mode. Defaults to true.",
  init_data: "Optional data to initialize the trader's state.",
  data_frequency: "The frequency at which the trader will fetch data and run its algorithm."
};

export const simpleThresholdTraderFieldDescriptions: Record<keyof SimpleThresholdTraderCreationRequest, string> = {
  ...baseTraderFieldDescriptions,
  ticker: "The stock or crypto ticker symbol this trader will operate on.",
  buy_threshold: "The price at or below which the trader will buy.",
  sell_threshold: "The price at or above which the trader will sell."
};

export const vpaTraderFieldDescriptions: Record<keyof VPATraderCreationRequest, string> = {
  ...baseTraderFieldDescriptions,
  ticker: "The stock or crypto ticker symbol this trader will operate on.",
  timespan: "The time interval used to grab historical aggregates.",
  window: "The number of timespan periods used to calculate VPA trends.",
  volume_sensitivity: "How sensitive the trader is to volume changes.",
  selloff_percentage: "The percentage drop that triggers a selloff.",
  stoploss_percentage: "The percentage loss that triggers a stop-loss."
};
