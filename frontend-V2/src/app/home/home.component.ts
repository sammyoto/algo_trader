import { Component } from '@angular/core';
import { ActivityFeedComponent } from '../activity-feed/activity-feed.component';
import { CryptoAccountSummaryComponent } from '../crypto-account-summary/crypto-account-summary.component';
import { BrokerageAccountSummaryComponent } from '../brokerage-account-summary/brokerage-account-summary.component';

@Component({
  selector: 'app-home',
  imports: [ActivityFeedComponent, CryptoAccountSummaryComponent, BrokerageAccountSummaryComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {

}
