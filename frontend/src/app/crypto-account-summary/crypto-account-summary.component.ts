import { Component } from '@angular/core';
import { BackendService } from '../../services/backend.service';
import { CryptoPortfolioStats } from '../../shared/bot-models';

@Component({
  selector: 'app-crypto-account-summary',
  imports: [],
  templateUrl: './crypto-account-summary.component.html',
  styleUrl: './crypto-account-summary.component.css'
})
export class CryptoAccountSummaryComponent {
  portfolio_stats: CryptoPortfolioStats | null = null;

  constructor(private backendService: BackendService) {
    
  }

  ngOnInit() {
    this.backendService.get_crypto_portfolio_stats().subscribe({
      next: stats => this.portfolio_stats = stats,
      error: err => console.error('Failed to fetch stats', err)
    })
  }


}
