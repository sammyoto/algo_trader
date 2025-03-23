import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiHandlerService {

  private apiUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) { }

  // GET method to retrieve account data
  getAccountData(): Observable<any> {
    return this.http.get<any>(this.apiUrl + "/account-data");
  }

  // GET 
  getBots(): Observable<any> {
    return this.http.get<any>(this.apiUrl + "/bot-list");
  }
}
