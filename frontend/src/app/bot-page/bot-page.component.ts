import { Component, ViewChild } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { BackendService } from '../../services/backend.service';
import { TraderState } from '../../shared/bot-models';
import { Chart, ChartConfiguration, ChartEvent, ChartType } from 'chart.js';
import { BaseChartDirective } from 'ng2-charts';
import { NgIf } from '@angular/common';
import * as BotModels from '../../shared/bot-models';

@Component({
  selector: 'app-bot-page',
  imports: [BaseChartDirective, NgIf],
  templateUrl: './bot-page.component.html',
  styleUrl: './bot-page.component.css'
})
export class BotPageComponent { 
  // This component is responsible for displaying the details of a specific bot
  // Fetch bot details and history and put here
  // Display bot profit on a graph
  showPopup: boolean = false;
  popupMessage: string = '';
  bot_name: string | null = '';
  bot_details: TraderState | null = null;
  bot_history: TraderState[] = [];
  paper_clicked = !this.bot_details?.paper;
  retired = false;
  paper = true;
  chartData: ChartConfiguration['data'] = {
    datasets: [
      {
        data: [],
        label: 'Profit',
        backgroundColor: 'rgba(214, 138, 229, 0.2)',
        borderColor: 'rgb(164, 106, 230)',
        pointBackgroundColor: 'rgb(177, 112, 197)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgba(182, 116, 199, 0.8)',
        fill: 'origin',
      },
      {
        data: [],
        label: 'Cash',
        backgroundColor: 'rgba(74, 126, 240, 0.2)',
        borderColor: 'rgb(117, 155, 236)',
        pointBackgroundColor: 'rgb(107, 146, 231)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgb(112, 146, 218)',
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
    this.paper = this.bot_details!.paper
  }

  live_switch() {
    this.paper_clicked = true;
    if (!this.paper) {
      this.popupMessage = 'Trader is already live!'
    } else {
      this.popupMessage = 'Are you sure you want to go live? The trader will reset to its initial state and start trading with real money!'
    }
    this.showPopup = true;
  }

  retire_trader() {
    this.paper_clicked = false;
    if (this.retired) {
      this.popupMessage = 'Trader is already retired!'
    } else {
      this.popupMessage = 'Are you sure you want to retire this trader? The trader will sell all assets it currently  manages and stop trading!';
    }
    this.showPopup = true;
  }

  live_confirmation() {
    this.popupMessage = 'Trader is live!'
    this.paper = false;
    this.showPopup = true;
  }

  retire_confirmation() {
    this.popupMessage = 'Trader retired!'
    this.retired = true
    this.showPopup = true
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
          this.paper = this.bot_details.paper;
          this.retired = this.bot_details.status == BotModels.TraderStatus.RETIRED;
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
