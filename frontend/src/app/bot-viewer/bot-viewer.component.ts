import { Component, Input, ViewChild} from '@angular/core';
import { ChartConfiguration, ChartType } from 'chart.js';
import { BaseChartDirective } from 'ng2-charts';
import { ApiHandlerService } from '../services/api-handler.service';
import { Trader_Metadata, Schwab_Trader_Data } from '../shared/backend_models';
import { Subscription } from 'rxjs';

const MAX_DATA_POINTS: number = 100;

@Component({
  selector: 'app-bot-viewer',
  standalone: true,
  imports: [BaseChartDirective],
  templateUrl: './bot-viewer.component.html',
  styleUrl: './bot-viewer.component.css',
  providers:[ApiHandlerService]
})
export class BotViewerComponent {
  @Input() traderMetadata!: Trader_Metadata;
  @ViewChild(BaseChartDirective) chart?: BaseChartDirective;

  currentPrice: string = '-';
  currentHoldings: string = '-';
  sessionProfit: string = '-';
  botCash: string = '-';

  // Subscription holder for cleanup
  private dataSubscription!: Subscription;
  private title!: string;

  constructor(private apiService: ApiHandlerService) { }
  
  // -----------------------------DATA SUBSCRIPTION-----------------------------
  ngOnInit(): void {
    this.apiService.setTraderMetadata(this.traderMetadata)
    this.title = `${this.traderMetadata.ticker} - ${this.traderMetadata.type}`;
    this.lineChartOptions!.plugins!.title!.text = this.title;

    // Subscribe to the data$ observable to receive WebSocket data updates.
    this.dataSubscription = this.apiService.data$.subscribe((data: Schwab_Trader_Data) => {
      const market_price = Number(data["trader_data"]["market_price"]);
      const holdings = Number(data["trader_data"]["current_holdings"]);
      const pl = Number(data["trader_data"]["session_profit"]);
      const botCash = Number(data["trader_data"]["account_cash"]);

      // Remove oldest data if we've reached maximum points
      if (this.lineChartData.datasets[0].data.length >= MAX_DATA_POINTS) {
        this.lineChartData.labels?.shift();
        this.lineChartData.datasets[0].data.shift();
      }

      this.updateBotData(market_price, holdings, pl, botCash);
    });
  }

  // Clean up the subscription to prevent memory leaks.
  ngOnDestroy(): void {
    if (this.dataSubscription) {
      this.dataSubscription.unsubscribe();
    }
  }

  updateBotData(price: number, holdings: number, pl: number, botCash: number) {
    const now = new Date();
    this.currentPrice = `$${price.toFixed(2)}`;
    this.currentHoldings = `${holdings.toFixed(2)}`;
    this.sessionProfit = `$${pl.toFixed(2)}`;
    this.botCash = `$${botCash.toFixed(2)}`

    this.lineChartData.labels?.push(now.toLocaleTimeString());
    this.lineChartData.datasets[0].data.push(price);
    this.chart?.update();
  }

  // --------------------------------LINE CHART---------------------------------
  public lineChartType: ChartType = 'line';

  public lineChartData: ChartConfiguration['data'] = {
    datasets: [
      {
        data: [],
        borderColor: '#965efd',
        pointBackgroundColor: 'white',
        pointRadius: 0, // make bigger if we want points
        pointHitRadius: 10,
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgba(148,159,177,0.8)',
        tension: 0.1
      },
    ],
    labels: [],
  };

  public lineChartOptions: ChartConfiguration['options'] = {
    responsive: true,
    scales: {
      // We use this empty structure as a placeholder for dynamic theming.
      y: {
        position: 'left',
      },
    },
    plugins: {
      legend: {
        display: false
      },
      title: {
        display: true,
        text: "nothing",
        color: "#dbdbdb",
        font: {
          size: 20
        }
      }
    }
  };
}
