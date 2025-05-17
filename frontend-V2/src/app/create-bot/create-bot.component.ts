import { Component } from '@angular/core';
import { NgFor, NgIf} from '@angular/common';
import {FormGroup, FormControl, ReactiveFormsModule} from '@angular/forms';
import { BackendService } from '../../services/backend.service';
import * as BotModels from '../../shared/bot-models';

@Component({
  selector: 'app-create-bot',
  imports: [ReactiveFormsModule, NgFor, NgIf],
  templateUrl: './create-bot.component.html',
  styleUrl: './create-bot.component.css'
})
export class CreateBotComponent {
  trader_types = Object.values(BotModels.TraderType);
  timespan_options: BotModels.Timespan[] = [
    'minute', 'hour', 'day', 'week', 'month', 'quarter', 'year'
  ];
  selected_option = BotModels.TraderType.SIMPLE_THRESHOLD
  errorMessage: string | null = null;

  hoveredField: keyof BotModels.TraderCreationRequest | null = null;

  setHoveredField(field: keyof BotModels.TraderCreationRequest) {
    this.hoveredField = field;
  }
  
  clearHoveredField() {
    this.hoveredField = null;
  }

  AlgoDescriptions: Record<string, string> = {
    "simple_threshold": "A simple trader that buys and sells at certain thresholds.",
    "vpa": "A trader that trades based off of Volume Price Analysis."
  }

  TraderFieldDescriptions: Record<keyof BotModels.TraderCreationRequest, string> = {
    trader_type: "The type of trader logic to use.",
    name: "The display name for this trader instance.",
    cash: "The initial capital allocated to the trader.",
    paper: "Whether this trader is in paper (simulated) mode. Defaults to true.",
    init_data: "Optional data to initialize the trader's state.",
    data_frequency: "The frequency at which the trader will fetch data and run its algorithm.",
    ticker: "The stock or crypto ticker symbol this trader will operate on.",
    buy_threshold: "The price at or below which the trader will buy.",
    sell_threshold: "The price at or above which the trader will sell.",
    timespan: "The time interval used to grab historical aggregates.",
    window: "The number of timespan periods used to calculate VPA trends.",
    volume_sensitivity: "How sensitive the trader is to volume changes.",
    selloff_percentage: "The percentage drop that triggers a selloff.",
    stoploss_percentage: "The percentage loss that triggers a stop-loss."
  };
  
  constructor(private backendService: BackendService) { }

  trader_creation_form = new FormGroup({
    trader_type: new FormControl(this.selected_option),
    name: new FormControl(''),
    cash: new FormControl(''),
    data_frequency: new FormGroup({
      days: new FormControl(0),
      hours: new FormControl(0),
      minutes: new FormControl(0),
      seconds: new FormControl(0),
    }),
    ticker: new FormControl('NVDA'),
    buy_threshold: new FormControl(''),
    sell_threshold: new FormControl(''),
    timespan: new FormControl<BotModels.Timespan | null>('day'),
    window: new FormControl(0),
    volume_sensitivity: new FormControl(0),
    selloff_percentage: new FormControl(0),
    stoploss_percentage: new FormControl(0)
  })

  send_trader_creation_request() {
    if (!this.trader_creation_form.value.trader_type) {
      this.errorMessage = 'Trader type must be selected!';
      return;
    }
    if (!this.trader_creation_form.value.name) {
      this.errorMessage = 'You must enter a name!';
      return;
    }
    if (!this.trader_creation_form.value.cash) {
      this.errorMessage = 'You must enter a cash amount!';
      return;
    }
    const data_frequency : BotModels.DataFrequency = {
      days: this.trader_creation_form.value.data_frequency!.days!,
      hours: this.trader_creation_form.value.data_frequency!.hours!,
      minutes: this.trader_creation_form.value.data_frequency!.minutes!,
      seconds: this.trader_creation_form.value.data_frequency!.seconds!,
    }
    const traderCreationRequest: BotModels.TraderCreationRequest = {
      trader_type: this.trader_creation_form.value.trader_type,
      name: this.trader_creation_form.value.name,
      cash: this.trader_creation_form.value.cash,
      paper: true,
      data_frequency:data_frequency,
      ticker: this.trader_creation_form.value.ticker!,
      buy_threshold: this.trader_creation_form.value.buy_threshold!,
      sell_threshold: this.trader_creation_form.value.sell_threshold!,
      timespan: this.trader_creation_form.value.timespan!,
      window: this.trader_creation_form.value.window!,
      volume_sensitivity: this.trader_creation_form.value.volume_sensitivity!,
      selloff_percentage: this.trader_creation_form.value.selloff_percentage!,
      stoploss_percentage: this.trader_creation_form.value.stoploss_percentage!,
    }

    console.log(traderCreationRequest)
    this.backendService.send_trader_creation_request(traderCreationRequest);
  }

  is_ticker_visible(): boolean {
    const type = this.trader_creation_form.get('trader_type')?.value;
    return type === 'simple_threshold' || type === 'vpa';
  }

  is_buy_threshold_visible(): boolean {
    const type = this.trader_creation_form.get('trader_type')?.value;
    return type === 'simple_threshold';
  }

  is_sell_threshold_visible(): boolean {
    const type = this.trader_creation_form.get('trader_type')?.value;
    return type === 'simple_threshold';
  }

  is_timespan_visible(): boolean {
    const type = this.trader_creation_form.get('trader_type')?.value;
    return type === 'vpa';
  }

  is_window_visible(): boolean {
    const type = this.trader_creation_form.get('trader_type')?.value;
    return type === 'vpa';
  }

  is_volume_sensitivity_visible(): boolean {
    const type = this.trader_creation_form.get('trader_type')?.value;
    return type === 'vpa';
  }

  is_selloff_percentage_visible(): boolean {
    const type = this.trader_creation_form.get('trader_type')?.value;
    return type === 'vpa';
  }

  is_stoploss_percentage_visible(): boolean {
    const type = this.trader_creation_form.get('trader_type')?.value;
    return type === 'vpa';
  }
}
