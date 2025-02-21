import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BotHistoryPageComponent } from './bot-history-page.component';

describe('BotHistoryPageComponent', () => {
  let component: BotHistoryPageComponent;
  let fixture: ComponentFixture<BotHistoryPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [BotHistoryPageComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(BotHistoryPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
