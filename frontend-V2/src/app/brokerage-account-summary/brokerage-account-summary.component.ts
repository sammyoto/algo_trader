import { Component } from '@angular/core';

@Component({
  selector: 'app-brokerage-account-summary',
  imports: [],
  templateUrl: './brokerage-account-summary.component.html',
  styleUrl: './brokerage-account-summary.component.css'
})
export class BrokerageAccountSummaryComponent {
  account_value: number = 0;
  cash: number = 0;
}
