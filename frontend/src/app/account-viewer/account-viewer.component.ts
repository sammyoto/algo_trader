import { Component } from '@angular/core';
import { ApiHandlerService } from '../services/api-handler.service';

@Component({
  selector: 'app-account-viewer',
  imports: [],
  templateUrl: './account-viewer.component.html',
  styleUrl: './account-viewer.component.css'
})
export class AccountViewerComponent {

  constructor(private apiService: ApiHandlerService) { }

  // -----------------------------DATA SUBSCRIPTION-----------------------------
  ngOnInit(): void {
    this.apiService.streamAccountData().subscribe(response => {
      console.log(response)
    })
  }
}
