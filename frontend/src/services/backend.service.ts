import { Injectable } from '@angular/core';
import { TraderState } from '../shared/bot-models';
import { TraderCreationRequest } from '../shared/bot-models';
import { CryptoPortfolioStats } from '../shared/bot-models';
import { HttpClient } from '@angular/common/http';
import { Observable, map, catchError, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BackendService {

  constructor(private http: HttpClient) { }

  backend_url = 'http://localhost:8000';

  json_to_trader(json: any): TraderState {
    return {
      ...json,
      // Convert ISO timestamp string to a real Date object if present
      timestamp: json.timestamp ? new Date(json.timestamp) : undefined
    };
  }

  get_all_bots() {
    return this.http.get<any>(`${this.backend_url}/trader`).pipe(
      map(json => {
        const traders: TraderState[] = [];
        for (const trader of json) {
          traders.push(this.json_to_trader(trader));
        }
        return traders;
      }),
      catchError(error => {
        console.error('There was a problem fetching traders:', error);
        return of([]);
      })
    );
  }

  get_bot_by_name(name: string): Observable<TraderState[]> {
    return this.http.get<any>(`${this.backend_url}/trader/${name}`).pipe(
      map(json => {
        const traders: TraderState[] = [];
        for (const trader of json) {
          traders.push(this.json_to_trader(trader));
        }
        return traders;
      }),
      catchError(error => {
        console.error('There was a problem fetching the trader:', error);
        return of([]);
      })
    );
  }

  delete_bot(name: string): Observable<String> {
    return this.http.delete<string>(`${this.backend_url}/trader/${name}`);
  }

  send_trader_creation_request(traderCreationRequest: TraderCreationRequest): Observable<String> {
    return this.http.post<string>(`${this.backend_url}/trader`, traderCreationRequest);
  }

  get_crypto_portfolio_stats(): Observable<CryptoPortfolioStats> {
    return this.http.get<CryptoPortfolioStats>(`${this.backend_url}/account/crypto`);
  }
}
