import { Injectable } from '@angular/core';
import { Subject, Observable } from 'rxjs';
import { Trader_Metadata, Schwab_Trader_Data } from '../shared/backend_models';

@Injectable({
  providedIn: 'root'
})
export class WebsocketHandlerService {
  private traderMetadata: Trader_Metadata;
  private wsUrl = 'ws://localhost:8000/ws';  // WebSocket endpoint
  private ws!: WebSocket;
  private retryCount: number = 0;
  private maxRetries: number = 3;
  private retryDelay: number = 3000; // 3 seconds

  // Create a Subject to emit data from the WebSocket
  private dataSubject = new Subject<Schwab_Trader_Data>();

  // Expose the observable so components can subscribe
  public data$: Observable<Schwab_Trader_Data> = this.dataSubject.asObservable();

  constructor() {
    this.traderMetadata = {type: "pivot", ticker: "NVDA"}
  }

  setTraderMetadata(data: Trader_Metadata) {
    this.traderMetadata = data
    this.initializeWebSocket();
  }

  private initializeWebSocket(): void {
    this.ws = new WebSocket(`${this.wsUrl}/${this.traderMetadata.type}/${this.traderMetadata.ticker}`);
    // Event handlers
    this.ws.onopen = () => {
      console.log('WebSocket connected');
      this.retryCount = 0; // Reset retries on success
    };

    this.ws.onmessage = (event) => {
      this.handleMessage(event.data);
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    this.ws.onclose = (event) => {
      console.log('WebSocket closed:', event.code, event.reason);
      if (this.retryCount < this.maxRetries) {
        setTimeout(() => {
          this.retryCount++;
          this.initializeWebSocket();
        }, this.retryDelay);
      }
    };
  }

  // Handle incoming messages
  handleMessage(data: any) {
    try {
      const parsedData: Schwab_Trader_Data = JSON.parse(data)
      console.log('Received data:', parsedData);
      this.dataSubject.next(parsedData)
      // Add your logic here (e.g., update UI, trigger actions)
    } catch (error) {
      console.error('Failed to parse message:', error);
    }
  }
}
