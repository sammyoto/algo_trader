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
    this.backendService.get_all_bots().subscribe({
      next: data => this.bots = data,
      error: err => console.error('Failed to fetch stats', err)
    })
  }

  selectBot(bot: any) {
    this.selectedBot = bot;
  }
}
