import { Component } from '@angular/core';
import { BotViewerComponent } from '../bot-viewer/bot-viewer.component';
import { AccountViewerComponent } from '../account-viewer/account-viewer.component';

@Component({
  selector: 'app-body',
  imports: [AccountViewerComponent, BotViewerComponent],
  templateUrl: './body.component.html',
  styleUrl: './body.component.css'
})
export class BodyComponent {

}
