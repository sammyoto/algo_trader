import { Component } from '@angular/core';
import { BotViewerComponent } from '../bot-viewer/bot-viewer.component';
import { AccountViewerComponent } from '../account-viewer/account-viewer.component';
import { Trader_Metadata } from '../shared/backend_models';

@Component({
  selector: 'app-body',
  imports: [AccountViewerComponent, BotViewerComponent],
  templateUrl: './body.component.html',
  styleUrl: './body.component.css'
})
export class BodyComponent {
  traderMetadataNVDA: Trader_Metadata = {type: "pivot", ticker: "NVDA"}
  traderMetadataAMZN: Trader_Metadata = {type: "pivot", ticker: "AMZN"}
  traderMetadataGOOG: Trader_Metadata = {type: "pivot", ticker: "GOOG"}
  traderMetadataBAH: Trader_Metadata = {type: "pivot", ticker: "BAH"}
}
