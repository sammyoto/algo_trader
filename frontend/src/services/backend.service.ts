import { Injectable } from '@angular/core';
import { TraderState } from '../shared/bot-models';

@Injectable({
  providedIn: 'root'
})
export class BackendService {

  constructor() { }

  backend_url = 'http://localhost:8000';

  json_to_trader(json: any): TraderState {
    return {
      ...json,
      // Convert ISO timestamp string to a real Date object if present
      timestamp: json.timestamp ? new Date(json.timestamp) : undefined
    };
  }

  get_all_bots() {
    return fetch(this.backend_url + '/trader', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    }).then(json => {
      var traders: TraderState[] = [];
      for (const trader of json['body']) {
        traders.push(this.json_to_trader(trader));
      }
      return traders;
    })
    .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
    });
  }

  get_bot_by_name(name: string) {
    return fetch(this.backend_url + '/trader/' + name, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    }).then(json => {
      var traders: TraderState[] = [];
      for (const trader of json['body']) {
        traders.push(this.json_to_trader(trader));
      }
      return traders;
    })
    .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
    });
  }

  send_trader_creation_request(traderCreationRequest: any) {
    return fetch(this.backend_url + '/trader', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(traderCreationRequest)
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    }).catch(error => {
      console.error('There was a problem with the fetch operation:', error);
    });
  }

}
