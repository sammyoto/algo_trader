import { Injectable } from '@angular/core';
import { TraderState } from '../shared/bot-models';

@Injectable({
  providedIn: 'root'
})
export class BackendService {

  constructor() { }

  backend_url = 'http://localhost:8000';

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
      var data: TraderState[] = [];
      for (const [key, value] of Object.entries(json['body'])) {
        console.log(key, value);
        data.push(json['body'][key]['state'] as TraderState);
      }
      return data;
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
      return json['body']['state'] as TraderState;
    })
    .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
    });
  }

}
