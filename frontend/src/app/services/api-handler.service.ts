import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiHandlerService {
  private botApiUrl = 'https://google.com';
  private accountApiUrl = 'https://google.com';

  constructor( private http:HttpClient ) { }

  // Returns an Observable of the HTTP response
  streamBotData(ticker: string, algorithm: string): Observable<any> {
    return this.http.get(this.botApiUrl);
  }

  streamAccountData(): Observable<any> {
    return this.http.get(this.accountApiUrl);
  }
}
