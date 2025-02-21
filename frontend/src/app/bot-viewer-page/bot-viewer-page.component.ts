import { Component, Input, ViewChild} from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChartConfiguration, ChartType } from 'chart.js';
import { BaseChartDirective } from 'ng2-charts';
import { WebsocketHandlerService } from '../services/websocket-handler.service';
import { Trader_Metadata, Schwab_Trader_Data } from '../shared/backend_models';
import { Subscription } from 'rxjs';
import { ActivatedRoute } from '@angular/router';

const MAX_DATA_POINTS: number = 100;

@Component({
  selector: 'app-bot-viewer-page',
  standalone: true,
  imports: [BaseChartDirective, CommonModule],
  templateUrl: './bot-viewer-page.component.html',
  styleUrl: './bot-viewer-page.component.css',
  providers:[WebsocketHandlerService]
})
export class BotViewerPageComponent {
  @ViewChild(BaseChartDirective) chart?: BaseChartDirective;

  // for comparing numbers and setting colors correctly
  firstPrice: number = 0;
  firstHoldings: number = 0;
  firstProfit: number = 0;
  firstBotCash: number = 500;

  pricePositive: boolean = true;
  holdingsPositive: boolean = true;
  profitPositive: boolean = true;
  botCashPositive: boolean = true;

  currentPrice: string = '-';
  currentHoldings: string = '-';
  sessionProfit: string = '-';
  botCash: string = '-';

  // Subscription holder for cleanup
  private dataSubscription!: Subscription;
  private title!: string;

  // Ticker and trader type
  traderMetadata: Trader_Metadata = {type: "pivot", ticker: "NVDA"}

  constructor(private activatedRoute: ActivatedRoute, private apiService: WebsocketHandlerService) { }

  // -----------------------------DATA SUBSCRIPTION-----------------------------
    ngOnInit(): void {
      // Get the parameter from the route
      this.activatedRoute.paramMap.subscribe(params => {
        this.traderMetadata.ticker = params.get('ticker')!;
        this.traderMetadata.type = params.get('trader')!;
      });
      this.apiService.setTraderMetadata(this.traderMetadata)
      this.title = `${this.traderMetadata.ticker} - ${this.traderMetadata.type.toUpperCase()}`;
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
      this.currentPrice = `${price.toFixed(2)}`;
      this.currentHoldings = `${holdings.toFixed(2)}`;
      this.sessionProfit = `${pl.toFixed(2)}`;
      this.botCash = `${botCash.toFixed(2)}`;
  
      this.updateChartBools();
  
      this.lineChartData.labels?.push(now.toLocaleTimeString());
      this.lineChartData.datasets[0].data.push(price);
      this.chart?.update();
    }
  
    updateChartBools() {
      if (Number(this.currentPrice) >= this.firstPrice) {
        this.pricePositive = true;
      } else {
        this.pricePositive = false;
      }
  
      if (Number(this.currentHoldings) >= this.firstHoldings) {
        this.holdingsPositive = true;
      } else {
        this.holdingsPositive = false;
      }
      if (Number(this.sessionProfit) >= this.firstProfit) {
        this.profitPositive = true;
      } else {
        this.profitPositive = false;
      }
  
      if (Number(this.botCash) >= this.firstBotCash) {
        this.botCashPositive = true;
      } else {
        this.botCashPositive = false;
      }
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
