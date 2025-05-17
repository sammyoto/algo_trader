import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { BackendService } from '../../services/backend.service';
import { TraderState } from '../../shared/bot-models';

@Component({
  selector: 'app-bot-page',
  imports: [],
  templateUrl: './bot-page.component.html',
  styleUrl: './bot-page.component.css'
})
export class BotPageComponent {
  // This component is responsible for displaying the details of a specific bot
  // Fetch bot details and history and put here
  // Display bot profit on a graph
  bot_name: string | null = '';
  bot_details: TraderState | null = null;

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
          this.bot_details = data;
        }
      });
    }
  }
}
