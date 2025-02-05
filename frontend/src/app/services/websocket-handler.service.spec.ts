import { TestBed } from '@angular/core/testing';

import { WebsocketHandlerService } from './websocket-handler.service';

describe('ApiHandlerService', () => {
  let service: WebsocketHandlerService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(WebsocketHandlerService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
