import { Component } from '@angular/core';
import { ChartConfiguration, ChartType } from 'chart.js';
import { BaseChartDirective } from 'ng2-charts';
import { ApiHandlerService } from '../services/api-handler.service';

@Component({
  selector: 'app-bot-viewer',
  standalone: true,
  imports: [BaseChartDirective],
  templateUrl: './bot-viewer.component.html',
  styleUrl: './bot-viewer.component.css'
})
export class BotViewerComponent {
  ticker: string = "NVDA";
  algorithm: string = "pivot";

  constructor(private apiService: ApiHandlerService) { }
  
  // -----------------------------DATA SUBSCRIPTION-----------------------------
  ngOnInit(): void {
    this.apiService.streamBotData(this.ticker, this.algorithm).subscribe(response => {
      console.log(response)
    })
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
