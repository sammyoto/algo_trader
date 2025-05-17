import { Component, ViewChild } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { BackendService } from '../../services/backend.service';
import { TraderState } from '../../shared/bot-models';
import { Chart, ChartConfiguration, ChartEvent, ChartType } from 'chart.js';
import { BaseChartDirective } from 'ng2-charts';

@Component({
  selector: 'app-bot-page',
  imports: [BaseChartDirective],
  templateUrl: './bot-page.component.html',
  styleUrl: './bot-page.component.css'
})
export class BotPageComponent {
  // This component is responsible for displaying the details of a specific bot
  // Fetch bot details and history and put here
  // Display bot profit on a graph
  bot_name: string | null = '';
  bot_details: TraderState | null = null;
  bot_history: TraderState[] = [];
  chartData: ChartConfiguration['data'] = {
    datasets: [
      {
        data: [],
        label: 'Profit',
        backgroundColor: 'rgba(148,159,177,0.2)',
        borderColor: 'rgba(148,159,177,1)',
        pointBackgroundColor: 'rgba(148,159,177,1)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgba(148,159,177,0.8)',
        fill: 'origin',
      },
      {
        data: [],
        label: 'Cash',
        backgroundColor: 'rgba(77,83,96,0.2)',
        borderColor: 'rgba(77,83,96,1)',
        pointBackgroundColor: 'rgba(77,83,96,1)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgba(77,83,96,1)',
        fill: 'origin',
      },
    ],
    labels: [],
  };

  chartOptions: ChartConfiguration['options'] = {
    elements: {
      line: {
        tension: 0.5,
      },
    },
    plugins: {
      legend: { display: true },
    }
  }

  @ViewChild(BaseChartDirective) chart?: BaseChartDirective;

  constructor(private route: ActivatedRoute, private backendService: BackendService) {
    this.bot_name = this.route.snapshot.paramMap.get('name') || '';
    this.getBotDetails();
  }

  ngOnInit() {

  }

  retire_trader() {

  }

  live_switch() {

  }

  getBotDetails() {
    if (this.bot_name) {
      this.backendService.get_bot_by_name(this.bot_name).then((data) => {
        if (!data) {
          console.error('No data received from backend');
        } else {
          this.bot_details = data[0];
          this.bot_history = data;
          this.init_chart();
          this.chart?.update();
        }
      });
    }
  }

  init_chart() {
    for (let i = this.bot_history.length - 1; i >= 0; i--) {
      const bot_state = this.bot_history[i];
      console.log(bot_state)
      this.chartData.datasets[0].data.push(bot_state.profit)
      this.chartData.datasets[1].data.push(bot_state.cash)
      this.chartData.labels!.push('')
    }
  }
}
