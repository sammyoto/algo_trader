import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BotBacktestingComponent } from './bot-backtesting.component';

describe('BotBacktestingComponent', () => {
  let component: BotBacktestingComponent;
  let fixture: ComponentFixture<BotBacktestingComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [BotBacktestingComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(BotBacktestingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
