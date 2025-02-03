import { Component, Input} from '@angular/core';
import { ChartConfiguration, ChartType } from 'chart.js';
import { BaseChartDirective } from 'ng2-charts';
import { ApiHandlerService } from '../services/api-handler.service';
import { Trader_Metadata, Schwab_Trader_Data } from '../shared/backend_models';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-bot-viewer',
  standalone: true,
  imports: [BaseChartDirective],
  templateUrl: './bot-viewer.component.html',
  styleUrl: './bot-viewer.component.css'
})
export class BotViewerComponent {
  @Input() traderMetadata!: Trader_Metadata;

  // Subscription holder for cleanup
  private dataSubscription!: Subscription;

  constructor(private apiService: ApiHandlerService) { }
  
  // -----------------------------DATA SUBSCRIPTION-----------------------------
  ngOnInit(): void {
    this.apiService.setTraderMetadata(this.traderMetadata)

    // Subscribe to the data$ observable to receive WebSocket data updates.
    this.dataSubscription = this.apiService.data$.subscribe((data: Schwab_Trader_Data) => {
      console.log('Received data in component:', data);
      // Update your chart data here.
      // For example, if your incoming data has a numeric field to add to the chart:
      // this.lineChartData.datasets[0].data.push(data.someNumericField);
      // Then, trigger a chart update if necessary.
    });
  }

  // Clean up the subscription to prevent memory leaks.
  ngOnDestroy(): void {
    if (this.dataSubscription) {
      this.dataSubscription.unsubscribe();
    }
  }

  // --------------------------------LINE CHART---------------------------------
  public lineChartType: ChartType = 'line';

  public lineChartData: ChartConfiguration['data'] = {
    datasets: [
      {
        data: [65, 59, 80, 81, 56, 55, 40],
        borderColor: '#965efd',
        pointBackgroundColor: 'white',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgba(148,159,177,0.8)',
        tension: 0.1
      },
    ],
    labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
  };

  public lineChartOptions: ChartConfiguration['options'] = {
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
        text: "NVDA - Pivot Trader",
        color: "#dbdbdb",
        font: {
          size: 20
        }
      }
    }
  };
}
