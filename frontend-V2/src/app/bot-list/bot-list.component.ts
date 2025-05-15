import { Component } from '@angular/core';
import { BackendService } from '../../services/backend.service';
import { TraderState } from '../../shared/bot-models';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-bot-list',
  imports: [RouterLink],
  templateUrl: './bot-list.component.html',
  styleUrl: './bot-list.component.css'
})
export class BotListComponent {
  bots: TraderState[] = [];
  selectedBot: any = null;

  constructor(private backendService: BackendService) {
    this.getAllBots();
  }

  getAllBots() {
    this.backendService.get_all_bots().then((data) => {
      if (!data) {
        console.error('No data received from backend');
      } else {
        this.bots = data;
      }
    });
  }

  selectBot(bot: any) {
    this.selectedBot = bot;
  }
}
