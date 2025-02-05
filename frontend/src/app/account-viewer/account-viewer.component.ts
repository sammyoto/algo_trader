import { Component } from '@angular/core';
import { ApiHandlerService } from '../services/api-handler.service';

@Component({
  selector: 'app-account-viewer',
  imports: [],
  templateUrl: './account-viewer.component.html',
  styleUrl: './account-viewer.component.css'
})
export class AccountViewerComponent {

  accountValue: string = '-';
  accountCash: string = '-';
  settledCash: string = '-';
  unsettledCash: string = '-';

  constructor(private apiService: ApiHandlerService) { }

  // -----------------------------DATA SUBSCRIPTION-----------------------------
  ngOnInit(): void {
  }
}
