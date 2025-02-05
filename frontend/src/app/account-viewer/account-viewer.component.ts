import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-account-viewer',
  imports: [],
  templateUrl: './account-viewer.component.html',
  styleUrl: './account-viewer.component.css',
  providers: []
})
export class AccountViewerComponent {

  accountValue: string = '-';
  accountCash: string = '-';
  settledCash: string = '-';
  unsettledCash: string = '-';

  constructor() { }

  // -----------------------------DATA SUBSCRIPTION-----------------------------
  ngOnInit(): void {
    
  }
}
