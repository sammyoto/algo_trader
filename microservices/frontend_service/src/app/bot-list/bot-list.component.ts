import { Component } from '@angular/core';
import { ApiHandlerService } from '../services/api-handler.service';
import { Trader_Data, Trader_Metadata } from '../shared/backend_models';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-bot-list',
  imports: [RouterLink],
  templateUrl: './bot-list.component.html',
  styleUrl: './bot-list.component.css'
})
export class BotListComponent {
  botList!: [Trader_Data];

  constructor(private apiHandlerService: ApiHandlerService) { }

  ngOnInit(): void {
    this.getBotList();
  }

  getBotList() {
    this.apiHandlerService.getBots().subscribe({
      next: (data) => {
        const parsedData: any = JSON.parse(data)
        console.log(parsedData)
        this.botList = parsedData.bot_list
      },
      error: (error) => console.error("Error fetching bot list", error)
    });
  }
}
