import { Component } from '@angular/core';
import { ApiHandlerService } from '../services/api-handler.service';
import { Schwab_Account_Data } from '../shared/backend_models';
import { interval, Subscription } from 'rxjs';

@Component({
  selector: 'app-account-viewer',
  imports: [],
  templateUrl: './account-viewer.component.html',
  styleUrl: './account-viewer.component.css',
  providers: []
})
export class AccountViewerComponent {

  account_data: Schwab_Account_Data = {
    accountValue: 0,
    accountCash: 0,
    settledCash: 0,
    unsettledCash: 0,
    tradableCash: 0,
    withdrawableCash: 0,
    shortMarketValue: 0,
    longMarketValue: 0
  }

  private subscription!: Subscription;
  
  constructor(private apiHandlerService: ApiHandlerService) { }

  // -----------------------------DATA SUBSCRIPTION-----------------------------
  ngOnInit(): void {
    this.updateAccountData();
    // Create an observable that emits every 10 seconds (10,000 ms)
    const source$ = interval(10000);
    
    // Subscribe to the observable
    this.subscription = source$.subscribe(() => {
      this.updateAccountData();
    });
      
  }

  updateAccountData() {
    this.apiHandlerService.getAccountData().subscribe({
      next: (data) => {
        // odd but for some reason data doesn't come in in the right order, possible alphabetic ordering?
        const parsedData: any = JSON.parse(data)
        this.account_data.accountValue = parsedData.account_value
        this.account_data.accountCash = parsedData.account_cash
        this.account_data.settledCash = parsedData.settled_cash
        this.account_data.unsettledCash = parsedData.unsettled_cash
        this.account_data.tradableCash = parsedData.tradable_cash
        this.account_data.withdrawableCash = parsedData.withdrawable_cash
        this.account_data.shortMarketValue = parsedData.short_market_value
        this.account_data.longMarketValue = parsedData.long_market_value
      },
      error: (error) => console.error("Error fetching account data", error)
    });
  }

  ngOnDestroy(): void {
    // Always unsubscribe to avoid memory leaks
    if (this.subscription) {
      this.subscription.unsubscribe();
    }
  }
}
