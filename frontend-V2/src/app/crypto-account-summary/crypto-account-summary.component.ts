import { Component } from '@angular/core';

@Component({
  selector: 'app-crypto-account-summary',
  imports: [],
  templateUrl: './crypto-account-summary.component.html',
  styleUrl: './crypto-account-summary.component.css'
})
export class CryptoAccountSummaryComponent {
  account_value: number = 0;
  cash: number = 0;
}
